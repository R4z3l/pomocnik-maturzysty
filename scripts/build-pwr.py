"""Odtwarza pakiet Politechniki Wrocławskiej wyłącznie z lokalnych dowodów audytu.

Nie pobiera stron. Kopie w docs/research/pwr zebrano po kontroli polityki źródeł.
"""
import json
import re
import unicodedata
from pathlib import Path

import pdfplumber
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/research/pwr'
DATE = '2026-11-02'
LIST_URL = 'https://rekrutacja.pwr.edu.pl/wyszukiwarka-kierunkow-studiow/'
HISTORY_URL = 'https://rekrutacja.pwr.edu.pl/rekrutacja/progi-punktowe/progi-studia-i-stopnia-stacjonarne/'
RULE_URL = 'https://rekrutacja.pwr.edu.pl/wp-content/uploads/2026/06/WIR-2027_2028-Zalacznik-nr-1-dokument-glowny.pdf'
SUBJECT_URL = 'https://rekrutacja.pwr.edu.pl/wp-content/uploads/2026/06/WIR-2027_2028-Zalacznik-nr-3-przedmioty-maturalne.pdf'


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def key(text):
    return clean(text).casefold()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def soup(path):
    return BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')


def source(id, title, url, note):
    return dict(id=id, title=title, url=url, publisher='Politechnika Wrocławska', checkedAt=DATE, kind='official', note=note)


# Załącznik 3 nie zawiera znaków X: dopuszczenia są kolorowym tłem komórek.
# Rozpoznajemy rzeczywiste wypełnienia wektorowe, nie kolejność tekstu w PDF.
additional = {}
columns = ['biologia', 'biznes i zarządzanie', 'chemia', 'fizyka', 'geografia', 'informatyka', 'matematyka']
with pdfplumber.open(EVIDENCE / 'subjects27.pdf') as document:
    for page in document.pages:
        blue = [r for r in page.rects if r['non_stroking_color'] and .50 < r['non_stroking_color'][0] < .54]
        rows = [r for r in page.rects if r['non_stroking_color'] and .94 < r['non_stroking_color'][0] < .96 and 260 < r['width'] < 300]
        for rect in rows:
            words = [w for w in page.extract_words() if w['x0'] >= rect['x0'] - 1 and w['x1'] < rect['x1'] + 1 and rect['top'] <= (w['top']+w['bottom'])/2 < rect['bottom']]
            lines = {}
            for w in words:
                lines.setdefault(round(w['top']), []).append(w)
            subjects = [name for i, name in enumerate(columns) if any(r['x0'] <= 341.8+21*i <= r['x1'] and r['top'] <= (rect['top']+rect['bottom'])/2 <= r['bottom'] for r in blue)]
            for line in lines.values():
                name = clean(' '.join(w['text'] for w in sorted(line, key=lambda w: w['x0'])))
                if name:
                    additional[key(name)] = subjects
assert additional['lekarski'] == ['chemia', 'fizyka']
assert additional['automatyka i robotyka'] == ['fizyka', 'informatyka', 'matematyka']
assert additional['pozostałe kierunki studiów'] == ['fizyka']
write(EVIDENCE / 'additional-subjects-2027.json', additional)

# Zachowujemy tury i dopiski. Tabele starsze od 2024/25 nie są przetwarzane.
tables = []
for table in soup(EVIDENCE / 'progi.html').select('main table'):
    year = table.find_previous(['h2', 'h3', 'h4']).get_text(' ', strip=True)
    if year not in ['2026/2027', '2025/2026', '2024/2025']:
        continue
    rows = [[dict(text=clean(c.get_text(' ', strip=True)), rowSpan=int(c.get('rowspan', 1)), colSpan=int(c.get('colspan', 1))) for c in tr.find_all(['td', 'th'], recursive=False)] for tr in table.select('tr')]
    tables.append(dict(year=year, rows=rows))
assert len(tables) == 3
write(EVIDENCE / 'thresholds-active.json', dict(url=HISTORY_URL, checkedAt=DATE, tables=tables))

