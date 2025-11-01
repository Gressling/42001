@echo off
REM ISO 42001 AI Management System - Master Build Script
REM Copyright (c) 2025 Gressling Consulting GmbH, Germany E.U.

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set BUILD_DIR=%PROJECT_ROOT%\build
set NSIS_SCRIPT=%BUILD_DIR%\iso42001-installer.nsi
set PYINSTALLER_SPEC=%BUILD_DIR%\iso42001.spec

echo.
echo =====================================
echo ISO 42001 Build System
echo =====================================
echo.

cd /d "%PROJECT_ROOT%"

if "%1"=="" goto :usage

if "%1"=="exe" goto :build_exe
if "%1"=="installer" goto :build_installer  
if "%1"=="portable" goto :build_portable
if "%1"=="all" goto :build_all
if "%1"=="clean" goto :clean
goto :usage

:usage
echo Usage: build.bat [command]
echo.
echo Commands:
echo   exe        Build standalone executable
echo   installer  Build Windows installer (requires NSIS)
echo   portable   Build portable ZIP distribution
echo   all        Build all distributions
echo   clean      Clean all build artifacts
echo.
goto :end

:build_exe
echo Building standalone executable...
call :check_venv || exit /b 1
call :activate_venv

python -c "import pyinstaller" 2>nul || (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build\build" rmdir /s /q "build\build"

echo Building with PyInstaller...
pyinstaller --clean --noconfirm "%PYINSTALLER_SPEC%"

if errorlevel 1 (
    echo ERROR: Executable build failed!
    exit /b 1
)

echo.
echo Executable: dist\ISO42001-AIManagementSystem.exe
goto :end

:build_installer
echo Building Windows installer...
call :check_nsis || exit /b 1
call :check_exe || call :build_exe || exit /b 1

if not exist "installer" mkdir installer
"%NSIS_EXE%" "%NSIS_SCRIPT%"

if errorlevel 1 (
    echo ERROR: Installer build failed!
    exit /b 1
)
echo Installer: installer\ISO42001-AIManagementSystem-Setup-v1.0.0.exe
goto :end

:build_portable
echo Building portable distribution...
call :check_exe || call :build_exe || exit /b 1

set DIST_NAME=ISO42001-AIManagementSystem-Portable-v1.0.0
if exist "portable" rmdir /s /q "portable"
mkdir "portable\%DIST_NAME%"

copy "dist\ISO42001-AIManagementSystem.exe" "portable\%DIST_NAME%\" >nul
copy "README.md" "portable\%DIST_NAME%\" >nul
copy "LICENSE" "portable\%DIST_NAME%\" >nul
copy "build\EULA.txt" "portable\%DIST_NAME%\" >nul
xcopy "docs" "portable\%DIST_NAME%\docs\" /E /I /Q >nul
mkdir "portable\%DIST_NAME%\data"
copy "data\README.md" "portable\%DIST_NAME%\data\" >nul

echo @echo off > "portable\%DIST_NAME%\Start.bat"
echo start ISO42001-AIManagementSystem.exe >> "portable\%DIST_NAME%\Start.bat"

powershell -Command "Compress-Archive -Path 'portable\%DIST_NAME%' -DestinationPath 'portable\%DIST_NAME%.zip' -CompressionLevel Optimal" 2>nul

echo Portable: portable\%DIST_NAME%.zip
goto :end

:build_all
call :build_exe || exit /b 1
call :build_installer 2>nul || echo WARNING: Installer build failed (NSIS not installed?)
call :build_portable || exit /b 1
echo All builds completed!
goto :end

:clean
if exist "build\build" rmdir /s /q "build\build"
if exist "dist" rmdir /s /q "dist"
if exist "installer" rmdir /s /q "installer"
if exist "portable" rmdir /s /q "portable"
echo Build artifacts cleaned.
goto :end

:check_venv
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found! Run: scripts\run.bat
    exit /b 1
)
exit /b 0

:activate_venv
call .venv\Scripts\activate.bat
exit /b 0

:check_exe
if exist "dist\ISO42001-AIManagementSystem.exe" exit /b 0
exit /b 1

:check_nsis
set NSIS_EXE=
if exist "%ProgramFiles(x86)%\NSIS\makensis.exe" (
    set "NSIS_EXE=%ProgramFiles(x86)%\NSIS\makensis.exe"
    exit /b 0
)
if exist "%ProgramFiles%\NSIS\makensis.exe" (
    set "NSIS_EXE=%ProgramFiles%\NSIS\makensis.exe"
    exit /b 0
)
echo ERROR: NSIS not found! Install from: https://nsis.sourceforge.io/
exit /b 1

:end