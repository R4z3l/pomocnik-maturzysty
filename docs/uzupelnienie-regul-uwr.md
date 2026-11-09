# Stan po integracji — 25.10.2026

Wszystkie29 reguł zintegrowano; katalog ma77 kalkulatorów Uniwersytetu Wrocławskiego i12 opisanych procedur dokumentowych. Dodatkowe etapy są obsługiwane w profilu i panelu kierunku, minimum240 dla matur jest niezależne od punktów rozmowy. Po rozszerzeniu listy formularza dodano grecki i kulturę antyczną do jawnej listy przedmiotów indywidualnych studiów międzydziedzinowych oraz biznes i zarządzanie / grecki do grup „inny przedmiot” na podstawie ich otwartego brzmienia (21 reguł). Odtworzono widoczne wzory z aktualnych grup. Pozostałe formalnie dozwolone przedmioty poza formularzem wymagają ręcznego przeliczenia.

Poniżej transkrypcje i zapis przygotowania pakietu przed integracją.

---

# Uzupełnienie zasad Uniwersytetu Wrocławskiego — 25.10.2026

Pakiet zawiera 29 nowych reguł, 41 aktualizacji kart i 12 jawnych blokad. Do integracji z silnikiem po dodaniu requirements, extraExam i minimumMaturaTotal. Plik stanowi osobny pakiet zmian; nie zmienia istniejącego katalogu automatycznie.
Źródła odczytano na żywo przez requests i BeautifulSoup, z kontenera `[data-block-id="KryteriaRek"] [data-program-year="6"]`. Ukryte roczniki oraz rozmowy dotyczące matur zagranicznych nie zostały przeniesione do polskiej nowej matury. Dla Ochrony środowiska kontener 6 nadal jest pusty; użyto jawnie 2026/2027 (kontener 2).

Kalkulatory obejmują pisemną polską nową maturę PP/PR. Dowolny przedmiot rozwinięto do obsługiwanego SUBJECTS. To podzbiór formalnej oferty przedmiotów; brak przedmiotu w profilu nie oznacza, że uczelnia go nie uznaje. Ogólny język obcy obejmuje wszystkie współczesne języki profilu. Poziom dwujęzyczny, IB/EB, stara i zagraniczna matura, olimpiady wymagają odrębnej ścieżki. Przedmiot do wyboru lub dodatkowy jest opcjonalny zgodnie z wprowadzeniem do tabel. Suma optymalizowana jest globalnie z wykluczeniami.

## Anglistyka

https://rekrutacja.uwr.edu.pl/kierunek/9?rok=6&tab=zasady-rekrutacji

Reguła `uwr-anglistyka-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język angielski | - | 1,0 | Przedmiot wymagany | język polski | - | 0,8 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | 0,25 | 0,5

## Bachelor of Business and Administration

https://rekrutacja.uwr.edu.pl/kierunek/16?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Biotechnology

https://rekrutacja.uwr.edu.pl/kierunek/27?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Chemistry

https://rekrutacja.uwr.edu.pl/kierunek/35?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Criminal Justice

https://rekrutacja.uwr.edu.pl/kierunek/38?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Culture, Thought and Humanity

https://rekrutacja.uwr.edu.pl/kierunek/40?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Data and Society

https://rekrutacja.uwr.edu.pl/kierunek/41?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Edukacja polonistyczna

https://rekrutacja.uwr.edu.pl/kierunek/49?rok=6&tab=zasady-rekrutacji

Reguła `uwr-edukacja-polonistyczna-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | język obcy nowożytny | 0,5 | 1,0 | Przedmiot dodatkowy | przedmiot inny niż wybrany powyżej | 0,25 | 0,5

## English for Knowledge, Culture and Innovation

https://rekrutacja.uwr.edu.pl/kierunek/54?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów. IELTS: co najmniej 5,5 z każdej umiejętności.

## Etyka

https://rekrutacja.uwr.edu.pl/kierunek/59?rok=6&tab=zasady-rekrutacji

Reguła `uwr-etyka-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | 0,25 | 0,5 | Przedmiot dodatkowy | filozofia | - | 2,0 | Przedmiot dodatkowy | język obcy nowożytny | 0,2 | 0,4

## European Cultures

https://rekrutacja.uwr.edu.pl/kierunek/61?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Filologia francuska

https://rekrutacja.uwr.edu.pl/kierunek/65?rok=6&tab=zasady-rekrutacji

Reguła `uwr-filologia-francuska-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język francuski | 0,5 | 1,0 | lub język obcy inny niż język francuski | 0,4 | 0,8 | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wybrany powyżej (w   tym drugi język obcy) | 0,25 | 0,5

