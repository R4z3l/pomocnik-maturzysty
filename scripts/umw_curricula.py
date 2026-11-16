"""Odczyt nazw zajęć z tabel godzinowych dokumentów OOXML UMW, bez sieci."""
from io import BytesIO
from zipfile import ZipFile
from xml.etree import ElementTree as E
import re

NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def text(node):
    return ' '.join(''.join(t.text or '' for t in p.findall('.//w:t',NS)) for p in node.findall('./w:p',NS)).strip()
def normal(value):return re.sub(r'[^\w]+',' ',value.lower()).strip()

def parse_umw_curriculum(content, programme, url):
    with ZipFile(BytesIO(content)) as archive:
        root=E.fromstring(archive.read('word/document.xml'))
    tables=[[[text(cell) for cell in row.findall('./w:tc',NS)] for row in table.findall('./w:tr',NS)] for table in root.findall('.//w:tbl',NS)]
    if not tables:raise ValueError('Brak tabel programu')
    meta={normal(r[1].split(':')[0]):r[-1] for r in tables[0] if len(r)>=3}
    name=next((v for k,v in meta.items() if k.startswith('nazwa kierunku')), '')
    expected=programme['name'].replace(' w języku angielskim','').replace('Kierunek ','')
    if not normal(name).startswith(normal(expected)):raise ValueError('Inny kierunek w programie: '+name)
    language=next((v for k,v in meta.items() if k.startswith('język wykładowy')), '')
    if ('angielski' if programme['language']=='en' else 'polski') not in language.lower():raise ValueError('Inny język programu')
    level=next((v for k,v in meta.items() if k.startswith('poziom studiów')), '').lower()
    if not (('jednolite' in level) if programme['level']=='long-cycle' else ('pierwszego' in level or 'i stopnia' in level)):
        raise ValueError('Inny poziom programu')
    form=next((v for k,v in meta.items() if k.startswith('forma formy')), '').lower()
    if not re.search(r'(?<!nie)stacjonarne',form):raise ValueError('Brak formy stacjonarnej')
    raw=''.join(root.itertext())
    if not re.search(r'202\s*6\s*/\s*202\s*7',raw):raise ValueError('Brak cyklu 2026/2027')
    groups=[]; rejected=[]
    for index,table in enumerate(tables):
        if not table or len(table[0])<8 or normal(table[0][1])!='przedmiot' or 'ects' not in ' '.join(table[0]).lower():continue
        names=[]
        for row in table[1:]:
            if len(row)<8 or not row[1]:continue
            if re.match(r'^(razem|suma|łącznie|total)\b',row[0],re.I):continue
            name=' '.join(row[1].split())
            if re.fullmatch(r'[\d.,\s-]+',name):rejected.append(name);continue
            if name not in names:names.append(name)
        if names:groups.append(dict(title=f'Tabela planu {index+1} — zajęcia i pozycje do wyboru',semester=None,subjects=names,sourceUrl=url))
    if not groups:raise ValueError('Brak rozpoznanych tabel zajęć')
    return dict(programmeId=programme['id'],checkedAt='2026-11-10',referenceYear='2026/2027',completeness='listed-subjects',groups=groups,
        specializations=[],specializationStatus='not-found',
        note='Odczyt nazw z tabel godzinowych oficjalnego programu 2026/2027. Spis częściowy: bez potwierdzenia kompletności koszyków i przypisania semestrów. Ogólne pozycje wyboru oraz warianty rozdzielone ukośnikiem zachowują zapis dokumentu; nie są osobnymi specjalnościami. Dokumenty wersji anglojęzycznej mogą podawać polskie nazwy zajęć.',
        sources=[dict(title='Oficjalny program studiów: '+programme['name'],url=url,year='2026/2027',note='Dokument BIP właściwego kierunku, poziomu i języka. Weryfikacja metryczki i kolumny nazw, bez importu efektów uczenia i sum godzin.')]),dict(tables=len(tables),courseTables=len(groups),rows=sum(len(g['subjects']) for g in groups),rejectedNumeric=rejected,metadata=meta)
