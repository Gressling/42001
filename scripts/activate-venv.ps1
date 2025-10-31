# Activate virtual environment for development - PowerShell version
# Copyright (c) 2025 Gressling Consulting GmbH, Germany E.U.

Write-Host "Activating ISO 42001 virtual environment..." -ForegroundColor Green

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Check if virtual environment exists
$VenvActivateScript = Join-Path $ProjectRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $VenvActivateScript)) {
    Write-Host "ERROR: Virtual environment not found at $ProjectRoot\.venv" -ForegroundColor Red
    Write-Host "Please run scripts\run.bat first to create the virtual environment" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Change to project root
Set-Location $ProjectRoot

# Activate virtual environment
& $VenvActivateScript

Write-Host "Virtual environment activated successfully!" -ForegroundColor Green
Write-Host "You can now run Python commands using the project's virtual environment." -ForegroundColor White
Write-Host "Current Python path: $((Get-Command python).Source)" -ForegroundColor Cyan
Write-Host "Type 'deactivate' to exit the virtual environment." -ForegroundColor White
Write-Host ""