Aktualny zakres historii: nabory2024/25,2025/26,2026/27. Starszych lat nie wyszukiwać, nie odświeżać ani nie przywracać z archiwum.

# Dodawanie uczelni — procedura i prompt

Rekomendacja: dodawać uczelnie kolejno. Proces obejmuje obecnie cztery uczelnie; zakres Uniwersytetu Przyrodniczego we Wrocławiu opisuje docs/audyt-upwr.md, a zakres Politechniki Wrocławskiej i ograniczenia jej danych opisuje docs/audyt-pwr.md. Zdefiniować wspólny zakres dla wszystkich, lecz research, kontrolę i publikację wykonywać małymi pakietami. Nie utożsamiać pełnego spisu ofert z kompletem dostępnych historycznych progów.

Przed każdym odczytem sprawdzaj `src/data/source-policy.json` i stosuj `docs/hierarchia-zrodel.md`: oficjalne uczelnie → otouczelnie.pl → pozostałe portale → prasa → społeczność. Adresów wykluczonych nie pobieraj ponownie; odrzuconych informacji nie importuj.

## Mechanizm dla wersji bez API

Research wykonuje agent poza aplikacją. Wynikiem jest osobny pakiet JSON i raport audytu. Kod aplikacji nie pobiera stron ani nie wywołuje modeli. Pakiet przechodzi walidację schematu, odwołań, kompletności spisu i testów obliczeń, a następnie zostaje jawnie włączony do katalogu. To obecnie procedura plikowa; interfejs importu pakietów uczelni jest proponowanym rozszerzeniem. Dostępny w aplikacji import JSON dotyczy wyłącznie profilu użytkownika.

Docelowy interfejs importu: wybór pakietu → podgląd zmian i pokrycia → raport błędów i konfliktów → zatwierdzenie → zachowanie poprzedniej wersji. Zaktualizowany pakiet zastępuje dane na podstawie stałych identyfikatorów, zachowując osobiste notatki i oceny. Dane importowane wymagają walidacji także w przeglądarce. Nie należy ładować z pliku kodu wykonywalnego ani HTML.

## Zawartość pakietu

- Manifest zakresu: pełna nazwa uczelni, miasto/kampus, poziomy, tryb, języki, roczniki, data sprawdzenia, adres oficjalnego spisu i liczba znalezionych ofert.
- Oferty: stałe identyfikatory, indywidualne źródła, opisy, nazwy, język, poziom i czas studiów, jawne braki.
- Reguły rekrutacji: wersje według rocznika i kategorii kandydata; opcje przedmiotów, poziomy, wagi, wykluczenia, minima, warunki dodatkowe, etapy i dokumenty.
- Progi: rok, tura lub null, liczba, rodzaj (kwalifikacja/przyjęcie/nieustalony), źródło i jego kategoria. Nie utożsamiać minimum formalnego z progiem ostatniej osoby.
- Audyt: każda oferta spisu rozliczona; lista braków, rozbieżności, pominiętych ofert i przyczyn; źródła, data, metoda.

## Warunki przyjęcia pakietu

1. Każda oferta oficjalnego spisu w ustalonym zakresie ma rekord albo jawne uzasadnienie wyłączenia. Brak na stronie nie dowodzi braku kierunku.
2. Brak duplikatów i osieroconych odwołań. Nie scalać podobnych nazw ani specjalności bez dowodu tożsamości.
3. Każda liczba ma źródło i rocznik. Nie ma wymyślonych progów, szans przyjęcia ani interpolowania braków.
4. Reguła ma testy ręcznie policzonych przykładów oraz przypadków granicznych: zero/brak, lepszy poziom, wykluczenia, minimum, rozmowa, niezależne warunki językowe.
5. Rocznik oferty, rocznik zasad i rok historycznego progu są rozdzielone. Opublikowanie uchwały nie dowodzi uruchomienia wszystkich kierunków.
6. Raport pokrycia ma liczniki: oferty/spis, reguły policzalne, procedury dokumentowe, historia według lat i kategorii źródeł. Nie ma jednego procentu ukrywającego luki.
7. Osobny przegląd reguł i próbny import. Przed publikacją potwierdzić liczbę widocznych kart i przykłady obliczeń w działającej aplikacji.

## Prompt do skopiowania

Przygotuj pakiet danych dla uczelni [PEŁNA NAZWA]. Zakres: [MIASTO/KAMPUS], [TRYB], [POZIOMY], [JĘZYKI], oferta [ROCZNIK], zasady rekrutacji [ROCZNIK], progi wyłącznie dla naborów2024/25,2025/26,2026/27. Korzystaj ze schematów projektu i oficjalnych źródeł; źródła zewnętrzne dopuszczaj dla brakujących progów z jawnym oznaczeniem pochodzenia i niepewności.

Najpierw odczytaj cały oficjalny spis ofert w zakresie i zapisz manifest. Następnie rozlicz każdą pozycję: indywidualna karta, nazwa, poziom, język, czas, opis, źródła i roczniki. Sprawdzaj BIP i uchwały, także gdy bieżąca strona rekrutacyjna pokazuje starszy rok. W HTML nie przenoś zasad z ukrytego kontenera innego rocznika.

Dla zasad rekrutacji odtwórz dokładne grupy, współczynniki, dopuszczone poziomy, wybór lepszego wyniku, wykluczenia podwójnego użycia przedmiotu, minima i etapy dodatkowe. Oddziel polską nową maturę od innych kategorii. Jeśli brak wzoru punktowego, opisz procedurę dokumentową zamiast tworzyć sumę. Przedmiot niezdawany, nieznany wynik i wynik zero muszą być rozróżnione.

Dla każdego historycznego progu ustal rok, tryb, poziom, język, turę, definicję, wartość i źródło. Zachowaj sprzeczne publikacje osobno, opisz konflikt i nie uśredniaj. Nie przenoś danych z innego kampusu ani podobnego kierunku. Minimum formalne nie jest progiem przyjęcia. Brak danych zapisuj jawnie; nie zgaduj i nie generuj liczb.

Wynik: pakiet zgodny ze schematem, raport pokrycia wszystkich pozycji, źródła z datą sprawdzenia, lista luk/konfliktów i przykłady obliczeń do niezależnej kontroli. W tekstach użytkowych używaj pełnych nazw uczelni. Nie zmieniaj istniejącego katalogu przed sprawdzeniem pakietu. Nie uznawaj pliku za wdrożony, dopóki dane nie są widoczne w przeglądarce.