## Filologia germańska

https://rekrutacja.uwr.edu.pl/kierunek/68?rok=6&tab=zasady-rekrutacji

Reguła `uwr-filologia-germanska-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,25 | 0,5 | Przedmiot do wyboru | (jeden do wyboru) | język niemiecki | 0,5 | 1,0 | język obcy nowożytny inny niż język   niemiecki | 0,4 | 0,8

## Filologia hiszpańska

https://rekrutacja.uwr.edu.pl/kierunek/70?rok=6&tab=zasady-rekrutacji

Reguła `uwr-filologia-hiszpanska-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język hiszpański | 0,5 | 1,0 | lub język obcy inny niż język hiszpański | 0,4 | 0,8 | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wybrany powyżej (w   tym drugi język obcy) | 0,25 | 0,5

## Filologia indyjska

https://rekrutacja.uwr.edu.pl/kierunek/71?rok=6&tab=zasady-rekrutacji

Reguła `uwr-filologia-indyjska-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot wymagany | język angielski | 0,5 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | 0,2 | 0,6 | Przedmiot dodatkowy | (jeden do wyboru) | filozofia, historia, język łaciński i kultura antyczna | - | 0,8

## Filologia polska

https://rekrutacja.uwr.edu.pl/kierunek/75?rok=6&tab=zasady-rekrutacji

Reguła `uwr-filologia-polska-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | język obcy nowożytny | 0,5 | 1,0 | Przedmiot dodatkowy | przedmiot inny niż wymienione w tabeli | 0,25 | 0,5

## Filozofia

https://rekrutacja.uwr.edu.pl/kierunek/81?rok=6&tab=zasady-rekrutacji

Reguła `uwr-filozofia-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | 0,25 | 0,5 | Przedmiot dodatkowy | filozofia | - | 2,0 | Przedmiot dodatkowy | język obcy nowożytny | 0,2 | 0,4

## Genetics and Experimental Biology

https://rekrutacja.uwr.edu.pl/kierunek/212?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Historia sztuki

https://rekrutacja.uwr.edu.pl/kierunek/103?rok=6&tab=zasady-rekrutacji

Reguła `uwr-historia-sztuki-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | język obcy nowożytny | 0,5 | 1,0 | Przedmiot wymagany | przedmiot inny niż wymienione w tabeli | 0,25 | 0,5

## Indywidualne studia międzydziedzinowe

https://rekrutacja.uwr.edu.pl/kierunek/107?rok=6&tab=zasady-rekrutacji

Reguła `uwr-indywidualne-studia-miedzydziedzinowe-2027`, rok 2027/2028. Karta uznaje również język grecki i kulturę antyczną, którego profil nie obsługuje. Warunek 240 dotyczy matur przed rozmową; wynik nie potwierdza zaproszenia. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik | dla poziomu podstawowego | Współczynnik | dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,6 | 1,0 | Przedmiot wymagany | matematyka | 0,6 | 1,0 | Przedmiot wymagany | język obcy nowożytny | 0,6 | 1,0 | Przedmiot do wyboru | (jeden do wyboru) | biologia, chemia, filozofia, fizyka,   geografia, historia, historia sztuki, historia muzyki, informatyka, język   łaciński i kultura antyczna, język grecki i kultura antyczna, język obcy   nowożytny (inny niż wybrany powyżej), wiedza o społeczeństwie | - | 1,0

## Informacja naukowa i bibliotekoznawstwo

https://rekrutacja.uwr.edu.pl/kierunek/109?rok=6&tab=zasady-rekrutacji

Reguła `uwr-informacja-naukowa-i-bibliotekoznawstwo-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | język obcy nowożytny | 0,5 | 1,0 | Przedmiot dodatkowy | (jeden do wyboru) | przedmiot inny niż wybrany powyżej (w   tym drugi język obcy nowożytny) | 0,25 | 0,5

## Italianistyka

https://rekrutacja.uwr.edu.pl/kierunek/116?rok=6&tab=zasady-rekrutacji

Reguła `uwr-italianistyka-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | (jeden do wyboru) | język włoski | 0,5 | 1,0 | lub język obcy inny niż język włoski | 0,4 | 0,8 | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | (jeden do wyboru) | przedmiot inny niż wybrany powyżej (w   tym drugi język obcy) | 0,25 | 0,5

## Judaistyka

https://rekrutacja.uwr.edu.pl/kierunek/117?rok=6&tab=zasady-rekrutacji

