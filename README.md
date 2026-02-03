# Sudoku Solver Web Application

A modern, Netflix-inspired Sudoku solver with OCR capabilities. Upload an image of a Sudoku puzzle or enter it manually, then solve it instantly or step-by-step with smooth animations.

![Dark Theme](https://img.shields.io/badge/Theme-Dark%20Netflix%20Style-e50914)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)

## Features

### 🎨 Modern UI
- **Netflix-inspired dark theme** with smooth animations
- **Responsive design** - works on desktop and mobile
- **Premium look** with rounded cards, shadows, and gradients
- Smooth hover effects and transitions

### 📷 Image Upload
- Upload Sudoku images (PNG, JPG, JPEG)
- **OCR processing** using OpenCV + Tesseract
- Automatic grid extraction and digit recognition
- Drag & drop support

### ✏️ Manual Entry
- Interactive 9×9 grid for manual input
- Smart keyboard navigation (arrow keys, tab)
- Auto-focus between cells
- Load sample puzzles

### 🧩 Two Solving Modes

#### ⚡ Solve Instantly
- Get the complete solution immediately
- Color-coded display (original vs solved numbers)

#### 🔍 Solve Step by Step
- Watch the backtracking algorithm in action
- Navigate forward/backward through steps
- Highlighted cells show current step
- Step counter

### 🎯 Additional Features
- Grid validation
- Error handling with user-friendly messages
- Loading animations
- Clear and intuitive controls

## Tech Stack

- **Backend**: Python Flask
- **Algorithm**: Backtracking for Sudoku solving
- **OCR**: OpenCV + Tesseract
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Styling**: Pure CSS with CSS Variables

## Prerequisites

Before running the application, make sure you have:

1. **Python 3.8 or higher**
2. **Tesseract OCR** installed on your system

### Installing Tesseract

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**Windows:**
- Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
- Add Tesseract to your PATH

## Installation

1. **Clone or download this project:**
```bash
cd sudoku-solver
```

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser and navigate to:**
```
http://localhost:5000
```

3. **Start solving Sudoku puzzles!**

## Usage Guide

### Method 1: Upload an Image

1. Click the **"Upload Image"** card or drag & drop an image
2. Wait for OCR processing to extract the grid
3. Review and edit the extracted numbers if needed
4. Click **"Solve Instantly"** or **"Solve Step by Step"**

**Tips for best OCR results:**
- Use clear, high-contrast images
- Ensure the Sudoku grid is fully visible
- Avoid skewed or rotated images
- Good lighting is important

### Method 2: Manual Entry

1. Click on the **"Manual Entry"** grid
2. Type digits 1-9 in empty cells
3. Use arrow keys or Tab to navigate
4. Click **"Load Sample"** to try an example puzzle
5. Click **"Solve Instantly"** or **"Solve Step by Step"**

### Solving Options

**Solve Instantly (⚡):**
- Shows the final solved puzzle immediately
- Original numbers are displayed in gray
- Solved numbers are shown in green

**Solve Step by Step (🔍):**
- Watch each step of the solving process
- Use **Next/Previous** buttons to navigate
- Current step is highlighted in green
- Step counter shows progress

## Project Structure

```
sudoku-solver/
├── app.py                 # Flask application and routes
├── sudoku_solver.py       # Backtracking algorithm with step tracking
├── ocr_processor.py       # OCR processing with OpenCV + Tesseract
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   └── style.css         # Netflix-style CSS
├── templates/
│   └── index.html        # Main HTML template
└── uploads/              # Temporary folder for image uploads
```

## How It Works

### Sudoku Solving Algorithm

The application uses a **backtracking algorithm** to solve Sudoku puzzles:

1. Find an empty cell
2. Try digits 1-9
3. Check if the digit is valid (row, column, 3×3 box)
4. If valid, place digit and recurse
5. If no solution, backtrack and try next digit
6. Each step is recorded for step-by-step playback

### OCR Processing

The OCR module:

1. Preprocesses the image (grayscale, blur, threshold)
2. Detects the Sudoku grid contour
3. Applies perspective transform for top-down view
4. Extracts individual cells
5. Uses Tesseract to recognize digits
6. Returns a 9×9 array

## Troubleshooting

**OCR not working:**
- Ensure Tesseract is installed and in PATH
- Try with a clearer image
- Check Tesseract installation: `tesseract --version`

**Port already in use:**
- Change port in `app.py`: `app.run(debug=True, port=5001)`

**Dependencies issues:**
- Update pip: `pip install --upgrade pip`
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

**Import errors:**
- Ensure virtual environment is activated
- Check Python version: `python --version` (should be 3.8+)

## Browser Compatibility

Tested and working on:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

## Performance

- Typical solving time: < 1 second
- OCR processing: 2-5 seconds depending on image
- Step-by-step mode: Instant navigation between steps

## Future Enhancements

Possible improvements:
- Multiple puzzle difficulty levels
- Hint system
- Puzzle generator
- Save/load puzzles
- User accounts
- Leaderboard
- Mobile app version

## Credits

**Created by Madhav**

- Algorithm: Classic backtracking
- OCR: OpenCV + Tesseract
- Design: Inspired by Netflix UI

## License

This project is open source and available for personal and educational use.

## Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section
2. Ensure all prerequisites are installed
3. Verify Python and Tesseract versions

---

**Enjoy solving Sudoku puzzles! 🎯**
