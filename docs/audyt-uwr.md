# Audyt UWr — 2026-10-24

Odczytano kompletny oficjalny filtr: 89/89 kart (77 PL, 12 EN), wszystkie stacjonarne we Wrocławiu. Każdy rekord ma własny skrót opisu, metadane, źródło i przykładowe możliwości zawodowe. Wszystkie 12 EN mają I stopień licencjacki; nie importowano II stopnia. 7 kart to jednoznaczne jednolite magisterskie. MSI jest jedną oficjalną kartą łączącą I stopień i jednolite; oznaczono to w uwadze. To kompletność katalogu strony, nie zapewnienie uruchomienia.

## Roczniki i metoda

Lista: https://rekrutacja.uwr.edu.pl/lista-kierunkow?poziom=i-stopnia-inzynierskie&poziom=i-stopnia-licencjackie&poziom=jednolite-magisterskie&poziom=i-stopnia-jednolite-magisterskie&forma=stacjonarne

Pobrano całą odpowiedź listy i wszystkie 89 kart za pomocą requests/BeautifulSoup, bez nowych zależności aplikacji. Select rocznika: 2=2026/2027 letnia, 6=2027/2028 letnia. Karty odczytano z obu adresów ?rok=2 i ?rok=6. HTML zawiera równocześnie ukryte roczniki: wybrano wyłącznie `[data-block-id="KryteriaRek"] [data-program-year="6"]`. 88 kart ma treść 2027/28. Ochrona środowiska ma pusty kontener 2027/28: jej zasady są jawnie 2026/27. Limitów „w przygotowaniu” nie uznano za ustalone.

https://rekrutacja.uwr.edu.pl/strona/20 opisuje wciąż uchwałę 84/2025 dla 2026/27. Źródłem reguł 2027/28 jest jawnie oznaczona sekcja na oficjalnych kartach, nie domniemanie z daty. Terminów i opłat 2027 nie deklarujemy bez odrębnego odczytu harmonogramów. Oferta katalogu i opublikowanie reguły nie stanowią zapewnienia otwarcia zapisów w IRK dla 2027.

## Kalkulator

48 reguł w `src/data/uwr-rules.json`: rok, URL, data, opcje przedmiot-poziom-współczynnik. Wynik = suma maksimum po opcjach każdej grupy. PP/PR wybiera się po przeliczeniu. `optional:true`: przedmiot niezdawany daje 0 i dopuszcza udział. Brak wyniku wymaganej grupy oznacza niepełne dane. Nieznany wynik różni się od świadomie niezdawanego. `excludeSubjectsFromGroups` wymusza inny przedmiot; potrzebny globalny wybór najlepszej kombinacji. Dwa przedmioty = dwie grupy z wykluczeniem powtórzenia. Matematyka może wystąpić ponownie tam, gdzie tabela tego nie wyklucza, np. Informatyka.

Reguły obejmują polską nową maturę pisemną PP/PR. `bilingual=0` oznacza brak obsługi tego poziomu. Matura dwujęzyczna ma odrębny przelicznik 4/3 i zaokrąglenie procentu; nie obsługiwać jej automatycznie bez odrębnej reguły i interpretacji limitu procentu. IB, EB, stara matura, olimpiady, świadectwa zagraniczne mają osobne ścieżki, poza kalkulatorem. Lista języków obsługiwanych w profilu nie ogranicza formalnie dozwolonych matur językowych.

Kluczowe reguły 2027/28 (adresy i transkrypcje niżej):

- Psychologia: max(polski PP×0,5; PR×1) + max(obcy PP×0,25; PR×0,5) + max(PR biologia/chemia/fizyka/geografia/historia/historia sztuki/informatyka/WOS×1; matematyka PP×0,5; PR×1). Polski i obcy obowiązkowe, trzecia grupa opcjonalna. Maksimum 250.
- Ekonomia i Prawo: grupa 1 max(matematyka PP×0,5; PR×1; historia PR×1). Grupa 2 INNY przedmiot: max(geografia/historia/WOS PR×0,5; polski/matematyka PP×0,25; PR×0,5). Grupa 3 max(obcy PP×0,2; PR×0,4). Grupa 1 wymagana, pozostałe opcjonalne. Maksimum 190. Ekonomia 2026 nie punktowała polskiego PP w tej samej postaci: nie przenosimy reguły między latami.
- Informatyka: 3×matematyka PR + 3×max(fizyka PR, informatyka PR, matematyka PR) + max(obcy PP×0,25; PR×0,5). Matematyka PR wymagana; minimum formalne 250 punktów, maksimum 650. Zmiana względem 2026; historia bez historycznej reguły jest nieporównywalna.
- ISIM: 4×matematyka PR + 3×max(fizyka PR, informatyka PR, matematyka PR) + max(obcy PP×0,25; PR×0,5); minimum 400.
- Matematyka i AI w analizie danych: 2×matematyka PR + max(fizyka PR, informatyka PR, matematyka PR) + max(obcy PP×0,1; PR×0,2). Matematyka PR minimum 30%.
- Fizyka i Astronomia: matematyka PP + max(fizyka PR, matematyka PR) + 0,5×max(biologia PR, chemia PR, fizyka PR, geografia PR, informatyka PR, matematyka PR); minimum 100 punktów.
- ISSP: matematyka PP + 1,5×max(fizyka PR, informatyka PR, matematyka PR); minimum 100.

