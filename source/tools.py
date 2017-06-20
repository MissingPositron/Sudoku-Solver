import cv2
import numpy as np


class Tools(object):
    """ Imaging manipulation tools """
    def show(self, img, windowName = 'Image'):
        resolution = [1280.0, 720.0]
        scale_width = resolution[0]/img.shape[1]
        scale_height = resolution[1]/img.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(img.shape[1]*scale)
        window_height = int(img.shape[0]*scale)

        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(windowName, window_width, window_height)

        cv2.imshow(windowName, img)
        cv2.waitkey(0)
        cv2.destroyAllWindows()


    def isCV2(self):
        return cv2.__version__.startswith('2.')


    def thresholdify(self, img):
        img = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                    cv2.THRESH_BINARY, 11, 3)
        return 255 - img


    def Canny(self, img):
        edges = cv2.Canny(img, 100, 200)
        self.show(edges)
        return edges


    def dilate(self,img, kernel):
        cv2.dilate(img, kernel)
        return img


    def largestContour(self, image):
        if self.isCV2():
            contours, h = cv2.findContours(
                img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, h = cv2.findContours(
                img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return max(contours, key = cv2.contourArea)


    def largest4sideContour(self, img):
        if self.isCV2():
            contours, h = cv2.findContours(
                img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            _, contours, h = cv2.findContours(
                img, cv2.RETR_TREE, cv2.CHAIN_APPROX_CHAIN)

        contours = sorted(contours, key = cv2.ContourArea, reverse = True)
        for cnt in contours[:min(5, len(contours))]:
            im = img.copy()
            cv2.drawContours(im, cnt, -1, (255, 255, 255), 5)
            self.show(im, 'contour')

            if len(self.approx(cnt)) == 4:
                return cnt
        return None


    def make_it_square(self, img, length = 306):
        return cv2.resize(img, (length, length))


    def area(self, img):
        return float(img.shape[0]*img.shape[1])


    def cut_out_sudoku_puzzle(self, img, contour):
        x, y, w, h = cv2.bondingRect(contour)
        img = img[y:y+h, x:x+w]
        return self.make_it_square(img, min(img.shape))


    def binarized(self, img):
        for i in xrange(img.shape[0]):
            for j in xrange(img.shape[1]):
                img[i][j] = 255*int(img[i][j]!=255)
        return img


    def approx(self, cnt):
        peri = cv2.arcLength(cnt, True)
        app = cv2.approxPolyDp(cnt, 0.01*peri, True)
        return app








