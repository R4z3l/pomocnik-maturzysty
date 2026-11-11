# Dodanie Uniwersytetu Medycznego im. Piastów Śląskich we Wrocławiu — 10.11.2026

Dodano 16 ofert (13 PL, 3 EN), 26 wersji reguł dla 13 ofert PL, 35 oficjalnych progów 2024–2026 i 16 częściowych spisów zajęć. Osobne zasady 2026/27 służą dopasowaniu matury i porównaniu progów; uwzględniono zmiany farmacji, psychologii i minimów. English Division bez automatycznej sumy z powodu nierozstrzygniętego zakresu zapisów w dokumencie. ELA pozostaje luką. Parser i adapter działają bez AI. Katalog: 215 ofert pięciu uczelni, 200 kalkulatorów, 116 pełnych i 99 częściowych spisów. Audyt: docs/audyt-umw.md.

# Dodanie Uniwersytetu Przyrodniczego we Wrocławiu — 10.11.2026

Dodano 28 ofert stacjonarnych, 28 pełnych spisów planów 2026/2027, reguły kalkulatorów 2027/2028 dla polskiej nowej matury PP/PR bez KZ i 53 nieoficjalne progi z portalu dla naborów 2025/2026 oraz 2026/2027. Tabela portalu 2024/2025 nie zawierała liczb. Brak ELA pozostaje jawny. Katalog: 199 ofert, 187 kalkulatorów, 116 pełnych planów i 83 listy częściowe. Adapter i monitor działają poza aplikacją, bez AI. Szczegóły: docs/audyt-upwr.md. Poniżej wcześniejsze stany audytu.

# Domknięcie katalogowej bazy trzech uczelni — 09.11.2026

Zakres potwierdzony przez użytkownika: Uniwersytet Wrocławski, Uniwersytet Ekonomiczny we Wrocławiu i Politechnika Wrocławska, 171 ofert stacjonarnych I stopnia i jednolitych we Wrocławiu, PL/EN. To zakres odbioru bazy katalogowej; nie jest to deklaracja ukończenia całego planu aplikacji ani potwierdzenie wszystkich ofert i warunków 2027/28.

- Wszystkie 171 ofert ma opis, tożsamość, czas studiów, źródła oraz spis zajęć. 88 rekordów to pełne plany wskazanego cyklu, 83 to jawne listy częściowe Uniwersytetu Wrocławskiego. Nie ma już rekordu programu ze statusem unavailable.
- European Cultures: odnaleziono w BIP uchwałę Senatu 168/2023 i wizualnie sprawdzono wszystkie tabele planu, strony 51–56 z 57 stron. 59 wpisów, sześć semestrów, pule wyboru, warunkowy język polski i WF. Plan od cyklu 2023/24, bez dopisywania potwierdzenia 2027/28. Odczyt jest chroniony skrótami dokumentu i transkrypcji.
- Politechnika Wrocławska: pełny odczyt wszystkich 62 opublikowanych planów 2026/27, 644 tabel i 763 rozwijanych grup. Usunięto instrukcje wyboru z przedmiotów, nazwy koszyków przeniesiono do tytułów; zagnieżdżone pule zachowują hierarchię. Zweryfikowano 5788 rzeczywistych wierszy zajęć. Szczegóły: docs/audyt-pwr.md i raport JSON w docs/research.
- 159 ofert ma zweryfikowaną regułę kalkulatora, 12 anglojęzycznych ofert Uniwersytetu Wrocławskiego — odrębne procedury dokumentowe. 604 rekordy historii z naborów 2024–2026; brak progu w części ofert pozostaje jawnym brakiem, a nie zerem.
- Okresowe utrzymanie bez tokenów: 66 adapterów odczytu tabel, metryczek i planów oraz monitor pozostałych oficjalnych źródeł. Nowe lub zmienione dokumenty bez zgodnego parsera wymagają przeglądu człowieka. Nie włączono stałego harmonogramu, nie zmieniono polityki wykluczeń i nie opublikowano aplikacji.

