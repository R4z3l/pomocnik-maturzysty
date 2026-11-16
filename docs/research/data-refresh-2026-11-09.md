# Sprawdzenie pobierania bazy bez AI — 9 listopada 2026

Zakres: Uniwersytet Wrocławski, Uniwersytet Ekonomiczny we Wrocławiu i Politechnika Wrocławska. Pobieranie przez kontrolę CLI źródeł oraz `guarded_get`; rejestr wykluczeń pozostał bez zmian. Nie zmieniono wzorów punktacji ani zakresu roczników historii.

## Wykonane odczyty i zastosowanie

- Oficjalne tabele Politechniki Wrocławskiej: 594 komórki trzech tur z naborów 2024/25–2026/27; 387 wartości przypisanych do obecnego katalogu. Brak nowych wartości względem dotychczasowego importu. Filie, braki i nieuruchomione oferty pozostają odrębne.
- Oficjalna zbiorcza tabela Uniwersytetu Ekonomicznego we Wrocławiu: 81 wierszy z trzech roczników, z czego 79 przypisanych do 20 obecnych ofert. Dwa wiersze filii nie są importowane. Rozwinięcia dopisku „studia w j. angielskim” są jawnie sprawdzane wraz z językiem oferty; nie ma dopasowania przez podobieństwo nazwy.
- Oficjalny program Uniwersytetu Ekonomicznego we Wrocławiu, uchwała R.0000.18.2026: 20 jednoznacznie dopasowanych metryczek. Uzupełniono 18 czasów po 6 semestrów i dwa po 7 semestrów. Każda oferta wskazuje nowe oficjalne źródło czasu studiów. Dotyczy programu 2026/27, nie gwarancji naboru 2027/28.
- Zastosowanie propozycji objęło trzy pliki po testach, walidacji danych, TypeScript, buildzie i kontroli paczki w oddzielnej kopii. Poprzednie pliki zachowano lokalnie w backup. Powtórne przygotowanie z tych samych źródeł dało zero zmienionych plików.

Lokalny raport zastosowania: `output/data-refresh/runs/20261109-180601-c2hywonn/report.md`; materiały, wynik parsera i logi pięciu kontroli są w tym samym folderze. Plik `coverage-after.json` pokazuje pokrycie po zmianie. Folder output jest wykluczony z repozytorium.

## Kontrola źródeł

Pierwszy monitor obejmował 459 pozycji rejestru. Dla trzech ZIP i jednego XLS rozpoznano brak obsługi ich typu w monitorze. Rozszerzono monitorowanie o porównywanie binarnych kopii dokumentów Word, arkuszy i ZIP, bez wykonywania makr lub rozpakowywania. Kolejne uruchomienie objęło także nowo dodany oficjalny opis European Cultures: 460 pozycji, zero błędów; 455 wykorzystanych kopii cache i 5 nowych materiałów.

To kontrola możliwości pobrania i materiał porównawczy, nie nowy audyt merytoryczny 460 dokumentów. Pierwszy zapis strony tworzy punkt odniesienia; nie dowodzi zgodności jej aktualnej treści z kanonicznym JSON. Raport: `output/data-refresh/runs/20261109-180447-xef8nwqg/report.md`.

## European Cultures i kompletność

Ponownie odczytano oficjalną kartę rekrutacyjną oraz https://hist.uwr.edu.pl/european-cultures/. Strona instytutu podaje obszary kształcenia i elastyczną organizację, ale nie identyfikowalną listę tytułów zajęć. Kopia: `curricula/uwr-a/european-cultures-2026-11-09.html`. Status `unavailable` zachowano i dodano źródło. Odczyt innej, starej domeny study.uni.wroc.pl nie przeszedł weryfikacji certyfikatu; nie obchodzono tego błędu i nie wykorzystano jej treści do importu.

Pozostaje 25 pełnych planów, 145 spisów częściowych i jeden brak. Automatyczne pobieranie nie jest podstawą do zmiany statusu na full-plan. Baza obejmuje 171 ofert, 604 progi, czas studiów wszystkich 171 ofert oraz 70 kohort ELA przypisanych do 69 ofert.

## Kontrole końcowe

- 29 testów aplikacji oraz 10 testów aktualizatora; pełne lokalne tabele i plan 20 ofert, bez sieci w testach aktualizatora.
- Odrzucenie nieznanego układu, konflikt bez nadpisania starej wartości, odrzucone twierdzenie, wykluczenie przed żądaniem i przed przekierowaniem, limit strumienia, wykrycie zmiany linku do planu, stara lub zmodyfikowana propozycja.
- Walidacja 171 ofert i źródeł, TypeScript, build i kontrola paczki — powodzenie. Pozostaje istniejące informacyjne ostrzeżenie wielkości bundla.
- Przeglądarka: nowy raport trzech uczelni, czas 20/20 dla Uniwersytetu Ekonomicznego we Wrocławiu, poprawny mianownik ELA 69/171, instrukcja z poleceniami refresh/apply/monitor; szerokość 390 px bez poziomego overflow.

Nie uruchomiono stałego harmonogramu, nie opublikowano strony i nie wykonano operacji Git. Zmiany pozostają w lokalnym projekcie.
