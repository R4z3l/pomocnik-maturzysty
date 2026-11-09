@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Brak Python. Wymagany Python 3.12 lub nowszy.
  pause
  exit /b 1
)
python -c "import requests, bs4, pdfplumber" >nul 2>nul
if errorlevel 1 (
  echo Najpierw zainstaluj narzedzia: python -m pip install -r requirements-data.txt
  pause
  exit /b 1
)
python scripts\refresh_data.py run %*
set "refresh_result=%errorlevel%"
echo.
echo Otworz raport we wskazanym folderze. Aktywna baza pozostala bez zmian.
pause
exit /b %refresh_result%
