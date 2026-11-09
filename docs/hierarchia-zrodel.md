Aktualny zakres historii: nabory2024/25,2025/26,2026/27. Starszych lat nie wyszukiwać, nie odświeżać ani nie przywracać z archiwum.

# Hierarchia i rejestr wykluczeń —25.10.2026

Źródło konfiguracji: `src/data/source-policy.json`. Aplikacja korzysta z niego do sortowania i oznaczania źródeł; skrypty researchu sprawdzają zakazane adresy przed pobraniem. Instrukcje dla przyszłych sesji są w AGENTS.md.

1. Oficjalna uczelnia/wydział/instytut/BIP.
2. otouczelnie.pl.
3. Pozostałe portale edukacyjne, w tym uczelnie.pl i opinieouczelniach.pl.
4. Prasa i materiały redakcyjne.
5. Społeczności i komentarze użytkowników, także na portalach o wyższym priorytecie.

Hierarchia jest kolejnością poszukiwania i prezentacji, a nie automatycznym certyfikatem poprawności. Formalne zasady bierzemy z dokumentu uczelni; portal może wskazać dokument albo uzupełnić historyczny brak z jawnym oznaczeniem. Nie zliczamy portalu kopiującego tę samą tabelę jako niezależnego potwierdzenia.

## Aktualność

Sprawdzamy rok w treści, a nie samym nagłówku. Dane historyczne zachowują własny rocznik. Nie dodajemy przeliczonego procentu skali portalowej jako wyniku matury. Błędna nazwa kierunku lub nieustalona tura nie są automatycznie poprawiane domysłem.

`excludedPages` blokuje ponowne odczyty konkretnych stron albo hosta. Zakres `all` oznacza wszystkie przyszłe aktualizacje; `current` wyklucza użycie jako informacji bieżącej, dopuszczając poprawnie oznaczoną historię. Ponowna kontrola wymaga wyraźnej zmiany decyzji użytkownika, nie samego upływu czasu. Zapis audytu pozostaje widoczny, ale nie stanowi aktywnego źródła danych.

`rejectedClaims` odrzuca konkretną informację: URL+oferta+rocznik. Nie wymaga odrzucenia pozostałych trafnych wierszy tej samej strony. Wartość ekonomii Uniwersytetu Ekonomicznego we Wrocławiu z Uczelnie.pl(2025/26) nie nadpisuje oficjalnych170pkt.

Kontrola ręczna: `node --experimental-strip-types scripts/check-source.ts URL current`. Skrypty Python: `guarded_get(url,purpose='history')`. Rejestr jest sprawdzany również przed celami przekierowań; do działania aplikacji nie dodano sieciowego importu.

## Wynik dwóch nowych audytów

Uczelnie.pl: cztery zapisane wartości Uniwersytetu Wrocławskiego mają zgodny odpowiednik w już istniejącej historii2025/26. Dopisano źródła porównawcze do tych rekordów bez dodawania kolejnych progów. Skala300/350 i portalowy procent nie służą automatycznym porównaniom ani ocenie szans. Sprzeczny wiersz ekonomii drugiej uczelni odrzucono.

Opinieouczelniach.pl: dziewięć sprawdzonych podstron nie wniosło nowych pewnych wartości do bieżącego zakresu. Zachowano informacje o kontroli. Wykluczono niespójny kalendarz (nagłówek2026/27, terminy2025/26) oraz podstronę progów Uniwersytetu Wrocławskiego z nieaktualnym uogólnieniem o publikacjach, pomijającym oficjalne dane Instytutu Filologii Romańskiej. Nie wykluczono całego portalu.


## Kontrola programów —28.10.2026

Wykluczono z bieżącego researchu wskazany w polityce PDF Informatyki stosowanej i systemów pomiarowych: nagłówek jednoznacznie określa zamknięty cykl2022–2026. Nie jest to dokument „obowiązujący od2022”, dlatego nie przypisujemy go nowym kandydatom. Pozostałe aktualnie publikowane plany z formułą „obowiązuje od…” oceniamy według treści i oficjalnego potwierdzenia, nie samej daty uchwalenia.
