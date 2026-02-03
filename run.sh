#!/bin/bash

# Sudoku Solver - Quick Start Script

echo "🎯 Sudoku Solver - Starting Application"
echo "========================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if Tesseract is installed
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  WARNING: Tesseract OCR is not installed!"
    echo "📝 Install it with: brew install tesseract (macOS)"
    echo "   OCR features will not work without it."
    echo ""
fi

# Create uploads directory
mkdir -p uploads

echo ""
echo "✅ Setup complete!"
echo "🚀 Starting Flask server..."
echo ""
echo "📍 Open your browser and go to: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Run the Flask app
python app.py
