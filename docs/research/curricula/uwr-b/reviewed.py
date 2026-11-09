# Reviewed corrections follow the actual course-name cells, never inferred subjects.
# This file runs in build.py's namespace.
modules={
'uwr-politologia':[
 ['Branding podmiotów politycznych','Media w Polsce: uwarunkowania i trendy','Anatomia konfliktu i sytuacji pokonfliktowej'],
 ['Kampanie marketingowe na rynku politycznym','Prawa człowieka','Przywództwo polityczne we współczesnym świecie'],
 ['Ponowoczesna polityka zagraniczna','Polityka administracyjna','Współczesne oblicza wpływu mediów','Źródła i przejawy populizmu w XXI w.']],
'uwr-zarzadzanie-projektami-spolecznymi':[
 ['Organizacje pozarządowe','Marketing podmiotów społecznych','Rozwój regionalny i lokalny','Ochrona środowiska'],
 ['Rynek pracy','Ochrona praw człowieka','Komunikowanie w sektorze samorządowym','Kobiety i ruchy kobiece w społeczeństwie nierówności'],
 ['Cywilizacje i religie','Dylematy tożsamości współczesnych społeczeństw','Konflikty i interwencje kryzysowe','Współczesne społeczeństwo polskie']]}
for record in records:
 for group in record['groups']:
  subjects=[]
  for name in group['subjects']:
   name=re.sub(r'\s+(?:E/[1-6]|Z\(E\)|Z|E)$','',name)
   name=name.replace('BUniwersytetu Wrocławskiego','Biblioteki Uniwersyteckiej we Wrocławiu')
   if name=='Lektorat języka polskiego dla':name+=' cudzoziemców'
   if name.startswith('Przedmiot:') or re.match(r'^O/W/',name):continue
   if record['programmeId']=='uwr-pedagogika-specjalna':name=re.sub(r'\s+[A-G]\d?(?:/F\d)?(?: \(NH\))?$','',name)
   if record['programmeId']=='uwr-studia-srodziemnomorskie':
    name=re.sub(r'(włoski|włoskiego) ([1-6])2$',r'\1 \2',name)
    name=re.sub(r'(cudzoziemców) ([1-4])5$',r'\1 \2',name)
   match=re.match(r'Moduł ([1-3])\. do wyboru',name)
   if match and record['programmeId'] in modules:
    subjects.extend(modules[record['programmeId']][int(match[1])-1]);continue
   if len(name)>3:subjects.append(name)
  group['subjects']=list(dict.fromkeys(subjects))
 record['groups']=[g for g in record['groups'] if g['subjects']]
 if record['groups']:record['completeness']='listed-subjects'

# A scanned framework; the parent agent verified both pages visually.
tour=json.loads(Path('tmp/pdfs/turystyka-transcription.json').read_text(encoding='utf8'))
r=by['uwr-turystyka'];r['referenceYear']=tour['referenceYear'];r['groups']=tour['groups'];r['note']=tour['note'];r['completeness']='listed-subjects'
url='https://wnoz.uwr.edu.pl/wp-content/uploads/sites/285/2024/01/lib-2023_24_t-k-lic_plan-skrocony_rama.pdf'
for group in r['groups']:group['sourceUrl']=url
r['sources'].append(dict(title='Turystyka — ramowy plan studiów stacjonarnych I stopnia Uniwersytetu Wrocławskiego',url=url,year=r['referenceYear'],note='Ręczny odczyt obu stron planu; zawartość modułów fakultatywnych nie jest częścią tego dokumentu.'))

