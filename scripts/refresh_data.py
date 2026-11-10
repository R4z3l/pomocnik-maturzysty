"""Pobieranie i przygotowanie zmian bazy wiedzy bez AI. Aktywna baza zmienia się tylko przez apply."""
import argparse
import copy
import hashlib
import io
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urldefrag, urlsplit

from bs4 import BeautifulSoup
from source_policy import canonical, ensure_source_allowed, guarded_get
from refresh_parsers import clean, history_tables, name_key, uew_durations
from pwr_curricula import parse_pwr_curriculum
from upwr_curricula import parse_upwr_curriculum
from european_cultures import reviewed_plan, DOCUMENT_URL, PROGRAMME_ID, SOURCE_ID

ROOT = Path(__file__).resolve().parents[1]
CORE = {
    'pwr-thresholds': ('pwr', 'https://rekrutacja.pwr.edu.pl/rekrutacja/progi-punktowe/progi-studia-i-stopnia-stacjonarne/', 'history'),
    'uew-thresholds': ('uew', 'https://rekrutacja.uew.pl/informacje-praktyczne/najwazniejsze-informacje/progi-punktowe/', 'history'),
    'uew-duration': ('uew', 'https://bip.ue.wroc.pl/download/attachment/4064/zalacznik-do-uchwaly-senatu-r0000182026.pdf?v=1778225564', 'current'),
    'uwr-european-cultures': ('uwr', DOCUMENT_URL, 'current'),
}
for _plan in json.loads((ROOT / 'src/data/curricula-pwr.json').read_text(encoding='utf-8')):
    _url = next(s['url'] for s in _plan['sources'] if urlsplit(s['url']).hostname == 'sylabus.usos.pwr.edu.pl')
    CORE['pwr-curriculum:' + _plan['programmeId']] = ('pwr', _url, 'current')
for _plan in json.loads((ROOT / 'src/data/curricula-upwr.json').read_text(encoding='utf-8')):
    _url = _plan['sources'][0]['url']
    CORE['upwr-curriculum:' + _plan['programmeId']] = ('upwr', _url, 'current')
ALLOWED_OUTPUTS = {
    'src/data/pwr.json', 'src/data/uew.json', 'src/data/uwr.json',
    'docs/research/pwr/thresholds-active.json', 'docs/research/pwr/thresholds-parsed.json',
    'src/data/curricula-pwr.json', 'src/data/curricula-uwr-a.json', 'src/data/curricula-upwr.json',
}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def digest(value):
    return hashlib.sha256(value).hexdigest()


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix='.refresh-', dir=path.parent)
    try:
        with os.fdopen(handle, 'wb') as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()


def input_hashes(root):
    files = list((root / 'src/data').glob('*.json'))
    files += [root / 'scripts' / name for name in ['refresh_data.py', 'refresh_parsers.py', 'source_policy.py', 'parse-history.ts', 'pwr_curricula.py', 'european_cultures.py', 'upwr_curricula.py']]
    files += [root / 'docs/research/curricula/uwr-a/european-cultures-semesters.json']
    files += [root / 'src/thresholds.ts']
    return {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in files}


def inventory(root):
    """Tylko zarejestrowane źródła oficjalne; fragmenty stron nie tworzą duplikatów."""
    found = {}
    def add(url, university, purpose, label):
        url = urldefrag(url)[0]
        key = (canonical(url), purpose)
        if key not in found:
            found[key] = dict(id=digest((url + purpose).encode())[:16], university=university, url=url, purpose=purpose, title=label)
    for university in ['uwr', 'uew', 'pwr', 'upwr']:
        data = read_json(root / f'src/data/{university}.json')
        history_ids = {t['sourceId'] for p in data['programmes'] for t in p['thresholds']}
        current_ids = {sid for p in data['programmes'] for sid in p['sourceIds']}
        current_ids.update(sid for u in data['universities'] for sid in u['sourceIds'])
        for source in data['sources']:
            if source['kind'] != 'official':
                continue
            purpose = 'history' if source['id'] in history_ids else 'current'
            if source['id'] in current_ids or source['id'] in history_ids:
                add(source['url'], university, purpose, source['title'])
    for path in (root / 'src/data').glob('curricula-*.json'):
        for row in read_json(path):
            university = row['programmeId'].split('-')[0]
            for source in row['sources']:
                add(source['url'], university, 'current', source['title'])
    for path in (root / 'src/data').glob('*-rules.json'):
        for rule in read_json(path):
            add(rule['sourceUrl'], path.stem.split('-')[0], 'current', rule['title'])
    for id, (university, url, purpose) in CORE.items():
        add(url, university, purpose, id)
    return sorted(found.values(), key=lambda row: (row['university'], row['url'], row['purpose']))


