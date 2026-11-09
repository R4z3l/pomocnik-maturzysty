# Kontrola drugiej partii programów Uniwersytetu Wrocławskiego

Lokalna ponowna ekstrakcja i kontrola: 28.10.2026. Wynik: 44 oferty, 43 ze spisem przedmiotów, 42 listy częściowe, 1 pełny plan i 1 jawny brak. 35 nazw specjalności lub modułów specjalnościowych w 11 ofertach. 2838 wpisów przedmiotów; liczba uwzględnia powtórzenia między semestrami i alternatywnymi wariantami.

## Naprawa odczytu

- Wybrano rzeczywistą komórkę nazwy przedmiotu, z uwzględnieniem pustych scalonych kolumn. Moduł USOS i nazwa kursu nie są łączone.
- Przeliczono współrzędne tabel w PDF z rotacją strony 90°: dotyczy m.in. kultury i praktyki tekstu, prawa, socjologii ekonomicznej oraz stron indywidualnych studiów informatyczno-matematycznych.
- Usunięto legendy, cele kształcenia, podsumowania godzin i egzaminów, a także akapity opisów. Skrót ECTS w rzeczywistej nazwie komórki nie powoduje utraty kursu: usuwana jest sama punktacja.
- Sprawdzono wszystkie 44 rekordy, zakresy stron i pełny rozkład nazw. Dodatkowo odczytano problematyczne zawinięcia z pierwotnej warstwy tekstowej PDF. Dla starszej czcionki socjologii ekonomicznej odtworzono polskie litery i logiczne wiersze pierwszych czterech stron; nie użyto części niestacjonarnej ani II stopnia.
- Matematyka obejmuje wyłącznie I stopień (strony 44–77), pięć nazwanych specjalności i wariant ogólny. Grupy pokazują wariant i stronę; strona łącząca dwa warianty wymienia obydwa. Listy nie są sumą obowiązkowych zajęć jednej osoby.
- Przedmioty trzech modułów politologii i zarządzania projektami społecznymi rozdzielono na nazwy. Political Science zachowuje cztery osobne warianty. Dwie nieobowiązkowe specjalności niderlandystyki mają oddzielne listy z końcowych stron programu. Psychologia zachowuje alternatywne moduły specjalnościowe.

## Zakres i ograniczenia

Pełny plan oznaczono tylko dla historii sztuki: sześć semestrów z oficjalnej strony instytutu. Rok obowiązywania nie został ustalony i jest jawnie opisany. Pozostałe źródła są oznaczone jako listy częściowe nawet wtedy, gdy odczytano większość tabel: nie utożsamia się samego odczytu PDF z potwierdzeniem kompletnego, aktualnego planu.

Jedyny brak: informatyka stosowana i systemy pomiarowe. Dostępny plan zamkniętego cyklu 2022–2026 pominięto w aktywnych źródłach. Nie przedstawia się go jako obecnego programu.

Turystykę przepisano ręcznie z obu stron skanu przy pomocy rodzica zadania. Plan obowiązuje od 2023/2024; moduły A–E są elementami planu ramowego, a nie potwierdzonymi specjalnościami. Starszy rok uchwały innych planów nie jest sam w sobie podstawą ich odrzucenia; rok i charakter źródła pokazano osobno. Żaden rekord nie potwierdza jeszcze programu naboru 2027/2028.

## Powtarzalność i dowody

Budowa z lokalnej ewidencji: `python scripts/build_curricula_uwr_b.py`.
Uzupełnienie brakujących ekstrakcji: ta sama komenda z `--extract`.
Inwentarz wszystkich wpisów i kontrola źródeł: `python docs/research/curricula/uwr-b/qa.py`.
Wynik ilościowy i SHA-256: `qa-summary.json`. Pełna lista do przeglądu: `reviewed-inventory.md`.

Wykonano po ostatniej zmianie danych:

- `node --experimental-strip-types --test tests/curricula.test.ts` — 2 testy, 2 zaliczone.
- `npm run validate:data` — walidacja bieżących rekordów obu uczelni zakończona poprawnie.
- `qa.py` — 44 oczekiwane identyfikatory, źródło każdej grupy w bibliografii rekordu, zero wskazanych nagłówków/legend/uszkodzeń czcionki.

W tej partii nie zmieniano UI i nie używano Git. Użyto istniejącego cache; nie wprowadzono pobierania ani modeli do działającej aplikacji.

Informatyka: oprócz siedmiu nazw obowiązkowych z tabeli 1 ujęto osobno dziesięć dodatkowych nazw/zakresów z tabeli treści programowych. Uchwała odsyła do odrębnej oferty dydaktycznej i sylabusów, więc nie zawiera zamkniętego spisu fakultetów.

Po niezależnej kontroli usunięto dwa dokładne wiersze sum „Łącznie” / „Łącznie:”; parser i QA odrzucają jedynie dokładne nazwy Łącznie/Razem/Suma/Total z opcjonalną interpunkcją, zachowując rzeczywiste nazwy typu Total Quality Management.
