"""Deterministyczne adaptery oficjalnych danych. Bez sieci i bez modeli AI."""
import re
from bs4 import BeautifulSoup


def clean(value):
    return re.sub(r'\s+', ' ', value).strip()


def name_key(value):
    # Jedyna dopuszczona równoważna pisownia z audytu PWr.
    return clean(value).casefold().replace('w j. angielskim', 'w języku angielskim')


def history_tables(content, years, university):
    soup = BeautifulSoup(content, 'html.parser')
    result = []
    for table in soup.find_all('table'):
        heading = table.find_previous(['h1', 'h2', 'h3', 'h4', 'strong'])
        title = clean(heading.get_text(' ', strip=True)) if heading else ''
        match = re.search(r'\b(20\d{2})/(20\d{2})\b', title)
        if not match or int(match[1]) not in years:
            continue
        if int(match[2]) != int(match[1]) + 1:
            raise ValueError('Niespójny rocznik tabeli: ' + title)
        rows = [[dict(text=clean(c.get_text(' ', strip=True)), rowSpan=int(c.get('rowspan', 1)), colSpan=int(c.get('colspan', 1)))
                 for c in tr.find_all(['th', 'td'], recursive=False)] for tr in table.find_all('tr')]
        if not rows:
            raise ValueError('Pusta tabela: ' + title)
        headers = [c['text'].casefold() for c in rows[0]]
        if university == 'pwr':
            if headers not in [['wydział', 'kierunek', 'i tura', 'ii tura', 'iii tura'], ['wydział', 'kierunek', 'tura 1', 'tura 2', 'tura 3']]:
                raise ValueError('Zmienił się układ tabeli Politechniki Wrocławskiej: ' + title)
            result.append(dict(year=match[0], rows=rows))
        else:
            if headers not in [['kierunek studiów', 'progi punktowe'], ['kierunek studiów', 'liczba punktów']]:
                raise ValueError('Zmienił się układ tabeli Uniwersytetu Ekonomicznego we Wrocławiu: ' + title)
            round_name = 'druga' if title.startswith('Drugie ') else 'pierwsza' if title.startswith('Pierwsze ') else None
            seen = set()
            for row in rows[1:]:
                if len(row) != 2 or any(c['rowSpan'] != 1 or c['colSpan'] != 1 for c in row):
                    raise ValueError('Niejednoznaczny wiersz: ' + title)
                name, raw = [c['text'] for c in row]
                if name_key(name) in seen or not re.fullmatch(r'\d+(?:[.,]\d+)?', raw):
                    raise ValueError('Powtórzona oferta lub nieznany próg: ' + name)
                seen.add(name_key(name))
                result.append(dict(year=match[0], round=round_name, programme=name, value=float(raw.replace(',', '.')), raw=raw))
    found = {int(row['year'].split('/')[0]) for row in result}
    if found != set(years):
        raise ValueError('Brak wymaganych roczników w treści tabel: ' + str(sorted(set(years) - found)))
    return result


def uew_durations(text, programmes):
    chunks = re.split(r'\nPAGE (\d+)\n', text)[1:]
    pages = [(int(chunks[i]), chunks[i+1]) for i in range(0, len(chunks), 2)]
    if not pages:
        raise ValueError('Brak stron w odczycie PDF')
    if pages[0][0] != 1 or 'R.0000.18.2026' not in pages[0][1]:
        raise ValueError('Nieznana uchwała — program wymaga nowego audytu')
    result = []
    for programme in programmes:
        matches = []
        for page_number, page in pages:
            if 'Poziom kształcenia' not in page:
                continue
            heading = clean(page.split('Poziom kształcenia')[0])
            if name_key(heading) != name_key(programme['name']):
                continue
            language = 'angielski' if programme['language'] == 'en' else 'polski'
            if not re.search(r'Poziom kształcenia\s+studia pierwszego stopnia\b', page):
                continue
            if not re.search(r'Język kształcenia\s+' + language + r'\b', page, re.I):
                continue
            form = re.search(r'Profil kształcenia(.+?)Liczba semestrów', page, re.S)
            if not form or 'Forma studiów' not in form[1] or not re.search(r'\bstudia stacjonarne\b', form[1]):
                continue
            semesters = re.search(r'Liczba semestrów\s+(\d+)\b', page)
            if not semesters or int(semesters[1]) not in [6, 7, 8]:
                raise ValueError('Nieznany czas studiów: ' + programme['id'])
            matches.append(dict(programmeId=programme['id'], duration=semesters[1] + ' semestrów', page=page_number))
        if len(matches) != 1:
            raise ValueError('Nie ustalono jednoznacznego wariantu programu: ' + programme['id'])
        result.extend(matches)
    return result
