# Weryfikacja opisów — 10.11.2026

Aktywna baza: 215 rekordów, 214 opracowań rozszerzonych i jedna karta z ograniczonym materiałem. Obszary pracy: 206 ofert; formy nauki: 58; redakcyjnie sprawdzone szczegóły praktyk: 20. Brak szczegółu w opracowaniu nie oznacza nieistnienia danej możliwości. Materiały i opracowania mają własne skróty w `audit.json`.

Własne streszczenia i tematy są w `editorial.tsv`. Rozszerzenia o praktyki, role i ścieżki są w `editorial-extra.json`. Kategorie zawodowe normalizowane są z kontekstu pracy w źródle, z pominięciem list firm partnerskich. Nie służą do wyprowadzania uprawnień. Podczas przeglądu poprawiono między innymi fałszywe dopasowania hospitality/szpital, technologist/logistyka, roboty budowlane/robotyka i środowisko biznesowe/ochrona środowiska; regresje obejmuje test opisów.

Ochrona środowiska na Uniwersytecie Wrocławskim: centralna karta nie zwróciła opisu, więc po sprawdzeniu treści użyto strony Studium dla I stopnia. Nie przypisano specjalności II stopnia. Weterynaria anglojęzyczna na Uniwersytecie Przyrodniczym we Wrocławiu: aktywny opis oparto na krótkiej polskojęzycznej karcie tej anglojęzycznej oferty. Dodatkowy anglojęzyczny materiał (`upwr-vet-en-expanded.html`) ma datę publikacji 14.08.2019 i nie potwierdza bieżącego programu; nie został aktywnym źródłem ani podstawą przypisania opisu polskiej weterynarii.

Świeże sprawdzenia:

- `npm test`: 42 testy, 42 zaliczone, zero błędów. Test opisów obejmuje wszystkie 215 rekordów, język, poziom, domeny, skróty lokalnych materiałów i przykłady błędów normalizacji.
- `npm run validate:data`: 215 opisów, jeden ograniczony; dotychczasowe 692 progi oraz 116 pełnych i 99 częściowych spisów zachowane.
- `npm run build` i `npm run check:release`: poprawne. Vite nadal zgłasza ostrzeżenie rozmiaru głównego pakietu. Materiały HTML nie trafiają do pakietu aplikacji.
- Testy Python: 12 aktualizatora, 1 odczytu programów Uniwersytetu Medycznego im. Piastów Śląskich we Wrocławiu i 2 programów Uniwersytetu Przyrodniczego we Wrocławiu zaliczone.
- Inwentarz sprawdzony dla wszystkich 215 opisów: każdy adres dozwolony i zarejestrowany do monitorowania. Weryfikacja UTF-8 nowych plików nie wykazała markerów uszkodzenia kodowania.

Przeglądarka Ego Lite, lokalny serwer na porcie 4194: sprawdzono otwieranie kart wszystkich pięciu uczelni, domyślną zakładkę opisu, treść i źródło Zdrowia publicznego, stronę Studium, ścieżki biologii i oznaczenie ograniczonej anglojęzycznej weterynarii. Przy szerokości 390 px opis ma jedną kolumnę, a szerokość dokumentu wynosi 390 px. Przełączenie na Program i specjalności zachowuje częściowy status programu. Nowa instrukcja jest dostępna przez Więcej → Instrukcje i renderuje dodany dokument.

Była to kontrola treści, struktury DOM i wymiarów w rzeczywistej przeglądarce. Zrzut ekranu nie powstał, ponieważ okno było zminimalizowane. Nie przeprowadzono oceny wizualnej na podstawie obrazu. Przestrzeń testowa została zamknięta; profil użytkownika nie był zapisywany.