## Historyczne progi 2022+

Nie znaleziono oficjalnej pełnej tabeli. Archiwalne https://study.uni.wroc.pl/vademecum/ mówi o niepublikowaniu statystyk, ale ma daty 2018; nie użyto go do obecnej punktacji. Nowszy indeks https://test.rekrutacja.uni.wroc.pl/vademecum-kandydata/ potwierdza politykę i wyjątki kierunków ścisłych. Requests odrzucił certyfikat hostname mismatch, narzędzie web odczytało indeksowany tekst. Nie wyłączano TLS.

Otouczelnie: pełna tabela zawiera 193 wpisy „zapytaj uczelnię”. Są przełączniki 2022/23–2025/26, ale pobrany wariant nie daje użytecznych liczb. Nie wymyślano braków.

Dostanesie.pl podaje Psychologia: 2022=203, 2023=208, 2024=199,5, tura 1. Status reported, bez oficjalnego pochodzenia, z błędnym polem stopnia. Rektorat.pl (30.09.2025) podaje 2022=190, 2023=195 bez tury: zachowano obie sprzeczne serie bez uśredniania. Podaje też Anglistyka 2023=171,4 bez tury. Informatyka 115 NIE importowana jako historyczny próg, bo może być minimum formalnym. Publiczny wpis Forum.Studia.net z 24.02.2023: prawo 2022/23=127/190, bez tury; status anecdote jako niepotwierdzone zestawienie użytkownika, nie dowód osobistego przyjęcia.

Maturalnie.pl: snippet pokazał 62/65/67 na skali 100, ale bezpośredni odczyt mówi o braku danych. Snippet odrzucono. Odrzucono również strony z rokiem „2026/2026” i nieznanymi skalami. Brak pełnej historii 2022–2026 dla pozostałych ofert jest jawnym brakiem. Minimum formalne nie zastępuje wyniku ostatniej przyjętej osoby. Wszystkie zapisane serie nie mają potwierdzonej historycznej reguły porównywalnej z 2027/28.

## Granice opracowania

Nie dopisywano specjalności jako odrębnych kierunków ani nazw nieobecnych w oficjalnym filtrze. Przykładowe kariery są możliwościami wynikającymi z obszaru kształcenia; nie są zapewnieniem kwalifikacji ani analizą rynku. Szczegóły zawodów regulowanych wymagają odrębnej weryfikacji. Opisy to własne krótkie streszczenia wprowadzeń uczelni, nie pełny audyt sylabusów. SubjectsVerified oznacza odczyt tabeli; lista przedmiotów nie zastępuje warunków grup.

## Karty bez aktywnego kalkulatora

41 kart: specjalne warunki, dowolny inny przedmiot, przypisy lub zagraniczna ścieżka językowa. Pełne warunki zapisano w rekordach albo są wskazane w źródle:

- Anglistyka
- Bachelor of Business and Administration
- Biotechnology
- Chemistry
- Criminal Justice
- Culture, Thought and Humanity
- Data and Society
- Edukacja polonistyczna
- English for Knowledge, Culture and Innovation
- Etyka
- European Cultures
- Filologia francuska
- Filologia germańska
- Filologia hiszpańska
- Filologia indyjska
- Filologia polska
- Filozofia
- Genetics and Experimental Biology
- Historia sztuki
- Indywidualne studia międzydziedzinowe
- Informacja naukowa i bibliotekoznawstwo
- Italianistyka
- Judaistyka
- Koreanistyka
- Kultura i praktyka tekstu: twórcze pisanie i edytorstwo
- Literatura światowa: komparatystyka i wielokulturowość
- LL.B. International and European Environmental Law
- Logopedia
- Medyczna biotechnologia molekularna
- Muzykologia
- Niderlandystyka
- Ochrona środowiska
- Pedagogika
- Pedagogika przedszkolna i wczesnoszkolna
- Pedagogika specjalna
- Political Science
- Publikowanie cyfrowe i sieciowe
- Sinologia
- Stosunki międzynarodowe, specjalność: Global Studies
- Techniki eksperymentalne w kryminalistyce
- Zielona chemia

