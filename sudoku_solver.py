"""
Sudoku Solver Module
Uses backtracking algorithm with step-by-step tracking
"""

import copy


class SudokuSolver:
    def __init__(self, grid):
        """
        Initialize solver with a 9x9 grid.
        Empty cells should be 0.
        """
        self.original_grid = copy.deepcopy(grid)
        self.grid = copy.deepcopy(grid)
        self.steps = []
        self.solved = False
    
    def is_valid(self, grid, row, col, num):
        """Check if placing num at grid[row][col] is valid."""
        # Check row
        if num in grid[row]:
            return False
        
        # Check column
        for r in range(9):
            if grid[r][col] == num:
                return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if grid[r][c] == num:
                    return False
        
        return True
    
    def find_empty(self, grid):
        """Find the next empty cell (value 0)."""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return (r, c)
        return None
    
    def solve(self):
        """
        Solve the Sudoku using backtracking.
        Records each step for step-by-step playback.
        """
        self.steps = []
        self.grid = copy.deepcopy(self.original_grid)
        self.solved = self._solve_recursive()
        return self.solved
    
    def _solve_recursive(self):
        """Recursive backtracking solver."""
        empty = self.find_empty(self.grid)
        if not empty:
            return True  # Solved
        
        row, col = empty
        
        for num in range(1, 10):
            if self.is_valid(self.grid, row, col, num):
                self.grid[row][col] = num
                # Record this step
                self.steps.append({
                    'row': row,
                    'col': col,
                    'value': num,
                    'grid': copy.deepcopy(self.grid)
                })
                
                if self._solve_recursive():
                    return True
                
                # Backtrack
                self.grid[row][col] = 0
        
        return False
    
    def get_final_steps(self):
        """
        Get only the final solution steps (one per empty cell).
        Returns a list of steps showing each cell being filled with its final answer.
        """
        if not self.solved:
            return []
        
        final_steps = []
        current_grid = copy.deepcopy(self.original_grid)
        
        # Find all empty cells in original grid
        for row in range(9):
            for col in range(9):
                if self.original_grid[row][col] == 0:
                    # This cell was empty, so add its final value
                    current_grid[row][col] = self.grid[row][col]
                    final_steps.append({
                        'row': row,
                        'col': col,
                        'value': self.grid[row][col],
                        'grid': copy.deepcopy(current_grid)
                    })
        
        return final_steps
    
    def solve_instant(self):
        """Solve and return only the final grid."""
        if self.solve():
            return self.grid
        return None
    
    def get_steps(self):
        """Get all solving steps for step-by-step display."""
        return self.steps
    
    def get_solution(self):
        """Get the final solved grid."""
        if self.solved:
            return self.grid
        return None
    
    def get_original(self):
        """Get the original input grid."""
        return self.original_grid
    
    @staticmethod
    def validate_grid(grid):
        """
        Validate that a grid is a proper Sudoku puzzle.
        Returns (is_valid, error_message)
        """
        if not grid or len(grid) != 9:
            return False, "Grid must have 9 rows"
        
        for i, row in enumerate(grid):
            if len(row) != 9:
                return False, f"Row {i+1} must have 9 columns"
            for j, val in enumerate(row):
                if not isinstance(val, int) or val < 0 or val > 9:
                    return False, f"Invalid value at row {i+1}, col {j+1}"
        
        # Check for duplicate values in rows, columns, and boxes
        for i in range(9):
            # Check row
            row_vals = [grid[i][j] for j in range(9) if grid[i][j] != 0]
            if len(row_vals) != len(set(row_vals)):
                return False, f"Duplicate values in row {i+1}"
            
            # Check column
            col_vals = [grid[j][i] for j in range(9) if grid[j][i] != 0]
            if len(col_vals) != len(set(col_vals)):
                return False, f"Duplicate values in column {i+1}"
        
        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                box_vals = []
                for r in range(3):
                    for c in range(3):
                        val = grid[box_row * 3 + r][box_col * 3 + c]
                        if val != 0:
                            box_vals.append(val)
                if len(box_vals) != len(set(box_vals)):
                    return False, f"Duplicate values in box ({box_row+1}, {box_col+1})"
        
        return True, "Valid grid"


def parse_grid_string(grid_string):
    """
    Parse a string representation of a Sudoku grid.
    Accepts various formats: comma-separated, space-separated, etc.
    """
    # Remove whitespace and split
    lines = grid_string.strip().split('\n')
    grid = []
    
    for line in lines:
        # Handle various separators
        line = line.replace(',', ' ').replace('|', ' ').replace('.', '0')
        values = line.split()
        
        if len(values) == 9:
            try:
                row = [int(v) if v.isdigit() else 0 for v in values]
                grid.append(row)
            except ValueError:
                continue
        elif len(line.replace(' ', '')) == 9:
            # Handle continuous string like "530070000"
            clean = line.replace(' ', '')
            row = [int(c) if c.isdigit() else 0 for c in clean]
            grid.append(row)
    
    if len(grid) != 9:
        return None
    
    return grid
