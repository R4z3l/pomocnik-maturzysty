# Przygotowanie prywatnej wersji online

Stan: przygotowanie lokalne; aplikacja nie jest opublikowana, a dostęp e-mail nie został jeszcze skonfigurowany ani przetestowany. Przykładowy wariant to Cloudflare Pages oraz Cloudflare Access z kodem wysyłanym na adres e-mail. Przed założeniem usługi sprawdź aktualną ofertę, limity i koszty dostawcy.

## Co pozostaje na urządzeniu

Profil, notatki, oceny i ulubione są zapisywane w pamięci konkretnej przeglądarki. Wersja online nie synchronizuje ich automatycznie. Adres lokalny i adres online mają oddzielną pamięć: przed zmianą urządzenia lub adresu wyeksportuj profil z aplikacji, zachowaj plik prywatnie i zaimportuj go w nowej przeglądarce. Nie umieszczaj eksportu profilu w folderze `public` ani `dist`.

Aktualizacje katalogu można przygotowywać w domu podczas rozmowy z AI korzystającym z dostępu abonamentowego: zmiany trafiają do plików projektu, po czym przechodzą testy i są ręcznie publikowane. Działająca aplikacja nie korzysta z API AI. Sama obecność dostępu abonamentowego nie zapewnia automatycznej publikacji ani stałego odświeżania.

## Przygotowanie wersji

1. W aplikacji wyeksportuj profil i przechowuj go poza projektem.
2. W folderze projektu uruchom kolejno `npm test`, `npm run validate:data`, `npm run build` i `npm run check:release`.
3. Sprawdź lokalnie wersję produkcyjną przez `npm run preview -- --port 4173` i adres http://127.0.0.1:4173/. Sprawdź kierunek, kalkulator, zapis i odczyt profilu oraz import/eksport kopii.
4. Przejrzyj zawartość `dist`. Kontrola `check:release` odrzuca nieoczekiwane nazwy plików i sprawdza odwołania z `index.html`; nie wykrywa wszystkich danych osobowych ani sekretów ukrytych w dozwolonych plikach. Nigdy nie przesyłaj całego folderu projektu ani pliku profilu.

## Dostęp po e-mailu: wariant Cloudflare

Zależnie od konfiguracji Pages adres strony może być publiczny zaraz po pierwszym przesłaniu. Aby nie wystawiać właściwej aplikacji podczas konfiguracji, utwórz projekt ze stroną z folderu `output/strona-testowa-dostepu`, a właściwy `dist` prześlij dopiero po uruchomieniu i sprawdzeniu ochrony wszystkich adresów. Sama dyrektywa `noindex` na stronie testowej nie stanowi zabezpieczenia. Przy tworzeniu wybierz Direct Upload, jeśli chcesz aktualizować pliki ręcznie bez repozytorium Git. Instrukcja dostawcy: [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/).

1. Skonfiguruj Cloudflare Zero Trust / Access oraz metodę [jednorazowego kodu e-mail](https://developers.cloudflare.com/cloudflare-one/integrations/identity-providers/one-time-pin/). Nowe organizacje mogą wymagać jawnego dodania tej metody.
2. Przygotuj politykę zezwalającą **wyłącznie konkretnym adresom e-mail**; sprawdź, czy żadna inna reguła nie daje szerszego dostępu. Lista adresów należy do konfiguracji konta, nie do plików aplikacji.
3. Obejmij ochroną adres produkcyjny `projekt.pages.dev`, wszystkie adresy podglądów oraz ewentualną własną domenę. Sam przełącznik ochrony podglądów nie zabezpiecza automatycznie głównego adresu. Szczegóły: [ochrona adresu i podglądów](https://developers.cloudflare.com/pages/platform/known-issues/) oraz [podglądy Pages](https://developers.cloudflare.com/pages/configuration/preview-deployments/).
4. W osobnej sesji przeglądarki bez zalogowania sprawdź każdy adres: stronę główną, bezpośredni adres podglądu oraz bezpośredni plik JavaScript i CSS. Oczekiwany wynik to wymuszenie logowania lub odmowa, nigdy treść aplikacji. Sprawdź też adres nieuwzględniony w polityce. Następnie sprawdź logowanie na dozwolony adres.
5. Dopiero po przejściu kontroli prześlij folder `dist` jako nową wersję. Po publikacji ponownie sprawdź ochronę głównego adresu, zasobów, podglądów i własnej domeny oraz podstawową ścieżkę aplikacji. W razie niepowodzenia nie traktuj witryny jako prywatnej.

Uwierzytelnianie e-mailem sprawdza dostęp do skrzynki, nie tożsamość osoby korzystającej z komputera. Ochrona strony nie szyfruje danych zapisanych w przeglądarce ani w wyeksportowanym pliku.

## Aktualizacja i powrót do poprzedniej wersji

Po zmianie danych powtórz cztery kontrole z sekcji „Przygotowanie wersji”, a następnie prześlij nowy `dist` do tego samego chronionego projektu. Zachowaj poprzednią sprawdzoną wersję wyłącznie w prywatnym miejscu; w razie błędu przywróć ją mechanizmem dostawcy i ponownie sprawdź polityki wszystkich adresów. Nie zakładaj, że nowy adres podglądu odziedziczył ochronę bez sprawdzenia.
