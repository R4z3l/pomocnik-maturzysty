"""Odczyt oficjalnego Sylabusa Uniwersytetu Przyrodniczego we Wrocławiu.

Parser nie pobiera sieci. Zachowuje semestry i koszyki wyboru, również ukryte w HTML.
Nie zamienia opisów ani efektów uczenia się w nazwy przedmiotów.
"""
import re
from collections import defaultdict
from bs4 import BeautifulSoup


def clean(value):
    return ' '.join(value.split())


def parse_upwr_curriculum(content, programme, url):
    soup = BeautifulSoup(content, 'html.parser')
    title = clean(soup.title.get_text()) if soup.title else ''
    if '2026/27' not in title or 'stacjonarne' not in title or 'niestacjonarne' in title:
        raise ValueError('Niepotwierdzony cykl albo forma planu: ' + title)
    level = 'jednolite studia magisterskie' if programme['level'] == 'long-cycle' else 'studia pierwszego stopnia'
    if level not in title:
        raise ValueError('Inny poziom planu: ' + title)
    expected = programme['name'].lower().replace(' w języku angielskim', '')
    if programme['language'] == 'en' and programme['level'] == 'long-cycle':
        expected = 'weterynaria (veterinary medicine)'
    actual = title.split(':')[0].lower()
    if expected != actual:
        raise ValueError('Inna nazwa planu: ' + title)
    tabs = soup.select('[role="tab"][aria-controls]')
    groups, counts = [], []
    for tab in tabs:
        match = re.fullmatch(r'Semestr (\d+)', clean(tab.get_text()))
        if not match:
            raise ValueError('Nieznany nagłówek semestru')
        panel = soup.find(id=tab['aria-controls'])
        if panel is None:
            raise ValueError('Brak treści semestru')
        baskets = {b['id']: clean(b.get_text()) for b in panel.select('button.syl-group-head[id]')}
        rows = defaultdict(list)
        for button in panel.select('button[data-syllabus-id]'):
            row = button.find_parent('tr')
            name = clean(button.get_text())
            if not row or not name:
                raise ValueError('Pusty przedmiot')
            basket = next((baskets.get(c.removesuffix('-element')) for c in row.get('class', []) if c.startswith('syl-group-')), None)
            cells = row.find_all('td', recursive=False)
            status = clean(cells[-1].get_text()) if len(cells) >= 5 else ''
            heading = ('Pula wyboru: ' + basket) if basket else ('Przedmioty — ' + status)
            if name not in rows[heading]:
                rows[heading].append(name)
        # Pozycja ogólna pozostaje ogólna, jeżeli uczelnia nie rozwinęła jej w przedmioty.
        for button in panel.select('button.syl-group-head[id]'):
            containers = [panel.find(id=i) for i in button.get('aria-controls', '').split()]
            if not any(c and c.select_one('button[data-syllabus-id]') for c in containers):
                rows['Nierozwinięte pozycje planu'].append(clean(button.get_text()))
        if not rows:
            raise ValueError('Pusty semestr ' + match[1])
        counts.append(sum(map(len, rows.values())))
        groups.extend(dict(title=heading, semester=match[1], subjects=names, sourceUrl=url) for heading, names in rows.items())
    if len(tabs) not in (6, 7, 8, 11, 12):
        raise ValueError('Niepotwierdzona liczba semestrów')
    duration = re.search(r'(\d+) semestr', programme.get('duration') or '')
    if not duration or int(duration[1]) != len(tabs):
        raise ValueError('Liczba semestrów nie zgadza się z kartą oferty')
    record = dict(programmeId=programme['id'], checkedAt='2026-11-10', referenceYear='2026/2027',
                  completeness='full-plan', groups=groups, specializations=[], specializationStatus='not-found',
                  note='Spis wszystkich opublikowanych semestrów i rozwiniętych koszyków wyboru w Sylabusie uczelni. '
                       'Pozycje ogólne pozostają ogólne. Warianty w puli nie oznaczają obowiązku ukończenia wszystkich zajęć. '
                       'Nie potwierdzono osobnej listy specjalności; nie utożsamiamy koszyków ze specjalnościami. '
                       'Plan cyklu 2026/2027 nie jest gwarancją programu dla naboru 2027/2028.',
                  sources=[dict(title='Uniwersytet Przyrodniczy we Wrocławiu — Sylabus: ' + programme['name'],
                                url=url, year='2026/2027', note='Właściwy kierunek, poziom i forma stacjonarna. Odczytano wszystkie semestry, także ukryte pule wyboru.')])
    return record, dict(semesters=len(tabs), subjectsPerSemester=counts, subjectRows=sum(counts), title=title)
