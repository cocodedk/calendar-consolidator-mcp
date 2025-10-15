# Setup script for Calendar Consolidator MCP (Windows PowerShell)

param()

$ErrorActionPreference = "Stop"

Write-Host "🚀 Setting up Calendar Consolidator MCP..."

Set-Location -LiteralPath $PSScriptRoot

Write-Host "📋 Checking prerequisites..."

# Resolve Python command (prefer python/python3, fall back to py -3)
$pythonCmdInfo = $null
foreach ($candidate in @("python", "python3")) {
    $command = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($command) {
        $pythonCmdInfo = $command
        break
    }
}

$pythonPrefixArgs = @()
if (-not $pythonCmdInfo) {
    $pyLauncher = Get-Command "py" -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        $pythonCmdInfo = $pyLauncher
        $pythonPrefixArgs = @("-3")
    }
}

if (-not $pythonCmdInfo) {
    Write-Error "❌ Python 3 not found. Please install Python 3.10+ and ensure it is on PATH."
    exit 1
}

$pythonExe = if ($pythonCmdInfo.Source) { $pythonCmdInfo.Source } else { $pythonCmdInfo.Name }

function Invoke-Python {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    if ($script:PythonPrefixArgs.Count -gt 0) {
        & $script:PythonExe @script:PythonPrefixArgs @Args
    } else {
        & $script:PythonExe @Args
    }
}

$script:PythonExe = $pythonExe
$script:PythonPrefixArgs = $pythonPrefixArgs

# Validate Python version
$pythonVersionArgs = $pythonPrefixArgs + "--version"
$pythonVersionOutput = (& $pythonExe @pythonVersionArgs 2>&1).Trim()
if ($pythonVersionOutput -match "Python (?<major>\d+)\.(?<minor>\d+)\.(?<patch>\d+)") {
    $pyVersion = [Version]::new([int]$Matches.major, [int]$Matches.minor, [int]$Matches.patch)
    if ($pyVersion -lt [Version]"3.10.0") {
        Write-Error "❌ Python 3.10+ required. Detected $pythonVersionOutput"
        exit 1
    }
} else {
    Write-Warning "⚠️ Unable to determine Python version from '$pythonVersionOutput'. Continuing..."
}

# Ensure Node.js is available
$nodeCmd = Get-Command "node" -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
    Write-Error "❌ Node.js not found. Please install Node.js 18+ and ensure it is on PATH."
    exit 1
}

Write-Host "✅ Prerequisites OK"

# Optionally create and activate virtual environment
$createVenv = Read-Host "Create Python virtual environment? (y/n)"
if ($createVenv -match '^[Yy]$') {
    Write-Host "📦 Creating virtual environment..."
    Invoke-Python -Args @("-m", "venv", "venv")
    Write-Host "📦 Activating virtual environment..."
    . "$PSScriptRoot\venv\Scripts\Activate.ps1"
    $script:PythonExe = "python"
    $script:PythonPrefixArgs = @()
} elseif (Test-Path -Path "$PSScriptRoot\venv\Scripts\Activate.ps1") {
    Write-Host "ℹ️ Detected existing virtual environment. Activate it manually if desired before rerunning."
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..."
Invoke-Python -Args @("-m", "pip", "install", "-r", "requirements.txt")

# Install Node dependencies
Write-Host "📦 Installing Node dependencies..."
npm install

# Initialize database
Write-Host "💾 Initializing database..."
Invoke-Python -Args @("python/init_db.py")

# Create .env file if missing
if ((Test-Path -Path ".env") -eq $false -and (Test-Path -Path ".env.example")) {
    Write-Host "⚙️ Creating .env file..."
    Copy-Item -LiteralPath ".env.example" -Destination ".env"
    Write-Host "📝 Please edit .env with your configuration."
}

Write-Host ""
Write-Host "✅ Setup complete!"
Write-Host ""
Write-Host "To start the application:"
Write-Host "  npm start"
Write-Host ""
Write-Host "Then open http://localhost:3000"
