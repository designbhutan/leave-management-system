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
echo Create the supervisor account now.
echo Example only: supervisor / ChangeMe123!
echo Use your real credentials when running the command.
echo.
set /p SUPUSER=Supervisor username: 
set /p SUPPASS=Supervisor password: 
.venv\Scripts\python.exe manage.py bootstrap_demo --supervisor-username "%SUPUSER%" --supervisor-password "%SUPPASS%"

echo.
echo Supervisor setup complete.
echo You can now run START_WINDOWS.bat whenever you want to start the system.
pause
