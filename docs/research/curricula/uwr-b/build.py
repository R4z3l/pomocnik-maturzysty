import json,re
from pathlib import Path
root=Path(__file__).parent
cache=root/'cache'
cards=json.loads((root/'cards.json').read_text(encoding='utf8'))
records=[]
for c in cards:
 records.append(dict(programmeId=c['id'],checkedAt='2026-10-25',referenceYear='rok programu nieustalony',completeness='unavailable',groups=[],specializations=[],specializationStatus='not-found',note='W oficjalnych materiałach nie potwierdzono pełnego spisu przedmiotów ani roku programu. Brak potwierdzenia specjalności nie oznacza ich nieistnienia.',sources=[dict(title=c['name']+' — oficjalny opis Uniwersytetu Wrocławskiego',url=c['url'],year='opis bieżący, odczyt 2026-10-25',note='Opis kierunku; rok rekrutacji nie wyznacza rocznika programu studiów.')]))
by={r['programmeId']:r for r in records}
mapping={
'historia':('1e2369b8d0556be9','2025/2026'),
'informatyka':('04781d78c4e3569e','uchwała 163/2023 — program publikowany obecnie przez instytut'),
'indywidualne-studia-informatyczno-matematyczne':('28a9217b670ca104','uchwała 90/2022 — program publikowany obecnie w BIP'),
'psychologia':('0a5d70ef73d1329b','program publikowany obecnie przez instytut; rok programu nieustalony'),
'prawo':('3dbd917e9ca61b20','od 2019/2020 — program publikowany obecnie przez wydział'),
'pedagogika-specjalna':('b87f7dfefa066a85','uchwała 95/2022 — program publikowany obecnie w BIP'),
'publikowanie-cyfrowe-i-sieciowe':('47dd0092d2e5fbd1','od 2023/2024'),
'ochrona-srodowiska':('684754e44a146247','od 2023/2024'),
'informacja-naukowa-i-bibliotekoznawstwo':('607848dedc3157d7','2024/2025'),
'inzynieria-geologiczna':('addb3d02c585ebb3','2025/2026'),
'italianistyka':('cf727cf4e9724481','2025/2026'),
'judaistyka':('77219c48a9bfaff5','2025/2026'),
'komunikacja-wizerunkowa':('9ee9faa1cb067728','2024/2025'),
'koreanistyka':('21cdfea431c48440','2025/2026'),
'kultura-i-praktyka-tekstu-tworcze-pisanie-i-edytorstwo':('687a6cc41b1b467d','uchwała 86/2022; plan udostępniony w sekcji 2026/2027'),
'kulturoznawstwo':('e37a3a33da818877','rok nieoznaczony w skróconym planie'),
'literatura-swiatowa-komparatystyka-i-wielokulturowosc':('e4ae0e1cd09b1f6c','2024/2025'),
'll-b-international-and-european-environmental-law':('add6d4e3c4f0027a','2024/2025'),
'logopedia':('1bea8d0e31c7f84c','2026/2027'),
'matematyka':('0a82482251f76c17','2026/2027'),
'medyczna-biotechnologia-molekularna':('91f0c5c9c783c128','2023/2024 — program publikowany obecnie przez wydział'),
'mikrobiologia':('c559d1ef651e1996','2026/2027 (program od 2023/2024)'),
'muzykologia':('7eb11fdf0ed64f2d','2026/2027'),
'niderlandystyka':('f53546919a57ada9','2025/2026'),
'political-science':('8aa125798454591a','2024/2025'),
'politologia':('b2b22700aa9f6414','2024/2025'),
'praca-socjalna':('55e9b9ae113f7a2d','2024/2025'),
'sinologia':('76b40106fea15ebb','2025/2026'),
'socjologia':('9babb9732af227db','2024/2025'),
'socjologia-ekonomiczna':('e1379c8287b422e7','program publikowany obecnie przez instytut; rok nieustalony'),
'stosunki-miedzynarodowe':('ff5924209372dc9d','2024/2025'),
'stosunki-miedzynarodowe-specjalnosc-global-studies':('ff5924209372dc9d','2024/2025'),
'studia-srodziemnomorskie':('32a44938069e16f8','2025/2026'),
'sztuczna-inteligencja-w-analizie-danych':('17e1456c2be5f03a','2025/2026'),
'techniki-eksperymentalne-w-kryminalistyce':('2b5b748ee09d20ad','2026/2027'),
'zarzadzanie-projektami-spolecznymi':('989700773cd625a0','2024/2025'),
'zarzadzanie-srodowiskiem-przyrodniczym':('95723042531130d5','2025/2026 (program od 2023/2024)'),
'zielona-chemia':('56931a4e3c053d65','2024/2025'),
}
def tidy(s):
 s=re.sub(r'(\w)-\s+(\w)',r'\1\2',s)
 s=re.sub(r'(?<=[a-ząćęłńóśźż])\d+\*?(?=\s|$)','',s)
 s=re.sub(r'\*+','',s)
 s=s.replace('UWr','Uniwersytetu Wrocławskiego')
 return re.sub(r'\s+',' ',s).strip()
