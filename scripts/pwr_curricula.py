"""Odczyt wszystkich semestrów i rozwijanych grup oficjalnego planu Politechniki Wrocławskiej."""
import re
from collections import OrderedDict
from bs4 import BeautifulSoup
from refresh_parsers import clean, name_key


def parse_pwr_curriculum(content, programme, source_url):
    soup = BeautifulSoup(content, 'html.parser')
    title = clean(soup.title.get_text(' ', strip=True)) if soup.title else ''
    year = re.search(r'\b20\d{2}/20\d{2}\b', title)
    name = title.split(':')[0]
    if programme['id'] == 'pwr-lekarski' and name_key(name) == 'kierunek lekarski':
        name = 'Lekarski'
    level = 'jednolite studia magisterskie' if programme['level'] == 'long-cycle' else 'studia pierwszego stopnia'
    if not year or name_key(name) != name_key(programme['name']) or level not in title or 'studia stacjonarne' not in title:
        raise ValueError('Niezgodna tożsamość planu: ' + programme['id'])
    english_name = 'w języku angielskim' in name_key(name) or name_key(name) in ['electronic and computer engineering', 'medical informatics']
    if (programme['language'] == 'en') != english_name:
        raise ValueError('Niezgodny język planu: ' + programme['id'])
    tabs = {a.get('aria-controls'): int(clean(a.get_text(' ', strip=True)).split()[-1])
            for a in soup.select('[role=tab]') if re.fullmatch(r'Semestr \d+', clean(a.get_text(' ', strip=True)))}
    duration = re.search(r'\b(\d+)\s+semestr', programme['duration'] or '')
    if not duration or sorted(tabs.values()) != list(range(1, int(duration[1]) + 1)):
        raise ValueError('Brak kompletnego zakresu semestrów: ' + programme['id'])
    groups = OrderedDict()
    notes, controls, course_rows, all_tables = [], 0, 0, set()
    for tab_id, semester in tabs.items():
        tab = soup.find(id=tab_id)
        if tab is None:
            raise ValueError('Brak treści semestru: ' + str(semester))
        tables = tab.find_all('table')
        if not tables:
            raise ValueError('Pusty semestr: ' + str(semester))
        for table in tables:
            all_tables.add(id(table))
            headers = [clean(t.get_text(' ', strip=True)) for t in table.select('thead th')]
            if headers != ['Przedmiot', 'Liczba godzin', 'Forma weryfikacji', 'Punkty ECTS', 'Obligatoryjność', 'Kod USOS']:
                raise ValueError('Nieznany układ planu: ' + programme['id'])
            variant_heading = table.find_previous('h2')
            variant = clean(variant_heading.get_text(' ', strip=True)) if variant_heading and variant_heading in tab.descendants else ''
            variant = (variant if re.match(r'(?i)ścieżka|moduł', variant) else 'Specjalność: ' + variant) if variant else ''
            parent_titles = {}
            for button in table.select('button.syl-group-head'):
                label = clean(button.get_text(' ', strip=True))
                targets = button.get('aria-controls', '').split()
                if not label or not targets:
                    raise ValueError('Grupa bez nazwy lub odsyłaczy')
                for target in targets:
                    body = table.find('tbody', id=target)
                    if body is None:
                        raise ValueError('Nieodczytany koszyk zajęć: ' + label)
                    parent_titles.setdefault(target, []).append((len(targets), label))
                controls += 1
            table_rows = 0
            for body in table.find_all('tbody', recursive=False):
                hierarchy = parent_titles.get(body.get('id'), [])
                bucket = ' / '.join(dict.fromkeys(label for _, label in sorted(hierarchy, key=lambda row: -row[0])))
                group_title = ' — '.join(filter(None, [variant, ('Do wyboru w grupie: ' + bucket) if bucket else 'Zajęcia planu']))
                names = groups.setdefault((str(semester), group_title), [])
                for tr in body.find_all('tr', recursive=False):
                    cells = tr.find_all('td', recursive=False)
                    if not cells:
                        raise ValueError('Nieznany pusty wiersz planu')
                    if len(cells) == 1 and cells[0].get('colspan') == '6':
                        notes.append(clean(cells[0].get_text(' ', strip=True)))
                        continue  # instrukcja wyboru nie jest nazwą zajęć
                    if len(cells) != 6:
                        raise ValueError('Nieznana liczba kolumn wiersza')
                    if cells[0].select_one('button.syl-group-head'):
                        continue  # nazwa koszyka znajduje się w tytule grupy
                    cell = BeautifulSoup(str(cells[0]), 'html.parser')
                    for metadata in cell.find_all('dl'):
                        metadata.decompose()
                    subject = clean(cell.get_text(' ', strip=True))
                    if not subject or re.match(r'(?i)(student/ka wybiera|student wybiera|studentka wybiera|razem$|suma$)', subject):
                        raise ValueError('Opis zamiast przedmiotu: ' + subject)
                    table_rows += 1
                    course_rows += 1
                    if subject not in names:
                        names.append(subject)
            if table_rows == 0:
                raise ValueError('Tabela bez nazw zajęć')
            # Każdy rozwijany koszyk ma zostać odczytany w całości, również gdy jest ukryty w UI.
            for target, hierarchy in parent_titles.items():
                body = table.find('tbody', id=target)
                if not body.find_all('tr', recursive=False):
                    raise ValueError('Koszyk bez opublikowanych pozycji: ' + str(hierarchy))
    if len(all_tables) != len(soup.find_all('table')):
        raise ValueError('Nieodczytana tabela poza zakładkami semestrów')
    result = [dict(title=title, semester=semester, subjects=names, sourceUrl=source_url)
              for (semester, title), names in groups.items() if names]
    return dict(groups=result, referenceYear=year[0], completeness='full-plan'), dict(
        documentTitle=title,
        semesters=sorted(tabs.values()), tables=len(all_tables), electiveControls=controls,
        courseRows=course_rows, subjectEntries=sum(len(g['subjects']) for g in result),
        excludedInstructions=sorted(set(notes)), unresolvedTables=0, unresolvedControls=0)