## Transkrypcja źródeł poszczególnych kierunków

PP=podstawowy, PR=rozszerzony. Komplet wierszy pierwszej tabeli nowej matury wybranego rocznika. Etykieta wiersza określa wymagalność.

### Administracja — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/3?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / historia / - / 1,0; matematyka / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru, inny niż wybrany powyżej) / wiedza o społeczeństwie, geografia, historia / - / 0,5; język polski, matematyka / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-administracja-2027`.

### Analityka społeczna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/6?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / matematyka / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / geografia, historia, wiedza o społeczeństwie / - / 0,5; język polski / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-analityka-spoleczna-2027`.

### Anglistyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/9?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język angielski / - / 1,0; Przedmiot wymagany / język polski / - / 0,8; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Archeologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/12?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / geografia, historia, historia sztuki / - / 1,0; język angielski, język niemiecki / 0,5 / 1,0; Przedmiot dodatkowy (jeden do wyboru, inny niż wybrany powyżej) / biologia, chemia, filozofia, fizyka, geografia, historia, historia sztuki, informatyka, wiedza o społeczeństwie / - / 0,5; język obcy nowożytny, matematyka / 0,25 / 0,5

Reguła: `uwr-archeologia-2027`.

### Astronomia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/14?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / matematyka / 1,0 / -; Przedmiot do wyboru (jeden do wyboru) / fizyka, matematyka / - / 1,0; Przedmiot dodatkowy (jeden do wyboru) / biologia, chemia, fizyka, geografia, informatyka, matematyka / - / 0,5

Reguła: `uwr-astronomia-2027`.

### Bachelor of Business and Administration — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/16?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie świadectwa uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty) pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Bezpieczeństwo narodowe — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/19?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / geografia, historia, wiedza o społeczeństwie / - / 0,5; matematyka / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-bezpieczenstwo-narodowe-2027`.

### Biologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/23?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / biologia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / chemia, fizyka, geografia / - / 1,0; matematyka / 0,5 / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-biologia-2027`.

### Biologia człowieka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/21?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / biologia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / chemia, fizyka, geografia / - / 1,0; matematyka / 0,5 / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-biologia-czlowieka-2027`.

### Biotechnologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/26?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / chemia / - / 1,0; biologia / - / 0,85; Przedmiot do wyboru (jeden do wyboru, inny niż wybrany powyżej) / biologia, chemia, fizyka / - / 0,75; matematyka / 0,5 / 0,75; Przedmiot dodatkowy / język angielski / 0,1 / 0,25

Reguła: `uwr-biotechnologia-2027`.

### Biotechnology — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/27?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty); pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Chemia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/33?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot do wyboru (dwa do wyboru) / matematyka / 0,5 / 1,0; biologia, chemia, fizyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-chemia-2027`.

### Chemia medyczna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/32?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot do wyboru (dwa do wyboru) / matematyka / 0,5 / 1,0; biologia, chemia, fizyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-chemia-medyczna-2027`.

### Chemistry — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/35?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty); pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Criminal Justice — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/38?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty); pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Culture, Thought and Humanity — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/40?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty); pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Data and Society — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/41?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie świadectwa uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty) pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Dyplomacja europejska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/43?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / język obcy nowożytny, język polski, matematyka / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru, inny niż wybrany powyżej) / filozofia, fizyka, geografia, historia, historia muzyki, historia sztuki, język łaciński i kultura antyczna, wiedza o społeczeństwie / - / 1,0; język obcy nowożytny , język polski, matematyka / 0,5 / 1,0; Przedmiot dodatkowy (jeden do wyboru, inny niż wybrany powyżej) / filozofia, fizyka, geografia, historia, historia muzyki, historia sztuki, język łaciński i kultura antyczna, wiedza o społeczeństwie / - / 1,0; język obcy nowożytny, język polski, matematyka / 0,5 / 1,0

Reguła: `uwr-dyplomacja-europejska-2027`.

