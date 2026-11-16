# Uniwersytet Medyczny im. Piastów Śląskich we Wrocławiu — zakres danych

Sprawdzono 10.11.2026. Dodano 16 ofert stacjonarnych we Wrocławiu: 13 po polsku i 3 po angielsku, I stopień oraz jednolite studia magisterskie. Osobne wersje językowe dotyczą kierunku lekarskiego, lekarsko-dentystycznego i pielęgniarstwa.

## Zakres oferty

Polskojęzyczne oferty: kierunek lekarski, kierunek lekarsko-dentystyczny, farmacja, analityka medyczna, fizjoterapia, psychologia, pielęgniarstwo, położnictwo, ratownictwo medyczne, zdrowie publiczne, dietetyka, elektroradiologia i biologia medyczna. Optometria jest ofertą II stopnia, więc nie została dodana. Filia w Wałbrzychu, pozostałe filie, studia niestacjonarne i II stopnia pozostają poza zakresem.

Oferta i dokumenty programowe odnoszą się do 2026/2027. Zasady 2027/2028 nie gwarantują uruchomienia każdego naboru. Farmacja ma rozbieżne zapisy czasu: karta oferty podaje 5,5 roku, metryczka programu 10 semestrów; program obejmuje praktykę w aptece. W aplikacji zachowano oba zapisy.

## Kalkulatory i dopasowanie matury

13 ofert PL ma osobne reguły 2027/2028 oraz 2026/2027. Obsługiwany wariant to polska nowa matura pisemna. Sprawdzono tabele PDF, współczynniki, wybór różnych przedmiotów, zaokrąglenia i minima. Dwa poziomy tego samego przedmiotu nie zastępują dwóch różnych przedmiotów.

- Kierunek lekarski i lekarsko-dentystyczny: biologia PR oraz chemia, matematyka lub fizyka PR; co najmniej 100 pkt sumy i minimum dla każdego przedmiotu.
- Farmacja: w 2026/2027 obowiązkowa chemia PR oraz biologia lub matematyka PP/PR. W 2027/2028 dwa różne przedmioty spośród chemii, biologii i matematyki PP/PR.
- Analityka medyczna: biologia PR oraz chemia lub matematyka PP/PR. Fizjoterapia: biologia PP/PR oraz chemia, matematyka lub fizyka PP/PR.
- Pozostałe kierunki I stopnia: dwa różne przedmioty z listy kierunku. Dietetyka ma węższy zestaw; zdrowie publiczne dopuszcza geografię, elektroradiologia informatykę. PP ×0,8, PR ×1, zaokrąglenie składnika do liczby całkowitej. W 2027/2028 język obcy dwujęzyczny jest liczony jak PR; nie rozciągamy tego przypisu na inne procedury.
- Psychologia: w 2026/2027 obowiązkowy polski, angielski i trzeci przedmiot, PP ×0,8. W 2027/2028 polski, dopuszczony język obcy i trzeci przedmiot, PP ×0,7. PR ×1 w obu latach. Nie dodajemy zaokrąglenia, którego nie wskazuje tabela psychologii.
- Minima są rozdzielone: dokumenty 2026/2027 określają minimum 30 punktów po przeliczeniu, dokumenty 2027/2028 — dla polskiej matury 30 procent z uwzględnianego przedmiotu. Np. PP 30% daje 24 pkt przy mnożniku 0,8: może spełnić minimum procentowe 2027/28, ale nie historyczne minimum 30 pkt.

Progi 2026/2027 porównujemy z wynikiem według reguły 2026/2027. Powiązanie jest jawne w `historicalAdmissionRuleId`. Filtr dopasowania wymaga również spełnienia warunków obecnego kalkulatora. Nie rozstrzyga remisów ani indywidualnych uprawnień. Badania lekarskie, dokumenty i pozostałe wymagania należy sprawdzić w oficjalnej procedurze.

## English Division

Załącznik 5 uchwały 2918/2026 obejmuje Medicine, Dentistry i Nursing. Potwierdzono listy przedmiotów i osobny wymóg angielskiego B2. Tabela podaje PP ×1 i PR ×1,5, a odrębny ustęp o polskiej nowej maturze opisuje 1%=1 pkt. Bez rozstrzygnięcia zakresu obu zapisów nie udostępniamy automatycznej sumy ani procentu dopasowania. Karta podaje warunki i odsyła do uczelni; brak kalkulatora nie oznacza braku wzoru w dokumencie. Nie przypisujemy tym ofertom progów polskojęzycznych.

