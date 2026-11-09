# Audyt przykładowych ogłoszeń pracy

**Stan sprawdzenia:** 2026-10-24  
**Plik danych:** `src/data/jobs.json`  
**Zakres:** konkretne ogłoszenia w lokalizacji Wrocław lub wskazana przez źródło praca zdalna z Polski.

## Wynik zbiórki

Zapisano **17 unikalnych ogłoszeń**, z 6 źródeł: PKP, Herbapol Wrocław, Pracuj.pl, Just Join IT, OgłoszeniaWroclaw.pl oraz StudentNews.pl (kopia oferty PUP Wrocław). Rekordy obejmują rodziny tech, finance, business, law, psychology, education i science.

| Status na 24.10.2026 | Liczba | Zasada |
|---|---:|---|
| `confirmed` | 11 | Źródło wskazywało trwający nabór albo przyszły termin ważności. |
| `unconfirmed` | 3 | Oferta widniała na aktualnej liście PKP, ale osadzona karta szczegółów nie wczytała się; nie można potwierdzić terminu ani wymagań. |
| `expired` | 3 | Źródło wprost oznaczało nabór jako zakończony albo upłynął wskazany termin. Zachowane jako przykłady historyczne, nie jako aktywne wakaty. |

Do aktualnie potwierdzonych przykładów należą: pięć ofert Herbapolu (w tym praca laboratoryjna, księgowość, kadry/płace i prawo), staż BSH w jakości, staż podatkowy BASF, staż HR Operations Schaeffler, wsparcie procesów prawnych CREDITEXPRESS, analityk process mining Capgemini oraz psycholog szkolny. Daty publikacji zapisano tylko przy ofertach, w których źródło podało jednoznaczną datę; w przeciwnym razie pole pozostaje `null`.

## Poziom stanowiska

Poziom oceniono na podstawie konkretnych wymagań. Przykładowo „Młodszy Analityk” Upvanta wymagał **co najmniej dwóch lat** doświadczenia z analizą danych, dlatego otrzymał poziom `experienced`, mimo etykiety Junior. Z kolei CreditExpress wymaga co najmniej roku doświadczenia, dlatego pozostaje na poziomie `entry`, a nie stażu. Analityk laboratorium Herbapolu z rocznym doświadczeniem sklasyfikowano jako `entry`. Gdy oferta nie podawała wymagań lub ich szczegóły były niedostępne, nie przypisywano poziomu (`unknown`).

W zbiorze jest kilka użytecznych przykładów łączenia pracy ze studiami: BASF (student, 20–32 godz./tydz.), Schaeffler HR (student, min. 25 godz./tydz., elastyczny grafik) i BSH (student, min. 25 godz./tydz., praktyki min. 9 miesięcy). Pełnoetatowych ofert nie oznaczono jako zgodnych ze studiami, jeśli źródło tego nie potwierdzało.

## Wygasłe i niepotwierdzone rekordy

- Junior Accounts Receivable Schaeffler: karta Pracuj.pl mówiła, że wygasła ponad miesiąc wcześniej; doświadczenie AR było mile widziane, nie obowiązkowe. Rekord nie liczy się jako aktualny popyt.
- Nauczyciel współorganizujący proces kształcenia SP nr 20: oferta PUP nr StPr/26/2669 była ważna do 30.09.2026, więc pozostaje tylko rekordem archiwalnym.
- Młodszy Analityk Przetwarzania Danych Upvanta: termin 24.09.2026 minął; status to `expired`. Wynagrodzenia nie zapisano, ponieważ strona wyświetlała kwotę przeliczoną na USD i nie potwierdzono oryginalnej kwoty.
- Trzy oferty PKP (dwa stanowiska specjalistyczne i praktykant w Wydziale Najmu) były widoczne na oficjalnej liście ofert z datami 6 i 12.10.2026. Ich karty szczegółowe opierały się na osadzonym rekruterze niedostępnym w odczycie, więc status pozostał `unconfirmed`, a pola wymagań, wynagrodzenia i terminu naboru są puste.
- Oferta psychologa szkolnego z portalu PUP zawiera niespójność: podaje 2 godziny tygodniowo, ale jednocześnie pełny etat. Uwzględniono ją z wyraźną adnotacją; warunki trzeba potwierdzić bezpośrednio u pracodawcy.

## Ograniczenia pokrycia i deduplikacja

To zestaw przykładów, a nie pełny ani reprezentatywny przegląd rynku. Nie należy porównywać liczby ogłoszeń z różnych rodzin jako miary ich popularności. Nie uzyskano potwierdzonych, bezpośrednich kart dla wszystkich obszarów. W szczególności nie znaleziono w tej sesji wystarczająco zweryfikowanego ogłoszenia dla osobnej rodziny humanistycznej (np. języki, kultura lub redakcja); treści cyfrowe z marketingiem nie są traktowane jako zastępstwo całej rodziny.

Każde wystąpienie w JSON odpowiada osobnej ofercie, zweryfikowanej po tytule, pracodawcy, lokalizacji i zakresie. Nie liczono kilku lokalizacji jednej oferty ani powtórzeń tego samego ogłoszenia w różnych portalach jako oddzielnych wakatów. Pole `url` każdego rekordu wskazuje konkretną kartę, jeśli źródło udostępniło taką kartę; wyszukiwanie i listy ogólne służyły wyłącznie do odkrycia oferty.

## Źródła i daty

Identyfikatory źródeł, bezpośrednie linki do ogłoszeń, daty publikacji i terminy ważności znajdują się w `src/data/jobs.json`. Cały zbiór sprawdzono 24.10.2026. Dla historycznych ogłoszeń `active` oznacza wygaśnięcie w dniu sprawdzenia; nie są one prezentowane jako aktualne wakaty. Dane nie deklarują liczby stanowisk poza przypadkiem, gdy źródło podaje tę informację, ani nie dowodzą popytu w całej branży.
