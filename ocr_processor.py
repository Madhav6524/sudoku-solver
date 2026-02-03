"""
OCR Processor Module
Extracts Sudoku grid from images using OpenCV and Tesseract
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
import os


class OCRProcessor:
    """Process Sudoku images and extract grid values."""
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in OCRProcessor.ALLOWED_EXTENSIONS
    
    @staticmethod
    def preprocess_image(image):
        """Preprocess image for better OCR results."""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        return thresh
    
    @staticmethod
    def find_sudoku_contour(thresh):
        """Find the largest square contour (the Sudoku grid)."""
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            return None
        
        # Find the largest contour by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        for contour in contours:
            # Approximate the contour
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            
            # If it has 4 corners, it might be the Sudoku grid
            if len(approx) == 4:
                return approx
        
        return None
    
    @staticmethod
    def order_points(pts):
        """Order points in: top-left, top-right, bottom-right, bottom-left."""
        rect = np.zeros((4, 2), dtype="float32")
        pts = pts.reshape(4, 2)
        
        # Top-left has smallest sum, bottom-right has largest
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        # Top-right has smallest diff, bottom-left has largest
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect
    
    @staticmethod
    def perspective_transform(image, contour):
        """Apply perspective transform to get a top-down view."""
        rect = OCRProcessor.order_points(contour)
        (tl, tr, br, bl) = rect
        
        # Compute the width
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        
        # Compute the height
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        
        # Use the larger dimension for a square output
        size = max(maxWidth, maxHeight)
        
        dst = np.array([
            [0, 0],
            [size - 1, 0],
            [size - 1, size - 1],
            [0, size - 1]
        ], dtype="float32")
        
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (size, size))
        
        return warped
    
    @staticmethod
    def extract_cells(warped):
        """Extract individual cells from the warped Sudoku grid."""
        cells = []
        height, width = warped.shape[:2]
        cell_height = height // 9
        cell_width = width // 9
        
        for row in range(9):
            row_cells = []
            for col in range(9):
                # Calculate cell boundaries with some padding
                y1 = row * cell_height
                y2 = (row + 1) * cell_height
                x1 = col * cell_width
                x2 = (col + 1) * cell_width
                
                cell = warped[y1:y2, x1:x2]
                row_cells.append(cell)
            cells.append(row_cells)
        
        return cells
    
    @staticmethod
    def recognize_digit(cell):
        """Recognize digit in a single cell using Tesseract."""
        # Preprocess the cell
        if len(cell.shape) == 3:
            gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        else:
            gray = cell
        
        # Resize for better OCR
        height, width = gray.shape
        if height < 50 or width < 50:
            gray = cv2.resize(gray, (50, 50), interpolation=cv2.INTER_CUBIC)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Add padding
        padded = cv2.copyMakeBorder(thresh, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=0)
        
        # Invert back for Tesseract (white background, black text)
        inverted = cv2.bitwise_not(padded)
        
        # Check if cell is mostly empty
        white_ratio = np.sum(padded == 255) / padded.size
        if white_ratio < 0.03:  # Less than 3% white pixels = empty cell
            return 0
        
        # Configure Tesseract for single digit recognition
        config = '--psm 10 --oem 3 -c tessedit_char_whitelist=123456789'
        
        try:
            text = pytesseract.image_to_string(inverted, config=config)
            text = text.strip()
            
            if text and text.isdigit() and 1 <= int(text) <= 9:
                return int(text)
        except Exception:
            pass
        
        return 0
    
    @classmethod
    def process_image(cls, image_path):
        """
        Main method to process a Sudoku image and extract the grid.
        Returns (grid, error_message)
        """
        try:
            # Read the image
            image = cv2.imread(image_path)
            if image is None:
                return None, "Could not read image file"
            
            # Preprocess
            thresh = cls.preprocess_image(image)
            
            # Find the Sudoku contour
            contour = cls.find_sudoku_contour(thresh)
            
            if contour is not None:
                # Apply perspective transform
                warped = cls.perspective_transform(image, contour)
            else:
                # Use the whole image if no contour found
                warped = image
            
            # Extract cells
            cells = cls.extract_cells(warped)
            
            # Recognize digits
            grid = []
            for row in cells:
                grid_row = []
                for cell in row:
                    digit = cls.recognize_digit(cell)
                    grid_row.append(digit)
                grid.append(grid_row)
            
            return grid, None
            
        except Exception as e:
            return None, f"Error processing image: {str(e)}"
    
    @classmethod
    def process_uploaded_file(cls, file_storage, upload_folder):
        """
        Process an uploaded file from Flask.
        Returns (grid, error_message)
        """
        if not file_storage or file_storage.filename == '':
            return None, "No file selected"
        
        if not cls.allowed_file(file_storage.filename):
            return None, "Invalid file type. Please upload PNG, JPG, or JPEG"
        
        # Check file size
        file_storage.seek(0, 2)  # Seek to end
        size = file_storage.tell()
        file_storage.seek(0)  # Seek back to start
        
        if size > cls.MAX_FILE_SIZE:
            return None, "File too large. Maximum size is 10MB"
        
        # Save temporarily
        filename = f"temp_sudoku_{os.urandom(8).hex()}.png"
        filepath = os.path.join(upload_folder, filename)
        
        try:
            file_storage.save(filepath)
            grid, error = cls.process_image(filepath)
            return grid, error
        finally:
            # Clean up temp file
            if os.path.exists(filepath):
                os.remove(filepath)
