#!/bin/bash
# Setup script for Calendar Consolidator MCP

set -e

echo "🚀 Setting up Calendar Consolidator MCP..."

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

echo "✅ Prerequisites OK"

# Create virtual environment (optional)
read -p "Create Python virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node dependencies
echo "📦 Installing Node dependencies..."
npm install

# Initialize database
echo "💾 Initializing database..."
python3 python/init_db.py

# Create .env file (optional)
if [ ! -f .env ] && [ -f .env.example ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env with your configuration"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  npm start"
echo ""
echo "Then open http://localhost:3000"