# Official live institute page publishes the complete six-semester bachelor table.
history=[
['Wprowadzenie do historii sztuki','Historia sztuki starożytnej','Historia sztuki wczesnochrześcijańskiej','Historia sztuki średniowiecznej powszechnej','Techniki sztuk plastycznych','Przedmiot fakultatywny (nr 1) sprofilowany','Lektorat języka łacińskiego'],
['Wprowadzenie do historii sztuki','Historia sztuki starożytnej','Historia sztuki średniowiecznej powszechnej','Historia sztuki średniowiecznej w Polsce','Przedmiot fakultatywny (nr 2)','Lektorat języka łacińskiego','Lektorat języka obcego nowożytnego','Objazd zabytkoznawczo-krajoznawczy nr 1'],
['Historia sztuki średniowiecznej w Polsce','Historia sztuki nowożytnej powszechnej: renesans i manieryzm','Ikonografia i ikonologia','Teoria i metodologia nauk o sztuce cz. 1','Nauki pomocnicze historii sztuki','Techniki informacyjne i komunikacyjne w historii sztuki','Proseminarium I (średniowiecze)','Proseminarium II (nowożytność, renesans)','Przedmiot fakultatywny (nr 3)','Lektorat języka łacińskiego','Lektorat języka obcego nowożytnego','Wychowanie fizyczne'],
['Historia sztuki nowożytnej powszechnej: barok','Ikonografia i ikonologia','Teoria i metodologia nauk o sztuce cz. 2','Przedmiot fakultatywny (nr 4) sprofilowany','Proseminarium III (nowożytność, barok)','Proseminarium IV (nowoczesność)','Rzemiosło artystyczne i design — wprowadzenie do problematyki','Komputerowe techniki dokumentacji zabytków','Lektorat języka obcego nowożytnego — poziom B2 II','Lektorat języka łacińskiego','Objazd zabytkoznawczo-krajoznawczy nr 2','Obóz inwentaryzatorski','Wychowanie fizyczne'],
['Historia sztuki nowożytnej w Polsce: renesans i manieryzm','Historia sztuki nowoczesnej: malarstwo i rzeźba (powszechna i polska)','Historia sztuki nowoczesnej: architektura (powszechna i polska)','Teoretyczne i praktyczne aspekty konserwacji zabytków','Rynek dzieł sztuki','Kolekcjonerstwo i muzealnictwo — wprowadzenie do problematyki','Seminarium licencjacko-pomocnicze (seminarium I i seminarium II)','Historia filozofii'],
['Historia sztuki nowożytnej w Polsce: barok','Historia sztuki powszechnej XX i XXI w.: malarstwo, rzeźba, nowe formy sztuki','Historia sztuki XX i XXI w.: architektura (powszechnej i polskiej)','Teoretyczne i praktyczne aspekty konserwacji zabytków','Wybrane zagadnienia ochrony krajobrazu kulturowego','Historia filozofii','Seminarium licencjacko-pomocnicze (seminarium I i seminarium II) oraz egzamin licencjacki','Objazd zabytkoznawczo-krajoznawczy nr 3']]
url='https://historiasztuki.uwr.edu.pl/programy-studiow/'
r=by['uwr-historia-sztuki'];r['referenceYear']='program publikowany obecnie przez instytut; rok programu nieustalony';r['groups']=[dict(title='Plan studiów stacjonarnych I stopnia',semester=str(i)+'. semestr',subjects=names,sourceUrl=url) for i,names in enumerate(history,1)];r['completeness']='full-plan';r['note']='Pełna tabela sześciu semestrów I stopnia z oficjalnej strony Instytutu Historii Sztuki Uniwersytetu Wrocławskiego. Fakultety i grupy tematyczne pozostają wyborami. Strona nie określa roku wejścia programu w życie; nie potwierdza programu naboru 2027/2028.';r['sources'].append(dict(title='Historia sztuki — program studiów stacjonarnych I stopnia Uniwersytetu Wrocławskiego',url=url,year=r['referenceYear'],note='Odczyt tabeli I–VI semestru, przed sekcją efektów uczenia się; pominięto program II stopnia.'))
r=by['uwr-informatyka-stosowana-i-systemy-pomiarowe'];r['note']='W oficjalnych materiałach znaleziono historyczny plan dla zamkniętego cyklu 2022–2026. Nie użyto go jako programu obecnej oferty ani naboru 2027/2028. Aktualnego spisu przedmiotów i specjalności nie potwierdzono.'

# The USOS plan explicitly calls these five variants "specjalności" (pp. 4, 6).
import pymupdf as fitz
r=by['uwr-matematyka'];url=r['sources'][-1]['url']
mathnames=['Analiza danych','Matematyka aktuarialno-finansowa','Matematyka nauczycielska','Matematyka stosowana','Matematyka teoretyczna']
r['specializations']=[dict(name=n,kind='specjalność',note='Specjalność I stopnia wymieniona w programie; obok nich dostępny jest wariant ogólny bez specjalności.',sourceUrl=url) for n in mathnames];r['specializationStatus']='listed'
doc=fitz.open(cache/'0a82482251f76c17.pdf')
for group in r['groups']:
 page=int(group['title'].rsplit(' ',1)[-1]);text=re.sub(r'\s+',' ',doc[page-1].get_text());head=text.split('Suma [h]')[-1]
 variant=re.match(r'\s*(.*?) Sem:',head)
 group['title']='Matematyka I stopnia — '+(variant[1].strip() if variant else 'przedmioty do wyboru')+' — strona '+str(page)
 semesters=list(dict.fromkeys(re.findall(r'Sem: 0([1-6])',text)))
 group['semester']=' / '.join(semesters)+'. semestr' if semesters else None
