# Audyt Opinieouczelniach.pl

**Kontrola:** 2026-10-25  
**Zakres:** Uniwersytet Wrocławski oraz Uniwersytet Ekonomiczny we Wrocławiu; stacjonarne studia I stopnia i jednolite magisterskie we Wrocławiu, polskie i angielskie.  
**Rekord źródeł i kandydatów:** [opinie-research.json](../src/data/opinie-research.json)

## Metoda i hierarchia

Najpierw należy stosować aktualne źródła oficjalne uczelni. Opinieouczelniach.pl służy tu jako źródło wtórne i kontrolne. Jego liczby, opisy i katalogi nie zastępują zasad opublikowanych przez uczelnie. Dla formalnych reguł zachowano URL portalu, ale nie przepisano reguł ogólnych portalu jako reguł uczelni. Nie wykorzystano komentarzy ani opinii studentów jako informacji oficjalnych.

Odczytano dziewięć trafnych podstron portalu: karty obu uczelni, podstrony kierunków, rekrutacji i progów obu uczelni oraz kartę Analityki gospodarczej. Nie crawlowano całego portalu.

## Uniwersytet Wrocławski

- [Karta uczelni](https://opinieouczelniach.pl/uczelnia/uniwersytet-wroclawski/) podaje ogólne informacje i prowadzi do oficjalnej rekrutacji. Nie wnosi formalnych zasad.
- [Lista kierunków](https://opinieouczelniach.pl/uczelnia/uniwersytet-wroclawski/kierunki-studiow/) jest opisana jako oferta 2026/2027. To katalog portalu; sama lista nie potwierdza dla każdej pozycji poziomu, trybu, języka ani uruchomienia w naborze 2027/2028. Nie użyto jej do dodawania programów.
- [Rekrutacja](https://opinieouczelniach.pl/uczelnia/uniwersytet-wroclawski/rekrutacja/) jest opisana jako 2027/2028, lecz treść dotyczy ogólnych kroków naboru i linkuje do oficjalnej strony. Nie podaje konkretnych kierunkowych zasad.
- [Progi punktowe](https://opinieouczelniach.pl/uczelnia/uniwersytet-wroclawski/progi-punktowe/) stwierdzają, że uczelnia nie publikuje statystyk punktowych z poprzednich lat, z wyjątkiem wybranych kierunków na Wydziale Matematyki i Informatyki oraz Wydziale Fizyki i Astronomii. Na tej stronie nie ma konkretnych progów 2022+. Wzmianka o wyjątku nie uzasadnia uogólnień ani dodawania wartości bez odczytu właściwej karty kierunku.

## Uniwersytet Ekonomiczny we Wrocławiu

- [Karta uczelni](https://opinieouczelniach.pl/uczelnia/uniwersytet-ekonomiczny-we-wroclawiu/) oraz [rekrutacja](https://opinieouczelniach.pl/uczelnia/uniwersytet-ekonomiczny-we-wroclawiu/rekrutacja/) zawierają ogólny opis naboru i odsyłają do oficjalnej rekrutacji. Podane na karcie ramy terminów są ogólnikowe; nie zastępują opublikowanego harmonogramu uczelni.
- [Lista kierunków](https://opinieouczelniach.pl/uczelnia/uniwersytet-ekonomiczny-we-wroclawiu/kierunki-studiow/) deklaruje 2027/2028, ale nie jest potwierdzeniem uruchomionych ofert, trybu, poziomu i języka każdej pozycji. Nie dodano z niej `programmeCandidates`.
- [Progi punktowe](https://opinieouczelniach.pl/uczelnia/uniwersytet-ekonomiczny-we-wroclawiu/progi-punktowe/) przedstawiają dla stacjonarnych studiów I stopnia wartości w latach 2026/2027, 2025/2026, 2023/2024 i 2022/2023; dla 2024/2025 nagłówek mówi o studiach I stopnia bez jawnego określenia trybu. Liczby z zakresu obecnej oferty stacjonarnej I stopnia są już obecne w `uew.json`, dlatego nie ma kandydatów do dopisania. Portal dla 2026/2027 podaje pojedynczą wartość na kierunek, a dane oficjalne rozróżniają pierwsze i drugie ustalenie; ta pojedyncza liczba nie powinna nadpisywać oficjalnej historii.
- Historyczne wpisy takie jak „Ekonomia biznesu i finanse”, „Zarządzanie w nowoczesnej gospodarce” i zapis „Rachunkowość i controling” nie zostały dopasowane do aktualnych rekordów bez potwierdzenia równoważności programu, poziomu i trybu. Nie kwalifikują się jako pewne kandydatury dla aktualnego zakresu.
- Odczytana [karta Analityki gospodarczej we Wrocławiu](https://opinieouczelniach.pl/kierunki-studiow/analityka-gospodarcza/wroclaw/) mówi, że studia występują na pierwszym i drugim stopniu, wymienia moduły i przykładowe przedmioty. Nie określa czasu trwania ani nie rozróżnia jednoznacznie naboru, trybu i wersji programu. Nie uzupełnia `duration: null` w danych Uniwersytetu Ekonomicznego we Wrocławiu.

## Wykluczona podstrona kalendarza

Podstrona [kalendarza akademickiego Uniwersytetu Ekonomicznego we Wrocławiu](https://opinieouczelniach.pl/uczelnia/uniwersytet-ekonomiczny-we-wroclawiu/kalendarz-akademicki/) została wykluczona dla bieżącego zakresu: nagłówek wskazuje 2026/2027, a podane faktyczne terminy dotyczą 2025/2026. Sprzeczność była już potwierdzona w wyszukiwaniu bieżącej sesji; nie odczytywano tej podstrony ponownie. Nie rozszerzamy tego zastrzeżenia na pozostałe strony portalu.

## Wniosek

Wynik bieżącego audytu portalu to brak nowych, pewnych `thresholdCandidates` i `programmeCandidates`. Przedstawione progi są już pokryte w istniejących danych albo dotyczą nazw/trybów, których nie można bezpiecznie utożsamić z aktualną ofertą. Portal nie dostarczył w odczytanych kartach czasu trwania dla Uniwersytetu Ekonomicznego we Wrocławiu ani formalnych reguł 2027/2028, które mogłyby zastąpić uchwały i strony uczelni.