def semantic_hash(content, content_type):
    if 'html' not in content_type.lower():
        return digest(content)
    soup = BeautifulSoup(content, 'html.parser')
    main = soup.find('main') or soup.find('article') or soup.body or soup
    for node in main.select('script, style, noscript, nav, footer'):
        node.decompose()
    # Uwzględniamy też zmianę linku do planu, nawet gdy tekst strony pozostaje taki sam.
    links = sorted({a.get('href', '') for a in main.find_all('a', href=True)})
    return digest(json_bytes([clean(main.get_text(' ', strip=True)), links]))


def download(item, directory, cache, root, force=False):
    url, purpose = item['url'], item['purpose']
    # Wymagana kontrola CLI oraz ponowna kontrola w guarded_get przed przekierowaniami.
    check = subprocess.run(['node', '--experimental-strip-types', str(root / 'scripts/check-source.ts'), url, purpose], capture_output=True)
    if check.returncode:
        raise ValueError('POMIŃ: polityka źródeł odrzuciła adres')
    ensure_source_allowed(url, purpose)
    key = digest((url + purpose).encode())
    metadata_path, body_path = cache / (key + '.json'), cache / (key + '.bin')
    old = read_json(metadata_path) if metadata_path.exists() and body_path.exists() else {}
    now = time.time()
    headers = {'User-Agent': 'PomocnikMaturzysty/1.0 (local data updater)', 'Accept': 'text/html, application/pdf'}
    if old.get('etag'):
        headers['If-None-Match'] = old['etag']
    if old.get('lastModified'):
        headers['If-Modified-Since'] = old['lastModified']
    if not force and old and now - old['fetchedAt'] < 86400:
        content = body_path.read_bytes()
        result = {**old, 'status': 'cached', 'network': False}
    else:
        response = guarded_get(url, purpose=purpose, timeout=(10, 25), headers=headers, max_bytes=25 * 1024 * 1024)
        if response.status_code == 304:
            if not old:
                raise ValueError('Serwer zwrócił 304 bez lokalnej kopii')
            content = body_path.read_bytes()
            result = {**old, 'fetchedAt': now, 'status': 'unchanged', 'network': True}
        else:
            content = response.content
            if not content or len(content) > 25 * 1024 * 1024:
                raise ValueError('Pusty materiał lub przekroczony limit 25 MiB')
            content_type = response.headers.get('Content-Type', '')
            binary_types = ['application/zip', 'application/x-zip-compressed', 'application/msword', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument']
            known_binary = any(t in content_type for t in binary_types) or 'application/octet-stream' in content_type and urlsplit(url).path.lower().endswith(('.pdf', '.zip', '.xls', '.xlsx', '.doc', '.docx'))
            if 'html' not in content_type and 'pdf' not in content_type and not content.startswith(b'%PDF-') and not known_binary:
                raise ValueError('Nieobsługiwany typ odpowiedzi: ' + content_type)
            semantic = semantic_hash(content, content_type)
            status = 'baseline-created' if not old else 'unchanged' if semantic == old.get('semanticHash') else 'changed'
            result = dict(status=status, network=True, fetchedAt=now, contentType=content_type, semanticHash=semantic,
                          etag=response.headers.get('ETag'), lastModified=response.headers.get('Last-Modified'), finalUrl=response.url)
        atomic_write(body_path, content)
        atomic_write(metadata_path, json_bytes(result))
    evidence = directory / (key + '.bin')
    atomic_write(evidence, content)
    return content, {**result, 'evidence': evidence.name, 'sha256': digest(content), 'bytes': len(content)}


def rejected(policy, url, programme_id, year):
    return any(canonical(row['url']) == canonical(url) and row['programmeId'] == programme_id and row['year'] == year
               for row in policy['rejectedClaims'])


def match_offer(name, programmes, university):
    language = None
    if university == 'uew':
        marker = re.search(r'\s*\(studia w j\.\s*angielskim\)$', name, re.I)
        if marker:
            name, language = name[:marker.start()], 'en'
        if name == 'Informatyka w zarządzaniu produkcją – nowy kierunek':
            name = 'Informatyka w zarządzaniu produkcją'
    matches = [p for p in programmes if name_key(p['name']) == name_key(name) and (language is None or p['language'] == language)]
    if len(matches) > 1:
        raise ValueError('Niejednoznaczna tożsamość oferty: ' + name)
    return matches[0] if matches else None


def add_observation(programme, row, source_id, url, policy, date):
    if rejected(policy, url, programme['id'], row['year']):
        raise ValueError('Odrzucone twierdzenie: ' + programme['id'] + '/' + row['year'])
    existing = programme['thresholds']
    same = [t for t in existing if t['year'] == row['year'] and (row['round'] is None or t['round'] == row['round'])]
    if any(t['status'] == 'official' and t['value'] == row['value'] for t in same):
        return False
    note = f"Odczyt tabeli oficjalnej {date}; komórka: {row['raw']}. "
    if same:
        note += 'Nowa publikacja różni się od zapisanych wartości; zachowano je osobno, bez założenia zgodności definicji i tur. '
    existing.append(dict(year=row['year'], round=row['round'], value=row['value'], status='official', sourceId=source_id,
                         basis='unspecified', note=note + 'Brak jednoznacznej definicji kwalifikacja/przyjęcie.'))
    return True


def core_proposal(id, content, root, policy, date, datasets):
    university, url, _ = CORE[id]
    dataset_path = f'src/data/{university}.json'
    data = datasets.setdefault(dataset_path, read_json(root / dataset_path))
    years = policy['history']['admissionYears']
    detail = dict(adapter=id, parsed=0, added=0, unmatched=[])
    if id == 'uwr-european-cultures':
        path = 'src/data/curricula-uwr-a.json'
        rows = datasets.setdefault(path, read_json(root / path))
        original = next(r for r in rows if r['programmeId'] == PROGRAMME_ID)
        updated = reviewed_plan(content, original, root, date)
        detail.update(parsed=59, added=sum(len(g['subjects']) for g in updated['groups']) - sum(len(g['subjects']) for g in original['groups']))
        rows[rows.index(original)] = updated
        source = next((s for s in data['sources'] if s['id'] == SOURCE_ID), None)
        if source is None:
            source = dict(id=SOURCE_ID, title='Uniwersytet Wrocławski — European Cultures, program i plan studiów',
                          url=DOCUMENT_URL, publisher='Uniwersytet Wrocławski', kind='official',
                          note='Uchwała 168/2023, plan stacjonarnego I stopnia w języku angielskim od cyklu 2023/24. Nie potwierdza niezmienionego programu naboru 2027/28.')
            data['sources'].append(source)
        source['checkedAt'] = date
        programme = next(p for p in data['programmes'] if p['id'] == PROGRAMME_ID)
        if SOURCE_ID not in programme['sourceIds']:
            programme['sourceIds'].append(SOURCE_ID)
        return detail
    elif id.startswith('upwr-curriculum:'):
        pid = id.split(':', 1)[1]
        programme = next(p for p in data['programmes'] if p['id'] == pid)
        path = 'src/data/curricula-upwr.json'
        rows = datasets.setdefault(path, read_json(root / path))
        original = next(r for r in rows if r['programmeId'] == pid)
        parsed, audit = parse_upwr_curriculum(content, programme, url)
        rows[rows.index(original)] = {**parsed, 'checkedAt': date}
        detail.update(parsed=audit['subjectRows'], added=0, planAudit=audit)
        return detail
    elif id.startswith('pwr-curriculum:'):
        pid = id.split(':', 1)[1]
        programme = next(p for p in data['programmes'] if p['id'] == pid)
        path = 'src/data/curricula-pwr.json'
        rows = datasets.setdefault(path, read_json(root / path))
        original = next(r for r in rows if r['programmeId'] == pid)
        parsed, audit = parse_pwr_curriculum(content, programme, url)
        updated = {**original, **parsed, 'checkedAt': date,
                   'sources': [{**s, 'year': parsed['referenceYear'], 'title': audit['documentTitle']} if canonical(s['url']) == canonical(url) else s for s in original['sources']],
                   'note': f"Pełny odczyt opublikowanego planu {parsed['referenceYear']}: wszystkie semestry, tabele i rozwijane koszyki, także zagnieżdżone. "
                           'Nazwy grup są tytułami, a instrukcje wyboru nie są przedmiotami. Listy są alternatywami; nie należy realizować wszystkich wariantów. '
                           'WF i języki pozostają ogólnymi pozycjami, gdy plan odsyła do osobnej oferty Studium. Pełny plan nie oznacza szczegółowych sylabusów każdego zajęcia ani potwierdzenia uruchomienia nowego naboru.'}
        rows[rows.index(original)] = updated
        detail.update(parsed=audit['courseRows'], added=0, planAudit=audit)
        return detail
    elif id == 'uew-duration':
        import pdfplumber
        # Audyt wskazuje strony metryczek wszystkich 20 ofert. Nie odczytujemy ponownie
        # setek stron efektów uczenia się i zajęć; przesunięcie metryczki zatrzyma parser.
        pages = {1}
        for record in read_json(root / 'src/data/curricula-uew.json'):
            for source in record['sources']:
                if canonical(source['url']) == canonical(url):
                    match = re.fullmatch(r'page=(\d+)', urlsplit(source['url']).fragment)
                    if match:
                        pages.add(int(match[1]))
        with pdfplumber.open(io.BytesIO(content)) as document:
            parts = []
            for number in sorted(pages):
                page = document.pages[number - 1]
                parts.append(f'\nPAGE {number}\n' + (page.extract_text(layout=False) or ''))
                page.close()
            text = ''.join(parts)
        rows = uew_durations(text, data['programmes'])
        source_id = 'uew-duration-plan-2026'
        for row in rows:
            programme = next(p for p in data['programmes'] if p['id'] == row['programmeId'])
            if programme['duration'] and programme['duration'] != row['duration']:
                raise ValueError('Sprzeczny czas studiów wymaga przeglądu: ' + programme['id'])
            if not programme['duration']:
                programme['duration'] = row['duration']
                detail['added'] += 1
            if source_id not in programme['sourceIds']:
                programme['sourceIds'].append(source_id)
        detail['parsed'] = len(rows)
        detail['evidenceRows'] = rows
        label = 'Czas studiów — program 2026/2027, uchwała R.0000.18.2026'
    else:
        raw = history_tables(content, years, university)
        if university == 'pwr':
            parsed = subprocess.run(['node', '--experimental-strip-types', str(root / 'scripts/parse-history.ts')], input=json_bytes(raw), capture_output=True, check=True)
            rows = json.loads(parsed.stdout)
            detail['parsed'] = len(rows)
            # Źródłowe tabele i wynik parsera zachowujemy także na potrzeby regresji całego importu.
            datasets['docs/research/pwr/thresholds-active.json'] = dict(url=url, checkedAt=date, tables=raw)
            datasets['docs/research/pwr/thresholds-parsed.json'] = rows
            rows = [r for r in rows if r['inScope'] and r['status'] == 'value']
            source_id = 'pwr-thresholds'
        else:
            rows = raw
            detail['parsed'] = len(rows)
            source_id = 'uew-thresholds-2026'
        label = 'Oficjalna tabela progów — nabory 2024/25, 2025/26 i 2026/27'
        for row in rows:
            programme = match_offer(row['programme'], data['programmes'], university)
            if programme is None:
                detail['unmatched'].append({k: row[k] for k in ['programme', 'year']})
                continue  # historyczna oferta nie staje się ofertą bieżącą
            detail['added'] += add_observation(programme, row, source_id, url, policy, date)
        # Zmiana liczby dawnych wartości/tur nie może usuwać poprawnej historii.
        if university == 'pwr':
            for programme in data['programmes']:
                actual = [(t['year'], t['round'], t['value']) for t in programme['thresholds'] if t['sourceId'] == source_id]
                expected = [(r['year'], r['round'], r['value']) for r in rows if name_key(r['programme']) == name_key(programme['name'])]
                if sorted(actual) != sorted(expected):
                    raise ValueError('Zmiana lub wycofanie progu Politechniki Wrocławskiej wymaga przeglądu: ' + programme['id'])
    source = next((s for s in data['sources'] if s['id'] == source_id), None)
    if source is None:
        source = dict(id=source_id, title=label, url=url, publisher=data['universities'][0]['name'], kind='official', note='Deterministyczny odczyt źródła; program nie potwierdza uruchomienia oferty na 2027/28.')
        data['sources'].append(source)
    source['checkedAt'] = date
    source['title'] = label
    return detail


def coverage(root):
    programmes = [p for u in ['uwr', 'uew', 'pwr', 'upwr'] for p in read_json(root / f'src/data/{u}.json')['programmes']]
    curricula = [r for path in (root / 'src/data').glob('curricula-*.json') for r in read_json(path)]
    matches = {r['programmeId'] for r in read_json(root / 'src/data/graduates.json')['matches']}
    return dict(offers=len(programmes), durationMissing=[p['id'] for p in programmes if not p['duration']],
                noThresholds=[p['id'] for p in programmes if not p['thresholds']],
                noGraduateData=[p['id'] for p in programmes if p['id'] not in matches],
                curriculum={status: [r['programmeId'] for r in curricula if r['completeness'] == status]
                            for status in ['full-plan', 'listed-subjects', 'unavailable']})


def write_report(directory, report):
    atomic_write(directory / 'report.json', json_bytes(report))
    lines = ['# Aktualizacja bazy bez AI', '', 'Utworzono: ' + report['createdAt'], 'Tryb: ' + report['mode'],
             ('Propozycja została zastosowana po walidacji.' if report['applied'] else 'Aktywna baza nie została zmieniona.') + ' Pobranie nie potwierdza merytorycznej aktualności dokumentu.', '', '## Źródła', '']
    for row in report['sources']:
        lines.append(f"- {row['id']}: {row['status']} — {row['url']}")
        if row.get('error'):
            lines.append('  Błąd: ' + row['error'])
        if row.get('detail'):
            d = row['detail']
            lines.append(f"  Odczytano {d['parsed']} rekordów; dodano/uzupełniono {d['added']}; niedopasowane historyczne wiersze: {len(d['unmatched'])}.")
    lines += ['', '## Propozycja plików', ''] + ['- ' + p for p in report['files']]
    lines += ['', 'Zmiany stron bez adaptera oraz nowe dokumenty wymagają przeglądu człowieka; nie wymagają użycia AI.',
              'Raport pokrycia i identyfikatory luk: coverage.json. Wyniki walidacji są zapisywane przy zastosowaniu propozycji.']
    atomic_write(directory / 'report.md', ('\n'.join(lines) + '\n').encode('utf-8'))


def run_refresh(root, mode='core', university=None, selected=None, force=False):
    base = root / 'output/data-refresh'
    (base / 'runs').mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix=datetime.now().strftime('%Y%m%d-%H%M%S-'), dir=base / 'runs'))
    (directory / 'evidence').mkdir()
    policy = read_json(root / 'src/data/source-policy.json')
    baseline = input_hashes(root)
    date = datetime.now().astimezone().date().isoformat()
    report = dict(version=1, mode=mode, createdAt=datetime.now(timezone.utc).isoformat(), inputHashes=baseline, sources=[], files={}, applied=False)
    datasets = {}
    if mode == 'core':
        sources = [dict(id=id, university=u, url=url, purpose=purpose) for id, (u, url, purpose) in CORE.items()]
    else:
        sources = inventory(root)
    if university:
        sources = [s for s in sources if s['university'] == university]
    if selected:
        sources = [s for s in sources if s['id'] in selected]
        if {s['id'] for s in sources} != set(selected):
            raise ValueError('Nieznany identyfikator źródła lub niezgodny filtr uczelni')
    if not sources:
        raise ValueError('Brak źródeł dla wybranego filtra')
    def process(item):
        nonlocal datasets
        row = {**item}
        try:
            ensure_source_allowed(item['url'], item['purpose'])
            content, result = download(item, directory / 'evidence', base / 'cache', root, force)
            row.update(result)
            if mode == 'core':
                # Nieudany adapter nie pozostawia częściowo zmienionego zestawu propozycji.
                candidate = copy.deepcopy(datasets)
                row['detail'] = core_proposal(item['id'], content, root, policy, date, candidate)
                datasets = candidate
                row['status'] = 'parsed'
        except Exception as error:
            row.update(status='excluded' if 'POMIŃ:' in str(error) else 'failed', error=str(error))
        time.sleep(.15)
        return row
    # Adaptery zapisują jeden wspólny zestaw propozycji, dlatego działają kolejno.
    # Monitor wyłącznie pobiera osobne materiały; najwyżej trzy żądania jednocześnie.
    with ThreadPoolExecutor(max_workers=3 if mode == 'monitor' else 1) as pool:
        for row in pool.map(process, sources):
            report['sources'].append(row)
            print(row['id'] + ': ' + row['status'], flush=True)
            write_report(directory, report)
    for name, data in datasets.items():
        payload = json_bytes(data)
        current = root / name
        # Różnice CRLF/LF i formatowania nie są zmianą danych.
        if current.exists() and read_json(current) == data:
            continue
        target = directory / 'proposal' / name
        atomic_write(target, payload)
        report['files'][name] = dict(before=digest(current.read_bytes()), after=digest(payload))
    atomic_write(directory / 'coverage.json', json_bytes(coverage(root)))
    write_report(directory, report)
    print('Raport: ' + str(directory / 'report.md'))
    return directory, report


