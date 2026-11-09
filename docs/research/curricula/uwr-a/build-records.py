import json,re
from pathlib import Path
from bs4 import BeautifulSoup
D=Path('docs/research/curricula/uwr-a');records=json.loads(Path('src/data/curricula-uwr-a.json').read_text(encoding='utf-8'));names={p['id']:p['name'] for p in json.loads(Path('src/data/uwr.json').read_text(encoding='utf-8'))['programmes']}
manifest={}
for f in D.glob('batch*.json'):
 if f.stem.endswith('results'):
  for x in json.loads(f.read_text(encoding='utf-8')):
   if x.get('type')=='pdf':manifest[x['name'].removesuffix('-plan')]=x['url']
 # The first batch had downloaded valid PDFs before a missing optional parser error.
 elif not f.stem.endswith('results'):
  for n,u in json.loads(f.read_text(encoding='utf-8-sig')):
   if u.endswith('.pdf') and (D/(n+'.pdf')).exists():manifest[n.removesuffix('-plan')]=u
grid=json.loads((D/'extracted-grid.json').read_text(encoding='utf-8'));tables=json.loads((D/'extracted-tables.json').read_text(encoding='utf-8'));bio=json.loads((D/'extracted-biology.json').read_text(encoding='utf-8'))
years={'uwr-etyka':'obowiązuje od 2023/2024','uwr-culture-thought-and-humanity':'obowiązuje od 2023/2024','uwr-bachelor-of-business-and-administration':'obowiązuje od 2023/2024','uwr-geografia':'obowiązuje od 2023/2024','uwr-biotechnologia':'obowiązuje od 2023/2024','uwr-biologia':'2023/2024–2025/2026','uwr-biologia-czlowieka':'2024/2025','uwr-genetyka-i-biologia-eksperymentalna':'2024/2025','uwr-genetics-and-experimental-biology':'2026/2027','uwr-bezpieczenstwo-narodowe':'2024/2025','uwr-analityka-spoleczna':'2024/2025','uwr-data-and-society':'2026/2027','uwr-ekonomia':'2026/2027','uwr-filozofia':'2026/2027','uwr-filologia-polska':'2026/2027','uwr-edukacja-polonistyczna':'2026/2027','uwr-english-for-knowledge-culture-and-innovation':'2024 – rok dokumentu','uwr-chemia':'2024/2025','uwr-chemia-medyczna':'2024/2025','uwr-geoinformacja':'2026 – publikacja planu','uwr-etnologia-i-antropologia-kulturowa':'nie podano – publikacja 2025','uwr-europeistyka':'2025 – aktualizacja programu','uwr-dziedzictwo-kultury-materialnej-ochrona-promocja-gospodarowanie':'2025 – publikacja programu'}
old={'uwr-criminal-justice','uwr-dyplomacja-europejska','uwr-gospodarka-przestrzenna'}
specs={'uwr-administracja':['Bezpieczeństwo wewnętrzne','Administracja europejska','Samorząd terytorialny','Administracja sektora publicznego'],'uwr-ekonomia':['Prawo w biznesie','Prawo podatkowe','Finanse i rachunkowość','Ekonomia innowacji','Gospodarka światowa'],'uwr-analityka-spoleczna':['Analityka danych miejskich','Analityka danych w marketingu','Analityka, zarządzanie i edukacja w obszarze bezpieczeństwa'],'uwr-anglistyka':['Globalne kultury i odmiany języka angielskiego','Tłumaczeniowa','Język angielski w komunikacji profesjonalnej'],'uwr-biologia':['Biologia człowieka','Biologia eksperymentalna','Mikrobiologia','Biologia środowiska','Nauczycielska'],'uwr-dziedzictwo-kultury-materialnej-ochrona-promocja-gospodarowanie':['Gospodarowanie dziedzictwem kultury materialnej','Turystyka historyczna'],'uwr-dziennikarstwo-i-komunikacja-spoleczna':['Creative writing','Dziennikarstwo audiowizualne','Media content creation'],'uwr-filologia-chorwacka-z-jezykiem-serbskim':['Bohemistyczna','Rusycystyczna','Ukrainistyczna'],'uwr-filologia-czeska':['Kroatystyczna','Rusycystyczna','Ukrainistyczna'],'uwr-filologia-rosyjska':['Bohemistyczna','Ukrainistyczna','Kroatystyczna','Anglistyczna'],'uwr-filologia-ukrainska':['Bohemistyczna','Kroatystyczna','Rusycystyczna','Anglistyczna'],'uwr-filologia-francuska':['Hispanistyczna','Italianistyczna','Belgijska'],'uwr-filologia-hiszpanska':['Italianistyczna','Romanistyczna'],'uwr-filologia-germanska':['Literatura i media krajów niemieckojęzycznych','Kultura krajów niemieckojęzycznych i Śląska','Komunikacja językowa i medialna w teorii i praktyce'],'uwr-filologia-polska':['Edytorstwo','Retoryka stosowana','Teatrologia'],'uwr-fizyka':['Ekonofizyka']}
fast=json.loads((D/'extracted-fast.json').read_text(encoding='utf-8'))
faculties=json.loads((D/'faculty-links.json').read_text(encoding='utf-8'))
for r in records:
 pid=r['programmeId'];s=BeautifulSoup((D/(pid+'-about.html')).read_text(encoding='utf-8'),'html.parser');a=s.select_one('link[rel=canonical]');about=a['href'] if a else ''
 r.update(referenceYear=years.get(pid,'2025/2026'),groups=[],specializations=[],sources=[],completeness='unavailable',specializationStatus='not-found')
 if about:r['sources'].append({'title':names[pid]+' — oficjalny opis Uniwersytetu Wrocławskiego','url':about,'year':'2026 – odczyt aktualnego opisu','note':'Opis oferty potwierdza zakres i jawnie wymienione specjalności; rok nagłówka rekrutacji nie datuje planu.'})
 for f in faculties:
  if pid in f['ids']:r['sources'].append({'title':'Uniwersytet Wrocławski — strona wydziału lub instytutu','url':f['url'],'year':'2026 – data odczytu','note':'Sprawdzono odnośniki do programów, planów i sylabusów; zapis przeglądu w dokumentacji researchu.'})
 sourcekey=pid+'-current' if pid=='uwr-edukacja-polonistyczna' else pid
 raw=grid.get(sourcekey,[]) or tables.get(pid,[])
 if pid in bio:raw=bio[pid]
 if pid in fast:raw=fast[pid]
 if sourcekey in manifest and pid not in old:
  url=manifest[sourcekey];r['sources'].append({'title':names[pid]+' — program lub plan studiów Uniwersytetu Wrocławskiego','url':url,'year':r['referenceYear'],'note':'Pierwotny dokument uczelni; rok odnosi się do programu, nie nagłówka rekrutacji. Lista może łączyć kursy obowiązkowe i do wyboru.'})
  seen=set()
  for g in raw:
   subs=[]
   for v in g['subjects']:
    v=re.sub(r'(?<=\w)-\s+(?=\w)','',v);v=re.sub(r'\s+',' ',v).strip();v=v.removeprefix('PRZEDMIOTY OBOWIĄZKOWE ').strip()
    if re.search(r'^(K[_ ]|DYSCYPLINY|INFORMACJE OGÓLNE|Przedmioty obowiązkowe|Przedmiot stanowi|O/W/OzW|Liczba|SUMA|Nazwa|dyscyplina/punkty)',v,re.I) or len(v)>220:continue
    key=v.casefold()
    if key not in seen:subs.append(v);seen.add(key)
   if subs:r['groups'].append({'title':('Semestr '+str(g['semester'])) if g.get('semester') else 'Przedmioty i bloki do wyboru — strona '+str(g.get('page','')),'semester':str(g['semester']) if g.get('semester') else None,'subjects':subs,'sourceUrl':url})
  if r['groups']:r['completeness']='listed-subjects'
 if pid in old:
  r['referenceYear']='nie potwierdzono aktualnego planu'
  r['note']='Odnaleziono oficjalną stronę programów oraz dokument starszy niż 2024; nie przeniesiono jego listy przedmiotów bez jednoznacznego potwierdzenia obowiązywania dla bieżącego cyklu. Specjalności, jeśli wymieniono, pochodzą z aktualnego opisu. Nie oznacza to braku programu.'
 else:r['note']='Odszukano materiały wydziału lub instytutu Uniwersytetu Wrocławskiego. Wypisano odczytane nazwy zajęć oraz bloków do wyboru. Status listed-subjects oznacza, że nie poświadczono kompletności ekstrakcji całego planu. Brak znalezionego wykazu specjalności nie potwierdza ich braku.' if r['groups'] else 'Sprawdzono opis kierunku i stronę właściwego wydziału lub instytutu oraz dostępne odnośniki do programu. Nie uzyskano jeszcze odczytywalnego wykazu zajęć właściwego aktualnego cyklu; jest to jawna luka w katalogu.'
 for name in specs.get(pid,[]):r['specializations'].append({'name':name,'kind':'specjalność','note':'Nazwa wymieniona w aktualnym oficjalnym opisie kierunku; dostępność grupy należy potwierdzić dla konkretnego naboru.','sourceUrl':about})
 if r['specializations']:r['specializationStatus']='listed'
Path('src/data/curricula-uwr-a.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('records',len(records),'with subjects',sum(bool(x['groups']) for x in records),'subjects',sum(len(g['subjects']) for x in records for g in x['groups']),'with specs',sum(bool(x['specializations']) for x in records))