### Dziedzictwo kultury materialnej - ochrona, promocja, gospodarowanie — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/44?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / historia / - / 1,0; język obcy nowożytny / 0,5 / 1,0

Reguła: `uwr-dziedzictwo-kultury-materialnej-ochrona-promocja-gospodarowanie-2027`.

### Dziennikarstwo i komunikacja społeczna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/47?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / biologia, chemia, filozofia, fizyka, geografia, historia, historia sztuki, wiedza o społeczeństwie / - / 1,0; matematyka / 0,5 / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,5 / 1,0

Reguła: `uwr-dziennikarstwo-i-komunikacja-spoleczna-2027`.

### Edukacja polonistyczna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/49?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / język obcy nowożytny / 0,5 / 1,0; Przedmiot dodatkowy / przedmiot inny niż wybrany powyżej / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wybrany powyżej

### Ekonomia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/52?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / matematyka / 0,5 / 1,0; historia / - / 1,0; Przedmiot do wyboru (jeden do wyboru, inny niż wybrany powyżej) / geografia, historia, wiedza o społeczeństwie / - / 0,5; język polski, matematyka / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-ekonomia-2027`.

### English for Knowledge, Culture and Innovation — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/54?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty, z zastrzeżeniem, że wynik University of Cambridge, ESOL Examinations, British Council, IDP IELTS Australia: International English Language Testing System IELTS – wynosi co najmniej 5,5 pkt z każdej umiejętności; pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą);

Bez kalkulatora: brak prostej tabeli nowej matury

### Etnologia i antropologia kulturowa — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/56?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot do wyboru (jeden do wyboru) / język polski / 0,25 / 0,5; filozofia, geografia, historia, historia sztuki, wiedza o społeczeństwie / - / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-etnologia-i-antropologia-kulturowa-2027`.

### Etyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/59?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / 0,25 / 0,5; Przedmiot dodatkowy / filozofia / - / 2,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### European Cultures — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/61?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty); pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Europeistyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/62?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / język obcy nowożytny, język polski, matematyka / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru, inny niż wybrany powyżej) / filozofia, fizyka, geografia, historia, historia muzyki, historia sztuki, język łaciński i kultura antyczna, wiedza o społeczeństwie / - / 1,0; język obcy nowożytny , język polski, matematyka / 0,5 / 1,0; Przedmiot dodatkowy (jeden do wyboru, inny niż wybrany powyżej) / filozofia, fizyka, geografia, historia, historia muzyki, historia sztuki, język łaciński i kultura antyczna, wiedza o społeczeństwie / - / 1,0; język obcy nowożytny, język polski, matematyka / 0,5 / 1,0

Reguła: `uwr-europeistyka-2027`.

### Filologia chorwacka z językiem serbskim — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/63?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język obcy nowożytny / 0,5 / 1,0; Przedmiot do wyboru / język polski / 0,5 / 1,0

Reguła: `uwr-filologia-chorwacka-z-jezykiem-serbskim-2027`.

### Filologia czeska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/64?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język obcy nowożytny / 0,5 / 1,0; Przedmiot do wyboru / język polski / 0,5 / 1,0

Reguła: `uwr-filologia-czeska-2027`.

### Filologia francuska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/65?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język francuski / 0,5 / 1,0; lub język obcy inny niż język francuski / 0,4 / 0,8; Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / przedmiot inny niż wybrany powyżej (w tym drugi język obcy) / 0,25 / 0,5

Bez kalkulatora: lub język obcy inny niż język francuski

### Filologia germańska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/68?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,25 / 0,5; Przedmiot do wyboru (jeden do wyboru) / język niemiecki / 0,5 / 1,0; język obcy nowożytny inny niż język niemiecki / 0,4 / 0,8

Bez kalkulatora: język angielski, język niemiecki, język francuski, język hiszpański, język rosyjski, język włoski, język portugalski inny niż język niemiecki

### Filologia hiszpańska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/70?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język hiszpański / 0,5 / 1,0; lub język obcy inny niż język hiszpański / 0,4 / 0,8; Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / przedmiot inny niż wybrany powyżej (w tym drugi język obcy) / 0,25 / 0,5

Bez kalkulatora: lub język obcy inny niż język hiszpański

### Filologia indyjska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/71?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / język angielski / 0,5 / 1,0; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / 0,2 / 0,6; Przedmiot dodatkowy (jeden do wyboru) / filozofia, historia, język łaciński i kultura antyczna / - / 0,8

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Filologia klasyczna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/72?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / język obcy nowożytny / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / filozofia, historia, język łaciński i kultura antyczna / - / 0,8

