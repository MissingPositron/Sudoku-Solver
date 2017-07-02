"""import modules"""
import cv2
import numpy as np

from tools import Tools
from digits import Digits


class Cells(object):
    "Extract the individual cells from the sudoku imaging"

    def __init__(self, image):
        print "Extracting cells...."
        self.tools = Tools()
        self.cells = self.extract_cells(image)
        print "done."

    def extract_cells(self, image):
        """extract the cells one by one from the image
        return the list of the cells"""
        cells = []
        width, height = image.shape
        cell_size = width / 9
        i, j = 0, 0
        for r in range(0, width, cell_size):
            row = []
            j = 0
            for c in range(0, height, cell_size):
                cell = image[r:r + cell_size, c:c + cell_size]
                cell = self.tools.make_it_square(cell, 28)
               # self.tools.show(cell, 'Before clean')
                cell = self.clean(cell)
                digit = Digits(cell).digits
                #self.tools.show(cell, 'After clean')
                digit = self.center_digit(digit)
                #self.tools.show(digit, 'After centering')
                row.append(digit // 255)
                j += 1
            cells.append(row)
            i += 1
        return cells

    def clean(self, cell):
        """ morphology transfer the cells again
        try to clean more the noise points"""
        contour = self.tools.largestContour(cell.copy())
        x, y, w, h = cv2.boundingRect(contour)
        cell = self.tools.make_it_square(cell[x:x+w, y:y+h], 28)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        cell = cv2.morphologyEx(cell, cv2.MORPH_CLOSE, kernel)
        cell = 255*(cell/130)
        return cell


    def center_digit(self, digit):
        """center digit"""
        digit = self.centerX(digit)
        digit = self.centerY(digit)
        return digit


    def centerY(self, digit):
        """ center  the Y direction"""
        top_line = self.tools.getTopLine(digit)
        bot_line = self.tools.getBottomLine(digit)
        if top_line is None or bot_line is None:
            return digit
        center_line = (top_line + bot_line) >> 1
        image_center = digit.shape[0] >> 1
        digit = self.tools.rowShift(digit, start = top_line, end = bot_line, 
        length = image_center - center_line)
        return digit


    def centerX(self, digit):
        """ center the X direction"""
        left_line = self.tools.getLeftLine(digit)
        right_line = self.tools.getRightLine(digit)
        if left_line is None or right_line is None:
            return digit
        center_line = (left_line + right_line) >> 1
        image_center = digit.shape[1] >> 1
        digit = self.tools.colShift(digit, start = left_line, end = right_line,
        length = image_center - center_line)
        return digit





