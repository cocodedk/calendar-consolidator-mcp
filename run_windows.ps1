# Run Calendar Consolidator MCP with virtual environment activated (Windows PowerShell)

param()

$ErrorActionPreference = "Stop"

Write-Host "[*] Starting Calendar Consolidator MCP..."

Set-Location -LiteralPath $PSScriptRoot

# Ensure the virtual environment exists
$venvActivate = Join-Path $PSScriptRoot "venv\Scripts\Activate.ps1"
if (-not (Test-Path -Path $venvActivate)) {
    Write-Error "[!] Virtual environment not found. Please run ./setup.sh (from WSL/Git Bash) or create the venv manually."
    exit 1
}

Write-Host "[*] Activating virtual environment..."
. $venvActivate

# Ensure Python can locate the project modules
$projectRoot = (Get-Location).Path
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$($env:PYTHONPATH);$projectRoot"
} else {
    $env:PYTHONPATH = "$projectRoot"
}

# Initialize the database if it does not exist
$databasePath = Join-Path $projectRoot "calendar_consolidator.db"
if (-not (Test-Path -Path $databasePath)) {
    Write-Host "[*] Database not found. Initializing..."
    python "python/init_db.py"
}

Write-Host "[*] Starting server on http://127.0.0.1:3000"
Write-Host ""
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""

npm start