Reguła: `uwr-filologia-klasyczna-2027`.

### Filologia polska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/75?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / język obcy nowożytny / 0,5 / 1,0; Przedmiot dodatkowy / przedmiot inny niż wymienione w tabeli / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Filologia rosyjska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/77?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język obcy nowożytny / 0,5 / 1,0; Przedmiot do wyboru / język polski / 0,5 / 1,0

Reguła: `uwr-filologia-rosyjska-2027`.

### Filologia ukraińska — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/78?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język obcy nowożytny / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / język polski, język ukraiński / 0,5 / 1,0

Reguła: `uwr-filologia-ukrainska-2027`.

### Filozofia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/81?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / 0,25 / 0,5; Przedmiot dodatkowy / filozofia / - / 2,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Fizyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/84?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / matematyka / 1,0 / -; Przedmiot do wyboru (jeden do wyboru) / fizyka, matematyka / - / 1,0; Przedmiot dodatkowy (jeden do wyboru) / biologia, chemia, fizyka, geografia, informatyka, matematyka / - / 0,5

Reguła: `uwr-fizyka-2027`.

### Genetics and Experimental Biology — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/212?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie świadectwa uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty) pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Genetyka i biologia eksperymentalna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/87?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / biologia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / matematyka / 0,5 / 1,0; chemia, fizyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-genetyka-i-biologia-eksperymentalna-2027`.

### Geografia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/89?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / geografia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / język polski, matematyka / 0,5 / 1,0; Przedmiot dodatkowy (jeden do wyboru) / biologia, chemia, fizyka, historia, informatyka, wiedza o społeczeństwie / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-geografia-2027`.

### Geoinformacja — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/313?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / geografia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / język polski , matematyka / 0,5 / 1,0; informatyka / - / 1,0; Przedmiot dodatkowy (jeden do wyboru) / biologia, fizyka, historia, wiedza o społeczeństwie / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-geoinformacja-2027`.

### Geologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/92?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / geografia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / matematyka / 0,5 / 1,0; biologia, chemia, fizyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-geologia-2027`.

### Gospodarka przestrzenna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/97?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot do wyboru (jeden do wyboru) / biologia, chemia, fizyka, geografia, historia, informatyka, wiedza o społeczeństwie / - / 1,0; Przedmiot dodatkowy (jeden do wyboru) / język polski, matematyka / 0,5 / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-gospodarka-przestrzenna-2027`.

### Historia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/100?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / historia / - / 1,0; język obcy nowożytny / 0,5 / 1,0

Reguła: `uwr-historia-2027`.

### Historia sztuki — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/103?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; język obcy nowożytny / 0,5 / 1,0; Przedmiot wymagany / przedmiot inny niż wymienione w tabeli / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Indywidualne studia informatyczno-matematyczne — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/105?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / matematyka / - / 4,0; Przedmiot do wyboru (jeden do wyboru) / fizyka, informatyka, matematyka / - / 3,0; Przedmiot dodatkowy / język obcy nowożytny / 0,25 / 0,5

Reguła: `uwr-indywidualne-studia-informatyczno-matematyczne-2027`.

### Indywidualne studia międzydziedzinowe — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/107?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,6 / 1,0; Przedmiot wymagany / matematyka / 0,6 / 1,0; Przedmiot wymagany / język obcy nowożytny / 0,6 / 1,0; Przedmiot do wyboru (jeden do wyboru) / biologia, chemia, filozofia, fizyka, geografia, historia, historia sztuki, historia muzyki, informatyka, język łaciński i kultura antyczna, język grecki i kultura antyczna, język obcy nowożytny (inny niż wybrany powyżej), wiedza o społeczeństwie / - / 1,0

Bez kalkulatora: dodatkowy warunek/egzamin lub przypis

### Informacja naukowa i bibliotekoznawstwo — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/109?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / język obcy nowożytny / 0,5 / 1,0; Przedmiot dodatkowy (jeden do wyboru) / przedmiot inny niż wybrany powyżej (w tym drugi język obcy nowożytny) / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wybrany powyżej (w tym drugi język angielski, język niemiecki, język francuski, język hiszpański, język rosyjski, język włoski, język portugalski)

### Informatyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/111?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / matematyka / - / 3,0; Przedmiot do wyboru (jeden do wyboru) / fizyka, informatyka, matematyka / - / 3,0; Przedmiot dodatkowy / język obcy nowożytny / 0,25 / 0,5