r['note']+=' Listy obejmują alternatywne specjalności I stopnia oraz wariant ogólny, a nie łączny obowiązek zaliczenia wszystkich pozycji. Powtórzenia między wariantami są zamierzone.'

r=by['uwr-political-science'];url=r['sources'][-1]['url'];names=['Global Security','Media and Politics','Comparative Politics','Europe in the World']
r['specializations']=[dict(name=n,kind='specjalność',note='Wariant programu I stopnia opisany jako Specializations; lista przedmiotów jest alternatywą dla innych specjalności.',sourceUrl=url) for n in names];r['specializationStatus']='listed'
for group in r['groups']:
 page=int(group['title'].rsplit(' ',1)[-1]);group['title']='Political Science — '+(names[page-9] if 9<=page<=12 else 'przedmioty wspólne')+' — strona '+str(page)
r=by['uwr-niderlandystyka'];url=r['sources'][-1]['url']
r['specializations']=[dict(name=n,kind='specjalność',note='Nieobowiązkowa specjalność I stopnia; warunki i zajęcia na stronach 28–30 programu.',sourceUrl=url) for n in ['Język, kultura i literatura niderlandzka w kontekście środkowoeuropejskim','Belgijska']];r['specializationStatus']='listed'
r['groups'].extend([
 dict(title='Specjalność: Język, kultura i literatura niderlandzka w kontekście środkowoeuropejskim',semester=None,sourceUrl=url,subjects=['Wstęp do komunikacji międzykulturowej (kurs internetowy)','Zajęcia do wyboru nr 1 z bloku Historia i kultura Europy Środkowej oraz Unii Europejskiej','Zajęcia do wyboru nr 2 z bloku Historia i kultura Europy Środkowej oraz Unii Europejskiej','Zajęcia do wyboru nr 1 z bloku Język, literatura i kultura niderlandzka w kontekście środkowoeuropejskim','Zajęcia do wyboru nr 2 z bloku Język, literatura i kultura niderlandzka w kontekście środkowoeuropejskim','Zajęcia do wyboru nr 3 z bloku Język, literatura i kultura niderlandzka w kontekście środkowoeuropejskim']),
 dict(title='Specjalność belgijska — zajęcia obowiązkowe i lista do wyboru',semester=None,sourceUrl=url,subjects=['Praktyczna nauka języka francuskiego — sprawności zintegrowane 1','Praktyczna nauka języka francuskiego — sprawności zintegrowane 2','Belgia walońska','Belgia flamandzka','Zróżnicowanie językowe Belgii','Komiks belgijski','Znani Belgowie w literaturze','Zajęcia kierunkowe — wykład monograficzny i konwersatorium monograficzne (powiązane tematycznie z Belgią)','Zajęcia specjalizacyjne (powiązane tematycznie z Belgią)','Francuskojęzyczna literatura belgijska'])])
r['note']+=' Zajęcia dwóch nieobowiązkowych specjalności pokazano osobno; część zastępuje elementy programu wspólnego.'
r=by['uwr-publikowanie-cyfrowe-i-sieciowe'];url=r['sources'][-1]['url'];r['specializations']=[dict(name=n,kind='specjalność',note='Specjalność opisana w planie I stopnia od 2023/2024.',sourceUrl=url) for n in ['Komunikacja cyfrowa','Projektowanie publikacji']];r['specializationStatus']='listed'
for group in r['groups']:
 page=int(group['title'].rsplit(' ',1)[-1])
 if page in [6,7]:group['title']='Specjalności — przedmioty alternatywne — strona '+str(page)

