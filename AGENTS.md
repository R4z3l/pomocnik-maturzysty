# Zasady aktualizacji katalogu

Przed każdym researchem i dodaniem źródła przeczytaj `src/data/source-policy.json` oraz `docs/hierarchia-zrodel.md`.

- Priorytet1: oficjalne strony uczelni, instytutów i BIP. Priorytet2: otouczelnie.pl. Priorytet3: pozostałe portale, w tym uczelnie.pl i opinieouczelniach.pl. Priorytet4: prasa. Priorytet5: społeczności/komentarze.
- Nie pobieraj ponownie hostów i URL z rejestru wykluczeń w wskazanym zakresie. Nie wyszukuj ich ponownie celowo, nie próbuj innego schematu/trackingparametru ani przekierowania. Rejestr można zmienić wyłącznie po wyraźnym poleceniu użytkownika.
- Przed otwarciem adresu uruchom `node --experimental-strip-types scripts/check-source.ts URL current` (albo `history` dla jawnej historii progów). Wynik1 oznacza pominięcie bez pobierania. Nie używaj narzędzi browser/web do obchodzenia tej decyzji.
- Skrypty Python pobierające strony mają używać `guarded_get` z `scripts/source_policy.py`; kontrola działa również przed pobraniem celu przekierowania.
- Odrzucone informacje o konkretnej ofercie/roku są w `rejectedClaims`. Nie dodawaj ich na podstawie innego odczytu tej samej strony; pozostałe poprawne wiersze strony mogą służyć porównaniu.
- Badaj i aktualizuj WYŁĄCZNIE progi naborów2024/25,2025/26,2026/27 (konfiguracja history.admissionYears). Nie wyszukuj ani nie odświeżaj starszych lat. Zebrane wcześniej dane2022–2023 są w docs/archive i nie należą do aktywnego katalogu. Nie przywracaj ich bez polecenia użytkownika.
- Rok w nagłówku, stopce lub snippecie nie wystarcza. Sprawdzaj treść, tryb, język, poziom, campus i pierwotny dowód. Nie scalać podobnych kierunków.
- Zachowuj sprzeczne opublikowane dane z etykietą, ale nie zastępuj nimi danych oficjalnych. Potwierdzenie tej samej liczby przez portal nie dowodzi niezależności źródeł ani zgodności tur.
- W tekstach użytkowych stosuj pełne nazwy uczelni. Brak zewnętrznych API/modeli w działającej aplikacji.
- Nowe i zmieniane instrukcje dla użytkownika dodawaj do widoku „Instrukcje” w aplikacji; źródłami są pliki dokumentacji importowane przez `src/InstructionsPanel.tsx`. Uaktualniaj listę instrukcji przy dodawaniu nowego pliku i sprawdzaj widok w przeglądarce.
- Nie używaj Git bez wyraźnego polecenia użytkownika. Po zmianach wykonaj testy i walidację danych; zmiany UI potwierdź w przeglądarce.

- Przy aktualizacji przedmiotów i specjalności przeczytaj docs/przedmioty-i-specjalnosci.md i raporty audytu. Zachowaj rozróżnienie full-plan/listed-subjects/unavailable; nie nadpisuj zweryfikowanych list historycznymi skryptami ekstrakcji. Efekty uczenia, matury, legendy i sumy godzin nie są nazwami zajęć.
