"""Buduje krótkie opracowania z lokalnych dowodów i redakcyjnego TSV, bez sieci i AI.

Nie jest adapterem automatycznej publikacji: po zmianie materiału wymagany jest
przegląd opracowania. Nie zmienia programów, zasad rekrutacji ani progów.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
from bs4 import BeautifulSoup
from source_policy import ensure_source_allowed

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/research/descriptions'


def clean(value):
    return ' '.join(value.replace('\xad', '').split())


def career_text(row, soup):
    """Tylko kontekst perspektyw zawodowych; nie program ani lista partnerów."""
    uni = row['universityId']
    if uni in ['uwr', 'pwr', 'umw']:
        sections = [s['text'] for s in row['sections'] if re.search(
            r'co po studiach|perspektywy|zatrudnieni|career|employment', s['title'], re.I)]
        # Politechnika pod tą samą zakładką publikuje dalej partnerów praktyk.
        context = re.split(r'Praktyki (?:zawodowe|i staże)|Miejsca pracy absolwentów|Partnerzy|Firmy współpracujące', ' '.join(sections), flags=re.I)[0]
        if not context and uni == 'pwr':
            text = ' '.join(s['text'] for s in row['sections'])
            start = re.search(r'(?:zatrudnieni[ae]|pracować|pracy w)', text, re.I)
            context = text[start.start():] if start else ''
        return context
    if uni == 'uew':
        body = soup.select_one('.uagb-inner-tab-0.b-custom-tabs')
        context = ' '.join(clean(p.get_text(' ', strip=True)) for p in body.select('p')
                           if re.search(r'prac[ęya]|zawodow|stanowisk|karier|career|employ|job|work as|kancelari|własnego biznesu', p.get_text(), re.I)) if body else ''
        return re.split(r'Jeśli ukończysz II|studia drugiego stopnia|Menedżer kierunku', context, flags=re.I)[0]
    body = soup.select_one('.text-content .text-content')
    if not body:
        return ''
    # Sekcja „Co dalej?” kończy się przed kolejnym nagłówkiem tego poziomu.
    text = clean(body.get_text(' ', strip=True))
    heading = re.search(r'Co dalej\?|Gdzie.{0,45}pracować.{0,30}\?|Perspektywy zawodowe', text, re.I)
    if heading:
        return text[heading.end():]
    # Niektóre karty podają miejsca pracy w akapicie wprowadzającym.
    paragraphs = []
    for p in body.select('p'):
        value = clean(p.get_text(' ', strip=True))
        start = re.search(r'(?:prac[ęy]|pracować|zatrudnieni[ae]).{0,30}(?:w |jako)|karier', value, re.I)
        if start:
            paragraphs.append(value[start.start():])
    return ' '.join(paragraphs)


# Normalizacja krótkich faktów, bez kopiowania akapitów promocyjnych.
# Etykiety są obszarami wspomnianymi w kontekście pracy, nie uprawnieniami.
CAREERS = [
    (r'administracj.{0,12}publiczn', 'Administracja publiczna'),
    (r'państwow|rządow|public administration|government', 'Administracja państwowa'),
    (r'samorząd|local (?:government|authorit)', 'Samorządy lokalne'),
    (r'non.profit|pozarząd|\bNGO|non.governmental', 'Organizacje społeczne'),
    (r'instytucj.{0,15}(?:unijn|europej)|EU institution', 'Instytucje Unii Europejskiej'),
    (r'dyploma|diploma', 'Dyplomacja'),
    (r'konsult|doradcz|consult|advis', 'Doradztwo'),
    (r'badawcz|research|naukow', 'Badania i rozwój'),
    (r'laborator', 'Praca laboratoryjna'),
    (r'farmaceu|pharmaceut', 'Sektor farmaceutyczny'),
    (r'biotechn|biotech', 'Sektor biotechnologiczny'),
    (r'chemiczn|chemical', 'Przemysł chemiczny'),
    (r'spożywcz|food industr|produkcj.{0,8}żywno', 'Przemysł spożywczy'),
    (r'szpital|\bhospitals?\b|\bclinics?\b|klinik|podmiot.{0,6}lecznicz', 'Placówki lecznicze'),
    (r'diagnost', 'Diagnostyka'),
    (r'zdrowi|health', 'Instytucje ochrony zdrowia'),
    (r'ubezpiecze|insuranc', 'Ubezpieczenia'),
    (r'medtech|aparatur.{0,12}medyczn|medical (?:device|equipment)', 'Technologie medyczne'),
    (r'bank|banking', 'Bankowość'),
    (r'rachunkow|account', 'Rachunkowość'),
    (r'finans|financ', 'Finanse'),
    (r'audyt|audit', 'Audyt'),
    (r'podatk|\btax', 'Rozliczenia podatkowe'),
    (r'analityk|analitycz|analy[st]', 'Analityka'),
    (r'programist|programmer|software develop', 'Tworzenie oprogramowania'),
    (r'informatycz|\bIT\b|information technolog', 'Usługi informatyczne'),
    (r'cyber|bezpieczeństw.{0,8}(?:sieci|system)', 'Bezpieczeństwo informatyczne'),
    (r'telekomunik|telecommunic', 'Telekomunikacja'),
    (r'automatyk|automatyzac|automation', 'Automatyzacja przemysłu'),
    (r'robotyk|robotyz|robotów|robotami|\brobotics?\b', 'Robotyka'),
    (r'utrzymani.{0,3}ruchu', 'Utrzymanie ruchu'),
    (r'elektroni|electronic', 'Branża elektroniczna'),
    (r'energet|energy', 'Sektor energii'),
    (r'motoryzac|automotive|pojazd', 'Branża pojazdów'),
    (r'lotnicz|aviation', 'Branża lotnicza'),
    (r'aerospace|kosmicz|space industr', 'Sektor kosmiczny'),
    (r'budowla|construction|budownictw', 'Realizacja inwestycji budowlanych'),
    (r'architekton|architectural|urbanist', 'Projektowanie architektury i urbanistyki'),
    (r'biur.{0,5}projekt(?:ow|ów)|design (?:office|studio)', 'Biura projektowe'),
    (r'nieruchomo|real estate', 'Rynek nieruchomości'),
    (r'geodezyjn|surveying', 'Usługi geodezyjne'),
    (r'geologiczn|geological', 'Usługi geologiczne'),
    (r'górnicz|górnictw|mining', 'Górnictwo'),
    (r'ochron.{0,15}(?:środowisk|przyrod)|monitor.{0,15}środowisk|zarządzan.{0,15}środowisk|environmental|przyrodnicz|ekologiczn', 'Ochrona i zarządzanie środowiskiem'),
    (r'ogrod.{0,5}(?:zoolog|botanicz)', 'Ogrody zoologiczne i botaniczne'),
    (r'rolnicz|rolnictw|agricultur', 'Rolnictwo'),
    (r'hodowl.{0,20}(?:zwierz|bydł|trzod|koni)|hodowc|breeding', 'Hodowla zwierząt'),
    (r'ogrodnicz|ogrodnictw|horticultur', 'Ogrodnictwo'),
    (r'weterynar|veterinar', 'Sektor weterynaryjny'),
    (r'\blogist|łańcuch.{0,5}dostaw|supply chain', 'Logistyka i łańcuchy dostaw'),
    (r'spedyc|transport', 'Transport i spedycja'),
    (r'gastronom|catering|HoReCa', 'Gastronomia'),
    (r'hotel|turysty|tourism|travel', 'Turystyka i hotelarstwo'),
    (r'wydawn|publishing|edytor|redaktor', 'Redakcja i wydawanie treści'),
    (r'tłumacz|translat', 'Usługi przekładu'),
    (r'medi[óa]|media|dziennik|journal', 'Media i dziennikarstwo'),
    (r'reklam|advertis', 'Reklama'),
    (r'marketing', 'Marketing'),
    (r'public relations|\bPR\b', 'Komunikacja i PR'),
    (r'kultur|cultur', 'Instytucje kultury'),
    (r'muze|museum|galeri', 'Muzea i galerie'),
    (r'zabytk|konserwat|heritage', 'Ochrona dziedzictwa'),
    (r'archeolog|archaeolog', 'Badania archeologiczne'),
    (r'bibliote|librar|archiw|archiv', 'Biblioteki i archiwa'),
    (r'oświat|szkoł|nauczyc|placówk.{0,10}edukac|teach|educational institution', 'Edukacja — zależnie od przygotowania'),
    (r'pomoc.{0,5}społeczn|socjaln|social work', 'Wsparcie i pomoc społeczna'),
    (r'psycholog|psychotherap', 'Wsparcie psychologiczne — zależnie od kwalifikacji'),
    (r'\bHR\b|kadrow|zasob.{0,5}ludzk|human resources', 'Zarządzanie personelem'),
    (r'własn.{0,20}(?:działalno|firm|praktyk)|own (?:business|company|practice)', 'Własna działalność'),
    (r'start.up', 'Rozwijanie start-upów'),
    (r'zrównoważon|sustainab', 'Zrównoważony rozwój organizacji'),
    (r'\bBHP\b', 'Bezpieczeństwo pracy'),
    (r'kancelari|obsług.{0,4}prawn|legal (?:assistant|office|advis|consult)', 'Obsługa prawna'),
    (r'law enforcement|policj|police|służb.{0,10}bezpieczeństw', 'Bezpieczeństwo i służby publiczne'),
    (r'criminal|justice|sądow|wymiar.{0,6}sprawiedliwości|prokuratur', 'Otoczenie wymiaru sprawiedliwości'),
    (r'quality control|kontrol.{0,8}jakoś', 'Kontrola jakości'),
]


def teaching_text(row):
    return ' '.join(s['text'] for s in row['sections']
                    if re.search(r'opis|ogólne|general information|forma|formy|classes|program', s['title'], re.I))


def build():
    rows = json.loads((EVIDENCE / 'sections.json').read_text(encoding='utf8'))
    editorial = {}
    for line in (EVIDENCE / 'editorial.tsv').read_text(encoding='utf8').splitlines():
        if line and not line.startswith('#'):
            id, overview, topics = line.split('|')
            if id in editorial:
                raise ValueError('Powtórzony identyfikator: ' + id)
            editorial[id] = (overview, topics.split(';') if topics else [])
    extras = json.loads((EVIDENCE / 'editorial-extra.json').read_text(encoding='utf8'))
    audit_path = EVIDENCE / 'audit.json'
    reviewed = {r['programmeId']: r for r in json.loads(audit_path.read_text(encoding='utf8'))['records']} if audit_path.exists() else {}
    programmes = {p['id']: p for uni in ['uwr','uew','pwr','upwr','umw']
                  for p in json.loads((ROOT / f'src/data/{uni}.json').read_text(encoding='utf8'))['programmes']}
    if set(editorial) != set(programmes) or {r['programmeId'] for r in rows} != set(programmes):
        raise ValueError('Niepełne lub nadmiarowe dopasowanie opisów')
    result, audit = [], []
    for row in rows:
        id = row['programmeId']
        ensure_source_allowed(row['url'], 'current')
        content = (EVIDENCE / row['file']).read_bytes()
        source_hash = hashlib.sha256(content).hexdigest()
        if id in reviewed and (reviewed[id]['sha256'] != source_hash or reviewed[id]['url'] != row['url']):
            raise ValueError(f'{id}: źródło zmienione od przeglądu. Najpierw sprawdź opracowanie i zaktualizuj dowód przeglądu w audit.json.')
        soup = BeautifulSoup(content.decode('utf8'), 'html.parser')
        overview, topics = editorial[id]
        context = career_text(row, soup)
        matches = [(match.start(), label) for pattern, label in CAREERS if (match := re.search(pattern, context, re.I))]
        careers = [label for _, label in sorted(matches)][:10]
        text = teaching_text(row)
        forms = []
        for pattern, label in [
            (r'zaję\w*\s+(?:terenow)|ćwicze\w*\s+terenow|field (?:work|classes|trip)', 'Nauka w terenie'),
            (r'zaję\w*.{0,20}laborator|laboratory (?:classes|work|practice)', 'Ćwiczenia laboratoryjne'),
            (r'warsztat\w*', 'Praca warsztatowa'),
            (r'zaję\w*.{0,20}klinicz|clinical classes', 'Zajęcia kliniczne'),
            (r'\bPBL\b|project.based learning', 'Nauka poprzez realizację projektów (PBL)'),
            (r'odwrócon.{0,4}klas', 'Odwrócona klasa'),
        ]:
            if re.search(pattern, text, re.I):
                forms.append(label)
        record = dict(programmeId=id, language=programmes[id]['language'], level=programmes[id]['level'], checkedAt='2026-11-10',
                      referenceYear='opis ogólny, bez wskazanego cyklu',
                      overview=[overview], topics=topics, teachingForms=forms,
                      practice=[], careerAreas=careers, careerRoles=[], specializations=[],
                      sourceSections=list(dict.fromkeys(s['title'] for s in row['sections'] if s['title'] and not re.search(
                          r'egzamin|kontakt|contact|limit|tuition|fee|disabilit|dlaczego|why |komu|who |specjalizacje|study length', s['title'], re.I))),
                      sourceUrl=row['url'], sourceTitle=row['name'] + ' — karta uczelni',
                      sourceHash=source_hash,
                      status='reviewed-source', notes=[])
        if id in extras:
            record.update(extras[id])
        # Brak czytelnego tekstu nie otrzymuje statusu pełnego opracowania.
        if not row['sections'] or id == 'upwr-weterynaria-w-jezyku-angielskim':
            record['status'] = 'limited-source'
        words = len(' '.join(record['overview'] + record['topics'] + record['teachingForms'] +
                            record['practice'] + record['careerAreas'] + record['careerRoles'] + record['specializations']).split())
        if words > 190:
            raise ValueError(f'Zbyt długie opracowanie {id}: {words}')
        result.append(record)
        audit.append(dict(programmeId=id, language=programmes[id]['language'], level=programmes[id]['level'],
                          url=row['url'], file=row['file'], sha256=record['sourceHash'],
                          status=record['status'], sections=len(row['sections']), summaryWords=words))
    (ROOT / 'src/data/programme-descriptions.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    (EVIDENCE / 'audit.json').write_text(json.dumps(dict(checkedAt='2026-11-10', records=audit), ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    print(json.dumps(dict(offers=len(result), limited=sum(r['status']=='limited-source' for r in result),
                         careers=sum(bool(r['careerAreas']) for r in result),
                         teaching=sum(bool(r['teachingForms']) for r in result),
                         practice=sum(bool(r['practice']) for r in result)), ensure_ascii=False))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf8')
    build()
