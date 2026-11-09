# Audyt danych UEW

**Sprawdzenie źródeł:** 2026-10-24  
**Zakres danych:** stacjonarne studia I stopnia we Wrocławiu, w języku polskim i angielskim.  
**Plik:** `src/data/uew.json`

## Pokrycie oferty

Najnowszy dostępny informator rekrutacyjny to oferta 2026/2027. Jego tabela rozróżnia stopień i tryb, osobno wskazuje filię w Jeleniej Górze oraz studia anglojęzyczne. Po zastosowaniu zakresu zlecenia w pliku znajduje się **20 ofert: 15 polskojęzycznych i 5 anglojęzycznych**. Lista odzwierciedla wyłącznie pozycje oznaczone jako I stopień stacjonarny w siedzibie UEW oraz ofertę anglojęzyczną:

| Język polski | Język angielski |
|---|---|
| Analityka gospodarcza | Business Informatics |
| E-biznes | Business Management |
| Ekobiznes | Finance |
| Ekonomia | International Business |
| Finanse i rachunkowość | Management Accounting |
| Informatyka w zarządzaniu produkcją | |
| Informatyka w biznesie | |
| Komunikacja społeczna | |
| Logistyka | |
| Międzynarodowe stosunki gospodarcze | |
| Nieruchomości i gospodarka przestrzenna | |
| Rachunkowość i podatki | |
| Zarządzanie | |
| Zarządzanie i inżynieria produkcji | |
| Zarządzanie projektami | |

Filia Jelenia Góra, studia niestacjonarne i II stopnia nie zostały zaimportowane. Kierunki nieobecne w tabeli stacjonarnych I stopnia (np. Controlling i Konsulting prawny i gospodarczy) nie zostały dodane. „Ekonomia” zachowuje identyfikator `uew-ekonomia` z poprzedniego katalogu.

