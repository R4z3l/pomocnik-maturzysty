"""Odczyt oficjalnej uchwały R.0000.18.2026 z lokalnego, sprawdzonego PDF.
Pliki badawcze pobierane uprzednio przez source_policy.guarded_get.
"""
from pathlib import Path
from collections import defaultdict
from bs4 import BeautifulSoup
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'docs/research/curricula/uew'
URL = 'https://bip.ue.wroc.pl/download/attachment/4064/zalacznik-do-uchwaly-senatu-r0000182026.pdf?v=1778225564'
pages = re.split(r'\nPAGE \d+\n', (CACHE / 'Programy-2026.txt').read_text(encoding='utf-8'))[1:]
starts = [i for i, text in enumerate(pages) if 'Poziom kształcenia' in text]
headings = json.loads((CACHE / 'headings.json').read_text(encoding='utf-8'))
row_pattern = re.compile(r'^(.+?)\s+([IVX]+(?:\s*[,/-]\s*[IVX]+)*)\s+(?:[EZez]|Exam|Grade|Pass|Credited)\s+([\d ].*)$')
programmes = json.loads((ROOT / 'src/data/uew.json').read_text(encoding='utf-8'))['programmes']
result = []
audit = []
for programme in programmes:
    slug = {'uew-informatyka-w-zarzadzaniu-produkcja': 'informatyka',
            'uew-nieruchomosci-i-gospodarka-przestrzenna': 'nieruchomosci-i-gospodarka-przestrzenna-2'}.get(
        programme['id'], programme['id'].removeprefix('uew-'))
    html = BeautifulSoup((CACHE / (slug + '.html')).read_text(encoding='utf-8'), 'html.parser')
    page_url = f'https://rekrutacja.uew.pl/kierunki-studiow/{slug}/'
    special_names = [e.get_text(' ', strip=True) for e in html.select('.wp-block-ub-content-toggle-accordion-title')]
    h2 = ' '.join(e.get_text(' ', strip=True).lower() for e in html.select('h2'))
    kind = 'moduł' if 'moduł' in h2 or 'modules' in h2 else 'specjalność'
    # Znajdź blok uczelni macierzystej I stopnia, z nazwą i językiem.
    selected = [i for i in starts if re.sub(r'\s+', ' ', pages[i].split('Poziom kształcenia')[0]).strip().casefold() == programme['name'].casefold()
                and 'studia pierwszego stopnia' in pages[i]
                and ('angielski' if programme['language'] == 'en' else 'polski') in pages[i].lower()]
    assert len(selected) == 1, (programme['id'], selected)
    start = selected[0]
    end = next((i for i in starts if i > start), len(pages))
    group_rows = defaultdict(list)
    section = 'Przedmioty planu'
    elective = False
    parsed, omitted, pdf_specials = [], [], []
    special_kind = kind
    for i in range(start, end):
        text = pages[i]
        if not (re.search(r'\b(?:SEKCJA|SECTION|SZCZEGÓŁOWY WYKAZ|LIST OF MODULES|LIST OF SPECIALIZATIONS)\b', text) or 'Sem.' in text and ('I ST' in text)):
            continue  # opisy kwalifikacji i efekty uczenia się nie są listą zajęć
        pending = ''
        for line in text.splitlines():
            line = re.sub(r'\s+', ' ', line).strip()
            if not line:
                pending = ''
                continue
            if line.startswith(('SEKCJA ', 'SECTION ')):
                section = line.split('. ', 1)[-1].capitalize()
                elective = False
                pending = ''
                continue
            if line.startswith(('SZCZEGÓŁOWY WYKAZ', 'LIST OF MODULES', 'LIST OF SPECIALIZATIONS')):
                special_kind = 'moduł' if ('MODUŁ' in line or 'MODULE' in line) else 'specjalność'
                section = 'Zajęcia do wyboru — moduły / specjalności'
                elective = True
                pending = ''
                continue
            if elective and (line in headings.get(str(i+1), []) or any(line.casefold() == name.casefold() for name in special_names)):
                section = 'Do wyboru: ' + line
                if line not in [x['name'] for x in pdf_specials]: pdf_specials.append({'name': line, 'kind': special_kind})
                pending = ''
                continue
            match = row_pattern.match(line)
            if match:
                name, semester, quantities = match.groups()
                name = (pending + ' ' + name).strip()
                pending = ''
                if re.search(r'\b(?:N|PT)[12]\b', name):
                    omitted.append(name)
                    continue
                name = re.sub(r'\s*-\s*(?:S|FT)[12]\b', '', name)
                group_rows[(section, semester)].append(name)
                parsed.append({'page': i + 1, 'name': name, 'semester': semester, 'section': section})
                continue
            # Wiersze sum, nagłówki tabeli i metadane nie są fragmentami nazwy.
            if (not re.match(r'^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż]', line)
                or line.startswith(('RAZEM', 'TOTAL', 'I ST', 'II ST', 'Studia ', 'Full-time', 'Part-time', 'Nazwa ', 'Liczba ', 'godzin ', 'hours ', 'Total ', 'Course', 'Sem.', 'Forma', 'Credit', 'form', 'zal.', 'E C T S', 'winter ', 'summer ', 'zima ', 'lato '))
                or len(line) < 3 or line.isupper() and not elective):
                pending = ''
                continue
            # Na stronie szczegółów: nazwa nowego modułu poprzedza jego kursy.
            if elective and not pending and not re.search(r'\d', line) and (line.isupper() or line in special_names):
                section = 'Do wyboru: ' + line
                continue
            pending = (pending + ' ' + line).strip()
    assert len(parsed) >= 30, (programme['id'], len(parsed))
    assert all(len(r['name']) < 180 for r in parsed), [(r['page'],r['name']) for r in parsed if len(r['name'])>=180]
    groups = [{'title': title, 'semester': sem, 'subjects': subjects, 'sourceUrl': URL + f'#page={start+1}'} for (title, sem), subjects in group_rows.items()]
    source_url = URL + f'#page={start+1}'
    record = {
        'programmeId': programme['id'], 'checkedAt': '2026-10-25', 'referenceYear': '2026/2027',
        'completeness': 'full-plan', 'groups': groups,
        'specializations': [{'name': x['name'], 'kind': x['kind'], 'note': 'Wariant z planu2026/27; lista na bieżącej stronie kierunku może mieć inne nazwy. Uruchomienie zależy od warunków uczelni.', 'sourceUrl': source_url} for x in pdf_specials],
        'specializationStatus': 'listed' if pdf_specials else 'not-found',
        'note': f'Spis z załącznika do uchwały Senatu R.0000.18.2026 z 23 kwietnia 2026 r., strony {start+1}–{end}. '
                'Studia I stopnia, Wrocław. Zachowano nazwy pozycji ogólnych (np. przedmiot do wyboru) i zajęć wariantowych. '
                'Pominięto wiersze językowe przeznaczone wyłącznie dla trybu niestacjonarnego. Lista zawiera alternatywne moduły/specjalności — nie należy realizować ich wszystkich.',
        'sources': [{'title': 'Oficjalny program studiów — załącznik do uchwały Senatu R.0000.18.2026', 'url': source_url, 'year': '2026/2027', 'note': f'Potwierdzono nazwę, I stopień, język i siedzibę; zakres stron {start+1}–{end}.'},
                    {'title': 'Specjalności i moduły — oficjalna strona kierunku', 'url': page_url, 'year': 'Opis bieżący; bez odrębnego rocznika modułów', 'note': 'Nazwy z sekcji specjalności/modułów, nie z listy zawodów. Weryfikacja25.10.2026.'}],
    }
    result.append(record)
    audit.append({'programmeId': programme['id'], 'pages': [start+1,end], 'parsed': parsed, 'omittedPartTime': omitted})
(ROOT / 'src/data/curricula-uew.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
(CACHE / 'extraction-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for r in result:
    print(r['programmeId'], sum(len(g['subjects']) for g in r['groups']), 'przedmiotów;', len(r['specializations']), 'wariantów')
