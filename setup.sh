#!/bin/bash

echo "🚀 Smart Document Manager - Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL 12 or higher."
    echo "   Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "   macOS: brew install postgresql"
    exit 1
fi

echo "✅ PostgreSQL found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your:"
    echo "   - DATABASE_URL (PostgreSQL connection string)"
    echo "   - OPENAI_API_KEY (from https://platform.openai.com/api-keys)"
    echo ""
    read -p "Press Enter after you've updated .env file..."
fi

# Create database if it doesn't exist
echo ""
echo "🗄️  Setting up database..."
read -p "Enter PostgreSQL username (default: postgres): " PG_USER
PG_USER=${PG_USER:-postgres}

echo "Creating database 'smart_docs' if it doesn't exist..."
psql -U $PG_USER -tc "SELECT 1 FROM pg_database WHERE datname = 'smart_docs'" | grep -q 1 || psql -U $PG_USER -c "CREATE DATABASE smart_docs"
echo "✅ Database ready"

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p chroma_db
echo "✅ Directories created"

echo ""
echo "════════════════════════════════════════"
echo "✨ Setup complete! "
echo "════════════════════════════════════════"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python app.py"
echo "  3. Open browser: http://localhost:5000"
echo ""
echo "Happy documenting! 📚"
