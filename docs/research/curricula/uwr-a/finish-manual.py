import json,re
from pathlib import Path
from docx import Document
D=Path('docs/research/curricula/uwr-a');P=Path('src/data/curricula-uwr-a.json');rs=json.loads(P.read_text(encoding='utf-8'));by={r['programmeId']:r for r in rs}
r=by['uwr-dziennikarstwo-i-komunikacja-spoleczna'];r['groups']=[];seen=set()
for folder,fn,title in [('media-cw','D_CW_licencjackiie_stacjonane_2023_2024.docx','Creative writing'),('media-mcc','D_MCC_licencjackie_stacjonarne_2024_2025.docx','Media content creation'),('media-da','D_DA_licencjackie_stacjonarne_2023_2024.docx','Dziennikarstwo audiowizualne')]:
 doc=Document(D/folder/fn);u=next(s['url'] for s in r['sources'] if title in s['title'] and s['url'].endswith('.zip'))
 for i,t in enumerate(doc.tables[:6]):
  ss=[]
  assert 'Nazwa przedmiotu' in t.rows[0].cells[1].text
  for rr in t.rows[1:]:
   if rr.cells[2].text.strip() not in ['O','F']:continue
   v=re.sub(r'\s+',' ',rr.cells[1].text).strip()
   if v and v.casefold() not in seen:seen.add(v.casefold());ss.append(v)
  if ss:r['groups'].append({'title':title+' — semestr '+str(i+1),'semester':str(i+1),'subjects':ss,'sourceUrl':u})
r['note']='Nazwy odczytano wyłącznie z sześciu semestralnych tabel Nazwa przedmiotu trzech oficjalnych stacjonarnych planów Uniwersytetu Wrocławskiego. Pominięto tabele efektów uczenia się i wskaźników ECTS. Wspólne nazwy występują raz; zachowano rzeczywiste lata programów.'
r=by['uwr-gospodarka-przestrzenna'];u='https://igrr.uwr.edu.pl/wp-content/uploads/sites/40/2023/06/gp_plan_Ist_2023.pdf'
# URL is replaced with the exact cached download manifest below.
for f in D.glob('batch*.json'):
 if 'results' in f.name:continue
 for name,url in json.loads(f.read_text(encoding='utf-8-sig')):
  if name=='uwr-gospodarka-przestrzenna-plan':u=url
texts=[('1','BHP i ppoż.|Ochrona własności intelektualnej|Historia gospodarcza z elementami odkryć geograficznych|Kształtowanie i ochrona środowiska|Podstawy kartografii społ.-gosp., planistycznej i geodezji|Prawne podstawy gospodarki przestrzennej i ochrony środowiska|Przyrodnicze uwarunkowania gospodarki przestrzennej|Społeczno-kulturowe uwarunkowania gospodarki przestrzennej|Systemy osadnicze|Technologie informacyjne w gospodarce przestrzennej|Wprowadzenie do statystyki'),('2','Demografia|Komputerowe wspomaganie projektowania (CAD)|Podstawy ekonomii|Podstawy gospodarki przestrzennej|Zasady projektowania|Źródła informacji w gospodarce przestrzennej|Ćwiczenia terenowe 1 - inwentaryzacja urbanistyczna (6 dni)|Język obcy nowożytny|Moduł A - przedmioty do wyboru'),('3','Fizjografia planistyczna|Historia urbanistyki|Kształtowanie krajobrazu|Podstawy geografii ekonomicznej|Podstawy zarządzania|Projektowanie urbanistyczne 1|Samorząd terytorialny|Systemy informacji geograficznej 1|Moduł B - przedmioty do wyboru'),('4','Klimatologia i meteorologia w gospodarce przestrzennej|Projektowanie urbanistyczne 2|Przemiany morfologiczne struktur zurbanizowanych|Strategia rozwoju gminy|Struktura i planowanie rozwoju usług|Systemy informacji geograficznej 2|Ćwiczenia terenowe 2 - inwentaryzacja przyrodnicza (6 dni)|Praktyki zawodowe (3 tygodnie)|Moduł C - przedmioty do wyboru'),('5','Metody analizy w gospodarce przestrzennej|Planowanie przestrzenne 1|Rewitalizacja obszarów zurbanizowanych|Seminarium dyplomowe 1|Wychowanie fizyczne|Język obcy nowożytny poziom B2II (egzamin)|Moduł D - przedmioty do wyboru'),('6','Ekonomika miast i regionów|Monitoring środowiska|Planowanie przestrzenne 2|Seminarium dyplomowe 2|Tematyczna informacja przestrzenna|Wpływ zjawisk ekstremalnych na gospodarowanie przestrzenią|Praca dyplomowa i egzamin'),(None,'Geologia gospodarcza w planowaniu przestrzennym|Problemy rozwoju infrastruktury transportowej|Problemy zagospodarowania obszarów Natura 2000|Teledetekcja|Zagospodarowanie turystyczne|Gospodarka leśna|Gospodarka zasobami glebowymi|Inwestycje liniowe w gospodarce przestrzennej|Podstawy polityki regionalnej w turystyce|Gospodarka wodna|Podstawy zarządzania jakością powietrza|Problemy zagospodarowania przestrzennego Dolnego Śląska|System przyrodniczy miasta|Gospodarka odpadami|Krajobrazy kulturowe świata a gospodarowanie przestrzenią|Problemy zagospodarowania obszarów wiejskich|Zastosowanie wiedzy o atmosferze w gospodarce przestrzennej')]
r['groups']=[{'title':'Semestr '+s if s else 'Przedmioty modułów A–D do wyboru','semester':s,'subjects':text.split('|'),'sourceUrl':u} for s,text in texts]
r['referenceYear']='obowiązuje od 2023/2024';r['completeness']='full-plan';r['note']='Pełny trzystronicowy skan planu Uniwersytetu Wrocławskiego odczytano wizualnie: sześć semestrów i wszystkie cztery listy modułów do wyboru. Bieżąca strona instytutu wskazuje ten plan jako obowiązujący od 2023/2024. Nazw wspólnych lektoratów nie powielono w każdym semestrze. Moduły A–D są blokami wyboru, nie specjalnościami.'
r['sources'].append({'title':'Gospodarka przestrzenna — plan studiów Uniwersytetu Wrocławskiego','url':u,'year':r['referenceYear'],'note':'Ręczny odczyt wszystkich trzech stron skanu; plan jest wskazany w oficjalnym bieżącym wykazie instytutu.'})
P.write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('DOCX',sum(len(g['subjects']) for g in by['uwr-dziennikarstwo-i-komunikacja-spoleczna']['groups']),'GOSP',sum(len(g['subjects']) for g in r['groups']),u)