Dalszy zakres: pełny audyt 83 częściowych spisów, nowe materiały 2027/28 w miarę publikacji oraz moduł doradczy z danymi absolwentów i ścieżkami zawodowymi. Jawne listy częściowe nie są oznaczane jako pełne. Kryteria i ograniczenia odbioru: docs/research/baza-trzy-uczelnie-2026-11-09.md. Wcześniejsze wpisy poniżej dokumentują stan na poprzednich etapach.

---

# Baza wiedzy i pobieranie bez AI — 09.11.2026

Aktualny zakres: 171 ofert trzech uczelni — Uniwersytetu Wrocławskiego, Uniwersytetu Ekonomicznego we Wrocławiu i Politechniki Wrocławskiej. Starsze wpisy poniżej pozostają historią, nie raportem aktualnego pokrycia.

Dodano lokalny proces pobierania, cache, porównanie zmian źródeł, osobne propozycje oraz zastosowanie po testach, walidacji, kontroli typów, buildzie i kontroli paczki. Bez modeli i API AI. Reguły polityki źródeł i wykluczeń obowiązują przed pobraniem i przed przekierowaniem. Zmiany nieznanego układu dokumentu lub reguły są zatrzymywane do przeglądu człowieka. Szczegóły i obsługiwane adaptery: `docs/aktualizacja-bez-ai.md`, widoczne w „Instrukcjach”. Nie włączono stałego harmonogramu ani automatycznej publikacji.

W „Źródła i pokrycie” dodano dynamiczny stan bazy osobno dla każdej uczelni; poprawiono mianownik pokrycia ELA po dodaniu Politechniki Wrocławskiej. README nie opisuje już katalogu dwóch uczelni. Pełne plany, częściowe spisy i luki pozostają odrębne. Uzupełniono czas studiów wszystkich 20 ofert Uniwersytetu Ekonomicznego we Wrocławiu z metryczek oficjalnego programu 2026/27. Wszystkie 171 ofert mają teraz potwierdzony czas studiów właściwego rocznika. Propozycja została zastosowana dopiero po pięciu kontrolach w oddzielnej kopii. Przeprowadzono monitorowanie 460 źródeł z rejestru; to kontrola pobierania i punkt odniesienia zmian, nie nowy audyt merytoryczny wszystkich dokumentów.

Nie uznajemy całego etapu bazy wiedzy za zakończony: nadal potrzeba potwierdzenia kompletności częściowych spisów, brakującego planu European Cultures, dodatkowych danych absolwentów i danych naboru 2027/28 w miarę publikacji. Monitorowanie źródeł nie usuwa tych luk automatycznie.

---

# Instrukcje w aplikacji — 29.10.2026

Dodano sekcję „Instrukcje” z pięcioma tematami: aktualizacja z AI, dodawanie uczelni, źródła, programy i specjalności oraz prywatna publikacja. Treść pochodzi bezpośrednio z dokumentów Markdown projektu i jest dołączana przy budowaniu; aktualizacja wersji online wymaga ponownej publikacji. Polecenie dla AI ma przycisk kopiowania i komunikat błędu, gdy przeglądarka nie udostępnia schowka. Zasada w AGENTS.md nakazuje dodawać przyszłe instrukcje dla użytkownika do widoku. W przeglądarce sprawdzono wybór instrukcji, linki, kopiowanie i układ przy szerokości 390 px. Testy, walidacja danych i build przeszły.

---

# Aktualizacja z AI w domu — 29.10.2026