for slug,(key,year) in mapping.items():
 p=cache/(key+'.repaired.json')
 if not p.exists():continue
 if key in ['e37a3a33da818877','e4ae0e1cd09b1f6c']:p=cache/(key+'.selected.json')
 data=json.loads(p.read_text(encoding='utf8'));source=json.loads((cache/(key+'.json')).read_text(encoding='utf8'))
 if slug=='stosunki-miedzynarodowe':data=[g for g in data if 79<=g['page']<=86]
 if slug=='stosunki-miedzynarodowe-specjalnosc-global-studies':data=[g for g in data if 87<=g['page']<=91]
 r=by['uwr-'+slug];r['referenceYear']=year
 groups=[]
 for g in data:
  subjects=list(dict.fromkeys(tidy(s) for s in g['subjects'] if len(s)>3 and not re.search(r'nazwa przedmiotu|liczba godzin|objaśnienie|znaczeń|zaliczenie z oceną|lektora[t]? w wymiarze|^Z –|^O/W/|^TEKSTU:',s,re.I)))
  if subjects:groups.append(dict(title='Plan studiów — strona '+str(g['page']),semester=None,subjects=subjects,sourceUrl=source['url']))
 r['groups']=groups;r['completeness']='listed-subjects' if groups else 'unavailable'
 r['sources'].append(dict(title=cards[[c['id'] for c in cards].index(r['programmeId'])]['name']+' — program Uniwersytetu Wrocławskiego',url=source['url'],year=year,note='Oficjalny dokument programu; zakres obejmuje poziom i tryb wskazany w ofercie.'))
 r['note']='Spis przedmiotów z oficjalnego programu Uniwersytetu Wrocławskiego. Rok źródła podano niezależnie od rekrutacji. Zajęcia do wyboru są alternatywami, nie obowiązkiem realizacji wszystkich pozycji. Program nie potwierdza jeszcze zasad dla naboru 2027/2028.'
def listed(slug,url,subjects,title='Przedmioty wskazane w oficjalnym opisie',year='opis bieżący, odczyt 2026-10-25',note=None):
 r=by['uwr-'+slug];r['referenceYear']=year;r['completeness']='listed-subjects';r['groups']=[dict(title=title,semester=None,subjects=subjects,sourceUrl=url)]
 r['sources'].append(dict(title=title+' — Uniwersytet Wrocławski',url=url,year=year,note='Oficjalny opis; lista nie stanowi pełnego planu studiów.'))
 r['note']=note or 'Oficjalny opis zawiera listę wybranych przedmiotów. Nie jest to pełny plan semestralny; roku obowiązywania całego programu nie potwierdzono.'