Reguła: `uwr-informatyka-2027`.

### Informatyka stosowana i systemy pomiarowe — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/112?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / matematyka / 1,0 / -; Przedmiot do wyboru (jeden do wyboru) / fizyka, informatyka, matematyka / - / 1,5

Reguła: `uwr-informatyka-stosowana-i-systemy-pomiarowe-2027`.

### Inżynieria geologiczna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/115?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot do wyboru (jeden do wyboru) / matematyka / 0,5 / 1,0; fizyka / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / chemia, geografia / - / 0,8; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-inzynieria-geologiczna-2027`.

### Italianistyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/116?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / język włoski / 0,5 / 1,0; lub język obcy inny niż język włoski / 0,4 / 0,8; Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / przedmiot inny niż wybrany powyżej (w tym drugi język obcy) / 0,25 / 0,5

Bez kalkulatora: lub język obcy inny niż język włoski

### Judaistyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/117?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / język angielski / 0,2 / 1,0; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / - / 0,5

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Komunikacja wizerunkowa — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/121?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / biologia, chemia, filozofia, fizyka, geografia, historia, historia sztuki, wiedza o społeczeństwie / - / 1,0; matematyka / 0,5 / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,5 / 1,0

Reguła: `uwr-komunikacja-wizerunkowa-2027`.

### Koreanistyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/124?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / język angielski / 0,5 / 1,0; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / - / 0,6; Przedmiot dodatkowy / język łaciński i kultura antyczna / - / 0,8

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Kultura i praktyka tekstu: twórcze pisanie i edytorstwo — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/127?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / język obcy nowożytny / 0,5 / 1,0; Przedmiot dodatkowy / przedmiot inny niż wymienione w tabeli / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Kulturoznawstwo — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/129?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / język obcy nowożytny / 0,5 / 1,0; Przedmiot dodatkowy (jeden do wyboru) / filozofia, geografia, historia, historia muzyki, historia sztuki, język łaciński i kultura antyczna, wiedza o społeczeństwie, wiedza o tańcu / - / 0,5

Reguła: `uwr-kulturoznawstwo-2027`.

### Literatura światowa: komparatystyka i wielokulturowość — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/130?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / - / 1,0; Przedmiot wymagany / język obcy nowożytny / 0,4 / 1,0; Przedmiot do wyboru (jeden do wyboru) / filozofia, geografia, historia, historia sztuki, język łaciński i kultura antyczna, drugi język obcy nowożytny (inny niż wybrany powyżej), wiedza o społeczeństwie / - / 0,5

Bez kalkulatora: filozofia, geografia, historia, historia sztuki, język łaciński i kultura antyczna, drugi język angielski, język niemiecki, język francuski, język hiszpański, język rosyjski, język włoski, język portugalski (inny niż wybrany powyżej), wiedza o społeczeństwie

### LL.B. International and European Environmental Law — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/131?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty); pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Logopedia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/133?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru / język obcy nowożytny / 0,5 / 1,0; Przedmiot dodatkowy (jeden do wyboru) / biologia, drugi język nowożytny (inny niż wybrany powyżej) / - / 0,75; matematyka / 0,25 / 0,5; chemia, fizyka, geografia, historia, informatyka, wiedza o społeczeństwie / - / 0,5

Bez kalkulatora: dodatkowy warunek/egzamin lub przypis

### Matematyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/136?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / matematyka / - / 2,0; Przedmiot do wyboru (jeden do wyboru) / fizyka, informatyka, matematyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,1 / 0,2

Reguła: `uwr-matematyka-2027`.

### Medyczna biotechnologia molekularna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/140?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / chemia / - / 1,0; Przedmiot wymagany / biologia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / matematyka / 0,4 / 1,0; fizyka / - / 1,0; Przedmiot dodatkowy / język angielski * / 0,1 / 0,25

Bez kalkulatora: dodatkowy warunek/egzamin lub przypis

### Mikrobiologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/142?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / biologia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / matematyka / 0,5 / 1,0; chemia, fizyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-mikrobiologia-2027`.

### Muzykologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/144?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; język obcy nowożytny / 0,5 / 1,0; Przedmiot wymagany / przedmiot inny niż wymienione w tabeli / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Niderlandystyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/146?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; język obcy nowożytny / 0,5 / 1,0; Przedmiot do wyboru / przedmiot inny niż wybrany powyżej (w tym drugi język obcy nowożytny) / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wybrany powyżej (w tym drugi język angielski, język niemiecki, język francuski, język hiszpański, język rosyjski, język włoski, język portugalski)

