# Dopasowanie matury

Moduł otworzysz przyciskiem „Dopasuj kierunki do mojej matury” w katalogu, z widoku „Mój profil” albo z menu „Więcej” → „Dopasowanie matury”. Korzysta z tego samego profilu co kalkulatory kierunków. Zmiany działają od razu; trwały zapis wymaga przycisku „Zapisz profil”.

## Jak korzystać

1. W profilu zaznacz zdawane rozszerzenia i wpisz procenty. Podstawy oraz poziom dwujęzyczny uzupełnij w odpowiedniej części profilu. Brak procentu różni się od wyniku 0%.
2. Otwórz dopasowanie. Kierunki są ułożone od największego udziału punktów za Twoje rozszerzenia. Filtruj uczelnię, język i nazwę kierunku.
3. Sprawdź „Twoje punkty” i obliczenie wiersz po wierszu. Dodatkowe egzaminy lub potwierdzenia wpisuje się w karcie kierunku. Niepełny kalkulator nie oznacza niespełnienia wszystkich warunków.
4. Sprawdź progi 2026/2027. To poprzedni nabór względem planowanego rozpoczęcia studiów 2027/2028. Każdy próg zachowuje źródło, status, turę lub ustalenie i uwagę o definicji.
5. Włącz „Osiągam próg 2026/27 i warunki kalkulatora”, aby zobaczyć oferty z wynikiem co najmniej równym jednemu porównywalnemu oficjalnemu progowi. To nie gwarancja przyszłego przyjęcia. Pozostałe wymagania, dokumenty i język trzeba sprawdzić oddzielnie.

## Dlaczego taka kolejność

Mierzymy zestaw rozszerzeń, nie liczbę wspólnych nazw przedmiotów. Dla każdej reguły wykonujemy dwie symulacje: wszystkie dopuszczone rozszerzenia na 100% oraz tylko Twoje rozszerzenia na 100% (pozostałe na 0%). Stosunek sum składników maturalnych PR jest miarą dopasowania. Korzystamy z tego samego kalkulatora: wagi, wybór najlepszego przedmiotu, wykluczenia i szczególne zasady Politechniki Wrocławskiej pozostają zachowane. Egzaminy dodatkowe i PP nie wchodzą do tej miary. Wybrane rozszerzenie z nieznanym lub zerowym wynikiem nadal należy do zestawu; rzeczywisty wynik liczy się osobno.

100% oznacza pokrycie maksymalnej punktacji za rozszerzenia, a nie prawdopodobieństwo przyjęcia. Remisy rozstrzyga alfabetycznie nazwa kierunku, następnie identyfikator oferty. Oferty bez reguły punktowej są na końcu i mają jawny brak oceny. Same punkty różnych uczelni nie ustalają kolejności, ponieważ mają różne skale. Zaokrąglenie wyświetlania nie wpływa na ranking ani filtr.

## Porównanie z poprzednim naborem

Wynik do progu obliczamy według zweryfikowanej reguły tego samego naboru. Obecnie takie osobne zasady są w bazie dla Uniwersytetu Ekonomicznego we Wrocławiu na 2026/2027. Zasady 2027/2028 dodają biznes i zarządzanie; jego punktów nie przenosimy do historycznego porównania. Pokazujemy obydwa wyniki oraz różnicę historyczny wynik minus próg, osobno przy każdym ustaleniu. Filtr wymaga kompletnego wyniku i spełnienia warunków objętych obydwoma kalkulatorami.

Dla Uniwersytetu Wrocławskiego, Politechniki Wrocławskiej i Uniwersytetu Przyrodniczego we Wrocławiu pokazujemy dostępne progi 2026/2027, ale nie obliczamy różnicy bez potwierdzonego wzoru historycznego. Progi zewnętrzne nie włączają oferty do filtra. Brak progu, nieznana porównywalność i niepełny profil nie są interpretowane jako wynik poniżej progu.

Wszystkie ustalenia zachowujemy. Filtr mówi o co najmniej jednym progu, nie o każdym z nich i nie o wybranej po cichu turze. Publikacja uczelni może nie rozróżniać kwalifikacji od przyjęcia; etykieta pozostaje widoczna. Starszą historię 2024/2025–2025/2026 można sprawdzić w karcie kierunku.

## Utrzymanie

Logika: `src/maturaMatching.ts`, widok: `src/MaturaMatchingPanel.tsx`. Nowe porównania historyczne wymagają osobnej zweryfikowanej reguły właściwego roku; sam rocznik lub oficjalny status progu nie dowodzi zgodności wzoru. Rok porównania jest jawny i nie przesuwa się automatycznie z datą urządzenia. Moduł nie pobiera danych i nie używa AI ani zewnętrznych API.
