import json,pymupdf,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
from docx import Document
import xlrd
D=Path('docs/research/curricula/uwr-a');P=Path('src/data/curricula-uwr-a.json');rows=json.loads(P.read_text(encoding='utf-8'));by={r['programmeId']:r for r in rows};sys.stdout.reconfigure(encoding='utf-8')
def add(pid,gs,url,year,title,note):
 r=by[pid];r['groups']=[];seen=set()
 for titleg,sem,ss in gs:
  sub=[]
  for v in ss:
   v=re.sub(r'(?<=\w)-\s+(?=\w)','',v);v=re.sub(r'\s+',' ',v).strip()
   if v.casefold() not in seen and len(v)>3:sub.append(v);seen.add(v.casefold())
  if sub:r['groups'].append({'title':titleg,'semester':sem,'subjects':sub,'sourceUrl':url})
 if r['groups']:r['completeness']='listed-subjects'
 r['referenceYear']=year;r['note']=note;r['sources'].append({'title':title,'url':url,'year':year,'note':note})
# Official current institute syllabus index identifies first-cycle courses and electives.
s=BeautifulSoup((D/'archeo-syl.html').read_text(encoding='utf-8'),'html.parser');m=s.select_one('main') or s;gs=[];active=None
for t in m.find_all(['h2','h3','h4','a']):
 if t.name!='a':
  title=t.get_text(' ',strip=True)
  if 'drugiego stopnia' in title:break
  active=[];gs.append((title,None,active))
 elif active is not None and '.pdf' in t.get('href',''):
  name=re.sub(r'^\d+[ab]?\s*','',t.get_text(' ',strip=True));name=re.sub(r'\s+pdf\s+.*$','',name);active.append(name)
add('uwr-archeologia',gs,'https://archeo.uwr.edu.pl/dydaktyka/sylabusy/','aktualny wykaz, odczyt 2026-10-25','Archeologia — oficjalny wykaz sylabusów Uniwersytetu Wrocławskiego','Wykaz sylabusów instytutu rozdziela trzy lata studiów pierwszego stopnia i konwersatoria specjalistyczne. Wypisano wszystkie nazwy tej sekcji; wykaz sylabusów nie jest poświadczonym pełnym planem.')
# Biotech: each of six landscape pages is one semester; course name column.
d=pymupdf.open(D/'uwr-biotechnologia-plan.pdf');gs=[]
for p in d:
 ss=[]
 for b in p.get_text('dict')['blocks']:
  names=[s['text'].strip() for l in b.get('lines',[]) for s in l['spans'] if 95<s['bbox'][0]<210 and s['bbox'][1]>140]
  v=' '.join(names)
  if len(v)>3 and not re.search(r'przedmiot|zajęcia do wyboru|zajecia do wyboru|ECTS|Semestr|Łącznie|Suma|zrealizować|wykład1|student',v,re.I):ss.append(v)
 gs.append(('Semestr '+str(p.number+1),str(p.number+1),ss))
u=next(x['url'] for x in by['uwr-biotechnologia']['sources'] if x['url'].endswith('.pdf'))
add('uwr-biotechnologia',gs,u,'obowiązuje od 2023/2024','Biotechnologia — program studiów Uniwersytetu Wrocławskiego','Oficjalna bieżąca strona wydziału przedstawia program jako obowiązujący od 2023/2024 i rozdziela wcześniejszy program 2019–2022. Zachowano rzeczywisty rok programu; nie datowano go nagłówkiem rekrutacji. Nazwy odczytano z sześciu stron semestralnych.')
# Three official DOCX plans, one per specialisation. Retain only full-time versions.
gs=[]
for folder,fn,title,yr in [('media-cw','D_CW_licencjackiie_stacjonane_2023_2024.docx','Creative writing','od 2023/2024'),('media-mcc','D_MCC_licencjackie_stacjonarne_2024_2025.docx','Media content creation','od 2024/2025'),('media-da','D_DA_licencjackie_stacjonarne_2023_2024.docx','Dziennikarstwo audiowizualne','od 2023/2024')]:
 doc=Document(D/folder/fn);subjects=[]
 for table in doc.tables:
  for rr in table.rows[1:]:
   if len(rr.cells)<3:continue
   v=rr.cells[1].text.strip()
   if v and len(v)<180 and not re.search(r'Suma|Łącznie|RAZEM|Nazwa przedmiotu|ECTS|Zasady|Objaśnienia|Specjalność',v,re.I):subjects.append(v)
 gs.append((title+' — '+yr,None,subjects))
 # add archive source separately; each group's own source URL is set below.
 url='https://idiks.uwr.edu.pl/wp-content/uploads/sites/576/2024/10/'+{'media-cw':'CW_programy.zip','media-mcc':'MCC_programy.zip','media-da':'DA_programy.zip'}[folder]
 r=by['uwr-dziennikarstwo-i-komunikacja-spoleczna'];r['sources'].append({'title':title+' — oficjalny plan specjalności Uniwersytetu Wrocławskiego','url':url,'year':yr,'note':'Wyłącznie dokument wersji stacjonarnej; pominięto starsze wersje i tryb niestacjonarny z archiwum ZIP.'})
add('uwr-dziennikarstwo-i-komunikacja-spoleczna',gs,'https://idiks.uwr.edu.pl/dziennikarstwo-i-komunikacja-spoleczna/','2023/2024 i 2024/2025 — obowiązujące programy','Dziennikarstwo i komunikacja społeczna — Uniwersytet Wrocławski','Wypisano nazwy z trzech oficjalnych planów stacjonarnych specjalności. Wersje o różnym roku wprowadzenia zachowano oddzielnie; powtarzających się wspólnych przedmiotów nie wypisano wielokrotnie.')
# Official workbook identifies obligatory subjects and elective module names.
b=xlrd.open_workbook(D/'geologia.xls');gs=[]
for sh in b.sheets():
 ss=[];section=sh.name
 for i in range(sh.nrows):
  vals=sh.row_values(i);v=str(vals[1]).strip() if len(vals)>1 else ''
  if vals and isinstance(vals[0],str) and vals[0].startswith('Semestr'):
   if ss:gs.append((section,None,ss));ss=[]
   section=sh.name+' — '+vals[0]
  if v and len(v)>3 and len(v)<180 and not re.search(r'Nazwa|Kierunek|Dokumentacja|Plan studiów|Liczba|ECTS|Razem|Moduły|Łącznie|Godziny|Przedmioty',v,re.I):ss.append(v)
 if ss:gs.append((section,None,ss))
add('uwr-geologia',gs,'https://ing.uwr.edu.pl/wp-content/uploads/sites/64/2023/02/lib-geologia-i-st-plan-studiow-od-2022_2023.xls','obowiązuje od 2022/2023','Geologia — plan studiów Uniwersytetu Wrocławskiego','Bieżąca oficjalna strona instytutu wskazuje arkusz jako plan studiów I stopnia; w arkuszu napisano obowiązuje od 2022/2023. Zachowano rok wprowadzenia, a nie rok bieżącego naboru. Uwzględniono oba arkusze: przedmioty obowiązkowe i moduły do wyboru.')
P.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('with subjects',sum(bool(r['groups']) for r in rows),'names',sum(len(g['subjects']) for r in rows for g in r['groups']))
