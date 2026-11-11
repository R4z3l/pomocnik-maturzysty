"""Plan sprawdzony wizualnie na stronach 51–56 uchwały 168/2023. Bez sieci."""
import hashlib
import json
from pathlib import Path

PROGRAMME_ID = 'uwr-european-cultures'
DOCUMENT_URL = 'https://bip.uni.wroc.pl/download/attachment/38170/uchwala-nr-168_2023-senatu-uwr-z-2023-06-21-w-sprawie-programu-studiow-dla-kierunku-european-cultures-i-stopnia.pdf?v=1687434829'
REVIEWED_SHA256 = '9e68395d8de937124efd9a28c7a4c2218ecaf33840908f671448dac5447a6aaa'
REVIEWED_ROWS_SHA256 = '692d8ce9d9caedd53db4910ffd4912fd19ea113183480533a7218dc7436e3179'
SOURCE_ID = 'uwr-european-cultures-programme-2023'


def reviewed_plan(content, original, root, date):
    if hashlib.sha256(content).hexdigest() != REVIEWED_SHA256:
        raise ValueError('Dokument European Cultures zmienił się od pełnego audytu; potrzebny przegląd nowej wersji')
    if original['programmeId'] != PROGRAMME_ID:
        raise ValueError('Niezgodna oferta European Cultures')
    if original['completeness'] == 'full-plan' and not any(s['url'].split('#')[0] == DOCUMENT_URL for s in original['sources']):
        raise ValueError('Istnieje inny pełny plan; nie zastępujemy go starszą uchwałą')
    reviewed_bytes = (Path(root) / 'docs/research/curricula/uwr-a/european-cultures-semesters.json').read_bytes()
    if hashlib.sha256(reviewed_bytes).hexdigest() != REVIEWED_ROWS_SHA256:
        raise ValueError('Zmieniono wizualnie sprawdzoną transkrypcję European Cultures')
    reviewed = json.loads(reviewed_bytes)
    groups = [dict(title=title, semester=semester, subjects=names, sourceUrl=DOCUMENT_URL + '#page=51')
              for semester, sections in reviewed.items() for title, names in sections.items()]
    if sum(len(g['subjects']) for g in groups) != 59:
        raise ValueError('Zmieniono zweryfikowaną listę 59 pozycji planu')
    source = dict(title='Uniwersytet Wrocławski — European Cultures, pełny plan sześciu semestrów', url=DOCUMENT_URL + '#page=51',
                  year='od 2023/2024 — uchwała 168/2023', note='Metryczka na stronach 1–2; cały plan na stronach 51–56 z 57 stron PDF. Wizualnie sprawdzono wszystkie tabele, pule wyboru i przypisy. Studia I stopnia, stacjonarne, w języku angielskim.')
    return {**original, 'checkedAt': date, 'referenceYear': 'od 2023/2024 — uchwała Senatu 168/2023',
            'completeness': 'full-plan', 'groups': groups,
            'sources': [source] + [s for s in original['sources'] if s['url'] != source['url']],
            'note': 'Pełny plan I stopnia, stacjonarny w języku angielskim, uchwała Senatu 168/2023, strony 51–56. '
                    'Język polski dla cudzoziemców: 60 godzin i 5 ECTS łącznie w I–II semestrze; obywatel polski, który go nie realizuje, wybiera dodatkowe zajęcia za co najmniej 5 ECTS. '
                    'WF: 60 godzin łącznie w II–V semestrze, bez ECTS. Zachowano pule wyboru i nazwy ze źródła, w tym pomyłkę redakcyjną „in the in”. '
                    'Plan obowiązuje dla cykli od 2023/24 i nie potwierdza niezmienionego programu naboru 2027/28. Starsze opisy braku spisu dokumentują poprzedni stan poszukiwań.'}
