@echo off
REM ISO 42001 Bookkeeping Application - Run Script
REM Copyright (c) 2025 Gressling Consulting GmbH, Germany E.U.

echo.
echo =====================================
echo ISO 42001 Bookkeeping Application
echo =====================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Check if virtual environment exists
if not exist "%PROJECT_ROOT%\.venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating .venv...
    python -m venv "%PROJECT_ROOT%\.venv"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please ensure Python 3.8+ is installed and in PATH
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

echo Activating virtual environment...
call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"

echo Checking Python environment...
python --version

echo.
echo Checking dependencies...
pip install -r "%PROJECT_ROOT%\requirements.txt" --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Starting ISO 42001 Bookkeeping Application...
echo Navigate to http://127.0.0.1:8050 to access the application
echo Press Ctrl+C to stop the application
echo.

cd /d "%PROJECT_ROOT%"
set ISO42001_DEBUG=false
python main.py

echo.
echo Application stopped.
pause