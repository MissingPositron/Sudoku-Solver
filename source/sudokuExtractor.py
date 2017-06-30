""" import module """
import cv2
import numpy as np

from tools import Tools
from cells import Cells


class Extractor(object):
    """ manipulate the image and extract the sudoku region """

    def __init__(self, path):
        self.tools = Tools()
        self.image = self.loadImage(path)
        self.preprocess()
        sudoku_image = self.cropSudoku()
        sudoku_image = self.strengthen(sudoku_image)
        self.cells = Cells(sudoku_image).cells


    def loadImage(self, path):
        """ load the Image"""
        color_img = cv2.imread(path)
        if color_img is None:
            raise IOError('Image not loaded')
        print 'Image Loaded.'
        return color_img


    def preprocess(self):
        """ image preprocessing"""
        print 'preprocessing...'
        self.image = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.image = self.tools.thresholdify(self.image)
        kernel = cv2.getStructingElement(cv2.MORPH_ELLIPSE, (2, 2))
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel)
        self.tools.show(self.image, 'After preprocessing.')
        print 'done'


    def cropSudoku(self):
        """ crop out the region of sudoku base on the largest contour"""
        print 'cropping out the sudoku...'
        contour = self.tools.largestContour(self.image.copy())
        sudoku_img = self.tools.cut_out_sudoku_puzzle(self.image.copy(), contour)
        self.tools.show(sudoku_img, 'Crop out.')
        print 'done.'
        return sudoku_img


    def strengthen(self, sudoku_img):
        """ use warp prespective to smooth the image"""
        print 'Strengthen the image...'
        largest = self.tools.largest4sideContour(sudoku_img.copy())
        approx = self.tools.approx(largest)
        corners = self.tools.get_rectangle_corners(approx)
        sudoku_img = self.tools.warp_perspective(corners, sudoku_img)
        self.tools.show(sudoku_img, 'Strengthen sudoku grid.')
        print 'done.'
        return sudoku_img
        