### Ochrona środowiska — 2026/2027

https://rekrutacja.uwr.edu.pl/kierunek/148?rok=2&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / biologia, geografia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / geografia (jeśli w przedmiocie 1 została wybrana biologia), biologia (jeśli w przedmiocie 1 została wybrana geografia), chemia, fizyka / - / 1,0; matematyka / 0,5 / 1,0; Przedmiot dodatkowy (jeden do wyboru) / informatyka / - / 0,4; język polski (pisemny), język obcy nowożytny (pisemny) / 0,2 / 1,0

Bez kalkulatora: geografia (jeśli w przedmiocie 1 została wybrana biologia), biologia (jeśli w przedmiocie 1 została wybrana geografia), chemia, fizyka

### Pedagogika — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/152?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; język obcy nowożytny / 0,2 / 0,4; Przedmiot do wyboru / przedmiot inny niż wybrane / 0,5 / 1,0

Bez kalkulatora: przedmiot inny niż wybrane

### Pedagogika przedszkolna i wczesnoszkolna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/154?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / matematyka / 0,5 / 1,0; Przedmiot wymagany / język obcy nowożytny / 0,2 / 0,4; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / 0,5 / 1,0

Bez kalkulatora: dodatkowy warunek/egzamin lub przypis

### Pedagogika specjalna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/156?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; język obcy nowożytny / 0,2 / 0,4; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / 0,5 / 1,0

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Political Science — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/158?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty); pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Politologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/160?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / język polski / 0,5 / 1,0; historia, wiedza o społeczeństwie / - / 1,0; Przedmiot dodatkowy (jeden do wyboru, inny niż wybrany powyżej) / język polski, matematyka / 0,25 / 0,5; geografia, historia, wiedza o społeczeństwie / - / 0,5; Przedmiot do wyboru / język obcy nowożytny / 0,25 / 0,5

Reguła: `uwr-politologia-2027`.

### Praca socjalna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/161?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / geografia, historia, wiedza o społeczeństwie / - / 0,5; matematyka / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-praca-socjalna-2027`.

### Prawo — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/163?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / matematyka / 0,5 / 1,0; historia / - / 1,0; Przedmiot do wyboru (jeden do wyboru, inny niż wybrany powyżej) / geografia, historia, wiedza o społeczeństwie / - / 0,5; język polski, matematyka / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-prawo-2027`.

### Psychologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/168?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / język obcy nowożytny / 0,25 / 0,5; Przedmiot do wyboru (jeden do wyboru) / biologia, chemia, fizyka geografia, historia, historia sztuki, informatyka, wiedza o społeczeństwie / - / 1,0; matematyka / 0,5 / 1,0

Reguła: `uwr-psychologia-2027`.

### Publikowanie cyfrowe i sieciowe — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/171?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / język obcy nowożytny, matematyka / 0,5 / 1,0; historia sztuki, informatyka / - / 1,0; Przedmiot dodatkowy / przedmiot inny niż wymienione w tabeli / 0,25 / 0,5

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Sinologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/173?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / język angielski / 0,5 / 1,0; Przedmiot do wyboru / przedmiot inny niż wymienione w tabeli / - / 0,6; Przedmiot dodatkowy / język łaciński i kultura antyczna / - / 0,8

Bez kalkulatora: przedmiot inny niż wymienione w tabeli

### Socjologia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/178?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / geografia, historia, wiedza o społeczeństwie / - / 0,5; matematyka / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-socjologia-2027`.

### Socjologia ekonomiczna — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/177?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / geografia, historia, wiedza o społeczeństwie / - / 0,5; matematyka / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-socjologia-ekonomiczna-2027`.

### Stosunki miedzynarodowe — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/182?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / historia, geografia, wiedza o społeczeństwie / - / 0,5; matematyka / 0,25 / 0,5; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-stosunki-miedzynarodowe-2027`.

### Stosunki międzynarodowe, specjalność: Global Studies — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/186?rok=6&tab=zasady-rekrutacji

Warunkiem przyjęcia na studia jest: posiadanie dokumentu uprawniającego do podjęcia studiów; przedstawienie dokumentu potwierdzającego znajomość języka angielskiego minimum na poziomie B2 w skali Rady Europy (szczegóły w zakładce dokumenty); pozytywna formalna ocena aplikacji przez koordynatora wydziałowego (dotyczy tylko świadectwa uzyskanego za granicą).