Dodano `docs/aktualizacja-ai.md` z pełnym promptem i procedurą aktualizacji w kopii, z zachowaniem polityki źródeł. `npm run update:start` tworzy osobne kopie referencyjną i roboczą wraz z manifestem; `npm run update:report -- "folder"` porównuje dane, kod i dokumenty, ostrzega o zmianach aktywnego projektu i sprawdza integralność kopii referencyjnej. Raport jest ograniczonym podglądem, nie walidacją merytoryczną ani mechanizmem podmiany. Integracja i publikacja są oddzielnymi krokami. Sprawdzono pełny cykl na kopii prawdziwego projektu: testy, walidację, build, wykrycie przykładowej zmiany, zmiany aktywnego pliku i modyfikacji kopii referencyjnej; test automatyczny odtwarza te sytuacje w izolowanym katalogu. Nie dodano API do aplikacji.

---

# Osobiste rekomendacje i audyt ELA — 29.10.2026

Dodano widok „Moje rekomendacje”: jawna liczba rodzajów znalezionych zgodności z wybranymi rozszerzeniami, dosłownie znalezionymi słowami zainteresowań oraz rodzajami pracy sugerowanych rodzin zawodów; ten sam rodzaj zgodności liczy się tylko raz. Przedmioty studiów są porównywane tylko z dostępnym spisem; częściowe listy są oznaczone. Zaprzeczenie w zainteresowaniach wstrzymuje porównanie słów. Lista nie ustala szans przyjęcia ani kwalifikacji, nie interpretuje synonimów, wyników matur ani swobodnego opisu stylu pracy. Brak wskazówki nie dowodzi niedopasowania. Użytkownik może otworzyć kartę kierunku; dane profilu nie wymagają migracji.

Uzupełniono informatykę stosowaną i systemy pomiarowe na podstawie planu uczelni dla cyklu 2025–2029: 40 przedmiotów obowiązkowych, 25 z puli wyboru oraz lektorat polskiego warunkowy dla cudzoziemców. Semestry potwierdzono w tabeli, po niezależnej kontroli poprawiono język obcy na III–V. Plan nie jest potwierdzeniem programu na 2027/28. Łączne pokrycie: 108/109 ofert ze spisem, 25 pełnych i 83 częściowe; European Cultures pozostaje bez potwierdzonej listy zajęć. Raport i źródło: `docs/research/curricula/uwr-b/ISSP-2025-2029.md`.

Kontrola lokalnego wycinka ELA edycji 11: 76 wierszy, 70 kohort w aplikacji. Dwa z sześciu pozostałych wierszy dotyczą filii w Jeleniej Górze; cztery inne mają nazwy odrębne od bieżących ofert. Nie ma podstaw do przenoszenia ich danych na podobnie nazwane kierunki; brak pola języka utrudnia dalsze dopasowanie. Pokrycie pozostaje 69 ofert. Do zakończenia etapu domykania danych potrzebna jest dalsza kontrola brakujących programów, specjalności i progów w wiarygodnych źródłach.

---

# Przygotowanie prywatnego udostępnienia — 29.10.2026

Dodano instrukcję `docs/publikacja-prywatna.md`, nieszkodliwą stronę do wstępnej konfiguracji oraz lokalną kontrolę `npm run check:release`. Instrukcja opisuje osobną ochronę głównego adresu, podglądów i domeny, logowanie kodem e-mail oraz kontrolę bezpośrednich plików. Cztery pliki obecnego `dist` przeszły kontrolę; próbny nieoczekiwany plik został odrzucony. Kontrola nazw nie gwarantuje braku danych w treści. Aplikacja nie została opublikowana; rzeczywista konfiguracja hostingu i autoryzacja nie były sprawdzone. Na lokalnej wersji produkcyjnej sprawdzono zapis, odczyt, eksport i import profilu testowego.

---

# Oferty komunikacji i marketingu — 29.10.2026