Podstawą kompletności jest [Informator dla kandydatów 2026/2027](https://rekrutacja.uew.pl/wp-content/uploads/sites/2/2026/04/Informator-dla-kandydatow-2026-2027.pdf), tabela „Lista wszystkich kierunków”, wraz z [oficjalną listą kierunków UEW](https://rekrutacja.uew.pl/wyszukiwarka-kierunkow/lista-kierunkow/). Uczelnia zastrzega, że uruchomienie kierunku może zależeć od liczby kandydatów.

## Rekrutacja i kalkulator

Oficjalna [strona zasad rekrutacji na stacjonarne studia I stopnia](https://rekrutacja.uew.pl/en/studia-i-stopnia-zasady-rekrutacji/) odsyła do uchwały R.0000.49.2025 dla roku 2026/2027. Dla polskiej matury podstawa kwalifikacji to suma punktów z trzech pisemnych przedmiotów:

1. matematyka;
2. jeden nowożytny język obcy (angielski, francuski, hiszpański, rosyjski, niemiecki albo włoski);
3. jeden wybrany przedmiot: język polski, geografia, historia, wiedza o społeczeństwie, fizyka, chemia, biologia, informatyka albo filozofia.

Przeliczniki opublikowane dla rekrutacji 2026/2027: poziom podstawowy × 0,5; rozszerzony × 1; język obcy zdawany na poziomie klas dwujęzycznych × 1,5. Kandydat na program anglojęzyczny musi mieć angielski na poziomie rozszerzonym lub dwujęzycznym oraz co najmniej 60%. Tabela IB/SL/HL na tej samej stronie jest odrębnym sposobem kwalifikacji i nie została włączona do kalkulatora polskiej matury.

Nie odnaleziono opublikowanej uchwały ani kompletnej reguły dla rekrutacji 2027/2028 w sprawdzonych źródłach. Powyższe dane mają zatem status jawnie rocznikowy i **nie potwierdzają zasad dla docelowego roku 2027/2028**. Lista przedmiotów przechowuje również filozofię i nowożytne języki obce, których nie ma wszystkich w bazowym `SUBJECTS`; kalkulator musi obsłużyć je albo jawnie wskazać ograniczenie.

## Progi historyczne

Uczelniana [tabela progów punktowych](https://rekrutacja.uew.pl/informacje-praktyczne/najwazniejsze-informacje/progi-punktowe/) zawiera archiwalne dane od 2020/2021 oraz progi 2026/2027. Z pliku zaimportowano tylko progi ofert należących do wrocławskiego zakresu katalogu i do lat 2022/2023 lub późniejszych. Gdy źródło rozróżnia rundy, rekord ma `round` „pierwsza” albo „druga”; gdy archiwalna tabela nie określa rundy, pozostaje `null`.

- **2026/2027:** pierwsze i drugie ustalenie progów. Dla wszystkich 20 ofert są obie wartości z oficjalnej tabeli.
- **2025/2026:** oficjalna tabela progów stacjonarnych I stopnia; tabela nie podaje rundy. Zawiera 20 ofert, w tym nowy kierunek Informatyka w zarządzaniu produkcją.
- **2024/2025:** tabela archiwalna na stronie oficjalnej podaje progi wszystkich 19 ówczesnych wrocławskich ofert. Dodatkowa oficjalna informacja z 18 lipca 2024 nazywa listę pierwszymi progami; wartości w katalogu opisano jako pierwsza runda.
- **2023/2024:** oficjalny komunikat IRK z 28 lipca 2023 wyjaśnia, że przyjęto w pierwszym ustaleniu wartości, bez obniżania progów. Wartości na stronie archiwalnej odpowiadają komunikatowi; `round` pozostawiono `null`, ponieważ komunikat nie numeruje ustalenia jako tury.
- **2022/2023:** strona oficjalna podaje wartości dla części ofert. Dla kierunków, których tabela w tym roczniku nie wymienia (np. E-biznes, Ekobiznes, Komunikacja społeczna, Nieruchomości i gospodarka przestrzenna, Zarządzanie projektami), próg pozostawiono bez rekordu. Nie dopisano wartości na podstawie sąsiedniego rocznika ani podobnej nazwy.

Sprawdzono także zewnętrzne strony [Otouczelnie dla rekrutacji 2026/2027](https://www.otouczelnie.pl/uczelnia_dzial/4820/Uniwersytet-Ekonomiczny-we-Wroclawiu-rekrutacja-na-studia-20262027) oraz [Otouczelnie – tabela progów](https://www.otouczelnie.pl/uczelnia_dzial/4820/Uniwersytet-Ekonomiczny-we-Wroclawiu-rekrutacja-na-studia-20222023/progi). Ponieważ oficjalna tabela UEW zawiera wartości dla potrzebnych roczników, dane z portalu nie zostały użyte jako dodatkowe progi ani jako niezależne potwierdzenia. Nie znaleziono potrzeby zastępowania oficjalnych danych relacjami kandydatów. Próg opisuje wynik kwalifikacyjny wskazany przez źródło, nie gwarancję przyjęcia w przyszłych latach.

## Opisy i pozostałe luki

Opisy zostały napisane odrębnie dla każdego programu, w oparciu o tematykę z oficjalnych kart kierunków i opis programu, o ile opis był widoczny w katalogu rekrutacyjnym; nie kopiują jednego tekstu na wszystkie rekordy. Oficjalna karta [Informatyki w zarządzaniu produkcją](https://rekrutacja.uew.pl/kierunki-studiow/informatyka/) podaje m.in. systemy produkcyjne, AutoCAD, Matlab/Simulink, C/C++/Java/Python, AI, IoT oraz role absolwentów. Portal rekrutacyjny publikuje listę kart, lecz nie wszystkie karty miały jednolicie dostępny, szczegółowy sylabus w odczycie źródeł.

- **Czas trwania:** pozostawiono `null`, bo przeglądane źródła oferty i rekrutacji nie potwierdziły wiarygodnie liczby semestrów dla każdego kierunku. Należy uzupełnić po sprawdzeniu aktualnych programów studiów, ze szczególną uwagą na kierunki inżynierskie.
- **Przedmioty w programie:** opisy wskazują ogólne treści, nie są pełnym audytem sylabusów.
- **Zawody:** przykłady są ilustracyjne. Nie dowodzą dostępności pracy, uprawnień zawodowych ani gwarancji zatrudnienia. Tam, gdzie karta uczelni wskazywała przykłady, zostały one ujęte w notatce kariery.
- **Przyszły nabór:** nie przypisano zasad ani oferty 2027/2028 jako potwierdzonych; aktualizację trzeba przeprowadzić po opublikowaniu nowego informatora i uchwały.

## Źródła w danych

Identyfikatory źródeł i daty sprawdzenia są zapisane w `src/data/uew.json`. Wszystkie użyte źródła kierunków, progów i zasad rekrutacji są stronami lub dokumentami UEW. Źródła zewnętrzne odnotowano wyłącznie w tym raporcie jako kontrolę pomocniczą i nie użyto ich do ustalania progu.
