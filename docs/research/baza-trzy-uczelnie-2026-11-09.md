# Odbiór katalogowej bazy trzech uczelni — 09.11.2026

Zakres potwierdzony przez użytkownika: Uniwersytet Wrocławski, Uniwersytet Ekonomiczny we Wrocławiu i Politechnika Wrocławska; 171 ofert stacjonarnych I stopnia i jednolitych we Wrocławiu, PL/EN. Odbiór dotyczy warstwy katalogowej i utrzymania bazy, z jawnymi brakami zgodnie z planem aplikacji. Nie obejmuje ukończenia wszystkich modułów doradczych ani pełnego audytu szczegółowych sylabusów każdego zajęcia.

## Kryteria i wynik

| Kryterium | Wynik |
| --- | --- |
| Tożsamość oferty: uczelnia, poziom, język, lokalizacja, identyfikator i rocznik | 171/171, bez łączenia podobnych kierunków |
| Opis i źródła | 171/171 |
| Czas studiów właściwego rocznika | 171/171 |
| Reguła lub jawna procedura dokumentowa | 159 kalkulatorów i 12 procedur dokumentowych |
| Spis zajęć i pochodzenie danych | 171/171: 88 pełnych planów wskazanego cyklu, 83 listy częściowe |
| Brak potwierdzonego spisu | 0; uzupełniono European Cultures |
| Historia naborów wyłącznie 2024/25, 2025/26, 2026/27 | 604 rekordy; brakujące roczniki i oferty nadal opisane jako braki |
| Aktualizacja bez AI | 66 adapterów i monitor zarejestrowanych oficjalnych źródeł; osobna propozycja i zastosowanie po kontrolach |
| Wykluczenia i ochrona danych | Rejestr wykluczeń bez zmian; błąd parsera nie nadpisuje aktywnej bazy |

## European Cultures

Oficjalna uchwała Senatu Uniwersytetu Wrocławskiego nr 168/2023 z 21.06.2023 ustala program dla cykli od 2023/24. Pełny 57-stronicowy PDF jest w `curricula/uwr-a/european-cultures-program-2023.pdf`. Metryczka: strony 1–2; plan: strony 51–56. Wszystkie tabele planu sprawdzono wizualnie po renderowaniu. Wynik: 59 wpisów w 14 grupach, sześć semestrów, pięć pul wyboru, osobne oznaczenie języka polskiego dla cudzoziemców i 60 godzin WF w przedziale II–V semestru.

Transkrypcja jest w `curricula/uwr-a/european-cultures-semesters.json`. `scripts/european_cultures.py` sprawdza skróty PDF i transkrypcji; zmiana dokumentu zatrzymuje adapter. Nie oznacza to potwierdzenia niezmienionego programu 2027/28. Poprzedni raport o braku spisu był wynikiem sprawdzenia samych kart opisowych i jest zastąpiony odczytem dokumentu Senatu.

## Politechnika Wrocławska

Zweryfikowano wszystkie 62 plany 2026/27 z oficjalnego serwisu sylabusów: 644 tabele wszystkich semestrów, 763 rozwijane grupy i 5788 rzeczywistych wierszy zajęć. Sprawdzane są także zagnieżdżone koszyki ukryte w interfejsie; nie ma nieodczytanych tabel ani odsyłaczy do grup. Poszczególne nazwy powtarzające się w semestrze i grupie są prezentowane jednokrotnie. Grupy pozostają alternatywami, nie sumą obowiązkowych zajęć jednej osoby.

W poprzednich 7104 wpisach były także nazwy koszyków i instrukcje typu „Student/ka wybiera…”. Nagłówki grup przeniesiono do tytułów, a instrukcje usunięto z przedmiotów. Dodano regresję odrzucającą taki tekst, przy zachowaniu rzeczywistego przedmiotu „Zajęcia uzupełniające - język angielski”.

Oficjalne kopie źródeł: `pwr/syllabi`. Odtwarzalny parser: `scripts/pwr_curricula.py`, uruchamiany przez `data:refresh`. Starszy `build-pwr.py` pozostaje checkpointem poprzedniego audytu i nie służy do nadpisywania obecnego pliku kanonicznego. WF i języki pozostają ogólnymi pozycjami, jeżeli sam plan odsyła do oferty Studium; pełny odczyt planu nie wymaga pobierania każdej szczegółowej karty kursu.

## Jawne ograniczenia

- 83 spisy Uniwersytetu Wrocławskiego pozostają listami częściowymi. Mają własny rocznik, status i źródła. Nie uznano ich za pełne ani za potwierdzone na 2027/28. Rozbudowany audyt wszystkich sylabusów jest osobnym rozszerzeniem w planie aplikacji.
- Brak progu w konkretnym roczniku nie jest zerem, dowodem braku rekrutacji ani podstawą do przenoszenia wartości podobnego kierunku. Nie wymyślono nowych progów.
- Aktualny program lub uchwała o regułach nie potwierdzają uruchomienia każdej oferty 2027/28. Terminy i warunki przyszłego naboru wymagają dalszych publikacji uczelni.
- Dane absolwentów i zweryfikowane ścieżki zawodowe nadal mają luki, szczególnie dla Politechniki Wrocławskiej. To dalszy zakres doradczy, poza odbiorem tej warstwy katalogowej.
- Nie włączono stałego harmonogramu, publikacji strony ani automatycznego przyjmowania zmian wymagających interpretacji. Nie wykonano operacji Git.

Kontrole techniczne obejmują pełne lokalne materiały wszystkich 62 planów Politechniki Wrocławskiej, transkrypcję European Cultures, testy aplikacji, walidację danych, TypeScript, build i paczkę produkcyjną. Wyniki poszczególnych zastosowań są w `output/data-refresh/runs/`, wraz z materiałami i kopiami poprzednich danych.

Końcowe wyniki: 32/32 testy aplikacji, 12/12 testów aktualizatora, walidacja 171/171 spisów i 88 pełnych planów, TypeScript, build i kontrola paczki — powodzenie. Przeglądarka: European Cultures i Architektura, oddzielne grupy obowiązkowe/warunkowe/wyboru, nowe pokrycie i instrukcja 66 adapterów; szerokość 390 px bez poziomego overflow. Powtórny odczyt wszystkich 66 adapterów nie przygotował żadnego zmienionego pliku.