listed('indywidualne-studia-miedzydziedzinowe','https://kmsi.uwr.edu.pl/',['Beyond Language','Metodologie badawcze z elementami Academic English','Filozofia Nauki / Filozofia Przyrody'],note='Zajęcia wspólne Kolegium Międzydziedzinowych Studiów Indywidualnych. Pozostały program student ustala indywidualnie z tutorem; nie istnieje jeden wspólny spis przedmiotów wszystkich studiujących.')
listed('pedagogika','https://pedagogika.uwr.edu.pl/studia-licencjackie/',['Andragogika','Psychologia rozwoju dorosłych','Problemy aktywizacji i rozwoju społeczności lokalnych','Edukacja kulturalna dorosłych','Film w działaniach edukacyjnych','Podstawy zarządzania karierą','Podstawy tutoringu, coachingu i mentoringu','Nowoczesne technologie informacyjne w edukacji dorosłych','Metodyka pracy z grupą','Metodyka projektów edukacyjnych','Podstawy pracy edukacyjnej z seniorami','Marketing społeczny','Teorie przyczyn przestępczości','Psychologia kliniczna i społecznego niedostosowania','Pedagogika specjalna w praktyce resocjalizacyjnej','Patologia społeczna','Pedagogika resocjalizacyjna','Metodyka resocjalizacji','Pedagogika penitencjarna','Diagnostyka w resocjalizacji','Profilaktyka niedostosowania społecznego','Terapia pedagogiczna','Praca korekcyjna z dziećmi z zaburzeniami w zachowaniu','Europejskie systemy resocjalizacji','Podstawy prawa rodzinnego','Prawne podstawy resocjalizacji','Prawa człowieka i ich ochrona','Higiena pracy pedagoga','Seminaria monograficzne','Seminarium licencjackie','Podstawy pomocy psychopedagogicznej i poradnictwa','Psychopatologia rozwoju','Metody pracy w poradnictwie indywidualnym i grupowym','Wprowadzenie do poradoznawstwa','Poradnictwo wielokulturowe','Orientacja i poradnictwo zawodowe z metodyką','Zarządzanie karierą','Podstawy wiedzy o małżeństwie i rodzinie','Poradnictwo wychowawcze i rodzinne z metodyką','Seksuologia i planowanie rodziny','Interwencja i terapia psychopedagogiczna','Metody diagnozy i terapii pedagogicznej','Logopedia','Treningi: relaksacyjny, interpersonalny, asertywności, umiejętności wychowawczych','Metody terapii pedagogicznej','Metody prowadzenia zajęć rozwijających kompetencje społeczno-emocjonalne'],title='Wybrane przedmioty specjalności (edukacja dorosłych, resocjalizacja, poradnictwo)')
listed('pedagogika-przedszkolna-i-wczesnoszkolna','https://pedagogika.uwr.edu.pl/studia-jednolite-magisterskie/',['Pedagogika przedszkolna','Pedagogika wczesnoszkolna','Dydaktyka edukacji przedszkolnej','Dydaktyka edukacji wczesnoszkolnej','Kultura przedszkola i szkoły','Edukacja międzykulturowa','Edukacje i metodyki: matematyczna, polonistyczna, plastyczna, techniczna, muzyczna, społeczno-przyrodnicza, zdrowotna, nauczania języka angielskiego, wychowania fizycznego, informatyczna i posługiwania się TiK','Psychologiczne i pedagogiczne podstawy nauczania języka obcego u dzieci','Współczesne koncepcje dziecka i dzieciństwa','Współpraca nauczyciela z rodzicami i środowiskiem wychowawczym','Diagnoza funkcjonalna','Terapia pedagogiczna dzieci ze specjalnymi potrzebami edukacyjnymi','Metody diagnozy dzieci ze SPE','Edukacja dziecka z problemami w obszarze językowym','Edukacja dziecka z trudnościami w uczeniu się matematyki','Elementy logopedii w pracy nauczyciela','Metody rozwiązywania trudności wychowawczych w edukacji przedszkolnej i wczesnoszkolnej','Konstruowanie programów pracy wychowawczo-dydaktycznej','Ewaluacja i ocenianie w edukacji przedszkolnej i wczesnoszkolnej','Praca w świetlicy szkolnej','Edukacja w instytutach kultury','Pedagogika twórczości','Metody wspierające twórczy rozwój dziecka','Metody arteterapii','Warsztaty edukacji teatralnej','Animacja zabawy','Przywództwo edukacyjne w pracy nauczyciela','Wystąpienia publiczne z kulturą żywego słowa','Zarządzanie projektami edukacyjnymi','Warsztaty rozwoju zawodowego','Warsztaty zapobiegania agresji','Stres i zarządzanie stresem'])
specs={
'historia':['Nauczycielska z historią / z WOS','Amerykanistyka','Archiwistyka i zarządzanie dokumentacją','Dokumentalistyka konserwatorska','Regionalistyka i kształtowanie społeczności lokalnej','Historia wojen i wojskowości'],
'italianistyka':['Hispanistyczna','Romanistyczna'],
'komunikacja-wizerunkowa':['Branding','Communication Design'],
'kulturoznawstwo':['Kultura filmowa','Studia miejskie i globalne','Ekologie kultury'],
'niderlandystyka':['DCC — Język, kultura i literatura niderlandzka w kontekście środkowoeuropejskim','Belgijska'],
'pedagogika':['Edukacja dorosłych i marketing społeczny','Pedagogika opiekuńcza z terapią','Poradnictwo i pomoc psychopedagogiczna','Resocjalizacja'],
'pedagogika-specjalna':['Edukacja i rehabilitacja osób z niepełnosprawnością intelektualną','Wczesne wspomaganie rozwoju dziecka'],
}
for slug,names in specs.items():
 r=by['uwr-'+slug];r['specializations']=[dict(name=name,kind='specjalność',note='Nazwa potwierdzona w oficjalnym opisie kierunku Uniwersytetu Wrocławskiego; uruchomienie może zależeć od liczby chętnych.',sourceUrl=r['sources'][0]['url']) for name in names];r['specializationStatus']='listed'
exec(compile((root/'reviewed.py').read_text(encoding='utf8'),str(root/'reviewed.py'),'exec'))
out=Path('src/data/curricula-uwr-b.json');out.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(len(records),'records;',sum(bool(r['groups']) for r in records),'with subjects')
