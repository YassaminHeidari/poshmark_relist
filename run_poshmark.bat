@echo off
REM Poshmark Auto-Relister - Windows Batch Script
REM Double-click this file to run the relister

echo ================================
echo Poshmark Auto-Relister
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
pip show selenium >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt
)

echo.
echo Starting Poshmark relister...
echo.

REM Run the Python script
python poshmark_relister.py

echo.
echo ================================
echo Process Complete
echo ================================
echo Check the log file for details.
echo.
pause
