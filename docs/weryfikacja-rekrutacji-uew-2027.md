# Uzupełnienie kontroli prowadzącego — 25.10.2026

Uchwałę pobrano bezpośrednio i odczytano wszystkie 26 stron. Lokalny wyciąg: `docs/research/uew-uchwala-2027.txt`. Potwierdzenie: §4 ust.3 na s.9 stosuje mnożnik1,5 dla języka dwujęzycznego, także poza samym ustępem dotyczącym studiów anglojęzycznych. Zachowano ten mnożnik w obu wariantach kalkulatora.

Korekta raportu poniżej: 12/20 ofert ma próg 2022/23 (nie15/20). Braki: E-biznes, Ekobiznes, Informatyka w zarządzaniu produkcją, Komunikacja społeczna, Nieruchomości i gospodarka przestrzenna, Rachunkowość i podatki, Zarządzanie projektami, Management Accounting. Sformułowania o pięciu brakach pomijały trzy pozycje. Runda2024/25 została ustalona z osobnej oficjalnej publikacji z18.07.2024, dlatego w aplikacji pozostaje „pierwsza”, choć zbiorcze archiwum nie nazywa rundy.

Wdrożono osobne reguły2026/27 i2027/28, domyślnie2027/28. Lista ofert nadal2026/27, nie przeniesiono jej bez dowodu na2027/28. Katalog i źródła zaktualizowano. Pozostała część dokumentu zachowuje zapis researchu przed integracją.

---

# Weryfikacja rekrutacji Uniwersytetu Ekonomicznego we Wrocławiu 2027/2028

**Stan na:** 25 października 2026 r.  
**Zakres:** stacjonarne studia I stopnia we Wrocławiu; przegląd uchwały, punktacji i archiwalnych progów.  
**Wynik:** Uniwersytet Ekonomiczny we Wrocławiu opublikował uchwałę rekrutacyjną 2027/2028. Stwierdzenie w `src/data/uew.json`, że uchwała nie była dostępna, jest nieaktualne.

## Źródła pierwotne i ścieżka weryfikacji

