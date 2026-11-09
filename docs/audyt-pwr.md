# Politechnika Wrocławska — zakres i jakość danych

Sprawdzono: **2 listopada 2026 r.**

## Zakres katalogu

Dodano **62 oferty**: 61 studiów I stopnia i kierunek lekarski jako jednolite studia magisterskie. Wszystkie dotyczą studiów stacjonarnych we Wrocławiu. 57 ofert jest po polsku, 5 po angielsku. Karty opisujące jednocześnie inne miasta lub formy studiów wykorzystano wyłącznie w zakresie Wrocławia i studiów stacjonarnych.

Oficjalna wyszukiwarka poziomu s1 zawierała 64 karty. Pominięto:

- Zarządzanie infrastrukturą i środowiskiem — metryczka wskazuje Jelenią Górę.
- Inżynierię mikrosystemów mechatronicznych — karta jawnie wskazuje brak naboru na 2026/27; nie potwierdzono uruchomienia w 2027/28.

Architekturę uwzględniono na podstawie metryczki. Uczelnia oznacza ją jako „Stacjonarne”, podczas gdy większość innych kart używa określenia „Dzienne”. Jeden filtr wyszukiwarki nie wystarcza do kontroli kompletności.

## Programy i specjalności

Dla wszystkich 62 ofert sprawdzono oficjalny program **2026/2027**, wskazany z indywidualnej karty kierunku. Odczytano 7104 pozycje w grupach i semestrach, w tym powtórzenia między wariantami. 31 ofert ma nazwane specjalności, ścieżki lub moduły. Są to warianty programu, a nie suma obowiązkowych zajęć jednej osoby.

Spisy mają status **lista częściowa**: pochodzą z tabel oficjalnego serwisu sylabusów, ale nie deklarujemy pełnego audytu wszystkich rozwijanych koszyków do wyboru ani szczegółowych kart zajęć. Wskazany cykl nie gwarantuje niezmienionego programu osobom rozpoczynającym studia w 2027 roku.

Nie traktujemy efektów uczenia się, godzin, sum ECTS i przedmiotów maturalnych jako nazw zajęć. Nazwy zajęć po angielsku zachowują język dokumentu. Ścieżki na kierunku lekarskim i moduły na mechanice i budowie maszyn energetycznych zachowują własną kategorię.

## Rekrutacja 2027/2028

Podstawą jest uchwała 384/26/2024-2028 z 11 czerwca 2026 r.: załącznik 1 (§9–12) oraz tabela przedmiotów dodatkowych w załączniku 3. Sprawdzono zmianę 412 z 24 września 2026 r. — dotyczy załącznika 5 i studiów II stopnia.

Kalkulatory obsługują **polską nową maturę pisemną na poziomach podstawowym i rozszerzonym**:

- Studia I stopnia: M + PD + 0,1JO + 0,1JP. Dla M, PD i JO wybieramy maksimum z P, P + 1,5R i 2,5R; oba poziomy muszą dotyczyć tego samego przedmiotu. JP to maksimum z P i R. Przy M = 0 oraz PD = 0 składniki językowe wynoszą 0.
- Matematyka może być jednocześnie składnikiem M i przedmiotem dodatkowym tylko tam, gdzie dopuszcza ją tabela uczelni. Przedmioty dodatkowe odczytano z kolorowego tła prostokątnych komórek na obu stronach załącznika, a nie z samego tekstu PDF. Całą tabelę 51 wierszy porównano z osobnym ręcznym odczytem; test sprawdza każdą komórkę dopuszczeń.
- Architektura: dodatkowo egzamin z rysunku z naboru 2027/28, 0–660 pkt, zaliczenie od 240 pkt. Brak wyniku blokuje podanie sumy.
- Kierunek lekarski: B + M + PD + 0,1JO + 0,1JP; B = 2,5R z biologii. Przy B = 0 lub M = 0 cały wynik wynosi 0. Minimum formalne to 500 pkt. PD obejmuje fizykę albo chemię.

Przedmiot niezdawany daje 0, a zaznaczony poziom bez wpisanego procentu oznacza brak danych i blokuje wynik. Kalkulator nie obejmuje matury dwujęzycznej, IB/EB, starej matury, egzaminów zawodowych, dobrowolnych egzaminów uczelni ani olimpiad. Profil z wynikiem dwujęzycznym otrzymuje jawną informację o ograniczeniu zamiast zaniżonej sumy. Dokumenty i wymagania językowe trzeba sprawdzić na stronie uczelni. Przeliczenie punktów nie potwierdza spełnienia wszystkich warunków przyjęcia.

## Progi historyczne

Z oficjalnej tabeli uczelni dodano **387 wartości**, z zachowaniem roczników i tur:

- 2026/27: 134 wartości dla 59 obecnych ofert.
- 2025/26: 132 wartości dla 59 obecnych ofert.
- 2024/25: 121 wartości dla 56 obecnych ofert.

Nie przenoszono progów filii, wartości z podobnie nazwanych kierunków ani starszych roczników. Dopuszczono wyłącznie równoważną pisownię „w j. angielskim” i „w języku angielskim”. Kreska i kierunek nieuruchomiony nie oznaczają zera. Dopiski do wartości pozostają w notatce źródłowej; nie są importowane jako osobny próg ani minimum nowego naboru. Tabela nie definiuje jednoznacznie kwalifikacji i przyjęcia, dlatego zachowano oznaczenie niepotwierdzonej definicji progu.

## Pozostałe ograniczenia

Nie dodano jeszcze dopasowanych kohort Ekonomicznych Losów Absolwentów ani zweryfikowanych ścieżek zawodowych dla nowych ofert. Aplikacja pokazuje brak takich danych. Opublikowane zasady na 2027/28 nie dowodzą uruchomienia każdej oferty w tym naborze.

## Źródła i odtwarzanie

- [Oficjalna wyszukiwarka kierunków](https://rekrutacja.pwr.edu.pl/wyszukiwarka-kierunkow-studiow/)
- [Akty prawne i załączniki do zasad rekrutacji](https://rekrutacja.pwr.edu.pl/rekrutacja/akty-prawne/)
- [Oficjalne progi stacjonarne](https://rekrutacja.pwr.edu.pl/rekrutacja/progi-punktowe/progi-studia-i-stopnia-stacjonarne/)
- [Oficjalny serwis sylabusów](https://sylabus.usos.pwr.edu.pl/)

Lokalne kopie, manifest wszystkich 64 kart i rozliczenie zakresu są w docs/research/pwr. Pakiet odtwarza scripts/build-pwr.py wyłącznie z tych kopii. Tabele aktywnej historii parsuje src/thresholds.ts; wynik jest sprawdzany ponownie w teście pakietu. W przyszłych aktualizacjach najpierw sprawdź politykę źródeł, pobierz nowe dowody, a potem ponownie skontroluj parser i zakres — nie nadpisuj pakietu samymi starymi kopiami.

Kontrola obejmuje zgodność spisu, odwołania do źródeł, rozdzielenie form i kampusów, porównanie importu progów z parserem oraz obliczenia ręczne i przypadki graniczne kalkulatorów.
