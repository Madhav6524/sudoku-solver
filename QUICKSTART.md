# 🚀 Quick Start Guide

Get your Sudoku Solver running in 3 easy steps!

## Prerequisites

1. **Python 3.8+** - Check with: `python3 --version`
2. **Tesseract OCR** - For image processing

### Install Tesseract (Required for OCR)

**macOS:**
```bash
brew install tesseract
```

**Verify installation:**
```bash
tesseract --version
```

## Installation

### Option 1: Automated Setup (Recommended)

Simply run:
```bash
cd sudoku-solver
./run.sh
```

This script will:
- Create a virtual environment
- Install all dependencies
- Start the Flask server automatically

### Option 2: Manual Setup

```bash
cd sudoku-solver

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

## Access the Application

Once the server is running, open your browser and go to:

**http://localhost:5000**

## Usage

### Method 1: Upload an Image 📷
1. Click "Upload Image" or drag & drop a Sudoku image
2. Wait for OCR to extract the grid
3. Review and edit if needed
4. Click "Solve Instantly" or "Solve Step by Step"

### Method 2: Manual Entry ✏️
1. Click on cells in the "Manual Entry" grid
2. Type numbers 1-9
3. Use arrow keys to navigate
4. Or click "Load Sample" to try an example
5. Click your preferred solve method

## Features

✅ **Solve Instantly** - Get the complete solution immediately  
✅ **Step by Step** - Watch the algorithm solve it move by move  
✅ **OCR Support** - Upload images of Sudoku puzzles  
✅ **Netflix-style UI** - Beautiful dark theme with animations  
✅ **Mobile Responsive** - Works on phones and tablets  

## Troubleshooting

**Port 5000 already in use?**
- Edit `app.py` and change `port=5000` to `port=5001`

**OCR not working?**
- Make sure Tesseract is installed: `tesseract --version`
- Use clear, high-contrast images

**Import errors?**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

## File Structure

```
sudoku-solver/
├── app.py              # Main Flask application
├── sudoku_solver.py    # Solving algorithm
├── ocr_processor.py    # Image processing
├── requirements.txt    # Dependencies
├── run.sh             # Quick start script
├── static/
│   └── style.css      # Netflix-style theme
└── templates/
    └── index.html     # Main page
```

## Need More Help?

See the full **README.md** for detailed documentation.

---

**Created by Madhav** | Enjoy solving Sudoku! 🎯