Reguła `uwr-judaistyka-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot wymagany | język angielski | 0,2 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | - | 0,5

## Koreanistyka

https://rekrutacja.uwr.edu.pl/kierunek/124?rok=6&tab=zasady-rekrutacji

Reguła `uwr-koreanistyka-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot wymagany | język angielski | 0,5 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | - | 0,6 | Przedmiot dodatkowy | język łaciński i kultura antyczna | - | 0,8

## Kultura i praktyka tekstu: twórcze pisanie i edytorstwo

https://rekrutacja.uwr.edu.pl/kierunek/127?rok=6&tab=zasady-rekrutacji

Reguła `uwr-kultura-i-praktyka-tekstu-tworcze-pisanie-i-edytorstwo-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | język obcy nowożytny | 0,5 | 1,0 | Przedmiot dodatkowy | przedmiot inny niż wymienione w tabeli | 0,25 | 0,5

## Literatura światowa: komparatystyka i wielokulturowość

https://rekrutacja.uwr.edu.pl/kierunek/130?rok=6&tab=zasady-rekrutacji

Reguła `uwr-literatura-swiatowa-komparatystyka-i-wielokulturowosc-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik   dla poziomu podstawowego | Współczynnik   dla poziomu rozszerzonego | Przedmiot   wymagany | język polski | - | 1,0 | Przedmiot   wymagany | język obcy   nowożytny | 0,4 | 1,0 | Przedmiot | do wyboru | (jeden do   wyboru) | filozofia, geografia,   historia, historia sztuki, język łaciński i kultura antyczna, drugi język   obcy nowożytny (inny niż wybrany powyżej), wiedza o społeczeństwie | - | 0,5

## LL.B. International and European Environmental Law

https://rekrutacja.uwr.edu.pl/kierunek/131?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Logopedia

https://rekrutacja.uwr.edu.pl/kierunek/133?rok=6&tab=zasady-rekrutacji

Reguła `uwr-logopedia-2027`, rok 2027/2028. II etap obowiązkowy; samo wyliczenie matur nie jest końcowym wynikiem. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | język obcy nowożytny | 0,5 | 1,0 | Przedmiot dodatkowy | (jeden do wyboru) | biologia, drugi język nowożytny (inny   niż wybrany powyżej) | - | 0,75 | matematyka | 0,25 | 0,5 | chemia, fizyka, geografia, historia, informatyka,   wiedza o społeczeństwie | - | 0,5

## Medyczna biotechnologia molekularna

https://rekrutacja.uwr.edu.pl/kierunek/140?rok=6&tab=zasady-rekrutacji

Reguła `uwr-medyczna-biotechnologia-molekularna-2027`, rok 2027/2028. Obowiązkowe minimum angielskiego z przypisu: PP≥75% LUB PR≥30%; nie wolno traktować etykiety przedmiot dodatkowy jako zwolnienia z warunku. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot   wymagany | chemia | - | 1,0 | Przedmiot   wymagany | biologia | - | 1,0 | Przedmiot do wyboru | (jeden do wyboru) | matematyka | 0,4 | 1,0 | fizyka | - | 1,0 | Przedmiot dodatkowy | język angielski | * | 0,1 | 0,25

## Muzykologia

https://rekrutacja.uwr.edu.pl/kierunek/144?rok=6&tab=zasady-rekrutacji

Reguła `uwr-muzykologia-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | język obcy nowożytny | 0,5 | 1,0 | Przedmiot wymagany | przedmiot inny niż wymienione w tabeli | 0,25 | 0,5

## Niderlandystyka

https://rekrutacja.uwr.edu.pl/kierunek/146?rok=6&tab=zasady-rekrutacji

Reguła `uwr-niderlandystyka-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | język obcy nowożytny | 0,5 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wybrany powyżej (w   tym drugi język obcy nowożytny) | 0,25 | 0,5

## Ochrona środowiska

https://rekrutacja.uwr.edu.pl/kierunek/148?rok=2&tab=zasady-rekrutacji

Reguła `uwr-ochrona-srodowiska-2026`, rok 2026/2027. Brak opublikowanej tabeli 2027/2028; kalkulator dotyczy wyłącznie 2026/2027. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | (jeden do wyboru) | biologia, geografia | - | 1,0 | Przedmiot do wyboru | (jeden do wyboru) | geografia (jeśli w przedmiocie 1   została wybrana biologia), biologia (jeśli w przedmiocie 1 została wybrana   geografia), chemia, fizyka | - | 1,0 | matematyka | 0,5 | 1,0 | Przedmiot dodatkowy | (jeden do wyboru) | informatyka | - | 0,4 | język polski (pisemny), język obcy   nowożytny (pisemny) | 0,2 | 1,0

## Pedagogika

