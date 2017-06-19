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




