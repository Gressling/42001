@echo off
REM Activate virtual environment for development
REM Copyright (c) 2025 Gressling Consulting GmbH, Germany E.U.

echo Activating ISO 42001 virtual environment...

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Check if virtual environment exists
if not exist "%PROJECT_ROOT%\.venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found at %PROJECT_ROOT%\.venv
    echo Please run scripts\run.bat first to create the virtual environment
    pause
    exit /b 1
)

REM Change to project root
cd /d "%PROJECT_ROOT%"

REM Activate virtual environment and start new command prompt
echo Virtual environment activated successfully!
echo You can now run Python commands using the project's virtual environment.
echo Type 'deactivate' to exit the virtual environment.
echo.

cmd /k ".venv\Scripts\activate.bat"