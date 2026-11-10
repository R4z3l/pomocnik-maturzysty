# Aktualizacja bazy z internetu bez AI

Baza obejmuje Uniwersytet Wrocławski, Uniwersytet Ekonomiczny we Wrocławiu i Politechnikę Wrocławską. Pobieranie uruchamia zwykły skrypt na komputerze z projektem. Nie wywołuje modeli, nie potrzebuje klucza API i nie zużywa tokenów. Działająca strona nadal korzysta wyłącznie z zapisanych plików.

## Pierwsze uruchomienie

Potrzebne są Node.js 24, Python 3.12 lub nowszy oraz zainstalowane zależności projektu. W folderze projektu wykonaj:

```powershell
npm ci
python -m pip install -r requirements-data.txt
```

Narzędzia pobierania i odczytu mają licencje Apache-2.0 lub MIT: requests, Beautiful Soup i pdfplumber. Nie wymagają abonamentu AI.

## Pobranie danych i propozycja zmian

Kliknij dwukrotnie `Aktualizuj-baze.cmd` albo wykonaj:

```powershell
npm run data:refresh
```

Polecenie zapisze folder uruchomienia w `output/data-refresh/runs/` i wyświetli ścieżkę `report.md`. Otwórz ten raport. W tym samym folderze są `report.json`, pobrane materiały w `evidence`, propozycja w `proposal` oraz lista luk z identyfikatorami w `coverage.json`. Pobranie nie zmienia aktywnej bazy.

Adaptery automatycznie odczytują:

- Oficjalną tabelę progów Politechniki Wrocławskiej: nabory 2024/25, 2025/26 i 2026/27, osobne tury i wyłączenie filii.
- Oficjalne tabele progów Uniwersytetu Ekonomicznego we Wrocławiu: te same trzy roczniki. Brak podanej tury pozostaje brakiem; kierunki filii nie są dopasowywane do Wrocławia.
- Czas studiów 20 ofert Uniwersytetu Ekonomicznego we Wrocławiu z metryczek audytowanego programu 2026/27. Adapter sprawdza nazwę, poziom, język i formę. Nie przenosi czasu studiów z podobnego kierunku.
- Pełne opublikowane plany wszystkich 62 ofert Politechniki Wrocławskiej: wszystkie semestry, tabele i rozwijane koszyki, w tym zagnieżdżone. Nieznany układ, brak zakładki lub nieodczytany koszyk zatrzymuje propozycję. Nazwy grup są oddzielone od nazw zajęć; instrukcje wyboru są pomijane.
- Plan European Cultures Uniwersytetu Wrocławskiego z uchwały 168/2023: wizualnie sprawdzono sześć semestrów i przypisy. Adapter korzysta z transkrypcji wyłącznie przy identycznych skrótach PDF i pliku sprawdzonych nazw. Zmieniony dokument wymaga nowego przeglądu.

Domyślny przebieg obejmuje 94 adaptery: cztery wspólne źródła tabel, metryczek i planu European Cultures oraz 62 plany Politechniki Wrocławskiej i 28 planów Uniwersytetu Przyrodniczego we Wrocławiu. Może trwać dłużej niż samo sprawdzenie progów. Wszystkie propozycje są w jednym raporcie.

Znany dokument PDF ma sprawdzane konkretne strony metryczek. Gdy uczelnia zmieni układ lub zastąpi dokument, brak zgodności zatrzyma adapter zamiast zgadywania. Nowa uchwała lub zmiana wzoru punktacji wymaga sprawdzenia i ewentualnej zmiany parsera przez osobę utrzymującą projekt.

## Zastosowanie sprawdzonej propozycji

Po przeczytaniu raportu wykonaj, podając rzeczywisty folder wyświetlony przez poprzednie polecenie:

```powershell
npm run data:apply -- "PEŁNA ŚCIEŻKA FOLDERU URUCHOMIENIA"
```

Polecenie uruchomi testy, walidację danych, kontrolę typów, build i kontrolę paczki w oddzielnej kopii walidacyjnej. Dopiero po powodzeniu kopiuje do bazy pliki propozycji. Wyniki kontroli zapisuje w plikach `check-*.log`, a poprzednie dane w `backup`. `coverage-after.json` pokazuje pokrycie po zmianie. Gdy aktywne dane lub parser zmieniły się od pobrania, uruchom pobieranie ponownie. Zmodyfikowana propozycja albo błąd kontroli zatrzymują zastosowanie.

Nie edytuj ręcznie `report.json`, manifestów ani gotowej propozycji. To lokalne zabezpieczenia przed przypadkowymi zmianami, nie podpis cyfrowy. Po przerwaniu procesu zastosowania przez wyłączenie komputera porównaj bazę z `backup` i ponownie uruchom kontrole przed dalszą pracą. Jeśli po przerwanym uruchomieniu pozostał `output/data-refresh/refresh.lock`, usuń go dopiero po sprawdzeniu, że poprzedni proces zakończył działanie.

