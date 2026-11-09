"""Ręczny import publicznego pliku ELA. Bez sieci w działającej aplikacji.

python scripts/import-ela.py --download  # pobranie i filtr rocznika 2024
python scripts/import-ela.py             # ponowny import lokalnego wycinka
Zmiana rocznika wymaga przeglądu definicji, powiązań i testów.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from source_policy import guarded_get

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'docs/research/ela'
DATA_URL = 'https://ela.nauka.gov.pl/sla-server/v6.0/dataExperts/graduates/graduates-major-data.csv'
INSTITUTIONS = {'3840': 'uwr', '3873': 'uew'}
YEAR = 2024
FIELDS = {
    'inZus': 'P_N_WZUS',
    'medianSalary': 'P_ME_ZAR_P1', 'meanSalary': 'P_E_ZAR_P1',
    'relativeSalary': 'P_WWZ_P1', 'relativeUnemployment': 'P_WWB_P1',
    'unemploymentRisk': 'P_PROC_MIES_BEZR_P1',
    'employmentPercent': 'P_CZY_PRACA_P1', 'furtherStudyPercent': 'P_IF_2st_P1',
    'jobSearchMonths': 'P_CZAS_PRACA',
    'jobSearchNoExperienceMonths': 'P_CZAS_PRACA_NDOSW',
}

def numeric(raw):
    # Puste pole jest brakiem wartości; jego przyczyny nie zgadujemy.
    if raw == '':
        return None
    value = float(raw.replace(',', '.'))
    if value < 0:
        raise ValueError(f'Nieznany kod braku / wartość ujemna: {raw}')
    return value

def eligible(row):
    return (row['P_ROKDYP'] == str(YEAR) and row['P_UCZELNIA'] in INSTITUTIONS
            and row['P_FORMA'] == 'S' and row['P_POZIOM'] in ['1', 'JM'])

parser = argparse.ArgumentParser()
parser.add_argument('--download', action='store_true')
args = parser.parse_args()
RESEARCH.mkdir(parents=True, exist_ok=True)
extract = RESEARCH / 'source-2024.csv'
if args.download:
    response = guarded_get(DATA_URL, timeout=120)
    reader = csv.DictReader(io.StringIO(response.content.decode('utf-8-sig')), delimiter=';')
    rows = [r for r in reader if eligible(r)]
    with extract.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=reader.fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)
    (RESEARCH / 'download.json').write_text(json.dumps({
        'sourceUrl': DATA_URL, 'checkedAt': '2026-10-25',
        'sha256': hashlib.sha256(response.content).hexdigest(),
        'bytes': len(response.content), 'retainedRows': len(rows),
        'criteria': '2024; institutions 3840/3873; S; level 1/JM',
    }, indent=2), encoding='utf-8')

with extract.open(encoding='utf-8', newline='') as handle:
    rows = list(csv.DictReader(handle, delimiter=';'))
assert all(eligible(r) for r in rows), 'Wycinek spoza zakresu'
programmes = [p for u in ['uwr', 'uew'] for p in json.loads(
    (ROOT / f'src/data/{u}.json').read_text(encoding='utf-8'))['programmes']]
cohorts, matches = {}, []
for programme in programmes:
    # Jedyny jawny alias: brak znaku diakrytycznego w nazwie katalogowej.
    name = {'uwr-stosunki-miedzynarodowe': 'Stosunki międzynarodowe'}.get(
        programme['id'], programme['name'])
    selected = [r for r in rows if INSTITUTIONS[r['P_UCZELNIA']] == programme['universityId']
                and r['P_KIERUNEK_NAZWA'].casefold() == name.casefold()
                and ('long-cycle' if r['P_POZIOM'] == 'JM' else 'bachelor') == programme['level']
                and not r['P_NAZWA_JEDN']]  # Filia w Jeleniej Górze poza zakresem.
    if not selected:
        continue
    for r in selected:
        cohort = {'id': r['P_KIERUNEK_ID'], 'universityId': programme['universityId'],
                  'name': r['P_KIERUNEK_NAZWA'], 'reportName': r['P_NAZWA_KIERUNKU_PELNA'],
                  'unit': r['P_NAZWA_JEDN'], 'specialty': r['P_SPEC_NAZWA'],
                  'level': programme['level'], 'graduates': int(r['P_N']),
                  **{key: numeric(r[column]) for key, column in FIELDS.items()}}
        assert cohort['id'] not in cohorts, 'Kohorta użyta do dwóch ofert; wymagany przegląd'
        cohorts[cohort['id']] = cohort
    matches.append({'programmeId': programme['id'],
                    'cohortIds': [r['P_KIERUNEK_ID'] for r in selected],
                    'note': 'Dopasowano uczelnię, nazwę, poziom i tryb stacjonarny. '
                            'Zestawienie ELA nie ma osobnego pola języka; nie rozdzielamy '
                            'ani nie łączymy wariantów językowych. Program absolwentów 2024 '
                            'może różnić się od programu rekrutacji 2027.'})

output = {
    'checkedAt': '2026-10-25', 'graduationYear': YEAR, 'edition': '11 / 2026',
    'observation': 'pierwszy rok po dyplomie (P1) dla wynagrodzeń, pracy, bezrobocia i dalszych studiów; '
                   'czas do pierwszej pracy i obecność w ZUS dotyczą całego okresu badania kohorty',
    'sourceUrl': 'https://ela.nauka.gov.pl/pl/experts/source-data',
    'dictionaryUrl': 'https://ela.nauka.gov.pl/sla-server/v6.0/dataExperts/graduates/graduates-major-dictionary.xlsx',
    'methodologyUrl': 'https://ela.nauka.gov.pl/ELA10_opis_badania_20250625.pdf',
    'citationUrl': 'https://ela.nauka.gov.pl/pl/citation',
    'citation': 'Ośrodek Przetwarzania Informacji – Państwowy Instytut Badawczy, '
                'Ogólnopolski system monitorowania ekonomicznych losów absolwentów szkół wyższych, '
                'absolwenci, Edycja 11, 2026.',
    'cohorts': list(cohorts.values()), 'matches': matches,
}
(ROOT / 'src/data/graduates.json').write_text(
    json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'ELA: {len(cohorts)} kohort / {len(matches)} ofert / {len(programmes)} w katalogu')