https://rekrutacja.uwr.edu.pl/kierunek/152?rok=6&tab=zasady-rekrutacji

Reguła `uwr-pedagogika-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | język obcy nowożytny | 0,2 | 0,4 | Przedmiot do wyboru | przedmiot inny niż wybrane | 0,5 | 1,0

## Pedagogika przedszkolna i wczesnoszkolna

https://rekrutacja.uwr.edu.pl/kierunek/154?rok=6&tab=zasady-rekrutacji

Reguła `uwr-pedagogika-przedszkolna-i-wczesnoszkolna-2027`, rok 2027/2028. II etap obowiązkowy. Karta zawiera dodatkowo zastrzeżenie, że o przyjęcie nie mogą ubiegać się osoby z dysleksją; kalkulator nie weryfikuje tego warunku, interpretację należy uzyskać w uczelni. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot wymagany | matematyka | 0,5 | 1,0 | Przedmiot wymagany | język obcy nowożytny | 0,2 | 0,4 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | 0,5 | 1,0

## Pedagogika specjalna

https://rekrutacja.uwr.edu.pl/kierunek/156?rok=6&tab=zasady-rekrutacji

Reguła `uwr-pedagogika-specjalna-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | język obcy nowożytny | 0,2 | 0,4 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | 0,5 | 1,0

## Political Science

https://rekrutacja.uwr.edu.pl/kierunek/158?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Publikowanie cyfrowe i sieciowe

https://rekrutacja.uwr.edu.pl/kierunek/171?rok=6&tab=zasady-rekrutacji

