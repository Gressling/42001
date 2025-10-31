@echo off
REM ISO 42001 Version Management Script
REM Copyright (c) 2025 Gressling Consulting GmbH, Germany E.U.

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set VERSION_FILE=%PROJECT_ROOT%\src\iso42001\__init__.py
set SETUP_FILE=%PROJECT_ROOT%\setup.py

echo.
echo =====================================
echo ISO 42001 Version Management
echo =====================================
echo.

if "%1"=="" goto :usage
if "%1"=="show" goto :show_version
if "%1"=="major" goto :bump_major
if "%1"=="minor" goto :bump_minor
if "%1"=="patch" goto :bump_patch
if "%1"=="set" goto :set_version
goto :usage

:usage
echo Usage: bump.bat [command] [version]
echo.
echo Commands:
echo   show          Show current version
echo   major         Bump major version (1.0.0 -> 2.0.0)
echo   minor         Bump minor version (1.0.0 -> 1.1.0)
echo   patch         Bump patch version (1.0.0 -> 1.0.1)
echo   set [version] Set specific version (e.g., set 1.2.3)
echo.
echo Examples:
echo   bump.bat show
echo   bump.bat major
echo   bump.bat minor
echo   bump.bat patch
echo   bump.bat set 2.1.0
echo.
goto :end

:show_version
echo Current version information:
echo.
for /f "tokens=2 delims='" %%a in ('findstr "__version__" "%VERSION_FILE%"') do (
    echo Package version: %%a
)
if exist "%SETUP_FILE%" (
    for /f "tokens=2 delims='" %%a in ('findstr "version=" "%SETUP_FILE%"') do (
        echo Setup.py version: %%a
    )
)
echo.
goto :end

:bump_major
call :get_current_version
set /a MAJOR+=1
set MINOR=0
set PATCH=0
set NEW_VERSION=!MAJOR!.!MINOR!.!PATCH!
echo Bumping major version: !CURRENT_VERSION! -> !NEW_VERSION!
call :update_version !NEW_VERSION!
goto :end

:bump_minor
call :get_current_version
set /a MINOR+=1
set PATCH=0
set NEW_VERSION=!MAJOR!.!MINOR!.!PATCH!
echo Bumping minor version: !CURRENT_VERSION! -> !NEW_VERSION!
call :update_version !NEW_VERSION!
goto :end

:bump_patch
call :get_current_version
set /a PATCH+=1
set NEW_VERSION=!MAJOR!.!MINOR!.!PATCH!
echo Bumping patch version: !CURRENT_VERSION! -> !NEW_VERSION!
call :update_version !NEW_VERSION!
goto :end

:set_version
if "%2"=="" (
    echo ERROR: Please specify version number
    echo Example: bump.bat set 1.2.3
    goto :end
)
set NEW_VERSION=%2
echo Setting version to: !NEW_VERSION!
call :update_version !NEW_VERSION!
goto :end

:get_current_version
for /f "tokens=2 delims='" %%a in ('findstr "__version__" "%VERSION_FILE%"') do (
    set CURRENT_VERSION=%%a
)
for /f "tokens=1,2,3 delims=." %%a in ("!CURRENT_VERSION!") do (
    set MAJOR=%%a
    set MINOR=%%b
    set PATCH=%%c
)
exit /b

:update_version
set UPDATE_VERSION=%1
echo.
echo Updating version files...

REM Update __init__.py
powershell -Command "(Get-Content '%VERSION_FILE%') -replace '__version__ = \".*\"', '__version__ = \"%UPDATE_VERSION%\"' | Set-Content '%VERSION_FILE%'"
echo Updated: %VERSION_FILE%

REM Update setup.py if it exists
if exist "%SETUP_FILE%" (
    powershell -Command "(Get-Content '%SETUP_FILE%') -replace 'version=\".*\"', 'version=\"%UPDATE_VERSION%\"' | Set-Content '%SETUP_FILE%'"
    echo Updated: %SETUP_FILE%
)

REM Update README.md version badge if it exists
if exist "%PROJECT_ROOT%\README.md" (
    powershell -Command "$content = Get-Content '%PROJECT_ROOT%\README.md'; $content = $content -replace 'version-.*-blue', 'version-%UPDATE_VERSION%-blue'; $content | Set-Content '%PROJECT_ROOT%\README.md'"
    echo Updated: README.md
)

echo.
echo Version updated successfully to: %UPDATE_VERSION%
echo.

REM Show Git status if in a Git repository
if exist "%PROJECT_ROOT%\.git" (
    echo Git status:
    cd /d "%PROJECT_ROOT%"
    git status --porcelain
    echo.
    echo To commit the version change:
    echo   git add .
    echo   git commit -m "Bump version to %UPDATE_VERSION%"
    echo   git tag v%UPDATE_VERSION%
    echo.
)

exit /b

:end
pause