import cv2
import numpy as np
import Queue

class Digits(object):
    """ Extract the digits from a cell image.
    implements the classic 'Largest connected components' """


    def __init__(self, image):
        self.graph = image.copy()
        self.W, self.H = self.graph.shape
        self.visited = [[False for _ in xrange(self.H)] for _ in xrange(self.W)]
        self.digits = [[None for _ in xrange(self.H) for _ in xrange(self.W)]]
        self.buildDigits()


    def buildDigits(self):
        componentId = 0
        A, C = self.H/4, self.H/4*3+1
        B, D = self.W/4, self.W/4*3+1
        for i in xrange(A, C):
            for j in xrange(B, D):
                if not self.visited[i][j]:
                    self.bfs(i, j, componentId)
                    componentId += 1
        
        componentSize = np.zeros(componentId)








