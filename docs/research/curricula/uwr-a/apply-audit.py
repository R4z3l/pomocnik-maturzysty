import json,re
from pathlib import Path
D=Path('docs/research/curricula/uwr-a');P=Path('src/data/curricula-uwr-a.json');rs=json.loads(P.read_text(encoding='utf-8'));by={r['programmeId']:r for r in rs}
def install(pid,gs,url):
 r=by[pid];seen=set();r['groups']=[]
 for g in gs:
  ss=[]
  for v in g['subjects']:
   v=re.sub(r'(?<=\w)-\s+(?=\w)','',v);v=re.sub(r'\s+',' ',v).strip().rstrip('*#% ')
   if re.search(r'^(O/W/OzW|K_|Wskazanie|UWAGA|SPECJALNOŚĆ|PRZEDMIOTY O WYBORU)|dyscyplina/punkty',v,re.I):continue
   if v.casefold() not in seen and len(v)>2:seen.add(v.casefold());ss.append(v)
  if ss:r['groups'].append({'title':'Przedmioty i bloki do wyboru — strona '+str(g.get('page','')),'semester':None,'subjects':ss,'sourceUrl':url})
 if r['groups']:r['completeness']='listed-subjects'
rect=json.loads((D/'audited-rectangles.json').read_text(encoding='utf-8'))
for pid,gs in rect.items():
 if not gs or pid=='uwr-edukacja-polonistyczna':continue
 actual=pid.removesuffix('-current');r=by[actual];u=next((s['url'] for s in r['sources'] if s['url'].endswith('.pdf')),None)
 if not u:continue
 if pid=='uwr-ekonomia':gs=[g for g in gs if 31<=g['page']<=40]
 if pid=='uwr-filozofia':gs=[g for g in gs if 21<=g['page']<=26]
 install(actual,gs,u)
# English BSc plan linked directly by official current BSc page. Rows with merged course cells stay combined rather than invented.
t=(D/'uwr-biotechnology-plan.txt').read_text(encoding='utf-8');ls=t.splitlines();ss=[]
for i,x in enumerate(ls):
 if re.fullmatch(r'\d+\.',x.strip()):
  a=[];j=i+1
  while j<len(ls) and not re.fullmatch(r'[\d\s.*/–-]+|[EZz]',ls[j].strip()):a.append(ls[j]);j+=1
  v=' '.join(a).strip()
  if v:ss.append(v)
u='https://biotech.uwr.edu.pl/wp-content/uploads/sites/261/2025/02/NEW_BSc_Biotechnology_2023_24.pdf';r=by['uwr-biotechnology'];install(r['programmeId'],[{'page':'1–5','subjects':ss}],u);r['referenceYear']='2023/2024';r['sources'].append({'title':'Biotechnology — plan BSc Uniwersytetu Wrocławskiego','url':u,'year':'2023/2024','note':'Angielski program BSc, 6 semestrów; dokument podlinkowany w bieżącej oficjalnej karcie BSc Biotechnology. Nie użyto programu MSc ani tabel przedmiotów rekrutacyjnych.'});r['note']='Odczytano nazwy z pięciostronicowego angielskiego planu BSc Uniwersytetu Wrocławskiego. Dokument łączy wybrane wykłady i ćwiczenia we wspólne komórki; nie poświadczono odrębnych nazw wszystkich wierszy laboratoryjnych. Rzeczywisty rok programu: 2023/2024.'
# Remove metadata duplicates on every run.
for r in rs:
 r['checkedAt']='2026-10-28';unique={}
 for s in r['sources']:unique[s['url']]=s
 r['sources']=list(unique.values())
P.write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'audit-names-after.txt').write_text('\n\n'.join(r['programmeId']+'\n'+'\n'.join(s for g in r['groups'] for s in g['subjects']) for r in rs),encoding='utf-8')
print([(r['programmeId'],sum(len(g['subjects']) for g in r['groups'])) for r in rs])