Bez kalkulatora: brak prostej tabeli nowej matury

### Studia śródziemnomorskie — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/191?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / język polski / 0,5 / 1,0; Przedmiot wymagany / język obcy nowożytny / 0,5 / 1,0; Przedmiot do wyboru (jeden do wyboru) / filozofia, historia, język łaciński i kultura antyczna / - / 0,8

Reguła: `uwr-studia-srodziemnomorskie-2027`.

### Sztuczna inteligencja w analizie danych — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/193?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / matematyka / - / 2,0; Przedmiot do wyboru (jeden do wyboru) / fizyka, informatyka, matematyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,1 / 0,2

Reguła: `uwr-sztuczna-inteligencja-w-analizie-danych-2027`.

### Techniki eksperymentalne w kryminalistyce — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/196?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / biologia*, chemia* / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / matematyka / 0,5 / 1,0; biologia*, chemia*, fizyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Bez kalkulatora: dodatkowy warunek/egzamin lub przypis

### Turystyka — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/198?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot do wyboru (dwa do wyboru) / biologia, chemia, fizyka, geografia, historia, wiedza o społeczeństwie / - / 1,0; Przedmiot dodatkowy / język polski / 0,5 / 1,0; Przedmiot dodatkowy / matematyka / 0,5 / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-turystyka-2027`.

### Zarządzanie projektami społecznymi — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/206?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany (jeden do wyboru) / język polski / 0,5 / 1,0; historia, wiedza o społeczeństwie / - / 1,0; Przedmiot dodatkowy (jeden do wyboru, inny niż wybrany powyżej) / język polski, matematyka / 0,25 / 0,5; historia, wiedza o społeczeństwie / - / 0,5; Przedmiot do wyboru / język obcy nowożytny / 0,25 / 0,5

Reguła: `uwr-zarzadzanie-projektami-spolecznymi-2027`.

### Zarządzanie środowiskiem przyrodniczym — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/209?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot wymagany / biologia / - / 1,0; Przedmiot do wyboru (jeden do wyboru) / chemia, geografia / - / 1,0; matematyka / 0,5 / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Reguła: `uwr-zarzadzanie-srodowiskiem-przyrodniczym-2027`.

### Zielona chemia — 2027/2028

https://rekrutacja.uwr.edu.pl/kierunek/210?rok=6&tab=zasady-rekrutacji

Tabela (etykieta / przedmiot / PP / PR): Przedmiot do wyboru (dwa do wyboru) / matematyka / 0,5 / 1,0; biologia, chemia, fizyka / - / 1,0; Przedmiot dodatkowy / język obcy nowożytny / 0,2 / 0,4

Bez kalkulatora: dodatkowy warunek/egzamin lub przypis

## Dodatkowe warunki, których nie upraszczono

- Logopedia: II etap: rozmowa dla maksymalnie70 najlepszych kandydatów z etapu matur. Ocenia komunikację, wymowę, głos, płynność, słuch i ewentualnie motorykę artykulacyjną; skala0–30, zaliczenie od18. Ranking sumuje oba etapy.
- Pedagogika przedszkolna i wczesnoszkolna: II etap: rozmowa o motywacji i edukacji dzieci; ocena komunikacji, artykulacji, wrażliwości muzycznej i myślenia twórczego. Skala1–6, zaliczenie od3; ranking sumuje oba etapy. Oficjalna karta zawiera zastrzeżenie wykluczające kandydatów z dysleksją — należy sprawdzić aktualne brzmienie i interpretację z uczelnią.
- Medyczna biotechnologia molekularna: Dodatkowy obowiązkowy warunek z przypisu: angielski pisemny PP minimum75% albo PR minimum30%, mimo etykiety „przedmiot dodatkowy” przy punktowaniu.
- Techniki eksperymentalne w kryminalistyce: Przypis: jeśli zdawano biologię i chemię, lepsza punktowo trafia do grupy wymaganej, druga może wejść do wyboru. Nie liczyć tego samego przedmiotu dwukrotnie.
- Indywidualne studia międzydziedzinowe: Dodatkowa rozmowa konsultacyjna wymaga oceny pozytywnej. Oceny rozmowy przeliczane są na punkty: bdb440, db+396, db352, dst+308, dst264, ndst0; ranking sumuje oba etapy.

Zielona chemia ma zagnieżdżoną strukturę HTML łączącą w jednym accordionie kilka typów matur. Nie aktywowano reguły mimo pozornie prostej pierwszej tabeli.