Dodano trzy przykłady dla rodziny języków, kultury i komunikacji: K+, Greenfields i praktykę absolwencką MONTANA PRIORITY COMPANY na Aplikuj.pl. Dwie pierwsze strony nie podają daty naboru, więc aktualność pozostaje niepotwierdzona; trzecia podaje termin 25.11.2026. Przykłady pochodzą z różnych dni sprawdzenia i nie są reprezentatywną próbą rynku. Przeglądarka przenosi ofertę po zapisanym terminie do archiwum według daty urządzenia; ewentualne przedłużenie wymaga kontroli źródła. Stare ogłoszenia zachowują poprzednią datę sprawdzenia.

---

# Wyszukiwanie ofert pracy — 29.10.2026

Każda rodzina zawodów ma przykładowe linki do wyszukiwania praktyk i pierwszej pracy we Wrocławiu na Pracuj.pl i Indeed. Otwierają zewnętrzne serwisy dopiero po kliknięciu; aplikacja sama nie pobiera ofert. Wyniki wymagają sprawdzenia daty, poziomu doświadczenia i dopasowania, a niektóre serwisy mogą ograniczyć dostęp. W sesji bezpośredni odczyt Pracuj.pl zwrócił 403; nie jest to dowód działania linków u każdej osoby. Wyszukiwarka internetowa znalazła publiczne strony wyników tych portali. Zapisana próbka ogłoszeń z 24.10 pozostaje historyczną próbką, nie jest nowym przeglądem rynku.

---

# Programy, specjalności i zakładki —28.10.2026

Domknięto naprawę importu przedmiotów i kontrolę zakładek. Zakres:109 ofert dwóch uczelni.107 ofert ma spis:24 pełne plany i83 listy częściowe (często szerokie, ale bez potwierdzenia kompletności).50 ofert ma potwierdzone specjalności/ścieżki/moduły. Liczby te nie są deklaracją kompletności wszystkich planów na nabór2027/28.

- Uniwersytet Wrocławski:87/89 ofert ze spisem,4 pełne plany,30 ofert z nazwanymi wariantami.
- Uniwersytet Ekonomiczny we Wrocławiu:20/20 spisów z pełnego planu2026/27;20 ofert z wariantami.
- Dwie jawne luki: European Cultures (brak potwierdzonych tytułów zajęć) oraz Informatyka stosowana i systemy pomiarowe (dostępny wyłącznie zamknięty cykl2022–2026, wykluczony z bieżącego importu).

Naprawiono wybór kolumn i scalonych komórek, rotacje stron PDF, zawinięcia nazw, mylenie efektów uczenia z kursami i wiersze sum godzin. Dodatkowa niezależna recenzja wskazała dwa wpisy „Łącznie”; obydwa zweryfikowano w PDF i usunięto. Walidator i regresja zabezpieczają przed ich powrotem. Weryfikacja na całych trzech plikach: brak wskazanych nagłówków, efektów uczenia, powtórzonych źródeł i zastępczych znaków Unicode. Raporty szczegółowe:docs/research/curricula/uwr-a/AUDIT-2026-10-28.md oraz uwr-b/QA.md.

Karta ma sześć prawdziwych zakładek, jedną widoczną sekcję, wyszukiwanie przedmiotów, podział na semestry i warianty oraz oficjalne źródła z rocznikami. Techniczne uwagi o odczycie przeniesiono do rozwijanego zakresu/źródeł. Stan kalkulatora i wyszukiwania zachowuje się między zakładkami. Nawigacja klawiaturą działa; profil i notatki nie wymagały migracji.

Dowody:21/21 testów; validate:data poprawne dla wszystkich109 ofert i pakietu ELA; TypeScript oraz build produkcyjny poprawne. Przeglądarka:6 zakładek/1 widoczny panel, zachowanie rocznika kalkulatora i wyszukiwania, PL/EN, obie uczelnie, kontrola107/109+24+50 w źródłach, dwa jawne braki, turystyka58 nazw, informatyka17, dziennikarstwo114, mikrobiologia37, Management Accounting70.390px w obu motywach bez poziomego overflow; zero pageerror. Nie dodano API ani modeli do aplikacji. Vite nadal zgłasza informacyjne ostrzeżenie o wielkości pojedynczego bundla (około245KB gzip).