Reguła `uwr-publikowanie-cyfrowe-i-sieciowe-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot do wyboru | (jeden do wyboru) | język obcy nowożytny, matematyka | 0,5 | 1,0 | historia sztuki, informatyka | - | 1,0 | Przedmiot dodatkowy | przedmiot inny niż wymienione w tabeli | 0,25 | 0,5

## Sinologia

https://rekrutacja.uwr.edu.pl/kierunek/173?rok=6&tab=zasady-rekrutacji

Reguła `uwr-sinologia-2027`, rok 2027/2028. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | język polski | 0,5 | 1,0 | Przedmiot wymagany | język angielski | 0,5 | 1,0 | Przedmiot do wyboru | przedmiot inny niż wymienione w tabeli | - | 0,6 | Przedmiot dodatkowy | język łaciński i kultura antyczna | - | 0,8

## Stosunki międzynarodowe, specjalność: Global Studies

https://rekrutacja.uwr.edu.pl/kierunek/186?rok=6&tab=zasady-rekrutacji

Karta 2027/2028 nie publikuje punktowej tabeli PP/PR dla polskiej nowej matury. Wymaga dokumentu uprawniającego do studiów oraz potwierdzenia angielskiego B2; formalna ocena koordynatora dotyczy świadectw zagranicznych. Do implementacji: odrębny formularz warunków dokumentowych i językowych; brak podstaw do wymyślenia sumy punktów.

## Techniki eksperymentalne w kryminalistyce

https://rekrutacja.uwr.edu.pl/kierunek/196?rok=6&tab=zasady-rekrutacji

Reguła `uwr-techniki-eksperymentalne-w-kryminalistyce-2027`, rok 2027/2028. Przypis: lepsza z biologii/chemii do wymaganej grupy, druga do puli wyboru. Ponieważ oba współczynniki PR wynoszą 1, globalna maksymalizacja z wykluczeniem powtórzenia daje identyczną sumę (także przy remisie). Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmioty | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot wymagany | (jeden do wyboru) | biologia*, chemia* | - | 1,0 | Przedmiot do wyboru | (jeden do wyboru) | matematyka | 0,5 | 1,0 | biologia*, chemia*, fizyka | - | 1,0 | Przedmiot dodatkowy | język obcy nowożytny | 0,2 | 0,4

## Zielona chemia

https://rekrutacja.uwr.edu.pl/kierunek/210?rok=6&tab=zasady-rekrutacji

Reguła `uwr-zielona-chemia-2027`, rok 2027/2028. Dwa różne przedmioty, brak zdawanego do wyboru daje 0. Zagnieżdżenie HTML nie zmienia prostej pierwszej tabeli nowej matury. Polska nowa matura pisemna PP/PR; bez dwujęzycznej, starej matury, IB/EB, zagranicznych świadectw i olimpiad. Lista dowolnych przedmiotów i języków ograniczona do SUBJECTS profilu; inne uznawane przedmioty wymagają ręcznego przeliczenia. Brak opcjonalnego przedmiotu daje 0; wymaganych nie wolno pominąć. Wynik nie gwarantuje przyjęcia ani zaproszenia do kolejnego etapu.

Tabela źródłowa (pierwsza tabela polskiej nowej matury): Przedmiot | Współczynnik dla poziomu podstawowego | Współczynnik dla poziomu rozszerzonego | Przedmiot do wyboru | (dwa do wyboru) | matematyka | 0,5 | 1,0 | biologia, chemia, fizyka | - | 1,0 | Przedmiot dodatkowy | język obcy nowożytny | 0,2 | 0,4

## Ścieżka obywateli polskich na 12 kartach anglojęzycznych

Odczytano również zakładkę Harmonogram i dokumenty, kontener DokumentyRek dla roku 6, część Nowa matura. Nie przenoszono zasad dla świadectw zagranicznych.

### uwr-bachelor-of-business-and-administration

https://rekrutacja.uwr.edu.pl/kierunek/16?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/16?rok=6&tab=harmonogram

### uwr-biotechnology

https://rekrutacja.uwr.edu.pl/kierunek/27?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/27?rok=6&tab=harmonogram

### uwr-chemistry

https://rekrutacja.uwr.edu.pl/kierunek/35?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/35?rok=6&tab=harmonogram

### uwr-criminal-justice

https://rekrutacja.uwr.edu.pl/kierunek/38?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/38?rok=6&tab=harmonogram

### uwr-culture-thought-and-humanity

https://rekrutacja.uwr.edu.pl/kierunek/40?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/40?rok=6&tab=harmonogram

### uwr-data-and-society

https://rekrutacja.uwr.edu.pl/kierunek/41?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/41?rok=6&tab=harmonogram

### uwr-english-for-knowledge-culture-and-innovation

https://rekrutacja.uwr.edu.pl/kierunek/54?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/54?rok=6&tab=harmonogram

### uwr-european-cultures

https://rekrutacja.uwr.edu.pl/kierunek/61?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/61?rok=6&tab=harmonogram

### uwr-genetics-and-experimental-biology

https://rekrutacja.uwr.edu.pl/kierunek/212?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/212?rok=6&tab=harmonogram

### uwr-ll-b-international-and-european-environmental-law

https://rekrutacja.uwr.edu.pl/kierunek/131?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/131?rok=6&tab=harmonogram

### uwr-political-science

https://rekrutacja.uwr.edu.pl/kierunek/158?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/158?rok=6&tab=harmonogram

### uwr-stosunki-miedzynarodowe-specjalnosc-global-studies

https://rekrutacja.uwr.edu.pl/kierunek/186?rok=6&tab=harmonogram

W dokumentach 2027/2028 dla obywateli polskich, sekcja Nowa matura, B2 można potwierdzić m.in. angielskim PR ≥60%, maturą dwujęzyczną z angielskiego, dyplomem studiów z lektoratem angielskiego minimum B2 w suplemencie albo dokumentem z załącznika nr 2 do rozporządzenia z 30 lipca 2025 r. Karta odsyła do wykazu dokumentów; nie rozpisuje kompletnej listy certyfikatów w kryteriach. Polska ścieżka jest więc jawnie przewidziana, ale nie opublikowano dla niej wzoru rankingu PP/PR. Źródło dokumentów: https://rekrutacja.uwr.edu.pl/kierunek/186?rok=6&tab=harmonogram


## Weryfikacja pakietu

JSON ponownie odczytano parserem. Sprawdzono 41 unikalnych identyfikatorów aktualizacji wobec pełnego zbioru kart bez reguły; 29 nowych reguł nie koliduje z dotychczasowymi 48. Wszystkie przedmioty są w SUBJECTS, wykluczenia odsyłają wyłącznie do wcześniejszych grup, daty sprawdzenia to 2026-10-25, a oba pliki są poprawnym UTF-8 bez znaków zastępczych i typowych markerów mojibake.

Wykonano calculateAdmission dla wszystkich 29 reguł przy PP=PR=100. Same sumy maturalne: Anglistyka 230; Etyka/Filozofia 390; Filologia germańska 150; Filologia indyjska/Koreanistyka/Sinologia 340; ISM 400; Logopedia 275; Medyczna biotechnologia molekularna 325; Ochrona środowiska 300; Pedagogika/Pedagogika specjalna/Techniki eksperymentalne w kryminalistyce/Zielona chemia 240; Pedagogika przedszkolna i wczesnoszkolna 340; pozostałe nowe reguły 250. To kontrola transkrypcji i wykonywalności sum PP/PR. Pola requirements, extraExam oraz minimumMaturaTotal wymagają równoległej zmiany typów i silnika; końcową kontrolę tych warunków należy wykonać po integracji.
