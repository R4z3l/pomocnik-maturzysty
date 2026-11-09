import json,re,pymupdf
from pathlib import Path
D=Path('docs/research/curricula/uwr-a');P=Path('src/data/curricula-uwr-a.json');rs=json.loads(P.read_text(encoding='utf-8'));by={r['programmeId']:r for r in rs}
r=by['uwr-biotechnologia'];gs=[];seen=set()
for p in pymupdf.open(D/'uwr-biotechnologia-plan.pdf'):
 ls=p.get_text().splitlines();ss=[]
 for i,l in enumerate(ls):
  if not l.strip().isdigit():continue
  acc=[];j=i+1
  while j<len(ls):
   v=ls[j].strip()
   if v in ['wykład','lab.','ćw.','ćw. komp.','lab.+ćw.','sem.','lektorat','e-learning'] or re.match(r'^wykład\d',v):break
   if v.isdigit() or v in ['Z','E','---'] or len(acc)>7:acc=[];break
   acc.append(v);j+=1
  if acc:
   v=' '.join(acc);v=re.sub(r'-\s+ćwiczenia',' - ćwiczenia',v);v=re.sub(r'[12]\)','',v).strip();v=re.sub(r'[\*#%]','',v)
   if len(v)>3 and len(v)<200 and v not in seen:ss.append(v);seen.add(v)
 if ss:gs.append({'title':'Przedmioty — strona '+str(p.number+1),'semester':None,'subjects':ss,'sourceUrl':r['groups'][0]['sourceUrl']})
u=r['groups'][0]['sourceUrl'];gs.append({'title':'Moduły i lektoraty wskazane w planie','semester':None,'subjects':['Moduł: Bioinformatyka i bazy danych / Bioinformatyka z modelowaniem białek','Moduł: Statystyka w analizie i planowaniu eksperymentu','Język polski dla cudzoziemców'],'sourceUrl':u});r['groups']=gs;r['note']='Odczytano nazwy z wszystkich sześciu stron oficjalnego programu Uniwersytetu Wrocławskiego obowiązującego od 2023/2024, wskazanego przez bieżącą stronę wydziału. Alternatywy w jednej komórce rozdzielono ukośnikiem; forma zajęć pozostaje w nazwie, gdy dokument tak rozróżnia wiersze. Nie poświadczono pełnej zgodności z osobnym katalogiem sylabusów.'
# Cleanup identified during reading every name, preserving original meaning.
replacements={
'Szkolenie wstępne w zakresie bezpieczeństwa i higieny pracy oraz':'Szkolenie wstępne w zakresie bezpieczeństwa i higieny pracy oraz ochrony przeciwpożarowej',
'Psychologicznosocjologiczne aspekty akwizycji języka':'Psychologiczno-socjologiczne aspekty akwizycji języka',
'Praktyczna nauka języka':'Praktyczna nauka języka rosyjskiego – gramatyka funkcjonalna 4',
'kosmetycznych i ich aktywność przeciwutleniająca (PDW-13)':'Ekstrakty roślinne w emulsjach kosmetycznych i ich aktywność przeciwutleniająca (PDW-13)',
'projekt indywidualny Seminarium licencjackie – projekt grupowy ****':'Seminarium licencjackie – projekt indywidualny / Seminarium licencjackie – projekt grupowy',
'Praktyka zawodowa Praktyka badawcza ***':'Praktyka zawodowa / Praktyka badawcza',
'Zarządzanie produktem i markąwarsztaty':'Zarządzanie produktem i marką – warsztaty',
'Praktyczna nauka języka hiszpańskiego – egzamin [gramatyka praktyczna IV + konwersacje i rozumienie ze słuchu IV + słownictwo i':'Praktyczna nauka języka hiszpańskiego – egzamin [gramatyka praktyczna IV + konwersacje i rozumienie ze słuchu IV + słownictwo i intensywne czytanie IV + język pisany IV]',
'Literatura czeska': 'Literatura czeska',
'Historia literatury czeskiej 19181945':'Historia literatury czeskiej 1918–1945',
'Kultura i historia Ukrainy XVIIXVIII w.':'Kultura i historia Ukrainy XVII–XVIII w.',
'Filozofia XVIIXVIII w.':'Filozofia XVII–XVIII w.',
'Pedagogikauczeń ze specjalnymi potrzebami edukacyjnymi':'Pedagogika – uczeń ze specjalnymi potrzebami edukacyjnymi',
'Przedmioty opcyjnie1':'Przedmioty opcyjne',
'Lektura tekstów sanskryckich: dharmasutry LUB Lektura tekstów':'Lektura tekstów sanskryckich: dharmasutry',
'Praktyka psychologicznopedagogiczna w szkole (śródroczna)':'Praktyka psychologiczno-pedagogiczna w szkole (śródroczna)',
'Kompetencje psychologicznopedagogiczne nauczyciela':'Kompetencje psychologiczno-pedagogiczne nauczyciela',
}
for r in rs:
 seen=set()
 for g in r['groups']:
  ss=[]
  for v in g['subjects']:
   v=replacements.get(v,v)
   if r['programmeId']=='uwr-administracja' and v=='Wychowanie fizyczne':continue
   if re.fullmatch(r'O\s*/\s*W\s*/\s*OzW|O\s*/\s*OzW',v) or v.startswith('UWAGA!'):continue
   v=re.sub(r'^PRZEDMIOTY UZUPEŁNIAJĄCE DO WYBORU [\d,]+\s+','',v)
   v=re.sub(r'^OPCJONALNY MODUŁ KSZTAŁCENIA.*?wersja 1 ','',v)
   v=re.sub(r'^(?:do wyboru przedmiot(?:y)? w wersji A albo B A |wersja 2 |[AB] )','',v)
   if r['programmeId']=='uwr-astronomia':
    v=re.sub(r'(Analiza matematyczna [123]) 1$',r'\1',v);v=re.sub(r'(Ćwiczenia obserwacyjne [12]) 2$',r'\1',v)
    v=re.sub(r' (?:[2345])$','',v) if v.startswith(('Wakacyjna praktyka','Praktyka heliofizyczna','Język obcy','Wychowanie fizyczne','Praca licencjacka')) else v
   if r['programmeId']=='uwr-fizyka':v=re.sub(r' [\d,]+ (?=\()',' ',v);v=re.sub(r' [234]$','',v) if v.startswith(('Język obcy','Praca licencjacka','Wychowanie fizyczne')) else v
   if r['programmeId']=='uwr-etnologia-i-antropologia-kulturowa':v=re.sub(r'^1 (?=Szkolenie)','',v);v=re.sub(r' [2-6]$','',v)
   if r['programmeId'] in ['uwr-filologia-francuska','uwr-filologia-hiszpanska','uwr-filologia-indyjska','uwr-filologia-klasyczna','uwr-edukacja-polonistyczna','uwr-europeistyka']:
    v=re.sub(r'(?<=[a-ząćęłńóśźż)\]IVX])\d+$','',v)
    if r['programmeId']=='uwr-filologia-klasyczna':v=re.sub(r'(cudzoziemców [1-4])4$',r'\1',v);v=v.replace('Lektura grecka9','Lektura grecka').replace('Lektura łacińska9','Lektura łacińska').replace('greckie 210','greckie 2')
   v=v.rstrip('*#% ')
   if v.casefold() not in seen:seen.add(v.casefold());ss.append(v)
  g['subjects']=ss
 r['groups']=[g for g in r['groups'] if g['subjects']]
