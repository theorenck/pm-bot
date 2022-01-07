from typing import List
from math import inf as infinity

import numpy as np
import cv2 as cv

from models import Colors, Location, Annotation, Annotations, Grid

class Minimap(object):

    LINE_WIDTH: int = 1
    TILE_SIZE: int = 5

    map: np.ndarray = None

    def __init__(self, name: str, grid: Grid):
        self.name = name
        self.grid = grid

    def __calculate_points(self, position):
        lw = self.LINE_WIDTH
        ts = self.TILE_SIZE
        w_offset = int(self.map_width -ts)/2
        h_offset = int(self.map_height -ts)/2
        px, py = position[:2]
        x1 = int(px * (ts + lw) + w_offset)
        y1 = abs(int(py * (ts + lw) - h_offset))
        x2 = int(x1 + ts - 1)
        y2 = int(y1 + ts - 1)
        return x1, y1, x2, y2

    def __draw_tile(self, position, color):
        x1, y1, x2, y2 = self.__calculate_points(position)
        cv.rectangle(self.map, (x1, y1), (x2, y2), color.bgr(), cv.FILLED)

    def __draw_dot(self, position, color):
        x1, y1, x2, y2 = self.__calculate_points(position)
        cv.rectangle(self.map, (x1+1, y1+1), (x2-1, y2-1), color.value, cv.FILLED)

    def draw(self) -> np.ndarray:
        lw = self.LINE_WIDTH
        ts = self.TILE_SIZE
        width, height = self.grid.width, self.grid.height
        self.map_width  = 2 * width * (lw + ts) + 2 * lw + ts
        self.map_height = 2 * height * (lw + ts) + 2 * lw + ts

        self.map = np.zeros((self.map_height, self.map_width, 3), np.uint8)
        g = self.grid
        for t in g.traversable:
            self.__draw_tile(t, Colors.WHITE)
        for b in g.blocked:
            self.__draw_tile(b, Colors.GRAY)
        for a in g.annotations.values():
            for l in a.locations:
                self.__draw_tile(l, a.color)
        self.__draw_tile(g.current, Colors.RED)
        return self.map

    def save(self, path):
        if not type(self.map) == np.ndarray:
            self.draw()
        cv.imwrite(path, self.map)

    def show(self, blocking=False):
        if not type(self.map) == np.ndarray:
            self.draw()
        cv.imshow(self.name, self.map)
        cv.waitKey(int(not blocking))

    @classmethod
    def load(cls, path: str, name: str, legend: List[Annotation] = []) -> 'Minimap':
        img = cv.imread(path)

        current = (0,0)
        traversable = []
        blocked = []
        annotations: Annotations = {}

        legend_by_color = {a.color: a for a in legend}

        map_height, map_width = img.shape[:2]
        lw = cls.LINE_WIDTH
        ts = cls.TILE_SIZE
        width  = int((map_width  - (2 * lw) - ts) / (2 * (lw + ts)))
        height = int((map_height - (2 * lw) - ts) / (2 * (lw + ts)))

        w_offset = int(map_width - ts)/2
        h_offset = int(map_height - ts)/2
        hts = int(ts/2)

        atol = 0
        rtol = 10

        def sample(location: Location):
            px, py = location
            x1 = int(px * (ts + lw) + w_offset) + hts
            y1 = abs(int(py * (ts + lw) - h_offset)) + hts
            c  = img[y1,x1]

            if np.allclose(c, Colors.BLACK.bgr(), atol, rtol):
                return
            elif np.allclose(c, Colors.WHITE.bgr(), atol, rtol):
                traversable.append(location)
            elif np.allclose(c, Colors.GRAY.bgr(), atol, rtol):
                blocked.append(location)
            elif np.allclose(c, Colors.RED.bgr(), atol, rtol):
                current = location
                traversable.append(location)
            else:
                for lc in legend_by_color.keys():
                    if np.allclose(c, lc.bgr(), atol, rtol):
                        a = legend_by_color[lc]
                        if a.name not in annotations.keys():
                            annotations[a.name] = Annotation(a.name, a.color, [], a.weight)
                        annotations[a.name].locations.append(location)
                        if infinity > a.weight > 0:
                            traversable.append(location)
                        else:
                            blocked.append(location)
                        break

        for x in range(-width, width+1, 1):
            for y in range(height, -height-1, -1):
                sample((x,y))
        
        g = Grid(width, height, current, traversable, blocked, annotations)
        
        return cls(name,g)