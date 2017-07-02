"""test the functionality"""

from sudokuExtractor import Extractor

img_path = '../data/test_pic/test1.jpg'
print img_path
cells = Extractor(img_path)