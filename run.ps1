# Run Calendar Consolidator MCP with virtual environment activated (PowerShell version)
# This script starts the development server on Windows

param(
    [switch]$SkipVenv,
    [switch]$Help
)

if ($Help) {
    Write-Host "Calendar Consolidator MCP Run Script" -ForegroundColor Green
    Write-Host ""
    Write-Host "This script starts the Calendar Consolidator MCP development server."
    Write-Host ""
    Write-Host "Parameters:" -ForegroundColor Yellow
    Write-Host "  -SkipVenv    Skip virtual environment activation"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "Usage: .\run.ps1 [-SkipVenv] [-Help]" -ForegroundColor Cyan
    exit 0
}

Write-Host "🚀 Starting Calendar Consolidator MCP..." -ForegroundColor Green

# Check if virtual environment exists and activate it (unless skipped)
$venvExists = Test-Path "venv"
if ($venvExists -and -not $SkipVenv) {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Blue
    try {
        & ".\venv\Scripts\Activate.ps1"
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Failed to activate virtual environment: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "   Continuing without virtual environment..." -ForegroundColor Yellow
    }
} elseif ($venvExists -and $SkipVenv) {
    Write-Host "⏭️ Skipping virtual environment activation" -ForegroundColor Yellow
} else {
    Write-Host "ℹ️ Virtual environment not found - running without it" -ForegroundColor Cyan
}

# Set up PYTHONPATH to include current directory
$currentPath = Get-Location
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$($env:PYTHONPATH);$currentPath"
} else {
    $env:PYTHONPATH = $currentPath
}
Write-Host "🔧 PYTHONPATH set to include current directory" -ForegroundColor Blue

# Check if database exists and initialize if needed
$dbExists = Test-Path "calendar_consolidator.db"
if (-not $dbExists) {
    Write-Host "💾 Database not found. Initializing..." -ForegroundColor Blue
    try {
        python python/init_db.py
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Database initialized" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Database initialization completed with warnings" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Failed to initialize database: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   Please run .\setup.ps1 first" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "✅ Database found" -ForegroundColor Green
}

# Start the server
Write-Host "🌐 Starting server on http://127.0.0.1:3000" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

try {
    # Run npm start (this will keep running until Ctrl+C)
    npm start
} catch {
    if ($_.Exception.Message -like "*Ctrl+C*") {
        Write-Host ""
        Write-Host "👋 Server stopped by user" -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "❌ Server stopped unexpectedly: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
}
