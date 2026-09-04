@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -m venv .venv
  .venv\Scripts\python.exe -m pip install --upgrade pip
  .venv\Scripts\python.exe -m pip install -r requirements.txt
)
if not exist ".env" copy ".env.example" ".env" >nul
.venv\Scripts\python.exe manage.py migrate

echo.
echo Starting Leave Management System...
echo Open http://127.0.0.1:8000/
echo.
.venv\Scripts\python.exe manage.py runserver
pause
