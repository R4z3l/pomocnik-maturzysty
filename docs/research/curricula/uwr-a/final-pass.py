import json,re
from pathlib import Path
D=Path('docs/research/curricula/uwr-a');P=Path('src/data/curricula-uwr-a.json');rs=json.loads(P.read_text(encoding='utf-8'));by={r['programmeId']:r for r in rs}
r=by['uwr-biotechnologia']
for g in r['groups']:
 ss=[]
 for s in g['subjects']:
  s=s.replace(' II zajęcia do wyboru:','')
  s=s.replace('j. polski dla cudzoziemców','Język polski dla cudzoziemców')
  for a,b in [('ćwiczenia Biologia','ćwiczenia / Biologia'),('zwierząt Metabolizm','zwierząt / Metabolizm'),('roślin Fizjologia','roślin / Fizjologia'),('medycznej Biofizyka','medycznej / Biofizyka'),('ćwiczenia Biofizyka','ćwiczenia / Biofizyka'),('roślinnych Hodowle','roślinnych / Hodowle'),('ćwiczenia Hodowle','ćwiczenia / Hodowle'),('medycznej Biotechnologia','medycznej / Biotechnologia'),('ćwiczenia Biotechnologia','ćwiczenia / Biotechnologia'),('farmaceutyczna Bioinżynieria','farmaceutyczna / Bioinżynieria'),('ćwiczenia Bioinżynieria','ćwiczenia / Bioinżynieria')]:s=s.replace(a,b)
  ss.append(s)
 g['subjects']=ss
r['groups'][-1]['subjects'].append('Wychowanie fizyczne')
r=by['uwr-filologia-polska'];parts={'Fonetyka z fonologią (I) Fonetyka z fonologią (II)':['Fonetyka z fonologią (I)','Fonetyka z fonologią (II)'],'Literatura XX wieku (I) Literatura XX wieku (II)':['Literatura XX wieku (I)','Literatura XX wieku (II)'],'Morfologia (słowotwórstwo i fleksja) (I) Morfologia (fleksja) (II) Morfologia (słowotwórstwo (III)':['Morfologia (słowotwórstwo i fleksja) (I)','Morfologia (fleksja) (II)','Morfologia (słowotwórstwo) (III)']}
for g in r['groups']:g['subjects']=[v for s in g['subjects'] for v in parts.get(s,[s])]
for g in by['uwr-biotechnology']['groups']:g['subjects']=[re.sub(r'1\)$','',s).strip() for s in g['subjects']]
r=by['uwr-geografia'];u='https://igrr.uwr.edu.pl/wp-content/uploads/sites/297/2025/04/2023_24_gf-lic_program-skrocony_fakult.pdf'
r['specializations']=[{'name':n,'kind':'ścieżka','sourceUrl':u,'note':'Ścieżka fakultatywna w oficjalnym planie Uniwersytetu Wrocławskiego od 2023/2024; nie odrębna specjalność.'} for n in ['Geografia fizyczna','Geografia człowieka']];r['specializationStatus']='listed'
for title,text in [('Geografia fizyczna','Chemia Ziemi|Geologia regionalna Polski|Gospodarka wodna|Lodowce i lądolody|Dzieje Ziemi|Formy i procesy obszarów suchych i półsuchych|Klimat obszarów górskich|Paleogeografia|Procesy rzeźbotwórcze|Środowiska górskie|Zanieczyszczenia i ochrona atmosfery|Geografia Republiki Czeskiej|Ilościowa analiza danych w geografii fizycznej|Podstawy dendrochronologii|Środowiska obszarów polarnych|Wstęp do sedymentologii|Adaptacja do zmian klimatu|Formy i osady czwartorzędowe|Geografia fizyczna kompleksowa|Klimaty świata|Permafrost i środowiska peryglacjalne|Problemy gospodarowania i ochrony środowiska na obszarach Natura 2000'),('Geografia człowieka','Ekonomika kultury|Geografia regionalna Azji i Australii|Geografia regionalna Europy|Pochodzenie i ewolucja człowieka|Elementy projektowania urbanistycznego|Geografia ekonomiczna Polski|Geografia Internetu|Geografia regionalna Ameryk|Geografia religii|Geografia transportu|Geografia ekonomiczna świata|Geografia kultur|Geografia obszarów wiejskich|Geografia regionalna Afryki|Problemy rozwoju obszarów pogranicznych|Geografia miast|Krajobrazy kulturowe świata|Krajoznawstwo|Nowy urbanizm|Podstawy przedsiębiorczości i zarządzania|Wybrane formy turystyki')]:r['groups'].append({'title':title+' — przedmioty fakultatywne','semester':None,'subjects':text.split('|'),'sourceUrl':u})
r['sources'].append({'title':'Geografia — plan ścieżek fakultatywnych Uniwersytetu Wrocławskiego','url':u,'year':'od 2023/2024','note':'Komplet 22 nazw ścieżki Geografia fizyczna i 21 nazw ścieżki Geografia człowieka z oficjalnego dokumentu.'})
r=by['uwr-chemia'];u='https://chem.uwr.edu.pl/studia/studia-licencjackie/studia-licencjackie-kierunek-chemia/'
r['specializations']=[{'name':n,'kind':'specjalność','sourceUrl':u,'note':'Jawna nazwa specjalności w oficjalnym opisie studiów licencjackich Uniwersytetu Wrocławskiego; opis nie określa naboru, w którym uruchomi się grupa.'} for n in ['Chemia Ogólna','Chemia Analityczna','Chemia Materiałów dla Nowoczesnych Technologii']];r['specializationStatus']='listed'
if not any(s['url']==u for s in r['sources']):r['sources'].append({'title':'Chemia — opis studiów licencjackich Uniwersytetu Wrocławskiego','url':u,'year':'bieżący opis; odczyt 2026-10-25','note':'Wykaz jawnie opisanych specjalności na stronie studiów licencjackich.'})
r=by['uwr-bachelor-of-business-and-administration'];u=next(s['url'] for s in r['sources'] if s['url'].endswith('.pdf'));r['specializations']=[{'name':n,'kind':'specjalność','sourceUrl':u,'note':'Dosłowna nazwa specjalności w programie Uniwersytetu Wrocławskiego od 2023/2024; plan stacjonarnego I stopnia, strony 61–65.'} for n in ['Biznes','Finanse','Governance']];r['specializationStatus']='listed'
for r in rs:
 seen=set()
 for g in r['groups']:g['subjects']=[s for s in g['subjects'] if not(s.casefold() in seen or seen.add(s.casefold()))]
 r['groups']=[g for g in r['groups'] if g['subjects']];r['sources']=list({s['url']:s for s in r['sources']}.values())
P.write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(D/'final-all-names.txt').write_text('\n\n'.join(r['programmeId']+'\n'+'\n'.join(s for g in r['groups'] for s in g['subjects']) for r in rs),encoding='utf-8')
print('records',len(rs),'with lists',sum(bool(r['groups']) for r in rs),'full',sum(r['completeness']=='full-plan' for r in rs),'names',sum(len(g['subjects']) for r in rs for g in r['groups']),'with specs',sum(bool(r['specializations']) for r in rs))
