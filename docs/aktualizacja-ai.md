# Aktualizacja danych z pomocą AI w domu

Możesz zlecić aktualizację w rozmowie z agentem, który ma dostęp do tego folderu oraz do stron źródłowych. Dostęp abonamentowy może służyć do pracy w takiej sesji; aplikacja nie wywołuje modelu ani płatnego API. Sam abonament nie oznacza, że każda usługa AI ma dostęp do lokalnych plików lub internetu — zależy to od używanego narzędzia i jego uprawnień.

Instrukcje możesz czytać w aplikacji w sekcji „Instrukcje”. Są włączane z plików projektu podczas budowania aplikacji; nowe lub zmienione teksty pojawią się po aktualizacji i ponownym zbudowaniu wersji online.

## Jak uruchomić aktualizację

1. Zapisz i wyeksportuj profil z aplikacji w bezpieczne miejsce poza projektem. Nie dołączaj go do aktualizacji danych.
2. Otwórz projekt w agencie i napisz, co ma odświeżyć. Możesz skopiować polecenie z końca tej instrukcji.
3. W głównym folderze projektu uruchom `npm run update:start`. Polecenie tworzy nowy folder w `output/aktualizacje-ai/` i wyświetla jego pełną ścieżkę. Wewnątrz znajdują się `przed` — kopia referencyjna, `propozycja` — oddzielna kopia do pracy, oraz manifest kontrolny. Nie edytuj kopii `przed` ani manifestu.
4. Przekaż agentowi pełną ścieżkę `propozycja`. W niej powinien pracować, dokumentować źródła i uruchomić kontrole. W pierwszej kolejności czyta zasady projektu i politykę źródeł z kopii, a dla programów dodatkowo dokumentację audytu przedmiotów. Nie powinien prowadzić researchu na wykluczonych stronach.
5. W folderze `propozycja` uruchom kolejno `npm test`, `npm run validate:data`, `npm run build` i `npm run check:release`. Jeśli kopia znajduje się w tym samym projekcie i ma dostęp do nadrzędnego `node_modules`, nie trzeba kopiować zależności. Na innym komputerze lub poza projektem najpierw zainstaluj zależności z `package-lock.json`, np. `npm ci`, po sprawdzeniu wersji Node w README.
6. W głównym folderze projektu uruchom `npm run update:report -- "PEŁNA ŚCIEŻKA FOLDERU AKTUALIZACJI"`. Ścieżka dotyczy folderu zawierającego `przed` i `propozycja`, nie jednej z tych podfolderów. Otwórz zapisany tam `raport-zmian.md`. Polecenie ponownie sprawdza integralność kopii referencyjnej, porównuje pliki propozycji i wskazuje zmiany w aktywnym projekcie od chwili wykonania kopii.
7. Przejrzyj raport i źródła. Jeśli aktywna wersja zmieniła się w międzyczasie, połącz zmiany ostrożnie — nie zastępuj całego folderu kopią. Włącz do projektu tylko sprawdzone pliki; zachowaj poprzednie pliki z `przed`. Po włączeniu powtórz testy, walidację, build i kontrolę w przeglądarce. Jeżeli wynik testów lub odczyt źródła jest niepewny, zachowaj poprzednią wersję danej informacji.
8. Jeżeli witryna została już skonfigurowana jako prywatna i chcesz ją zaktualizować, korzystaj z `docs/publikacja-prywatna.md`. Aktualizacja plików lokalnych nie publikuje ich automatycznie.

Kopie zawierają kod, dane, instrukcje i materiały badawcze, ale nie kopiują profilu z pamięci przeglądarki ani `node_modules`. Mogą być duże, bo zawierają lokalne dokumenty źródłowe. Traktuj je jako prywatne pliki projektu. Nigdy nie wysyłaj na hosting folderów `przed`, `propozycja` ani całego projektu — instrukcja publikacji opisuje osobno folder `dist`.

## Co obejmuje raport

Raport wymienia dodane, usunięte i zmienione pliki w kodzie, danych, testach, skryptach i dokumentacji. Dla zmienionych plików JSON w `src/data` pokazuje ścieżki pól oraz skrócone wartości przed i po zmianie; rekordy z jednoznacznym `id` lub `programmeId` porównuje po identyfikatorach. Dla innych plików sygnalizuje konieczność ręcznego przeglądu. Przy dużych zmianach niektóre wartości i dalsze pozycje są ucinane: należy sprawdzić pełne pliki oraz źródła. Raport jest podglądem, nie dowodem poprawności i nie wykonuje testów.

Jeśli kopia `przed` zmieni się w stosunku do manifestu, raport przerwie pracę. Manifest jest lokalną kontrolą przypadkowych zmian, a nie podpisem kryptograficznym chroniącym przed osobą mogącą zmienić zarówno manifest, jak i kopię. Raport wyróżnia zmianę `source-policy.json`; rejestr wykluczeń można zmienić wyłącznie na wyraźne polecenie użytkownika.

## Polecenie do skopiowania dla AI

> Zaktualizuj w kopii `propozycja` dane dotyczące: **[wpisz uczelnię, kierunek lub rodzaj informacji]**. Pracuj tylko w zakresie projektu: Uniwersytet Wrocławski i Uniwersytet Ekonomiczny we Wrocławiu, Wrocław, studia stacjonarne pierwszego stopnia i jednolite, po polsku i angielsku, chyba że zlecę inny zakres. Nie zmieniaj aktywnej aplikacji ani kopii `przed` podczas researchu.
>
> Przeczytaj `AGENTS.md`, `src/data/source-policy.json` i `docs/hierarchia-zrodel.md`. Przed otwarciem każdego adresu wykonaj wymaganą kontrolę źródła; respektuj wykluczenia i odrzucone twierdzenia. Stosuj kolejność: oficjalne źródła uczelni, otouczelnie.pl, inne portale, prasa, społeczności. Zachowuj datę sprawdzenia, rocznik, język, poziom, tryb, turę, pochodzenie, sprzeczności i braki; nie dopisuj niepotwierdzonych danych. Progi badaj wyłącznie dla naborów 2024/25, 2025/26 i 2026/27, o ile użytkownik nie zmieni tego zakresu. Nie odświeżaj starszych lat.
>
> Jeśli aktualizujesz przedmioty lub specjalności, przeczytaj `docs/przedmioty-i-specjalnosci.md` i raporty audytu. Nie nadpisuj zweryfikowanych danych historycznymi skryptami. Rozróżnij pełny plan, częściowy wykaz i brak potwierdzenia; nie przypisuj zajęć do semestru bez podstawy w dokumencie.
>
> Zapisz w kopii propozycję oraz raport merytoryczny z linkami, datami, lukami, niepewnością i uzasadnieniem każdej zmiany. Uruchom testy, walidację danych, build i kontrolę paczki; dla zmian widocznych w aplikacji sprawdź ją również w przeglądarce. Następnie wygeneruj raport techniczny poleceniem `update:report` z folderu głównego. Porównaj także aktywny projekt od czasu utworzenia kopii. Nie traktuj wyniku testów ani automatycznego raportu jako dowodu poprawności źródeł. Włączaj tylko zweryfikowane zmiany, nie nadpisuj nowszej pracy i ponownie wykonaj kontrole po włączeniu. Nie korzystaj z Git ani nie publikuj strony bez mojego polecenia.

Gdy chcesz dodać nową uczelnię, skorzystaj dodatkowo z dokładniejszego promptu w `docs/dodawanie-uczelni.md`.
