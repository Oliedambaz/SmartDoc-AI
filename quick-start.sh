#!/bin/bash
# SmartDoc AI - Quick Start Script

echo "🚀 SmartDoc AI - Quick Start"
echo "=============================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p uploads

echo ""
echo "=============================="
echo "✅ Setup Complete!"
echo "=============================="
echo ""
echo "To start the application, run:"
echo "  source venv/bin/activate  (or venv\\Scripts\\activate on Windows)"
echo "  python -m uvicorn app.main:app --reload"
echo ""
echo "Then visit:"
echo "  🌐 http://localhost:8000/index.html"
echo "  📚 http://localhost:8000/docs"
echo ""