# Remove row totals and restore wrapped labels checked against the source cells.
for r in records:
 for g in r['groups']:
  names=[]
  for n in g['subjects']:
   if re.search(r'^Liczba egzaminów|^Przedmioty do wyboru za|^Specjalność:|^wykład$|^\(PDW-',n,re.I):continue
   if n.startswith('Praktyka po III lub na IV roku Punkty ECTS'):n='Praktyka po III lub na IV roku'
   if n=='Formalne i nieformalne systemy':n='Formalne i nieformalne systemy wsparcia'
   if n.startswith('zoologii, Metodyka'):n='Metodyka prowadzenia badań terenowych w botanice i zoologii'
   if n.startswith('w-f '):n='Wychowanie fizyczne (60 godzin między semestrem 3. a 9.)'
   if n.startswith('Edukacje i metodyki:'):n='Edukacje i metodyki'
   if n=='Zarządzanie kolekcjami e- dokumentów':n='Zarządzanie kolekcjami e-dokumentów'
   if n=='Rynek wydawniczy w anglojęzycznych zasobach':n='Rynek wydawniczy w anglojęzycznych zasobach informacji'
   names.append(n)
  g['subjects']=list(dict.fromkeys(names))
 r['groups']=[g for g in r['groups'] if g['subjects']]

corrections={
'Gospodarka wodna i':'Gospodarka wodna i zarządzanie zasobami wodnymi',
'Zajęcia terenowe z':'Zajęcia terenowe z geologii gospodarczej',
'Bezpieczeństwo w':'Bezpieczeństwo w laboratorium chemicznym',
'Fizyczne metody badań w':'Fizyczne metody badań w ochronie środowiska naturalnego',
'Technologie informacyjno-komunikacyjne w':'Technologie informacyjno-komunikacyjne w pracy nauczyciela',
'Przedmiot fakultatywny E1 (do wyboru dla obu':'Przedmiot fakultatywny (do wyboru dla obu specjalności)',
'Przedmiot fakultatywny E1 (dla obu':'Przedmiot fakultatywny (dla obu specjalności)',
'Rehabilitacja osób z NI i z zaburzeniami ze':'Rehabilitacja osób z NI i z zaburzeniami ze spektrum autyzmu (ASD)',
'Wybrane metody terapii zajęciowej dorosłych z':'Wybrane metody terapii zajęciowej dorosłych z NI',
'Rehabilitacja osób z':'Rehabilitacja osób z niepełnosprawnościami',
'Praca socjalna z jednostką w':'Praca socjalna z jednostką w kryzysie (blok zajęć do wyboru)',
'Aksjologia pracy socjalnej z':'Aksjologia pracy socjalnej z elementami etyki',
'Lektorat nowożytnego języka':'Lektorat nowożytnego języka obcego',
'Zarządzanie kolekcjami edokumentów':'Zarządzanie kolekcjami e-dokumentów',
'Podstawy przedsiębiorczości w zawodach językowych lub':'Podstawy przedsiębiorczości w zawodach językowych',
}
for r in records:
 for g in r['groups']:
  names=[]
  for n in g['subjects']:
   n=corrections.get(n,n)
   if n=='Metodyka kształcenia i wychowania uczniów z':
    names.extend(['Metodyka kształcenia i wychowania uczniów z głębszą NI','Metodyka kształcenia i wychowania uczniów z lekką NI w kl. I–III']);continue
   n=re.sub(r'([)])([1-5])$',r'\1',n)
   if r['programmeId']=='uwr-indywidualne-studia-informatyczno-matematyczne':
    alternatives={'Algebra II Algebra 1':['Algebra II','Algebra 1'],'Algorytmy i struktury danych L Algorytmy i struktury danych M':['Algorytmy i struktury danych L','Algorytmy i struktury danych M'],'Matematyka dyskretna L Matematyka dyskretna M':['Matematyka dyskretna L','Matematyka dyskretna M'],'Równania różniczkowe 1 Równania różniczkowe 1 R':['Równania różniczkowe 1','Równania różniczkowe 1 R']}
    if n in alternatives:names.extend(alternatives[n]);continue
   names.append(n)
  g['subjects']=list(dict.fromkeys(names))
r=by['uwr-psychologia'];url=r['sources'][-1]['url'];psych=['Psychologia kliniczna i zdrowia','Psychologia kliniczna i wychowawcza dzieci i młodzieży','Psychologia biznesu i organizacji']
for g in r['groups']:g['subjects']=[n for n in g['subjects'] if not n.startswith('Moduł specjalnościowy')]
for n in psych:r['groups'].append(dict(title='Moduł specjalnościowy — '+n,semester=None,sourceUrl=url,subjects=[n+' '+i for i in ['I','II','III']]))
r['specializations']=[dict(name=n,kind='moduł',note='Wybierany moduł specjalnościowy I–III w programie jednolitych studiów magisterskich.',sourceUrl=url) for n in psych];r['specializationStatus']='listed'
r['note']+=' Trzy moduły specjalnościowe pokazano jako alternatywne warianty, nie wspólny obowiązek.'
# Source headings retain the official names of the variants even on pages mixing common rows.
for g in by['uwr-pedagogika-specjalna']['groups']:g['title']=g['title'].replace('Plan studiów','Przedmioty wspólne i warianty dwóch specjalności')