Pozostaje uzupełnianie/poświadczanie83 list częściowych i2 luk w miarę publikacji wiarygodnych źródeł; programów nie udajemy potwierdzonymi na2027/28. Publikacja prywatna online i dalszy rozwój analiz rynku pracy pozostają osobnymi etapami.

---

# Losy absolwentów — 25.10.2026

Dodano oficjalne dane ELA edycja11/2026: absolwenci2024, 70 osobnych kohort przypisanych do69 z109 ofert.40 ofert bez potwierdzonego dopasowania. Dane P1 odróżnione od wskaźników całego okresu;21braków wartości i44zera zachowane. Osobne warianty informatyki6/7sem. Panel na karcie i podsumowanie pokrycia w źródłach. Import ręczny z pliku publicznego, bez API w aplikacji. Metoda PDF linkowana przez ELA nadal opisuje edycję10/2025 — jawnie oznaczono.

Weryfikacja:19/19 testów; validate:data:70kohort/69ofert; produkcyjny build poprawny. Niezależny przegląd wszystkich70rekordów versus76wierszy wycinka bez rozbieżności. Przeglądarka: obie uczelnie, EN, dwa warianty informatyki, WWB0, historia sztuki znull, Chemistry bez dopasowania;390px bezoverflow, brak pageerror.

Kolejne zlecenie: oficjalne przedmioty/specjalności dla109ofert oraz prawdziwe zakładki karty.

---

# Szeroka karta kierunku i motywy —25.10.2026

Wybrany kierunek zajmuje szeroką część ekranu, a pozostałe108 ofert (przy pełnym katalogu) tworzą jedną kolumnę obok. Na desktopie lista ma własne przewijanie, szczegóły są pełną stroną dokumentu bez ciasnego wewnętrznego panelu. Na telefonie szczegóły przed listą. Nawigacja sekcji: rekrutacja, progi, zawód/perspektywy, notatki/źródła.

Adres `#kierunek/ID` otwiera kartę także po odświeżeniu i z bezpośredniego linku. Przycisk Wstecz przeglądarki przywraca poprzedni kierunek, przycisk powrotu odtwarza katalog i fokus. Tytuł karty przeglądarki zawiera nazwę kierunku.

Przełącznik motywu w nagłówku, zapis w osobnym kluczu localStorage `akcja-studia-theme`, domyślnie preferencja systemowa. Motyw nie zmienia zapisu profilu. Granatowe powierzchnie, jasny tekst i morski akcent obejmują formularze, historię, porównanie oraz panel doradczy.

Browser1600px: karta933px, lista290px, jedna kolumna i108 innych ofert. Browser390px: karta przed listą, brak poziomego overflow; także profil i źródła mieszczą się na ekranie. Potwierdzono zapis/odczyt obu motywów, odświeżenie adresu kierunku, Wstecz oraz fokus po powrocie. Kontrola kontrastu ujawniła i poprawiła stare kolory etykiet/sekcji doradczych i tła ekspertów.

---

# Zakres historii ograniczony na polecenie użytkownika —25.10.2026

Aktywna historia: nabory2024/25,2025/26,2026/27. Starsze progi przeniesiono do `docs/archive/progi-2022-2023.json`, poza bundlowany katalog. Nie są dalej wyszukiwane ani odświeżane. Konfiguracja, skrypt researchu, walidator, widok i prompt aktualizacji korzystają z tego zakresu. Starsze liczby w raportach poniżej są zapisem poprzednich etapów.

---

# Hierarchia źródeł i dwa nowe portale —25.10.2026