Zastosowanie danych nie przebudowuje aktywnego `dist` ani nie publikuje strony. Do przygotowania aktualnej wersji produkcyjnej wykonaj `npm run build` i `npm run check:release`; zasady udostępniania opisuje instrukcja „Prywatna wersja online”.

## Kontrola pozostałych źródeł

```powershell
npm run data:monitor
```

Monitor pobiera zarejestrowane oficjalne źródła czterech uczelni: karty, programy, dokumenty zasad i źródła historii. Obsługuje HTML, PDF, dokumenty Word, arkusze i archiwa ZIP. Dokumenty binarne porównuje po skrócie pliku; nie wykonuje makr ani nie rozpakowuje archiwów. Przestrzega wykluczeń, także przed przekierowaniem. Nie wyszukuje starszych progów. Nie pobiera portali niższego priorytetu i nie odkrywa samodzielnie całego internetu.

Pierwsze uruchomienie tworzy punkt odniesienia. Następne rozpoznają zmienioną treść albo link do dokumentu. Status `changed` oznacza potrzebę przeglądu, a nie automatyczne potwierdzenie nowej informacji. Status `baseline-created` nie potwierdza zgodności strony z bazą. Monitor nie podmienia list zajęć, zasad ani opisów kierunków. Pozwala zauważyć ich zmianę bez okresowego zlecania researchu AI.

Źródła bez adaptera wymagają przeglądu człowieka. Może on przepisać zmianę ręcznie lub zlecić jednorazowo rozbudowę parsera. Szczególnie dotyczy to skanów PDF, zmian nazw i wariantów ofert, nowych zasad rekrutacji oraz potwierdzania kompletności programu. Pobranie PDF nie jest równoznaczne z potwierdzeniem całego planu na nowy nabór.

Przykładowe ograniczenie zakresu:

```powershell
npm run data:monitor -- --university uwr
npm run data:refresh -- --source pwr-thresholds
npm run data:sources
npm run data:coverage
```

Zwykły odczyt wykorzystuje kopię pobraną w ciągu ostatnich 24 godzin. Starsze materiały są sprawdzane w sieci z nagłówkami warunkowymi, jeśli serwer je udostępnia. `--force` wymusza sprawdzenie sieci przed upływem doby; nie omija polityki źródeł. Błąd odczytu nie oznacza wygaśnięcia dokumentu. Folder `output` zawiera cache i materiały robocze; nie należy przesyłać go na hosting ani do repozytorium.

## Okresowa praca bez rozmowy z agentem

Te same komendy można uruchamiać z Harmonogramu zadań Windows albo z własnego systemu CI. Nie trzeba otwierać rozmowy. Dla pobierania wybierz program `python`, argumenty `scripts/refresh_data.py run` i katalog roboczy projektu. Dla monitorowania dopisz `--mode monitor`. Proces wymaga działającego komputera i internetu. Nie uruchamiaj równolegle kilku aktualizacji; blokada chroni wspólny cache i zastosowanie danych.

W projekcie nie włączono stałego harmonogramu. Częstotliwość i maszynę wykonującą zadanie można wybrać osobno. Raport nadal trzeba przejrzeć przed zastosowaniem zmian. Przegląd raportu nie wymaga AI.

## Stan i ograniczenia bazy

Aktualne liczby są wyliczane w „Źródła i pokrycie” → „Stan bazy wiedzy”. Raport rozróżnia pełne plany, częściowe spisy i brak potwierdzenia. Do braków danych nie podstawiamy zer ani treści z podobnych kierunków. Automatyczne pobieranie nie uzupełni dokumentu, którego uczelnia nie opublikowała. Częściowe listy Uniwersytetu Wrocławskiego zachowują ten status do sprawdzenia pełnego dokumentu; nie stają się pełne po samym pobraniu. Pełny plan wskazanego cyklu nie jest gwarancją programu naboru 2027/28.

Testy mechanizmu bez wykonywania żądań sieciowych:

```powershell
npm run test:data-refresh
```

Dotychczasowa procedura aktualizacji z pomocą AI pozostaje opcją dla zmian wymagających opracowania. Nie jest potrzebna do pobierania, monitorowania ani zastosowania propozycji z obsługiwanych adapterów.

## Uniwersytet Przyrodniczy we Wrocławiu

`npm run data:refresh -- --university upwr` przygotowuje propozycję dla 28 pełnych spisów planów cyklu 2026/2027, bez korzystania z AI. Parser zachowuje semestry i koszyki wyboru oraz sprawdza tożsamość kierunku, języka weterynarii, formę, poziom i liczbę semestrów. Nowy cykl wymaga przeglądu człowieka. Monitor obejmuje również oficjalne karty IRK i zasady 2027/2028. Nie pobiera portali z progami; 53 wartości portalu otouczelnie.pl z audytu 10.11.2026 mają odrębny status i rocznik. Więcej w instrukcji „Uniwersytet Przyrodniczy we Wrocławiu — zakres danych”.
