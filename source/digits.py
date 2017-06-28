""" import modules"""
import Queue
import numpy as np


class Digits(object):
    """ Extract the digits from a cell image.
    implements the classic 'Largest connected components' """

    def __init__(self, image):
        self.graph = image.copy()
        self.wid, self.hei = self.graph.shape
        self.visited = [[False for _ in xrange(
            self.hei)] for _ in xrange(self.wid)]
        self.digits = [[None for _ in xrange(
            self.hei) for _ in xrange(self.wid)]]
        self.build_digits()

    def build_digits(self):
        """ search in the 1/4 to 3/4 region of the image
        find the connected components by bfs.
        find the largets componnents"""

        component_id = 0
        hei_start, hei_stop = self.hei / 4, self.hei / 4 * 3 + 1
        wid_start, wid_stop = self.wid / 4, self.wid / 4 * 3 + 1
        for i in xrange(hei_start, hei_stop):
            for j in xrange(wid_start, wid_stop):
                if not self.visited[i][j]:
                    self.bfs(i, j, component_id)
                    component_id += 1

        component_size = [0 for _ in xrange(component_id)]
        for row in self.digits:
            for cell in row:
                if cell is not None:
                    component_size[cell] += 1

        largest = component_size.index(max(component_size))
        for i in xrange(self.hei):
            for j in xrange(self.wid):
                self.digits[i][j] = 255 if self.digits[i][j] == largest else 0
        self.digits = np.asarray(self.digits, dtype=np.uint8)

    def bfs(self, i, j, component_id):
        """ breath first search"""
        queue = Queue.Queue()
        queue.put((i, j))
        while not queue.empty():
            i, j = queue.get()
            invalid_row = i not in xrange(0, self.hei)
            invalid_col = j not in xrange(0, self.wid)
            invalid_pixel = invalid_row or invalid_col or self.graph[i][j] != 255

            if invalid_pixel or self.visited[i][j]:
                continue

            self.digits[i][j] = component_id
            self.visited[i][j] = True
            for delta_i in [-1, 0, 1]:
                for delta_j in [-1, 0, 1]:
                    queue.put((i + delta_i, j + delta_j))