- Uczelnie.pl:4 wartości Uniwersytetu Wrocławskiego2025/26 zgodne z zapisanymi danymi; dodano odnośniki porównawcze bez powielania rekordów. Wartość180 dla ekonomii Uniwersytetu Ekonomicznego we Wrocławiu odrzucona wobec oficjalnych170. Nie zamieniono portalowego procentu skali na wynik matury.
- Opinieouczelniach.pl:9 podstron, bez nowych pewnych progów/programów do importu. Wpisy dokumentują wynik kontroli.
- Katalog109 ofert,391 rekordów progów i97 kalkulatorów bez zmian; rejestr ma191 źródeł.
- Trwała konfiguracja: `src/data/source-policy.json`, funkcje rankingu/wykluczeń `src/sources.ts`, widoczny panel hierarchii. Oficjalne uczelnie1 →otouczelnie.pl2 →inne portale3 →prasa4 →społeczność5.
-4 wykluczenia stron/hosta i1 odrzucona informacja o konkretnej ofercie/roku. Przyszłe sesje mają instrukcję w AGENTS.md; skrypt researchu korzysta z kontroli przed siecią i przed przekierowaniem. Nie dodano automatycznego pobierania w aplikacji.
-18/18 testów, build i walidacja wszystkich danych przechodzą. KontrolaPython potwierdza0 żądań dla blokowanego hosta i zatrzymanie przed pobraniem wykluczonego celu przekierowania. CLI zwracaPOMIŃ/kod1 dla wykluczonej witryny bez otwierania jej.
- Przeglądarka: kolejność źródeł,4 wykluczenia, odnośnik potwierdzający tę samą wartość, mobilnie390px bez poziomego przepełnienia.

Szczegóły: `docs/hierarchia-zrodel.md`, `docs/audyt-uczelnie-pl.md`, `docs/audyt-opinieouczelniach.md`.

---

# Etap rekrutacji po rozszerzeniu — 25.10.2026

- Widoczny katalog109 ofert obu uczelni. 97 kalkulatorów (77+20),12 opisanych procedur dokumentowych.
- Uchwała Uniwersytetu Ekonomicznego we Wrocławiu R.0000.26.2026 z25.06.2026 potwierdzona bezpośrednim odczytem26stron; reguły2027/28 mają biznes i zarządzanie, zachowano osobne2026/27. Oferta kierunków2027/28 nie została założona na podstawie samej uchwały.
- Historia391 rekordów:121 publikacje uczelni,269 portal/prasa,1 społecznościowy. 70 ofert pierwszej uczelni i20 drugiej ma co najmniej jeden rocznik. Braki i niepotwierdzone skale pozostają jawne.
- Dodatkowe etapy: Logopedia18/30, pedagogika3/6, indywidualne studia międzydziedzinowe (minimum240 matur i264 rozmowy), medyczna biotechnologia angielski PP75 lubPR30. Testy wartości granicznych.
- Osobny przegląd wykrył możliwość błędu przy imporcie wyniku rozmowy poza skalą. Panel obsługuje taki import komunikatem i umożliwia poprawę pola zamiast wywracać aplikację. Browser: import Logopedia31→ostrzeżenie, zmiana18→238pkt (220matur+18rozmowy),17→warunek niespełniony. Profil testowy nie został zapisany.
- Browser:97kalkulatorów sprawdzane walidatorem dla pełnych wyników; przełączanie zasad2027/28→2026/27, oficjalne pięć roczników filologii francuskiej, mobilnie390px bez overflow. 14 testów przechodzi; walidator wszystkich danych i wzorów przechodzi.
- Procedura i prompt rozszerzania katalogu: `docs/dodawanie-uczelni.md`. Interfejs importu pakietów uczelni jest propozycją dalszej funkcji; istniejący importJSON w aplikacji dotyczy profilu.

Szczegóły źródeł i luk: `docs/uzupelnienie-progow-2022.md`, `docs/uzupelnienie-regul-uwr.md`, `docs/weryfikacja-rekrutacji-uew-2027.md`.

---