def validation_workspace(root, directory, report):
    workspace = directory / 'validation'
    if workspace.exists():
        raise ValueError('Katalog walidacji już istnieje; uruchom ponownie przygotowanie')
    workspace.mkdir()
    for folder in ['src', 'scripts', 'tests', 'public']:
        shutil.copytree(root / folder, workspace / folder, ignore=shutil.ignore_patterns('__pycache__'))
    for name in ['package.json', 'package-lock.json', 'tsconfig.json', 'index.html', 'AGENTS.md', 'README.md']:
        shutil.copy2(root / name, workspace / name)
    # Build potrzebuje instrukcji, a test PWr ma konkretne, niewielkie materiały audytu.
    for path in (root / 'docs').glob('*.md'):
        target = workspace / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for name in ['audit.json', 'additional-subjects-2027.json', 'subjects-review.txt', 'thresholds-active.json', 'thresholds-parsed.json']:
        target = workspace / 'docs/research/pwr' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / 'docs/research/pwr' / name, target)
    for name in report['files']:
        target = workspace / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(directory / 'proposal' / name, target)
    return workspace


def apply_refresh(root, supplied):
    directory = Path(supplied).resolve()
    allowed = (root / 'output/data-refresh/runs').resolve()
    if directory.parent != allowed or directory.is_symlink():
        raise ValueError('Wskaż konkretny folder uruchomienia w output/data-refresh/runs')
    report = read_json(directory / 'report.json')
    if report.get('version') != 1 or report.get('mode') != 'core' or report.get('applied'):
        raise ValueError('To nie jest nowa propozycja adapterów danych')
    if any(r['status'] != 'parsed' for r in report['sources']):
        raise ValueError('Źródło lub adapter nie przeszedł kontroli; poprzednia baza pozostaje bez zmian')
    if report['inputHashes'] != input_hashes(root):
        raise ValueError('Dane, polityka lub adapter zmieniły się po przygotowaniu propozycji. Uruchom odświeżenie ponownie')
    if not set(report['files']).issubset(ALLOWED_OUTPUTS):
        raise ValueError('Propozycja zawiera plik poza zakresem adapterów')
    for name, info in report['files'].items():
        proposal = directory / 'proposal' / name
        if proposal.is_symlink() or digest(proposal.read_bytes()) != info['after'] or digest((root / name).read_bytes()) != info['before']:
            raise ValueError('Zmodyfikowano propozycję lub plik bazowy: ' + name)
    if not report['files']:
        print('Brak zmian danych do zastosowania.')
        return
    workspace = validation_workspace(root, directory, report)
    checks = [(['node', '--experimental-strip-types', '--test', 'tests/*.test.ts'], 'tests'),
              (['node', '--experimental-strip-types', 'scripts/validate-data.ts'], 'data'),
              (['node', str(root / 'node_modules/typescript/bin/tsc'), '--noEmit'], 'types'),
              (['node', str(root / 'node_modules/vite/bin/vite.js'), 'build'], 'build'),
              (['node', 'scripts/check-release.mjs'], 'release')]
    for command, label in checks:
        result = subprocess.run(command, cwd=workspace, capture_output=True)
        atomic_write(directory / f'check-{label}.log', result.stdout + result.stderr)
        if result.returncode:
            raise ValueError('Kontrola ' + label + ' nie przeszła; aktywna baza bez zmian. Zobacz log w folderze raportu')
    # Po dłuższej walidacji ponownie wykrywamy pracę równoległą.
    if report['inputHashes'] != input_hashes(root):
        raise ValueError('Aktywne dane zmieniły się podczas walidacji; niczego nie zastosowano')
    originals = {name: (root / name).read_bytes() for name in report['files']}
    for name, payload in originals.items():
        atomic_write(directory / 'backup' / name, payload)
    try:
        for name in originals:
            atomic_write(root / name, (directory / 'proposal' / name).read_bytes())
    except Exception:
        for name, payload in originals.items():
            atomic_write(root / name, payload)
        raise
    report['applied'] = True
    report['appliedAt'] = datetime.now(timezone.utc).isoformat()
    write_report(directory, report)
    atomic_write(directory / 'coverage-after.json', json_bytes(coverage(root)))
    print('Zastosowano po pięciu kontrolach: ' + str(len(originals)) + ' plików. Kopia poprzednich danych: ' + str(directory / 'backup'))


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['sources', 'run', 'apply', 'coverage'])
    parser.add_argument('folder', nargs='?')
    parser.add_argument('--mode', choices=['core', 'monitor'], default='core')
    parser.add_argument('--university', choices=['uwr', 'uew', 'pwr', 'upwr'])
    parser.add_argument('--source', action='append')
    parser.add_argument('--force', action='store_true', help='Sprawdź sieć także przed upływem 24 godzin')
    args = parser.parse_args()
    base = ROOT / 'output/data-refresh'
    base.mkdir(parents=True, exist_ok=True)
    lock = base / 'refresh.lock'
    try:
        if args.command == 'sources':
            print(json.dumps(inventory(ROOT), ensure_ascii=False, indent=2))
        elif args.command == 'coverage':
            print(json.dumps(coverage(ROOT), ensure_ascii=False, indent=2))
        else:
            # Wyłączne uruchomienie chroni cache i wieloplikowe zastosowanie danych.
            with lock.open('x', encoding='utf-8') as stream:
                stream.write(str(os.getpid()))
            try:
                if args.command == 'apply':
                    if not args.folder:
                        raise ValueError('Podaj folder uruchomienia z raportem')
                    apply_refresh(ROOT, args.folder)
                else:
                    _, report = run_refresh(ROOT, args.mode, args.university, args.source, args.force)
                    if any(r['status'] in ['failed', 'blocked'] for r in report['sources']):
                        return 2
            finally:
                lock.unlink()
        return 0
    except FileExistsError:
        print('Aktualizacja już trwa albo poprzedni proces pozostawił blokadę: ' + str(lock), file=sys.stderr)
        return 2
    except Exception as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