sources = [source('pwr-list', 'Politechnika Wrocławska — wyszukiwarka kierunków', LIST_URL, 'Pełny spis poziomu s1, sprawdzony także bez filtrów; metryczki rozstrzygają formę i kampus.'), source('pwr-rules-2027', 'Politechnika Wrocławska — zasady rekrutacji 2027/2028', RULE_URL, 'Uchwała 384/26/2024-2028, załącznik 1, §9–12. Zmiana 412 z 24.09.2026 dotyczy załącznika 5 (II stopnia), nie tego zakresu.'), source('pwr-subjects-2027', 'Politechnika Wrocławska — przedmioty dodatkowe 2027/2028', SUBJECT_URL, 'Załącznik 3: odczyt kolorowych komórek tabeli, obie strony.'), source('pwr-thresholds', 'Politechnika Wrocławska — oficjalne progi stacjonarne', HISTORY_URL, 'Wyłącznie nabory 2024/25, 2025/26, 2026/27; tury rozdzielone, filie pominięte.')]
programmes, curricula, audit = [], [], []
links = {x['courseId']: x['url'] for x in json.loads((EVIDENCE/'syllabus-links.json').read_text(encoding='utf-8'))}
foreign = ['język angielski', 'język niemiecki', 'język francuski', 'język hiszpański', 'język rosyjski', 'język włoski']
for item in json.loads((EVIDENCE/'manifest-all.json').read_text(encoding='utf-8')):
    cid = item['courseId']
    card = soup(EVIDENCE/'cards'/f'{cid}.html').find('main')
    fields = {d.h3.get_text(' ', strip=True): clean(d.ul.get_text(' ', strip=True)) for d in card.select('.course-data-bar__data-wrapper')}
    name = clean(item['name'])
    reason = 'Filia w Jeleniej Górze — poza Wrocławiem.' if 'Wrocław' not in fields.get('Miasto', '') else 'Karta oznaczona bez naboru na 2026/27; brak potwierdzenia uruchomienia 2027/28.' if cid == '139' else None
    if reason:
        audit.append(dict(**item, included=False, reason=reason)); continue
    assert any(x in fields['Forma studiów'] for x in ['Dzienne', 'Stacjonarne']), name
    slug = unicodedata.normalize('NFKD', name.lower().replace('ł', 'l')).encode('ascii', 'ignore').decode()
    pid = 'pwr-' + re.sub('[^a-z0-9]+', '-', slug).strip('-')
    language = 'en' if fields['Język wykładowy'] == 'angielski' else 'pl'
    level = 'long-cycle' if cid == '10248' else 'bachelor'
    duration = re.search(r'\d+\s*semestr\w*', fields.get('Czas trwania', ''))
    duration = duration.group() if duration else '7 semestrów' if fields.get('Czas trwania') == '7' else None
    description_tab = card.select_one('.content-tabs__content-wrapper[data-tab-id="1-1"]')
    paragraphs = description_tab.select('p') if description_tab else []
    paragraph = next((clean(p.get_text(' ', strip=True)) for p in paragraphs if len(clean(p.get_text(' ', strip=True))) > 80), '')
    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    description = ''
    for sentence in sentences[:2]:
        if len(description + sentence) > 650: break
        description += (' ' if description else '') + sentence
    if not description:
        description = f'{name} — studia stacjonarne we Wrocławiu. Obszar kształcenia według metryczki uczelni: {fields.get("Dyscyplina", "opis na oficjalnej karcie")}. Szczegóły programu znajdziesz w źródłach.'
    # Nazwy obszarów pochodzą z metryczki, nie z nazw przedmiotów maturalnych.
    areas = [clean(x) for x in fields.get('Dyscyplina', '').split(',') if clean(x)]
    pd_name = re.sub(r' w j\. angielskim$', '', key(name))
    pd = additional.get(pd_name, additional['pozostałe kierunki studiów'])
    subjects = list(dict.fromkeys(['matematyka', *pd, *(['biologia'] if level == 'long-cycle' else []), 'język polski', *foreign]))
    sid = 'pwr-card-' + cid
    sources.append(source(sid, f'Politechnika Wrocławska — {name}', item['url'], 'Metryczka i opis kierunku; wyłącznie stacjonarny wariant we Wrocławiu. Karta może równocześnie opisywać inne formy lub miasta.'))
    groups, specializations = [], []
    curriculum_sources = [dict(title=f'{name} — karta kierunku', url=item['url'], year='Sprawdzono 2026-11-02; karta nie datuje programu', note='Metryczka potwierdza język, poziom, formę i lokalizację.')]
    syllabus_file = EVIDENCE/'syllabi'/f'{cid}.html'
    year = 'Rocznik nieustalony'
    if cid in links and syllabus_file.exists():
        syllabus = soup(syllabus_file)
        title = clean(syllabus.title.get_text(' ', strip=True)) if syllabus.title else ''
        match = re.search(r'20\d\d/20\d\d', title)
        valid = match and 'studia stacjonarne' in title and ('studia pierwszego stopnia' in title if level == 'bachelor' else 'jednolite studia magisterskie' in title)
        if valid:
            year = match.group()
            curriculum_sources.append(dict(title=title, url=links[cid], year=year, note='Oficjalny program wskazany bezpośrednio przez kartę kierunku; zajęcia do wyboru i specjalności są wariantami.'))
            tabs = {a.get('aria-controls'): clean(a.get_text(' ', strip=True)).removeprefix('Semestr ') for a in syllabus.select('[role=tab]') if re.fullmatch(r'Semestr \d+', clean(a.get_text(' ', strip=True)))}
            for tab_id, semester in tabs.items():
                tab = syllabus.find(id=tab_id)
                if not tab: continue
                for table in tab.find_all('table'):
                    subjects_in_table = []
                    for tr in table.select('tbody > tr'):
                        td = tr.find('td', recursive=False)
                        if not td: continue
                        for detail in td.find_all('dl'): detail.decompose()
                        value = clean(td.get_text(' ', strip=True))
                        if value and value not in ['Suma', 'Łącznie', 'Total'] and not re.fullmatch(r'[\d\s.,]+', value): subjects_in_table.append(value)
                    if subjects_in_table:
                        special = table.find_previous('h2')
                        variant = clean(special.get_text(' ', strip=True)) if special and special in tab.descendants else ''
                        variant_title = variant if key(variant).startswith(('ścieżka', 'moduł')) else 'Specjalność: ' + variant
                        groups.append(dict(title=variant_title if variant else 'Zajęcia kierunkowe i do wyboru', semester=semester, subjects=list(dict.fromkeys(subjects_in_table)), sourceUrl=links[cid]))
            for h in syllabus.select('.tab-pane h2'):
                value = clean(h.get_text(' ', strip=True))
                kind = 'ścieżka' if key(value).startswith('ścieżka') else 'moduł' if key(value).startswith('moduł') else 'specjalność'
                if value and not any(x['name'] == value for x in specializations): specializations.append(dict(name=value, kind=kind, note='Wariant programu; uruchomienie nie jest gwarantowane dla nowego naboru.', sourceUrl=links[cid]))
    note = 'Sprawdzono kartę rekrutacyjną i wskazany przez nią oficjalny program. Nie potwierdza to oferty 2027/28. Spis zachowuje semestry oraz alternatywne grupy zajęć. Nie zebrano szczegółowych kart efektów uczenia się.' if groups else 'Sprawdzono kartę rekrutacyjną i jej odsyłacze do programu. Brak zweryfikowanego spisu przedmiotów dla tego wariantu w zebranych materiałach; brak listy nie oznacza braku programu.'
    curricula.append(dict(programmeId=pid, checkedAt=DATE, referenceYear=year, completeness='listed-subjects' if groups else 'unavailable', groups=groups, specializations=specializations, specializationStatus='listed' if specializations else 'not-found', note=note, sources=curriculum_sources))
    programme = dict(id=pid, universityId='pwr', name=name, language=language, level=level, city='Wrocław', duration=duration, referenceYear=year, description=description, fields=areas, subjects=subjects, subjectsVerified=True, admissionNote='Opublikowane zasady 2027/2028, uchwała 384/26/2024-2028. Polska nowa matura: ' + ('WM = B + M + PD + 0,1JO + 0,1JP; biologia rozszerzona i matematyka wymagane, minimum formalne 500 pkt.' if level == 'long-cycle' else 'WI = M + PD + 0,1JO + 0,1JP; architektura dodatkowo wymaga zdanego egzaminu z rysunku (240–660 pkt).') + ' Rocznik zasad nie potwierdza uruchomienia oferty 2027/28. Szczególne uprawnienia, egzaminy zawodowe i inne rodzaje matur wymagają osobnej weryfikacji.', sourceIds=[sid, 'pwr-list', 'pwr-rules-2027', 'pwr-subjects-2027', 'pwr-thresholds'], thresholds=[], careers=[], careerNote='Nie przypisano jeszcze zweryfikowanych ścieżek zawodowych do tej oferty. Opis perspektyw na oficjalnej karcie nie stanowi potwierdzenia uprawnień zawodowych ani gwarancji zatrudnienia.', admissionRuleId=pid+'-2027')
    historical_key = key(name).replace('w j. angielskim', 'w języku angielskim')
    for t in json.loads((EVIDENCE/'thresholds-parsed.json').read_text(encoding='utf-8')):
        if not t['inScope'] or t['status'] != 'value' or key(t['programme']).replace('w j. angielskim', 'w języku angielskim') != historical_key: continue
        programme['thresholds'].append(dict(year=t['year'], round=t['round'], value=t['value'], status='official', sourceId='pwr-thresholds', basis='unspecified', note='Oficjalna tabela Politechniki Wrocławskiej, wydział: ' + t['faculty'] + '. Publikacja nie precyzuje tu definicji kwalifikacja/przyjęcie. Zapis komórki: ' + t['raw'] + '. Dopisek w nawiasie pozostaje dopiskiem źródła, nie drugim progiem; kreska i brak uruchomienia nie są zerem.'))
    programmes.append(programme)
    audit.append(dict(**item, included=True, programmeId=pid, metadata=fields, programmeYear=year, subjectCount=sum(len(g['subjects']) for g in groups), additionalSubjects=pd))

