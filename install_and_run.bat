@echo off
setlocal ENABLEDELAYEDEXPANSION

REM
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.7+ and add it to your PATH.
    pause
    exit /b 1
)

REM
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed.
    echo Please install pip for Python.
    pause
    exit /b 1
)

REM
echo Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements.
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo If you get a 'python not found' error, add Python to your PATH.
echo.

:MENU
echo 1. Start TTS Spammer
set "has_update_py=0"
if exist update.py (
    echo 2. Check for Updates
    set "has_update_py=1"
)
echo 0. Exit
set /p choice=Choose an option: 
if "%choice%"=="1" goto RUN
if "%choice%"=="2" if !has_update_py! == 1 goto UPDATE
if "%choice%"=="0" exit /b 0
goto MENU

:RUN
python tts_spammer.py
pause
goto MENU

:UPDATE
python update.py
pause
goto MENU 