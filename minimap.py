import numpy as np
import cv2 as cv
from enum import Enum
from time import time, sleep

class COLOR(Enum):
    BLACK   = [0,0,0]
    BLUE    = [255,0,0]
    GREEN   = [0,255,0]
    RED     = [0,0,255]
    RED4    = [191,191,255]
    YELLOW  = [0,255,255]
    ORANGE  = [0,127,255]
    MAGENTA = [255,0,255]
    GREY    = [127,127,127]
    WHITE   = [255,255,255]

Location = tuple[int, int]

class Minimap:

    map = None
    matrix = None
    

    def __init__(self, name, start=(0,0), square_size=5, radius=55, line_width=1):
        self.start = start
        self.current = start
        self.walkable = []
        self.blocked = []
        self.warpable = []
        self.catchable = []
        self.consumable = []
        self.path = []

        self.name = name
        self.square_size = square_size
        self.radius = radius
        unit = square_size+(2*line_width)
        side = (1+radius*2)
        self.map_size = (side * square_size) + (side+1) * line_width 
        self.line_width = line_width

    def update(self, current, walkable=[], blocked=[], warpable=[], catchable=[], consumable=[], path=[]):
        self.current = current
        if walkable != None: self.walkable = walkable
        if blocked != None: self.blocked = blocked
        if warpable != None: self.warpable = warpable
        if catchable != None: self.catchable = catchable
        if consumable != None: self.consumable = consumable
        if path != None: self.path = path
        self.map = None

    def set_path(self, path):
        self.path = path
        self.map = None
    
    
    def set_current(self, current):
        self.current = current
        self.map = None

    # def __translate(self, node):
    #     x, y = node[:2]
    #     return (x+self.radius, self.__grid_size()-(y+self.radius))

    # def __add_node(self, node, v):
    #     x, y = self.__translate(node)
    #     self.matrix[y][x] = v

    # def __grid_size(self):
    #     return self.radius*2+1

    # def render_matrix(self):
    #     gs = self.__grid_size()
    #     self.matrix = np.full((gs,gs), 0, int)

    #     for w in self.walkable:
    #         self.__add_node(w,1)

    #     for b in self.blocked:
    #         self.__add_node(b,2)

    #     for h in self.highlighted:
    #         self.__add_node(h,3)

    #     return self.matrix

    def __calculate_points(self, position):
        lw = self.line_width
        ss = self.square_size
        offset = int(self.map_size -ss)/2

        px, py = position[:2]

        x1=int(px*(ss+lw)+offset)
        y1=abs(int(py*(ss+lw)-offset))
        x2=int(x1+ss-1)
        y2=int(y1+ss-1)
        return x1, y1, x2, y2

    # def __pt1_to_position(self, pt1):
    #     lw = self.line_width
    #     ss = self.square_size
    #     offset = int(self.map_size -ss)/2
    #     hss = int(ss/2)

    #     x1, y1 = pt1[:2]

    #     x = int(x1/(ss+lw))-offset+hss
    #     y = abs(int(y1/(ss+lw))+offset)+hss

    #     return x, y

    def __render_square(self, position, color):
        x1, y1, x2, y2 = self.__calculate_points(position)
        cv.rectangle(self.map, (x1, y1), (x2, y2), color.value, cv.FILLED)

    # def __render_dot(self, position, color):
    #     x1, y1, x2, y2 = self.__calculate_points(position)
    #     x, y  = int((x1+x2)/2), int((y1+y2)/2)
    #     self.map[y,x] = color.value

    def __render_dot(self, position, color):
        x1, y1, x2, y2 = self.__calculate_points(position)
        cv.rectangle(self.map, (x1+1, y1+1), (x2-1, y2-1), color.value, cv.FILLED)

    # def __calculate_viewport(self, current):
    #     x, y = current
    #     return list(set(self.walkable).intersection([(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y-1),(x-1,y),(x-1,y+1)]))

    def render(self):
        self.map = np.zeros((self.map_size, self.map_size, 3), np.uint8)
        
        for e in self.walkable:
            self.__render_square(e, COLOR.WHITE)

        for b in self.blocked:
            self.__render_square(b, COLOR.GREY)

        for w in self.warpable:
            self.__render_square(w, COLOR.BLUE)
        
        for c in self.catchable:
            self.__render_square(c, COLOR.MAGENTA)

        for i in self.consumable:
            self.__render_square(i, COLOR.ORANGE)

        # view = []
        # for v in self.__calculate_viewport(self.current):
        #     view.append(v)
        #     view.extend(self.__calculate_viewport(v))
        # for v in view:   
        #     self.__render_square(v, COLOR.RED4)
            
        
        self.__render_square(self.start, COLOR.GREEN)
        self.__render_square(self.current, COLOR.RED)

        for p in self.path:
            self.__render_dot(p, COLOR.RED)

        return self.map

    def save(self, path):
        if not type(self.map) == np.ndarray:
            self.render()
        cv.imwrite(path, self.map)

    def show(self, blocking=False):
        if not type(self.map) == np.ndarray:
            self.render()
        cv.imshow(self.name, self.map)
        cv.waitKey(int(not blocking))

    # def edit_map(self, path):
    #     if path:
    #         self.map = cv.imread(path)
        
        
    #     while True:
    #         cv.imshow(self.name, self.map)
    #         key = cv.waitKey(25)
    #         if key == ord('q'):
    #             cv.destroyAllWindows()
    #             break
    #         if key == ord('s'):
    #             cv.imwrite(f'images/minimap_{time()}.jpg', self.map)

    def load_map(self, path):
        img = cv.imread(path)
        # h, w = img.shape[:2]
        start = (0,0)
        current = (0,0)
        walkable = []
        blocked = []
        warpable = []
        catchable = []
        consumable = []

        r = self.radius 
        # ss = self.square_size
        # width = w/ss
        # height = h/ss
        # hss = int(ss/2)

        # square = (self.radius*-1, self.radius)
        # pixel = (hss,hss)

        def sample(pos):
            atol = 0
            rtol = 10
            hss = int(self.square_size/2)
            x1, y1 = self.__calculate_points(pos)[:2]
            c  = img[y1+hss,x1+hss]
            if np.allclose(c,COLOR.BLACK.value,atol,rtol):
                return
            elif np.allclose(c,COLOR.WHITE.value,atol,rtol):
                walkable.append(pos)
            # elif np.allclose(c,COLOR.GREEN.value,atol,rtol):
            #     start = pos                
            #     walkable.append(pos)
            elif np.allclose(c,COLOR.GREY.value,atol,rtol):
                blocked.append(pos)
            elif np.allclose(c,COLOR.BLUE.value,atol,rtol):
                warpable.append(pos)
                blocked.append(pos)
            elif np.allclose(c,COLOR.MAGENTA.value,atol,rtol):
                catchable.append(pos)
                walkable.append(pos)
            elif np.allclose(c,COLOR.ORANGE.value,atol,rtol):
                consumable.append(pos)
                blocked.append(pos)
            elif np.allclose(c,COLOR.RED.value,atol,rtol):
                current = pos
                walkable.append(pos)

        for x in range(-r, r+1, 1):
            for y in range(r, -r-1, -1):
                sample((x,y))
        print(f'loaded current={self.current}, walkable={len(walkable)}, blocked={len(blocked)}, warpable={len(warpable)} catchable={len(catchable)} consumable={len(consumable)}')
        self.update(current,walkable,blocked,warpable,catchable,consumable)
    