1. [BIP Uniwersytetu Ekonomicznego we Wrocławiu – Uchwały Senatu 2026](https://www.bip.ue.wroc.pl/575/uchwaly-senatu-2026.html), wpis „Uchwała Senatu R.0000.26.2026”, wśród uchwał z 25 czerwca 2026 r. (wiersz 120 w odczycie strony). To rejestr BIP, nie wtórna strona informacyjna.
2. [PDF uchwały R.0000.26.2026](https://www.bip.ue.wroc.pl/download/attachment/4202/uchwala-senatu-r0000262026.pdf?v=1782885195), 26 stron. Strona tytułowa (PDF s. 1) podaje numer, organ, datę 25.06.2026 oraz rok 2027/2028.
3. [Akty prawne Biura Rekrutacji UEW](https://rekrutacja.uew.pl/akty-prawne/) nadal wymieniają jako najnowszą uchwałę rekrutacyjną R.0000.49.2025 dla 2026/2027; strona nie została zaktualizowana o R.0000.26.2026. Nie jest to dowód braku uchwały. Wpis w BIP rozstrzyga tę rozbieżność.

Krótki cytat z PDF, s. 1: „UCHWAŁA NR R.0000.26.2026 […] z dnia 25 czerwca 2026 r. […] w roku akademickim 2027/2028”.

## Reguła kwalifikacji 2027/2028

Podstawa: PDF uchwały, § 4, PDF s. 5–8 (tekst PDF s. 5–8; w odczycie przeglądarki wiersze 139–260).

- Dla obywateli polskich na studiach I stopnia podstawą jest konkurs świadectw i suma punktów z trzech grup: **matematyka + jeden język obcy nowożytny + jeden przedmiot do wyboru**. Języki obce: angielski, francuski, hiszpański, niemiecki, rosyjski, włoski (§ 4 ust. 2 pkt 1–2).
- Lista przedmiotu do wyboru: język polski, geografia, historia, wiedza o społeczeństwie, fizyka, chemia, biologia, informatyka, filozofia **oraz biznes i zarządzanie** (§ 4 ust. 2 pkt 2; PDF s. 8).
- Matura od 2005 r., studia po polsku: podstawa ×0,5, rozszerzenie ×1; jeśli istnieją wyniki PP i PR z przedmiotu, wybiera się korzystniejszy wynik po przeliczeniu (§ 4 ust. 1 pkt 1 lit. a–b; PDF s. 5).
- Studia anglojęzyczne: językiem kwalifikacyjnym może być wyłącznie angielski na poziomie rozszerzonym albo dwujęzycznym, minimum 60%; angielski rozszerzony ×1, dwujęzyczny ×1,5 (§ 4 ust. 1 pkt 1 lit. c i ust. 2; PDF s. 5 i 8). To reguła dla właściwej grupy językowej, nie premia za dowolny wynik dwujęzyczny.
- Dodatkowe rozstrzygnięcie remisu: gdy nie da się wypełnić limitu przy identycznej punktacji na granicy przyjęcia, komisja może zastosować średnią ocen z przedmiotów wskazanych przez Rektora (§ 4 ust. 4, PDF s. 8). To kryterium remisu, nie dodatkowe punkty doliczane każdemu.
- Uchwała R.0000.26.2026 nie ustanawia punktów za olimpiady. Odrębna uchwała olimpiadowa na stronie Biura Rekrutacji obejmuje lata 2023/24–2026/27; nie wolno automatycznie przenosić jej na 2027/28. PDF rekrutacyjny mówi o rankingu i progach, nie o bonusie punktowym „na wniosek”.
- Uchwała obejmuje też inne ścieżki (m.in. maturę przed 2005 r., IB/EB, kandydatów zagranicznych, ocenę szkolną w szczególnym przypadku); istniejący kalkulator jawnie ich nie obsługuje. Nie należy opisywać modelu polskiej matury jako kompletnej implementacji wszystkich trybów.

### Różnice względem aplikacji / zasad 2026/2027

1. **Nowy przedmiot w 2027/2028:** biznes i zarządzanie znalazł się na oficjalnej liście do wyboru. Nie ma go ani w `src/admission.ts` (tablica trzeciej grupy), ani w `subjects` kierunków UEW w `src/data/uew.json`. To wymaga dodania przedmiotu do grupy, list UI/danych dla wszystkich programów UEW oraz aktualizacji opisów reguł.
2. **Wartość współczynnika dwujęzycznego w modelu:** `src/admission.ts` ustawia ogólnie `bilingual:0`; jedynie język angielski dla UEW_EN ma 1,5. Wyniki są zgodne z samą regułą trzech grup dla polskiej matury, ale należy zweryfikować ścieżkę użytkownika i jawnie ograniczyć dwujęzyczny poziom do języka obcego, zamiast rozszerzać go na wszystkie przedmioty.
3. **Minimum 60% i angielski:** uchwała utrzymuje minimum 60% dla angielskiego w kierunkach anglojęzycznych; obecna reguła modelowa to odzwierciedla. Zachować minimum i rozszerzyć jawny opis z „angielski rozszerzony lub dwujęzyczny” na zapis uchwały o obydwu wariantach.
4. **Progi nie są regułą na przyszły nabór:** uchwała ustala zasady, natomiast próg jest wynikiem rankingu i limitu miejsc. Dane progowe 2027/2028 nie są jeszcze opublikowane i nie można ich wyliczyć z uchwały ani kopiować z 2026/2027.

## Progi historyczne i pokrycie JSON

Oficjalna [strona „Progi punktowe” Biura Rekrutacji UEW](https://rekrutacja.uew.pl/informacje-praktyczne/najwazniejsze-informacje/progi-punktowe/) (odczyt: sekcje 2026/27, 2025/26, 2024/25, 2023/24, 2022/23) publikuje 5 roczników. Dla 2026/27 podaje pierwsze i drugie progi. Dla 2025/26–2022/23 podaje jedną tabelę bez oznaczenia rundy. Starsze tabele obejmują także kierunki filii w Jeleniej Górze i historyczne nazwy; niniejsze porównanie dotyczy tylko programów w zakresie JSON, czyli Wrocław, studia I stopnia.

**Stan `src/data/uew.json` według kontroli wszystkich 20 rekordów `programmes`:**

- 15/20 rekordów zawiera wpis z każdego rocznika 2022/23–2026/27.
- Pięć rekordów ma lukę 2022/23: E-biznes, Ekobiznes, Komunikacja społeczna, Rachunkowość i podatki, Zarządzanie projektami. Oficjalna tabela 2022/23 nie wymienia tych nazw, więc brak w JSON jest zgodny z dostępnym źródłem, a nie dowodem pominięcia opublikowanej wartości.
- Informatyka w zarządzaniu produkcją ma wpisy dopiero od 2025/26; oficjalna tabela na stronie oznacza ją jako nowy kierunek właśnie w 2025/26, więc starszych progów dla tego kierunku nie ma.
- Nieruchomości i gospodarka przestrzenna ma wpisy od 2024/25; nie ma jej w tabelach 2022/23 i 2023/24.
- W pozostałych latach archiwalna tabela wymienia programy z katalogu UEW we Wrocławiu; JSON zawiera wartości, lecz wykorzystuje przy wielu z nich `uew-thresholds-2026` jako źródło zbiorcze, co jest zgodne z tym, że archiwum jest na tej stronie. Wartości i mapowanie nazw historycznych należy utrzymywać przy źródle i roku, nie zakładać, że nazwa kierunku była identyczna (np. „Rachunkowość i controlling” w 2022/23 vs obecne kierunki rachunkowości).
- Dane `2026/2027` z JSON są spójne z oficjalną stroną: wartości pierwsza/druga runda. Roczniki 2025/26, 2024/25, 2023/24 i 2022/23 są w tabelach archiwalnych UEW. Odmienny poziom szczegółowości rund musi pozostać jawny: `round=null` dla tabel, które nie identyfikują tury.

Uwaga dotycząca zakresu: oficjalna tabela progów podaje wyłącznie rekrutację stacjonarną I stopnia (bieżąca strona 2024 podaje Wrocław; tabele archiwalne mają osobne wiersze „Filia”). Nie należy dopisywać progów filii do wrocławskich programów w tej próbce. Progi to wynik kwalifikacji w historycznym naborze, nie minimalny warunek na kolejny rok.

## Zalecane zmiany w danych i kodzie

1. Zaktualizować notatkę zakresu i metadane kontroli: odnotować uchwałę R.0000.26.2026 z 25.06.2026 dla 2027/28; rozróżnić „uchwała opublikowana” od „strona zasad na rekrutacja.uew.pl nadal pokazuje 2026/27”.
2. Dodać `biznes i zarządzanie` do trzeciej grupy w `src/admission.ts` i do `subjects` każdego programu UEW, aktualizując notatki/źródła reguł na rocznik 2027/28. Nie zmieniać historycznych progów.
3. Jeśli aplikacja ma pokazywać reguły obu naborów, utrzymać osobne identyfikatory i lata zasad (2026/27 vs 2027/28) zamiast nadpisywać historyczną regułę jedną wartością.
4. Pozostawić brakujące progi 2022/23 jawnie puste dla pięciu programów, a pozostałe braki roczników starsze niż uruchomienie danego programu także puste; nie imputować ich z podobnych kierunków.
5. Korygować komunikat w JSON o „punktach dodatkowych przyznawanych na wniosek”: uchwała 2027/28 nie potwierdza takiego mechanizmu. Opisać odrębnie wyjątki (olimpiady na mocy osobnej uchwały i tylko okres, który obejmuje; remis; niestandardowe typy matur).
6. Rozważyć przechowywanie źródeł oddzielnie: osobny identyfikator uchwały `uew-rules-2027` oraz progów 2022/23–2026/27 jako archiwalnej tabeli; obecny wpis `uew-thresholds-2026` łączy dane z 2026/27 i kilku wcześniejszych lat.

## Konkretne lokalizacje w repo

- `src/admission.ts`: `UEW_PL` jest `year:'2026/2027'`; lista `Przedmiot do wyboru` kończy się na `filozofia`; `UEW_EN` ma `minPercent:60` i angielski dwujęzyczny ×1,5; caveat nadal zawiera „punktów dodatkowych przyznawanych na wniosek”.
- `src/data/uew.json`: `scopeNote` nadal stwierdza, że uchwała 2027/28 nie była dostępna; wszystkie programy mają `referenceYear:2026/2027`; 20 programów i ich progi pokrywają tylko istniejące historyczne roczniki.

## Zakres nieweryfikowany

W tym researchu nie zmieniono logiki ani rekordów źródłowych. Nie ustalano, czy po 25.10.2026 ukazała się nowa wersja uchwały ani progi naboru 2027/28; w tej dacie nie ma ich w przeglądanej tabeli. Weryfikacja dotyczy wyłącznie naboru I stopnia w ramach zakresu danych projektu i nie stanowi oceny innych ścieżek przyjęć.
