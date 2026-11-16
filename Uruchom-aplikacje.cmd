@echo off
setlocal
cd /d "%~dp0"

rem Portable Node.js: szukany w folderze Node/nodejs obok aplikacji, wyzej oraz w korzeniu pendrive.
for %%D in ("%~dp0Node" "%~dp0nodejs" "%~dp0..\Node" "%~dp0..\nodejs" "%~d0\Node" "%~d0\nodejs") do (
  if exist "%%~fD\node.exe" (
    set "NODE_HOME=%%~fD"
    goto :node_found
  )
  for /d %%S in ("%%~fD\node-v*") do (
    if exist "%%~fS\node.exe" (
      set "NODE_HOME=%%~fS"
      goto :node_found
    )
  )
)
where node >nul 2>nul
if errorlevel 1 (
  echo Nie znaleziono Node.js. Umiesc portable Node.js w folderze "Node" na pendrive
  echo ^(obok folderu aplikacji lub w jego korzeniu^) i uruchom ten plik ponownie.
  pause
  exit /b 1
)
goto :node_ready

:node_found
set "PATH=%NODE_HOME%;%PATH%"
echo Uzywam portable Node.js: %NODE_HOME%

:node_ready
set "npm_config_cache=%~dp0.npm-cache"
set "npm_config_update_notifier=false"

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