r=by['uwr-ochrona-srodowiska']
extra={
'Zasady pisania':['Zasady pisania dyplomowych i naukowych prac przyrodniczych'],
'Porosty jako biowskaźniki':['Porosty jako biowskaźniki stanu środowiska'],
'Zanieczyszczenia':['Zanieczyszczenia atmosfery'],
'Antropocen - rola':['Antropocen — rola człowieka w globalnym ekosystemie'],
'Płazy Świata - biologia,':['Płazy Świata — biologia, zagrożenia i ochrona'],
'Praktyki zawodowe':['Praktyki zawodowe (ochrona różnorodności biologicznej)','Praktyki zawodowe (monitoring i technologie środowiskowe)','Praktyki zawodowe (zarządzanie i edukacja ekologiczna)'],
'Problematyka nauk':['Problematyka nauk przyrodniczych (ochrona różnorodności biologicznej)','Problematyka nauk przyrodniczych (monitoring i technologie środowiskowe)'],
'Przygotowanie pracy':['Przygotowanie pracy dyplomowej (ochrona różnorodności biologicznej)','Przygotowanie pracy dyplomowej (monitoring i technologie środowiskowe)'],
'Seminarium dyplomowe':['Seminarium dyplomowe (ochrona różnorodności biologicznej)','Seminarium dyplomowe (monitoring i technologie środowiskowe)']}
for g in r['groups']:g['subjects']=[n for old in g['subjects'] for n in extra.get(old,[old])]
r['groups'].append(dict(title='Przedmioty fakultatywne — uzupełnienie odczytu strony 5',semester=None,sourceUrl=r['sources'][-1]['url'],subjects=['Wulkanizm i środowisko']))
for g in by['uwr-sinologia']['groups']:g['subjects']=[n.replace('Chinkanony','Chin — kanony') for n in g['subjects']]
# Some USOS pages finish one variant and start another. Label both explicitly.
r=by['uwr-matematyka'];doc=fitz.open(cache/'0a82482251f76c17.pdf')
variants=[n.lower() for n in mathnames]+['ogólna']
for g in r['groups']:
 p=int(g['title'].rsplit(' ',1)[-1]);lines=[re.sub(r'\s+',' ',t.strip()) for t in doc[p-1].get_text().splitlines()]
 present=[n for n in variants if n in lines]
 if len(present)>1:g['title']='Matematyka I stopnia — '+ ' / '.join(present)+' — strona '+str(p)

r=by['uwr-informatyka'];url=r['sources'][-1]['url']
for g in r['groups']:g['title']='Siedem przedmiotów obowiązkowych wymaganych do zaliczenia semestrów — tabela 1'
r['groups'].append(dict(title='Dodatkowe nazwy i zakresy z tabeli treści programowych I stopnia — strony 13–14',semester=None,sourceUrl=url,subjects=['Rachunek prawdopodobieństwa i statystyka','Inżynieria oprogramowania','Programowanie i projektowanie obiektowe','Architektury systemów komputerowych','Systemy operacyjne','Sieci komputerowe','Bazy danych','Ochrona własności intelektualnej','Projekt programistyczny','Proseminarium']))
r['note']='Elastyczny program studiów inżynierskich I stopnia. Pierwsza grupa obejmuje siedem nazw z tabeli obowiązkowych przedmiotów wymaganych do zaliczenia semestrów; druga dziesięć dodatkowych nazw lub zakresów z tabeli treści programowych. Pozostałe zajęcia wybiera się z oferty dydaktycznej zgodnie z kategoriami i limitami ECTS (m.in. kursy, projekty i seminaria); uchwała odsyła do osobnej oferty i sylabusów, nie publikuje zamkniętej listy wszystkich fakultetów. To nie pełny plan ani potwierdzenie programu naboru 2027/2028.'

for r in records:
 for g in r['groups']:g['subjects']=[n for n in g['subjects'] if not re.fullmatch(r'(?:Łącznie|Razem|Suma|Total)[:.]?',n,re.I)]
