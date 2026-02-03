"""
Sudoku Solver Web Application
Flask backend with OCR and solving capabilities
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json

from sudoku_solver import SudokuSolver
from ocr_processor import OCRProcessor
from sudoku_generator import SudokuGenerator

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max


@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@app.route('/play')
def play_mode():
    """Render the play mode page."""
    return render_template('play.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle image upload and OCR processing."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['file']
    
    # Process the image
    grid, error = OCRProcessor.process_uploaded_file(file, app.config['UPLOAD_FOLDER'])
    
    if error:
        return jsonify({'success': False, 'error': error})
    
    if grid is None:
        return jsonify({'success': False, 'error': 'Could not extract Sudoku from image'})
    
    # Validate the extracted grid
    is_valid, validation_error = SudokuSolver.validate_grid(grid)
    if not is_valid:
        return jsonify({
            'success': True,
            'grid': grid,
            'warning': f'Grid extracted but may have issues: {validation_error}'
        })
    
    return jsonify({'success': True, 'grid': grid})


@app.route('/solve', methods=['POST'])
def solve():
    """Solve the Sudoku puzzle."""
    data = request.get_json()
    
    if not data or 'grid' not in data:
        return jsonify({'success': False, 'error': 'No grid provided'})
    
    grid = data['grid']
    solve_mode = data.get('mode', 'instant')  # 'instant' or 'steps'
    
    # Validate grid
    is_valid, error = SudokuSolver.validate_grid(grid)
    if not is_valid:
        return jsonify({'success': False, 'error': error})
    
    # Create solver and solve
    solver = SudokuSolver(grid)
    solved = solver.solve()
    
    if not solved:
        return jsonify({
            'success': False,
            'error': 'No solution found for this puzzle'
        })
    
    if solve_mode == 'steps':
        # Get only final steps (one per empty cell)
        steps = solver.get_final_steps()
        
        # Store in session for navigation
        session['original_grid'] = solver.get_original()
        session['steps'] = steps
        session['current_step'] = 0
        
        return jsonify({
            'success': True,
            'original': solver.get_original(),
            'solution': solver.get_solution(),
            'steps': steps,
            'total_steps': len(steps)
        })
    else:
        # Instant solve - return final solution
        return jsonify({
            'success': True,
            'original': solver.get_original(),
            'solution': solver.get_solution()
        })


@app.route('/step/<int:step_num>', methods=['GET'])
def get_step(step_num):
    """Get a specific step in the solving process."""
    if 'steps' not in session:
        return jsonify({'success': False, 'error': 'No solving session active'})
    
    steps = session['steps']
    
    if step_num < 0 or step_num >= len(steps):
        return jsonify({'success': False, 'error': 'Invalid step number'})
    
    step = steps[step_num]
    session['current_step'] = step_num
    
    return jsonify({
        'success': True,
        'step': step,
        'step_num': step_num,
        'total_steps': len(steps),
        'is_first': step_num == 0,
        'is_last': step_num == len(steps) - 1
    })


@app.route('/validate', methods=['POST'])
def validate():
    """Validate a Sudoku grid."""
    data = request.get_json()
    
    if not data or 'grid' not in data:
        return jsonify({'success': False, 'error': 'No grid provided'})
    
    is_valid, message = SudokuSolver.validate_grid(data['grid'])
    return jsonify({
        'success': True,
        'is_valid': is_valid,
        'message': message
    })


@app.errorhandler(413)
def file_too_large(e):
    """Handle file too large error."""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 10MB'
    }), 413


@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return jsonify({
        'success': False,
        'error': 'An internal error occurred. Please try again.'
    }), 500


# ==================== PLAY MODE ROUTES ====================

@app.route('/generate', methods=['POST'])
def generate_puzzle():
    """Generate a new Sudoku puzzle."""
    data = request.get_json()
    difficulty = data.get('difficulty', 'medium')
    
    if difficulty not in ['easy', 'medium', 'hard']:
        difficulty = 'medium'
    
    # Generate puzzle
    puzzle, solution = SudokuGenerator.generate_puzzle(difficulty)
    
    # Store in session
    session['play_mode'] = True
    session['puzzle'] = puzzle
    session['solution'] = solution
    session['current_grid'] = puzzle
    session['difficulty'] = difficulty
    
    return jsonify({
        'success': True,
        'puzzle': puzzle,
        'difficulty': difficulty
    })


@app.route('/play/check', methods=['POST'])
def check_move():
    """Check if a move is correct."""
    data = request.get_json()
    
    if 'puzzle' not in session or 'solution' not in session:
        return jsonify({
            'success': False,
            'error': 'No active game'
        })
    
    row = data.get('row')
    col = data.get('col')
    value = data.get('value')
    
    if row is None or col is None or value is None:
        return jsonify({
            'success': False,
            'error': 'Missing row, col, or value'
        })
    
    puzzle = session['puzzle']
    solution = session['solution']
    current_grid = session.get('current_grid', puzzle)
    
    # Check if cell is editable
    if puzzle[row][col] != 0:
        return jsonify({
            'success': False,
            'error': 'This cell cannot be changed',
            'is_correct': False
        })
    
    # Check if value is correct
    is_correct = (solution[row][col] == value)
    
    if is_correct:
        # Update current grid
        current_grid[row][col] = value
        session['current_grid'] = current_grid
        
        # Check if puzzle is complete
        is_complete = SudokuGenerator.is_puzzle_complete(current_grid)
        if is_complete:
            is_won, message = SudokuGenerator.check_win(current_grid, solution)
            return jsonify({
                'success': True,
                'is_correct': True,
                'is_complete': True,
                'is_won': is_won,
                'message': message
            })
        
        return jsonify({
            'success': True,
            'is_correct': True,
            'message': 'Correct!'
        })
    else:
        return jsonify({
            'success': True,
            'is_correct': False,
            'message': 'Wrong answer! Try again',
            'correct_value': solution[row][col]  # Optional: remove in production
        })


@app.route('/play/hint', methods=['POST'])
def get_hint():
    """Get a hint for the current puzzle."""
    if 'puzzle' not in session or 'solution' not in session:
        return jsonify({
            'success': False,
            'error': 'No active game'
        })
    
    puzzle = session['puzzle']
    solution = session['solution']
    current_grid = session.get('current_grid', puzzle)
    
    # Find an empty cell to hint
    empty_cells = []
    for row in range(9):
        for col in range(9):
            if current_grid[row][col] == 0:
                empty_cells.append((row, col))
    
    if not empty_cells:
        return jsonify({
            'success': False,
            'error': 'Puzzle is already complete'
        })
    
    # Pick a random empty cell
    import random
    row, col = random.choice(empty_cells)
    hint_value = solution[row][col]
    
    return jsonify({
        'success': True,
        'row': row,
        'col': col,
        'value': hint_value
    })


@app.route('/play/validate', methods=['POST'])
def validate_progress():
    """Validate current progress and show errors."""
    if 'solution' not in session:
        return jsonify({
            'success': False,
            'error': 'No active game'
        })
    
    data = request.get_json()
    current_grid = data.get('grid')
    solution = session['solution']
    
    is_valid, errors = SudokuGenerator.validate_current_state(current_grid, solution)
    
    return jsonify({
        'success': True,
        'is_valid': is_valid,
        'errors': errors,
        'error_count': len(errors)
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