assert len(programmes) == 62
write(ROOT/'src/data/pwr.json', dict(version='2026-11-02', checkedAt=DATE, scopeNote='Stacjonarne, Wrocław, I stopień i jednolite magisterskie; PL/EN.', universities=[dict(id='pwr', name='Politechnika Wrocławska', shortName='PWr', sourceIds=['pwr-list', 'pwr-rules-2027', 'pwr-subjects-2027', 'pwr-thresholds'], coverage='62 oferty we Wrocławiu z 64 kart spisu poziomu s1: 61 ofert I stopnia i kierunek lekarski (jednolite magisterskie). Pominięto ofertę filii w Jeleniej Górze i kartę bez naboru 2026/27. Programy mają własne roczniki; zasady 2027/28 nie potwierdzają uruchomienia każdej oferty. Karty bez datowanego programu mają rocznik nieustalony.')], sources=sources, programmes=programmes))
write(ROOT/'src/data/curricula-pwr.json', curricula)
write(EVIDENCE/'audit.json', dict(checkedAt=DATE, scope='Wrocław, stacjonarne, I stopień/jednolite, PL/EN', listUrl=LIST_URL, listCount=len(audit), included=len(programmes), rows=audit))
rules = []
for p in programmes:
    row = next(x for x in audit if x.get('programmeId') == p['id'])
    def group(label, subjects, weight=1, extended=2.5, basic=1):
        return dict(label=label, subjects=subjects, factors=dict(basic=basic, extended=extended, bilingual=0), weight=weight, optional=True)
    groups = [group('Matematyka', ['matematyka']), group('Przedmiot dodatkowy', row['additionalSubjects']), group('Język obcy', foreign, .1), group('Język polski', ['język polski'], .1, 1)]
    medical = p['level'] == 'long-cycle'
    if medical: groups.insert(0, group('Biologia rozszerzona', ['biologia'], basic=0))
    rule = dict(id=p['admissionRuleId'], year='2027/2028', title='Politechnika Wrocławska — ' + p['name'] + ', polska nowa matura', formula=('WM = B + M + PD + 0,1JO + 0,1JP' if medical else 'WI = M + PD + 0,1JO + 0,1JP + RA') + '; M, PD i JO = max(P, P + 1,5R, 2,5R), osobno dla każdego przedmiotu; JP = max(P, R). B = 2,5R z biologii; RA dotyczy wyłącznie architektury.', sourceUrl=RULE_URL, checkedAt=DATE, groups=groups, caveat='Uchwała 384/26/2024-2028, załącznik 1 (§9–12) i załącznik 3. Kalkulator obsługuje wyłącznie polską nową maturę pisemną PP/PR; zaznaczony wynik bez procentu blokuje obliczenie, przedmiot niezdawany daje 0. Matematyka może być również przedmiotem dodatkowym, gdy dopuszcza ją tabela. Nie obejmuje matury dwujęzycznej (w tym dodatkowych egzaminów w obcym języku), IB/EB, starej matury, egzaminów zawodowych, dobrowolnych egzaminów uczelni ani olimpiad. Brak zewnętrznego wyniku nie jest szacowany. Zasady 2027/28 nie potwierdzają uruchomienia oferty. Dokumenty i ewentualne wymagania językowe dla studiów po angielsku trzeba sprawdzić osobno. Minimalne wskaźniki rektora i progi komisji dla nowego naboru mogą zostać ogłoszone odrębnie; nie są przenoszone z historii.')
    if medical:
        rule['minimumTotal'] = 500
        rule['caveat'] += ' Jeżeli B = 0 lub M = 0, cały WM wynosi 0; minimum formalne 500 pkt nie jest progiem ostatniej osoby.'
    else:
        rule['caveat'] += ' Jeżeli M = 0 i PD = 0, składniki JO i JP przyjmują wartość 0.'
    if p['name'] == 'Architektura': rule['extraExam'] = dict(key='rysunek', label='Egzamin z rysunku', min=0, max=660, passMin=240, note='Dwa zadania rysunkowe; zaliczenie od 240 pkt. Uwzględnia się wyłącznie egzamin z rekrutacji 2027/2028.')
    rules.append(rule)
write(ROOT/'src/data/pwr-rules.json', rules)
print('Pakiet:', len(programmes), 'ofert;', sum(bool(c['groups']) for c in curricula), 'spisów;', len(sources), 'źródeł')