## Historia

Oficjalne zestawienie po rekrutacji: 13 wartości dla 2026/2027, 12 dla 2025/2026, 10 dla 2024/2025, łącznie 35. Odczytano wyłącznie te roczniki i część stacjonarną. Filia w Wałbrzychu jest osobnym wierszem; nie przenosimy jej progów do Wrocławia. Wiersze II stopnia i części niestacjonarnej wyłączono. Rok 2023/2024 w zbiorczym pliku pozostaje poza importem.

Tabela nazywa wartości „progiem punktowym”, bez oznaczenia tury i rozróżnienia kwalifikacja/przyjęcie. Zachowano `round: null` oraz `basis: unspecified`. Nie mylimy tych liczb z minimami formalnymi. Dostępne oficjalne dane mają pierwszeństwo przed wskazanym przez użytkownika portalem otouczelnie.pl.

## Przedmioty i luki

16 częściowych spisów nazw zajęć pochodzi z dokumentów BIP 2026/2027, właściwych dla kierunku, poziomu, języka i formy. Odczyt obejmuje 1244 pozycje z tabel godzinowych, z powtórzeniami między tabelami, rocznikami i wariantami; nie jest to liczba obowiązkowych zajęć jednej osoby. Pominięto efekty uczenia, sumy godzin, legendy i opisy programowe. Ogólne pozycje fakultatywne i nazwy rozdzielone ukośnikiem zachowują zapis dokumentu. Nie potwierdzono pełnego rozwinięcia koszyków ani semestrów, dlatego nie oznaczono ich jako pełnych planów i nie dopisano specjalności. Angielski program może zawierać polskie nazwy zajęć.

Kontrola tożsamości odrzuciła załącznik 19558: dotyczy zdrowia publicznego II stopnia, mimo pobrania w toku przeglądu strony kilku programów. Psychologia pochodzi z właściwego załącznika 18479. Parser sprawdza metryczkę, nie samą nazwę pobranego pliku.

Brak dopasowanych danych ELA i opracowanych indywidualnych analiz rynku pracy pozostaje jawną luką. Nie dodano wynagrodzeń ani prognoz zatrudnienia na podstawie podobnych kierunków.

## Aktualizacja bez AI

`npm run data:refresh -- --university umw` odtwarza propozycję częściowych list z 16 zarejestrowanych dokumentów. `npm run data:monitor -- --university umw` sprawdza zmiany oficjalnych źródeł. `npm run data:apply -- "folder"` waliduje propozycję przed zastosowaniem. Nowy cykl, zmiana wzoru, nieznany układ dokumentu i zmiana znaczenia opublikowanego progu wymagają przeglądu człowieka. Monitor nie potwierdza kompletności ani semantyki danych. Aplikacja nie pobiera danych w tle i nie wywołuje AI.

## Główne źródła

- [Oficjalny katalog rekrutacyjny](https://rekrutacja.umw.edu.pl/)
- [English Division](https://admission.umw.edu.pl/)
- [Uchwały i załączniki 2027/2028](https://bip.umw.edu.pl/artykul/195/7547/zasady-i-tryb-przyjmowania-na-studia-2027-2028)
- [Uchwały i załączniki 2026/2027](https://bip.umw.edu.pl/artykul/195/6850/zasady-i-tryb-przyjmowania-na-studia-2026-2027)
- [Statystyki po rekrutacji — odczyt wyłącznie 2024–2026](https://rekrutacja.umw.edu.pl/wp-content/uploads/2026/11/statystyki-2023-2026-2.pdf)
- [Programy studiów w BIP](https://bip.umw.edu.pl/artykuly/198/programy-studiow)

Manifest, metryczki dokumentów i lokalne dowody są w `docs/research/umw/manifest.json`. Dane aplikacji: `src/data/umw.json`, `umw-rules.json`, `curricula-umw.json`; parser tabel: `scripts/umw_curricula.py`.