Poniżej historia poprzednich przyrostów; wcześniejsze liczby nie opisują bieżącego zakresu.

# Aktualny stan — 25.10.2026

Bieżący zakres: wyłącznie UWr i UEW, studia stacjonarne I stopnia / jednolite we Wrocławiu, PL i EN. Starszy raport poniżej opisuje poprzedni przyrost i nie jest aktualnym zakresem.

## Integracja wykonana

- Runtime `src/catalogue.ts` korzysta z `uwr.json` i `uew.json`: 109 ofert, 2 uczelnie, 17 EN, 102 źródła, 116 rekordów progów.
- Podłączone `AdmissionPanel`, `ProfileExtras`, `CareerPanel`, `DecisionPanel`. 68 ofert ma kalkulator; 41 wymaga odczytu tekstowych reguł i warunków dodatkowych.
- Przeglądarka: liczba kart 109 / UWr89 / UEW20 / UWr EN12 / UEW EN5. Ekonomia UEW: R matematyka100, angielski80, biologia75 →255pkt; 6 progów i 3 horyzonty scenariuszy widoczne.
- Widoki mobilne 390×844: porównanie i szczegóły bez poziomego przepełnienia.
- Osobny przegląd integracji wykrył blokadę starych porównań (niewidoczne ID zajmowały limit). Dodano jawną sekcję usuwania pozycji spoza zakresu; notatki i oceny zachowane.
- Test regresyjny matury dwujęzycznej UWr: najpierw czerwony (zwracano wynik), po poprawce brak automatycznej sumy i jawne wyjaśnienie. 10/10 testów przechodzi. Walidacja obejmuje wszystkie rekordy obu uczelni, 48 reguł i 17 ofert pracy.

## Jawne granice materiału

Brak kompletu progów UWr; zewnętrzne wartości mają status i konflikty. UEW nie ma potwierdzonych zasad 2027/28 ani czasu studiów dla każdej oferty. Scenariusze AI są dla rodzin zawodów i nie stanowią indywidualnej ekspertyzy każdego kierunku. Nie zaimportowano kohort ELA. 17 ogłoszeń to datowana próbka, bez automatycznego odświeżania i bez trendu rynkowego. Aplikacja nie wywołuje zewnętrznych API ani modeli.

---

# Realizacja planu aplikacji

Plan: docs/plan-aplikacji.md. Start: 2026-10-24.

## Decyzje
- Pracujemy w wskazanym pustym katalogu, bez operacji Git. Dokument postępu zastępuje dziennik wymagający repozytorium.
- Pierwszy przyrost: lokalny katalog, rejestr źródeł i pokrycia, profil, porównanie i macierz decyzji. Zakres danych będzie jawny; brak dokumentów 2027/28 nie uprawnia do przenoszenia zasad ze starszych lat.
- Kontrakt danych: src/types.ts. Kalkulatory rekrutacyjne pozostają nieaktywne do zweryfikowania konkretnych wzorów.
- Projekt wizualny: atlas wyboru studiów. Granat #14364b, morski #167b85, tło #f3f6f8, biel #ffffff, bursztyn #a25d12. Systemowa typografia Segoe UI; duże tytuły i spokojne tabelaryczne metadane. Boczna nawigacja, główna lista, panel profilu; mobilnie pojedyncza kolumna. Bez zewnętrznych fontów i API.

## Zadania
- [x] Audyt źródeł i pierwsza partia: 17 ofert, 10 uczelni, 18 źródeł katalogowych + oficjalna tabela PWr.
- [x] Statyczna aplikacja React/TypeScript.
- [x] Logika profilu, import/eksport, ważone porównanie z brakami danych.
- [x] Weryfikacja danych, build, testy i rzeczywista przeglądarka.
- [x] Ocena pozostałego zakresu i instrukcja dalszych aktualizacji w README.md.

