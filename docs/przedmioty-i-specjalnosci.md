Aktualizacja **10.11.2026 — Uniwersytet Medyczny im. Piastów Śląskich we Wrocławiu**: dodano 16 częściowych spisów zajęć z dokumentów BIP 2026/2027. Odczyt 1244 pozycji z tabel godzinowych obejmuje powtórzenia; nie potwierdza kompletności koszyków ani przypisania semestrów. Katalog: 215 spisów, 116 pełnych i 99 częściowych. Parser: `scripts/umw_curricula.py`, audyt: `docs/audyt-umw.md`.

Aktualizacja **10.11.2026**: dodano 28 pełnych spisów planów 2026/2027 Uniwersytetu Przyrodniczego we Wrocławiu (wszystkie semestry i rozwijane koszyki). Katalog ma 199 ofert ze spisem: 116 pełnych planów i 83 listy częściowe. Źródło: `src/data/curricula-upwr.json`, adapter `scripts/upwr_curricula.py`, audyt `docs/audyt-upwr.md`. Brak osobnej potwierdzonej listy specjalności nie oznacza braku specjalności. Poniższe wcześniejsze liczby opisują stan historyczny.

# Programy studiów i specjalności

Aktualizacja **09.11.2026**: wszystkie 171 ofert ma spis zajęć. 88 rekordów to pełne plany wskazanego cyklu, 83 to jawne listy częściowe Uniwersytetu Wrocławskiego. Uzupełniono European Cultures na podstawie pełnego planu sześciu semestrów z uchwały Senatu 168/2023; nie zamieniano obszarów nauki z opisów rekrutacyjnych w przedmioty. Dla 62 ofert Politechniki Wrocławskiej sprawdzono wszystkie tabele i rozwijane koszyki oraz usunięto instrukcje wyboru z list przedmiotów. Pozostałe wcześniejsze liczby w tym dokumencie są historią audytu.

Aktualizację planów Politechniki Wrocławskiej wykonuje `npm run data:refresh -- --university pwr`; parser: `scripts/pwr_curricula.py`. Plan European Cultures jest chroniony skrótem sprawdzonego PDF i transkrypcji, a zmiana dokumentu wymaga nowego przeglądu. Skrypt `scripts/build-pwr.py` zachowano jako checkpoint z 02.11.2026: nie odtwarza obecnego audytu pełnych planów i nie służy do nadpisywania kanonicznego pliku `curricula-pwr.json`.

Źródło aplikacji: `src/data/curricula-uwr-a.json`, `curricula-uwr-b.json`, `curricula-uew.json`, `curricula-pwr.json`. Kontrakt: `src/curriculumTypes.ts`. Każda oferta ma osobny rekord; brak listy jest jawnym wynikiem sprawdzenia, nie dowodem braku przedmiotów/specjalności.

## Co uznajemy za spis

- `full-plan`: odczyt listy zajęć całego wskazanego planu, także ogólnouczelnianych i wariantów do wyboru. Nie oznacza znajomości szczegółowego sylabusa każdego zajęcia. Pozycja ogólna „przedmiot do wyboru” pozostaje pozycją ogólną, jeśli plan nie rozwija jej nazw.
- `listed-subjects`: lista częściowa podana przez uczelnię lub częściowy odczyt dokumentu. Nie nazywamy kilku przykładów kompletem.
- `unavailable`: nie potwierdzono listy. Źródła i opis poszukiwań pozostają przy kierunku.

Każda grupa ma źródło i ewentualny semestr. Specjalność, specjalizacja, ścieżka i moduł zachowują nazewnictwo dokumentu. Nie przepisujemy zawodów absolwenta jako specjalności. Brak znalezionej listy nie oznacza braku specjalności. Nazwy i oferta uruchomienia z planu2026/27 nie stanowią gwarancji dla2027/28.

Widok przedmiotów grupuje wyłącznie według potwierdzonych semestrów; pozycje bez potwierdzenia pozostają na wspólnej liście. Dla komunikacji wizerunkowej przypisania semestrów zweryfikowano w lokalnej kopii planu 2024/2025, również tam, gdzie na jednej stronie kończy się jeden semestr i zaczyna następny. Przed ponownym uruchomieniem historycznych skryptów dla drugiej partii należy zachować te przypisania i porównać wynik z kanonicznym JSON.

## Aktualizacja w domu przez AI

Przed researchem przeczytaj AGENTS.md i politykę źródeł. Wyszukaj oficjalny plan na stronie wydziału/instytutu/BIP, nie kończ na karcie rekrutacyjnej. Zweryfikuj nazwę, Wrocław, I stopień/jednolite, język, tryb stacjonarny i faktyczny cykl kształcenia. Rok w nagłówku rekrutacji lub stopce nie datuje programu. Nie importuj przedmiotów maturalnych jako zajęć studiów.

Pobieranie ręczne: `scripts/source_policy.py:guarded_get`. Zapisz PDF/HTML i odczyt tekstowy w docs/research/curricula. Nie pobieraj wykluczonych materiałów ponownie. Nowy plik źródłowy lub inny układ PDF wymaga ponownej kontroli parsera na całym pliku.

Dla Uniwersytetu Ekonomicznego we Wrocławiu punktem bazowym jest załącznik do uchwały Senatu R.0000.18.2026 z23.04.2026 (BIP,300stron). Dla każdego z20kierunków sprawdzono nagłówek poziomu i języka; nie importowano studiów II stopnia ani programów filii w Jeleniej Górze. Dane odtwarza `python scripts/import-curricula-uew.py` z lokalnych kopii. Wycinek audytu ma1474pozycje oraz60pominiętych wierszy wyłącznie niestacjonarnych lektoratów. Kontrola nietypowych wierszy zaliczeń:0. Specjalności/moduły z uchwalonego planu mają pierwszeństwo przed różnie zapisanym opisem marketingowym.

Przed oddaniem: `npm test`, `npm run validate:data`, `npm run build`, a następnie przeglądarka — program PL i EN, wyszukiwanie przedmiotu, alternatywne specjalności, jawna luka, klawiatura i telefon. Aplikacja korzysta z plików statycznych; nie wywołuje API ani modeli.


## Kontrola końcowa28.10.2026

107/109 spisów:24pełne i83częściowe.50ofert z nazwanymi wariantami. Dwie luki opisane w docs/postep.md. Dane z końcowych plików JSON są kanoniczne. Starsze skrypty build-records.py/enrich-records.py w folderze badawczym pierwszej partii Uniwersytetu Wrocławskiego to historyczne checkpointy: NIE odtwarzają ręcznych poprawek, nie nadpisuj nimi danych. Przed aktualizacją przeczytaj AUDIT-2026-10-28.md. Druga partia ma odtwarzalny skrypt scripts/build_curricula_uwr_b.py oraz własne QA.

Kontrola parsera musi obejmować cały dokument i wszystkie listy: puste scalone kolumny, rotację PDF90°, tytuły kursów vs efekty uczenia, legendy i sumy „Łącznie”. Długie prawidłowe nazwy egzaminów oraz Total Quality Management pozostają dozwolone. Nie naprawiaj samym obcinaniem długości tekstu.


## Politechnika Wrocławska — 02.11.2026

Dodano 62 częściowe spisy z oficjalnego serwisu sylabusów dla cyklu 2026/2027, z semestrami i wariantami. Zakres, metoda, liczby i ograniczenia są w docs/audyt-pwr.md, dostępnej również w widoku „Instrukcje”. Skrypt scripts/build-pwr.py odtwarza wyłącznie ten nowy pakiet z lokalnych dowodów; nie nadpisuje danych pozostałych uczelni.