# English programme: use only English-language section from the bilingual approved document.
r=by['uwr-data-and-society'];active=False
for g in r['groups']:
 ss=[]
 for s in g['subjects']:
  if s=='Introduction to sociology':active=True
  if active:ss.append(s)
 g['subjects']=ss
r['groups']=[g for g in r['groups'] if g['subjects']];r['note']='Wykorzystano angielskojęzyczną sekcję planu Uniwersytetu Wrocławskiego dla Data and Society; pominięto polskojęzyczną wersję tego samego programu, aby nie dublować nazw i zachować język oferty. Nie potwierdzono kompletności całego wykazu.'
# Additional full titles are explicitly visible in the translation/professional tables of the English philology PDF.
r=by['uwr-anglistyka'];u=r['groups'][0]['sourceUrl'];r['groups'].append({'title':'Przedmioty specjalności tłumaczeniowej i komunikacji profesjonalnej','semester':None,'sourceUrl':u,'subjects':['Elementy teorii przekładu','Tłumaczenia kreatywne','Elementy leksykologii i leksykografii w pracy tłumacza','Tłumaczenia internetowe','Przekład naukowo-techniczny','Przekład audiowizualny','Tłumaczenia biznesowe','Adaptacja tekstów narracyjnych jako przekład multimodalny','Wstęp do komunikacji profesjonalnej – biznes','Wstęp do komunikacji profesjonalnej – prawo','Komputerowe opracowywanie tekstów biznesowych','Przekład tekstów biznesowych','Różnice kulturowe a zachowania w biznesie','Język specjalistyczny: komunikacja w biznesie','Język angielski dla biznesu – finanse, bankowość, gospodarka']})
r=by['uwr-biotechnology'];r['groups'][0]['subjects']+=['Genetics','Foreign language (other than English) for Polish citizens']
# Dedup after manual additions.
for r in rs:
 seen=set()
 for g in r['groups']:
  g['subjects']=[s for s in g['subjects'] if not(s.casefold() in seen or seen.add(s.casefold()))]
 r['groups']=[g for g in r['groups'] if g['subjects']]
 r['sources']=list({s['url']:s for s in r['sources']}.values())
P.write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'final-all-names.txt').write_text('\n\n'.join(r['programmeId']+'\n'+'\n'.join(s for g in r['groups'] for s in g['subjects']) for r in rs),encoding='utf-8')
print('records',len(rs),'with lists',sum(bool(r['groups']) for r in rs),'full',sum(r['completeness']=='full-plan' for r in rs),'names',sum(len(g['subjects']) for r in rs for g in r['groups']))
