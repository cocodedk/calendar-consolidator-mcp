# Setup script for Calendar Consolidator MCP (PowerShell version)
# This script sets up the development environment on Windows
#
# This script handles Windows execution policy issues automatically

param(
    [switch]$SkipVenv,
    [switch]$Help
)

# Handle execution policy issues automatically
try {
    # Try to set execution policy for current process if restricted
    $currentPolicy = Get-ExecutionPolicy -Scope Process
    if ($currentPolicy -eq "Restricted") {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force 2>$null
        Write-Host "ℹ️ Adjusted execution policy for this session" -ForegroundColor Cyan
    }
} catch {
    # If we can't set execution policy, the script will still work due to -Force parameter usage
}

if ($Help) {
    Write-Host "Calendar Consolidator MCP Setup Script" -ForegroundColor Green
    Write-Host ""
    Write-Host "This script sets up the development environment for the Calendar Consolidator MCP project."
    Write-Host ""
    Write-Host "Parameters:" -ForegroundColor Yellow
    Write-Host "  -SkipVenv    Skip virtual environment creation"
    Write-Host "  -Help        Show this help message"
    Write-Host ""
    Write-Host "Usage: .\setup.ps1 [-SkipVenv] [-Help]" -ForegroundColor Cyan
    exit 0
}

Write-Host "🚀 Setting up Calendar Consolidator MCP..." -ForegroundColor Green

# Function to check if a command exists
function Test-CommandExists {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Blue

$pythonFound = Test-CommandExists "python"
$nodeFound = Test-CommandExists "node"

if (-not $pythonFound) {
    Write-Host "❌ Python not found. Please install Python 3.10+" -ForegroundColor Red
    Write-Host "   Download from: https://python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

if (-not $nodeFound) {
    Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    Write-Host "   Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check Python version
$pythonVersion = & python --version 2>&1
Write-Host "✅ Python found: $pythonVersion"

# Check Node.js version
$nodeVersion = & node --version 2>&1
Write-Host "✅ Node.js found: $nodeVersion"

Write-Host "✅ Prerequisites OK" -ForegroundColor Green
Write-Host ""

# Create virtual environment (optional)
if (-not $SkipVenv) {
    $createVenv = Read-Host 'Create Python virtual environment? (y/n)'
    if ($createVenv -eq 'y' -or $createVenv -eq 'Y') {
        Write-Host "📦 Creating virtual environment..." -ForegroundColor Blue
        python -m venv venv

        # Activate virtual environment for this session
        Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
        & "./venv/Scripts/Activate.ps1"
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    }
} else {
    Write-Host "⏭️ Skipping virtual environment creation" -ForegroundColor Yellow
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Blue
try {
    & pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Python dependencies installation completed with warnings" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Failed to install Python dependencies: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Make sure Python and pip are installed and accessible" -ForegroundColor Yellow
    exit 1
}

# Install Node dependencies
Write-Host "📦 Installing Node dependencies..." -ForegroundColor Blue
try {
    & npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Node dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Node dependencies installation completed with warnings" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Failed to install Node dependencies: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Make sure Node.js and npm are installed and accessible" -ForegroundColor Yellow
    exit 1
}

# Initialize database
Write-Host "💾 Initializing database..." -ForegroundColor Blue
try {
    & python python/init_db.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Database initialized" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Database initialization completed with warnings" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Failed to initialize database: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Make sure Python is installed and accessible" -ForegroundColor Yellow
    exit 1
}

# Create .env file (optional)
if (-not (Test-Path .env) -and (Test-Path .env.example)) {
    $createEnv = Read-Host 'Create .env file from .env.example? (y/n)'
    if ($createEnv -eq 'y' -or $createEnv -eq 'Y') {
        Write-Host "⚙️ Creating .env file..." -ForegroundColor Blue
        Copy-Item .env.example .env
        Write-Host "📝 Please edit .env with your configuration" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host "  npm start" -ForegroundColor White
Write-Host ""
Write-Host "Then open http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Note: If you created a virtual environment, make sure to activate it first:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
