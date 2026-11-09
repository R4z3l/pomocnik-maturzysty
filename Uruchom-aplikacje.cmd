@echo off
setlocal
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
  echo Brak Node.js. Zainstaluj Node.js 24 LTS i uruchom ten plik ponownie.
  pause
  exit /b 1
)
if not exist "node_modules\vite\bin\vite.js" (
  echo Instalowanie zaleznosci aplikacji...
  call npm install
  if errorlevel 1 (
    pause
    exit /b 1
  )
)
powershell -NoProfile -Command "try { $r = Invoke-WebRequest 'http://127.0.0.1:5173/' -UseBasicParsing -TimeoutSec 2; if ($r.Content -match 'Akcja Studia 2027') { exit 0 } } catch {}; exit 1"
if not errorlevel 1 (
  start "" "http://127.0.0.1:5173/"
  exit /b 0
)
echo Aplikacja otworzy sie w przegladarce pod adresem http://127.0.0.1:5173/
echo Pozostaw to okno otwarte podczas korzystania z aplikacji.
call npm run dev -- --port 5173 --strictPort --open
if errorlevel 1 (
  echo Nie udalo sie uruchomic aplikacji. Szczegoly bledu sa powyzej.
  pause
)
