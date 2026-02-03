"""
Sudoku Generator Module
Generates valid Sudoku puzzles with different difficulty levels
"""

import random
import copy
from sudoku_solver import SudokuSolver


class SudokuGenerator:
    """Generate Sudoku puzzles with varying difficulty levels."""
    
    # Number of cells to remove for each difficulty
    DIFFICULTY_LEVELS = {
        'easy': 30,      # Remove 30 cells
        'medium': 45,    # Remove 45 cells
        'hard': 55       # Remove 55 cells
    }
    
    @staticmethod
    def generate_complete_grid():
        """Generate a complete, valid Sudoku grid."""
        grid = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the diagonal 3x3 boxes first (they don't affect each other)
        for box in range(3):
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            for i in range(3):
                for j in range(3):
                    grid[box * 3 + i][box * 3 + j] = numbers[i * 3 + j]
        
        # Use solver to fill the rest
        solver = SudokuSolver(grid)
        solver.solve()
        return solver.get_solution()
    
    @staticmethod
    def remove_cells(grid, difficulty='medium'):
        """
        Remove cells from a complete grid to create a puzzle.
        Returns (puzzle_grid, solution_grid)
        """
        if difficulty not in SudokuGenerator.DIFFICULTY_LEVELS:
            difficulty = 'medium'
        
        cells_to_remove = SudokuGenerator.DIFFICULTY_LEVELS[difficulty]
        puzzle = copy.deepcopy(grid)
        
        # Get list of all cell positions
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        
        removed = 0
        for row, col in positions:
            if removed >= cells_to_remove:
                break
            
            # Save the value
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            
            # Check if puzzle still has unique solution
            # (For simplicity, we skip this check and just remove cells)
            # A more robust implementation would verify uniqueness
            removed += 1
        
        return puzzle, grid
    
    @classmethod
    def generate_puzzle(cls, difficulty='medium'):
        """
        Generate a complete Sudoku puzzle.
        Returns (puzzle_grid, solution_grid)
        """
        complete_grid = cls.generate_complete_grid()
        puzzle_grid, solution_grid = cls.remove_cells(complete_grid, difficulty)
        return puzzle_grid, solution_grid
    
    @staticmethod
    def check_cell(puzzle, row, col, value, solution):
        """
        Check if a value placed in a cell is correct.
        Returns (is_correct, message)
        """
        if puzzle[row][col] != 0:
            return False, "This cell is already filled"
        
        if value < 1 or value > 9:
            return False, "Value must be between 1 and 9"
        
        # Check against solution
        if solution[row][col] == value:
            return True, "Correct!"
        else:
            return False, "Wrong answer! Try again"
    
    @staticmethod
    def validate_current_state(grid, solution):
        """
        Validate current grid state against solution.
        Returns (is_valid, errors_list)
        """
        errors = []
        
        for row in range(9):
            for col in range(9):
                if grid[row][col] != 0 and grid[row][col] != solution[row][col]:
                    errors.append({
                        'row': row,
                        'col': col,
                        'value': grid[row][col],
                        'correct': solution[row][col]
                    })
        
        return len(errors) == 0, errors
    
    @staticmethod
    def is_puzzle_complete(grid):
        """Check if puzzle is completely filled."""
        for row in grid:
            if 0 in row:
                return False
        return True
    
    @staticmethod
    def check_win(grid, solution):
        """
        Check if the puzzle is solved correctly.
        Returns (is_won, message)
        """
        if not SudokuGenerator.is_puzzle_complete(grid):
            return False, "Puzzle not complete yet"
        
        is_valid, errors = SudokuGenerator.validate_current_state(grid, solution)
        
        if is_valid:
            return True, "Congratulations! You solved it correctly! 🎉"
        else:
            return False, f"There are {len(errors)} incorrect cells"