## Dowody i przegląd
- `npm test`: 5/5; logika była uruchomiona z niezaimplementowanymi funkcjami przed implementacją, następnie zielona. Test parsera na całych pięciu tabelach. Korekta założenia testowego: rzeczywista pusta komórka źródła jest poprawnym brakiem, nie błędem parsera.
- `npm run validate:data`: 981 komórek; 725 wartości, 239 braków, 17 nieuruchomionych; 87 poza Wrocławiem. Walidacja wszystkich rekordów i odwołań, nie wybranych wierszy.
- `npm run build`: TypeScript i produkcyjny Vite build przechodzą.
- Przeglądarka 1440×1000 oraz 390×844: wyszukiwanie, filtr EN, karta i 8 progów EN PWr, ulubione, limit 4 porównań, oceny częściowe, zerowe wagi, zapis/odczyt wartości 0, zły import zachowujący profil, eksport i ponowny poprawny import, reset. Bez poziomego overflow na telefonie.
- Osobny przegląd Sol wykrył zapis nadmiernie długich notatek odrzucanych przy odczycie. Test regresyjny najpierw czerwony, po walidacji zapisu i eksportu zielony. Browser: zapis odrzucony, poprzednia kopia identyczna. Dodano również limity pól.
- Poprawiono fokus szczegółów i powrót do przycisku: przed poprawką panel nie był aktywny i znajdował się poza viewportem; po poprawce fokus i powrót potwierdzone w przeglądarce mobilnej.
- Po końcowym przeładowaniu konsola bez błędów; lista żądań do zewnętrznych serwisów pusta.

## Wykorzystanie modeli
| Model | Zakres | Wynik kontroli |
|---|---|---|
| GPT-6 Luna | Pierwszy research i katalog, następnie uzupełnienie czterech uczelni | Wymagał poprawek źródeł ASP, roczników i terminologii zawodowej; poprawki sprawdzone przez prowadzącego |
| GPT-6.1 Sol | Interfejs w dwóch przypisanych plikach | Zintegrowany i sprawdzony w przeglądarce; poprawiony zapis i fokus |
| GPT-6.1 Sol, osobny kontekst | Jeden przegląd przyrostu | 1 istotny problem zapisu naprawiony; uwagi o pokryciu i fokusie także uwzględnione |
| Model prowadzący sesję | Kontrakt, logika, import tabel PWr, integracja, testy | Nie zakładamy nazwy modelu ani kosztu na podstawie zwrotu użytkownika „Astra” |

Nie ma dostępnego rozliczenia kosztów per delegacja; nie deklarujemy procentowych oszczędności. Żaden model nie jest wywoływany przez aplikację.

## Następne prace — pełny plan pozostaje otwarty
1. Pełny katalog i kompletne programy, roczniki, ścieżki językowe oraz aktualne oficjalne nazwy/rejestr uczelni; szczegółowe opisy czterech wpisów ASP.
2. Wersjonowane reguły rekrutacji i testy konkretnych kalkulatorów; profil uwzględniający również podstawowe wyniki, gdy wymagają ich wzory. Obecne pole przedmiotów jest wyłącznie orientacyjnym przecięciem list, nie oceną wymagań.
3. Pozostałe oficjalne i nieoficjalne progi od 2022, z weryfikacją tury, języka i wariantu. Archiwum PWr ma wszystkie wiersze, katalog tylko dwa powiązane kierunki.
4. Drogi do zawodów i uprawnień, dane ELA, datowane zestawienia staży/pracy, eksperci i scenariusze AI 5/10/15. W bieżącym pakiecie nie ma takich ocen.
5. Strukturalny profil preferencji/warunków, oceny dla konkretnych ścieżek i automatyczna analiza wrażliwości. Obecnie preferencje/ścieżki są notatkami, oceny ręczne, zmianę wag użytkownik sprawdza sam.
6. Pełny odbiór produktu i ewentualna publikacja po wyborze hostingu.
