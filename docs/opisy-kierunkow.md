# Opisy kierunków i informacje ze stron uczelni

W karcie kierunku pierwsza zakładka **Opis kierunku** przedstawia krótkie opracowanie oficjalnej karty uczelni. Zakres obejmuje 215 ofert pięciu uczelni we Wrocławiu, oddzielnie dla języka polskiego i angielskiego.

## Co znajdziesz w opisie

- Charakterystykę studiów oraz zagadnienia wskazane w opisie uczelni. Tematy nie są listą nazw przedmiotów.
- Potwierdzone formy nauki i informacje o praktykach, jeśli udało się je wyodrębnić z opisu.
- Obszary pracy wymienione przez uczelnię; w wybranych kartach także przykładowe role zawodowe.
- Ścieżki i specjalności z karty opisowej, jeżeli zostały sprawdzone. To odrębna informacja od stanu zweryfikowanego planu studiów.
- Przykłady zajęć z już zebranych programów, z własnym rocznikiem i oznaczeniem pełnego albo częściowego spisu.
- Link do oficjalnej karty, datę odczytu i zakres materiału.

Treść jest opracowaniem, a nie kopią wszystkich akapitów promocyjnych. Dłuższy tekst pozostaje dostępny przez link do uczelni. Możliwości zawodowe nie oznaczają ofert pracy, pomiaru zatrudnienia ani automatycznego uzyskania uprawnień. Wyniki absolwentów są w zakładce ELA, a aktualne ogłoszenia w części poświęconej pracy.

## Zakres i braki — odczyt 10 listopada 2026

Wszystkie 215 ofert ma własny rekord opisu. W 206 wyodrębniono obszary pracy, w 58 formy nauki, a w 20 dodano redakcyjnie sprawdzone szczegóły praktyk. Brak wpisu w tej sekcji nie oznacza braku praktyk albo możliwości zatrudnienia. Szczegóły mogą znajdować się w planie lub osobnym regulaminie.

Oznaczenie ograniczonego materiału ma Weterynaria po angielsku na Uniwersytecie Przyrodniczym we Wrocławiu: krótka karta odsyła do programu. Link do rozszerzonej anglojęzycznej charakterystyki prowadzi do materiału z datą publikacji 14.08.2019; nie użyto go do potwierdzania bieżącego programu. Nie uzupełniamy luki opisem polskiej wersji językowej. Dla Ochrony środowiska na Uniwersytecie Wrocławskim czytelny opis I stopnia znaleziono na stronie Międzywydziałowego Studium Ochrony Środowiska, zamiast w centralnym serwisie rekrutacyjnym.

Ogólna charakterystyka bez wskazanego cyklu ma oznaczenie daty odczytu. Nie jest potwierdzeniem uruchomienia oferty ani niezmienności programu na 2027/28. Rekrutacja, progi, specjalności i programy zachowują własne źródła i lata. Przykładowo sekcja WORK & STUDY na karcie Zdrowia publicznego Uniwersytetu Medycznego im. Piastów Śląskich we Wrocławiu dotyczy II stopnia i nie została przypisana ofercie licencjackiej.

## Aktualizacja bez zużywania tokenów

Zarejestrowane adresy opisów są częścią inwentarza źródeł. Polecenie `npm run data:monitor` pobiera materiały i wykrywa ich zmiany zwykłym kodem, bez agentów AI, modeli i płatnych API. Samo wykrycie zmiany nie potwierdza jej znaczenia i nie publikuje nowego streszczenia.

Po zmianie strony trzeba porównać jej treść z opracowaniem. Może to zrobić człowiek bez używania AI. Uaktualnienie opisów nie wymaga zmieniania progów ani ponownego odtwarzania planów studiów.

## Dla osoby utrzymującej projekt

Aktywny plik to `src/data/programme-descriptions.json`. Każdy rekord ma identyfikator oferty, język, poziom, URL, datę, skrót SHA-256 dowodu i jawne listy informacji. Puste listy są dozwolone i wyświetlają komunikat o braku potwierdzenia.

Materiały źródłowe oraz redakcyjne opracowania są w `docs/research/descriptions`. `editorial.tsv` zawiera własne streszczenia i tematy dla 215 ofert, a `editorial-extra.json` sprawdzone uzupełnienia. Budowa: `python scripts/build_programme_descriptions.py`. Jest to narzędzie lokalne, bez sieci i AI; nie zmienia zasad rekrutacji ani programów. Ograniczony słownik normalizuje wymienione w kontekście pracy obszary, a nie wnioskuje uprawnień z nazwy kierunku. Szczegóły praktyk i ścieżek pochodzą z jawnego pliku redakcyjnego.

`audit.json` wiąże przegląd z konkretną kopią materiału. Gdy jej URL lub skrót zmieni się, skrypt zatrzyma odtworzenie danych. Dopiero po porównaniu źródła i poprawieniu opracowania należy jawnie uaktualnić odpowiedni wpis audytu. Nie usuwaj audytu, aby ominąć kontrolę. Wersje stron i pełne akapity nie są importowane do aplikacji.

Po edycji wykonaj `npm test`, `npm run validate:data` i `npm run build`, a zmiany prezentacji sprawdź w przeglądarce. Parser wykrywania zmian nie potwierdza kompletności informacji. Nowy adres najpierw sprawdź poleceniem `node --experimental-strip-types scripts/check-source.ts URL current`.
