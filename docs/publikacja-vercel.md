# Publikacja online na Vercel

Aplikacja jest w pełni statyczna: bez API i bez zmiennych środowiskowych. Konfiguracja leży w pliku `vercel.json` (framework Vite, `npm ci`, budowanie z kontrolą wydania, katalog `dist`). Nawigacja używa adresów z `#`, więc nie są potrzebne przekierowania.

## 1. Kontrola przed publikacją

W folderze projektu uruchom po kolei:

```
npm test
npm run validate:data
npm run build
npm run check:release
```

Publikuj dopiero, gdy wszystkie cztery polecenia kończą się powodzeniem.

## 2. Publikacja przez repozytorium GitHub

1. Zaloguj się na konto Vercel.
2. Wybierz Add New, potem Project.
3. Wskaż repozytorium `R4z3l/pomocnik-maturzysty`.
4. Ustawienia wczytają się z `vercel.json`. Niczego nie zmieniaj ręcznie.
5. Kliknij Deploy.

Później każdy push na gałąź główną publikuje nową wersję produkcyjną. Gałęzie i pull requesty dostają osobne adresy podglądu.

## 3. Alternatywa: wiersz poleceń

```
npm i -g vercel
vercel
vercel --prod
```

Polecenie `vercel` tworzy wersję podglądową, a `vercel --prod` wersję produkcyjną.

## 4. Gdzie jest profil

Profil zapisuje się w przeglądarce, osobno dla adresu domeny Vercel. Jest oddzielny od profilu w wersji lokalnej (`http://127.0.0.1:5173/`). Aby przenieść dane, użyj Eksportuj JSON i Importuj JSON.

## 5. Prywatność

- Adres jest domyślnie **publiczny dla każdego, kto go zna**.
- Nagłówek `X-Robots-Tag: noindex` zniechęca wyszukiwarki, ale **nie jest zabezpieczeniem**.
- Opcje ochrony dostępu (Deployment Protection: Vercel Authentication, ochrona hasłem) zależą od planu i ustawień projektu. Przed publikacją sprawdź w [dokumentacji Vercel](https://vercel.com/docs/deployment-protection), czy dana ochrona obejmuje adres produkcyjny w używanym planie.
- Po włączeniu ochrony sprawdź adres w oknie incognito, bez zalogowania.

Wariant z Cloudflare opisuje instrukcja „Publikacja prywatna” (`docs/publikacja-prywatna.md`). Jeśli potrzebujesz pewnej ochrony dostępu, rozważ ją jako alternatywę.
