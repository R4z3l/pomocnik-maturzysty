# Audyt Uczelnie.pl — Uniwersytet Wrocławski i Uniwersytet Ekonomiczny we Wrocławiu

**Data kontroli:** 2026-10-25  
**Zakres:** stacjonarne studia I stopnia/jednolite we Wrocławiu, język polski/angielski; porównanie informacji portalu z `src/data/uwr.json`, `src/data/uew.json` oraz dostarczoną kontrolą zasad rekrutacji UEW 2027/28.

## Wyniki

Uczelnie.pl publikuje dla każdego kierunku „próg (ostatni znany)”, rok, tryb i status aktualności. Odczytane strony pokazują wartości dla 2025/26 albo 2026/27; nie prezentują w treści czytelnej tabeli roczników historycznych 2022/23–2024/25. Tytuł strony zawiera „2026/27”, ale sam w sobie nie oznacza, że każdy wiersz dotyczy tego naboru.

Na stronie Ekonomii widnieją: Uniwersytet Wrocławski — 87,5/300 pkt, 2025/26, stacjonarne; Uniwersytet Ekonomiczny we Wrocławiu — 180/350 pkt, 2025/26, stacjonarne. Analogiczne bieżące wpisy Uniwersytetu Wrocławskiego to Matematyka 101,2/300, Turystyka 84/300 oraz Stosunki międzynarodowe 95,5/300, wszystkie 2025/26 i stacjonarne. Wartości UWr są takie same jak w istniejących rekordach JSON; źródło Uczelnie.pl nie daje nowego rocznika ani dodatkowej rundy.

Portal objaśnia, że wartości procentowe na stronie są stosunkiem punktów do skali danej uczelni. Nie traktuję ich jako procentu wyniku matury. Zapisy `/300` i `/350` nie są tu dowodem, że oficjalna uczelniana reguła rekrutacji ma tę samą skalę ani że wynik można porównywać między uczelniami.

Wartość UEW 180/350 dla Ekonomii z 2025/26 jest sprzeczna z oficjalnym źródłem progów UEW zapisanym w `src/data/uew.json`, które podaje 170. Nie importuję wartości portalowej jako nowej lub skorygowanej danej. Wymaga wyjaśnienia, czego dokładnie dotyczy licznik i mianownik użyty przez portal.

Portalowy wiersz „Stosunki Międzynarodowe” dla UEW (170/350, 2025/26) nie jest mapowany na rekord UEW: w danych uczelni występują „Międzynarodowe stosunki gospodarcze”, co nie jest tą samą nazwą kierunku. Nie przenoszę progu między nimi.

## Kierunki, język i czas trwania

Na odczytanych listach UWr strona kierunku nie daje kart programu ani potwierdzenia czasu trwania. Nie zmieniam metadanych programu na podstawie listy progowej. Lista programów UEW w `src/data/uew.json` obejmuje też pięć kierunków anglojęzycznych, lecz wskazane strony progowe nie potwierdzają dla nich ofert ani czasu studiów. Czas trwania UEW pozostaje nieustalony (`null`); nie wyciągam go z samego progu.

## Zasady rekrutacji 2027/28

Uczelnie.pl w zbadanych podstronach nie publikuje reguł rekrutacji, wzorów punktacji ani podstawy do uaktualnienia zasad na 2027/28. Dla UEW obowiązuje ustalenie z dostarczonej kontroli dokumentu pierwotnego: uchwała R.0000.26.2026 istnieje i określa zasady 2027/28, mimo że strona informacyjna Biura Rekrutacji może być starsza. Portal nie jest źródłem do potwierdzania ani zastępowania tych zasad. Progi historyczne nie są progami przyszłego naboru.

## Ograniczenia i rozstrzygnięcia

- Zachowuję Uczelnie.pl jako źródło wtórne, z jawną prowieniencją URL, rokiem i trybem widocznym na stronie.
- Nie dodaję progów 2022/23–2024/25: na otwartych stronach brak tych roczników. Nie odtwarzam ich z wyników wyszukiwarki ani z ogólnego tytułu strony.
- Wartości z 2025/26 dla UWr są zgodne z istniejącymi danymi; zapisuję je jako kandydatury porównawcze, nie jako uzupełnienia historii.
- Odrzucam konflikt UEW Ekonomia i nie mapuję UEW „Stosunki Międzynarodowe” do „Międzynarodowych stosunków gospodarczych”.
- Nie stwierdzono konkretnych nowych programów, języków, czasu trwania ani zasad 2027/28 do dodania z Uczelnie.pl.

## Sprawdzone strony

- [Ekonomia](https://www.uczelnie.pl/progi-punktowe/ekonomia)
- [Matematyka](https://www.uczelnie.pl/progi-punktowe/matematyka)
- [Turystyka](https://www.uczelnie.pl/progi-punktowe/turystyka)
- [Stosunki międzynarodowe](https://www.uczelnie.pl/progi-punktowe/stosunki-miedzynarodowe)

