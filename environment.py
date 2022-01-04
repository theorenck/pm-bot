from time import time, sleep
from typing import Iterable
import win32gui, win32ui, win32con
import numpy as np
import cv2 as cv
import threading
import matplotlib.pyplot as plt
import pickle
from queue import PriorityQueue
from heapq import heappush, heappop

from windowcapture import Vision
from windowscontroller import Control
from minimap import Minimap, Location

# TODO: Rename it to Navigation
class Environment:

    # constructor
    def __init__(self, window_name=None, forefront=False, resolution=(960,540)):
        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
        
        self.chwnd = win32gui.GetWindow(self.hwnd, win32con.GW_CHILD)
        if not self.chwnd:
            raise Exception('Child window not found: {}'.format(window_name))

        if forefront:
            win32gui.SetForegroundWindow(self.hwnd)

        self.vision = Vision(self.hwnd, resolution)
        self.control = Control(self.chwnd)
        self.map = Minimap('Minimap')

    @staticmethod
    def h(current, goal):
        cx, cy = current
        gx, gy = goal
        return (abs(cx - gx) + abs(cy - gy))

    @staticmethod
    def heuristic(a, b) -> float:
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def neighbors(self, node, walkable=True):
        x, y = node
        edges = [(x,y+1),(x-1,y),(x,y-1),(x+1,y)]
        if walkable:
            return list(set(self.map.walkable).difference(self.map.catchable).intersection(edges))
        else:
            return edges.values()
    
    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        # path.append(start) # optional
        path.reverse() # optional
        return path

    def cost(self, current, next):
        return 1
        # original_cost = 1
        # nudge = 0
        # (x1, y1) = current
        # (x2, y2) = next
        # if (x1 + y1) % 2 == 0 and x2 != x1: nudge = 1
        # if (x1 + y1) % 2 == 1 and y2 != y1: nudge = 1
        # return original_cost + 0.001 * nudge


    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {}
        current_cost = {}
        came_from[start] = None
        current_cost[start] = 0
        
        while not frontier.empty():
            _, current = frontier.get()
            if current == goal:
                break
            
            for next in self.neighbors(current):
                new_cost = current_cost[current] + self.cost(current, next)
                if next not in current_cost or new_cost < current_cost[next]:
                    current_cost[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put((priority, next))
                    came_from[next] = current
        
        return self.reconstruct_path(came_from, start, goal)
    # def astar(self, start, goal, reversePath=False):

    #     def reached_goal():
    #         return start == goal

    #     def h(current, goal):
    #         cx, cy = current
    #         gx, gy = goal
    #         return (abs(cx - gx) + abs(cy - gy))

    #     # if reached_goal():
    #     #     return [start]

    #     open = PriorityQueue()
    #     for p in enumerate(self.map.walkable - self.map.catchable - [start]):
    #         open.put((h(p,goal),p))
    #     open.put((0,start))
    #     path={}
       
    #     while open:
    #         current = heappop(open)
    #         if reached_goal():
    #             return self.reconstruct_path(current, reversePath)
    #         current.out_openset = True
    #         current.closed = True
    #         for neighbor in [open[n] for n in self.neighbors(current.data)]:
    #             if neighbor.closed:
    #                 continue
    #             tentative_gscore = current.gscore + \
    #                 self.distance_between(current.data, neighbor.data)
    #             if tentative_gscore >= neighbor.gscore:
    #                 continue
    #             neighbor.came_from = current
    #             neighbor.gscore = tentative_gscore
    #             neighbor.fscore = tentative_gscore + \
    #                 self.heuristic_cost_estimate(neighbor.data, goal)
    #             if neighbor.out_openset:
    #                 neighbor.out_openset = False
    #                 heappush(open, neighbor)
    #     return None
    
    # infinite depth-first search
    def explore(self, start=(0,0), limit=100000, show_minimap=True, show_debug=True):
        depth=0

        self.map.current = start
        current = self.map.current

        if not self.map.walkable: 
            self.map.walkable=[start]
        explored=self.map.walkable

        if not self.map.blocked: 
            self.map.blocked=[]
        blocked=self.map.blocked

        if not self.map.blocked: 
            self.map.blocked=[]
        blocked=self.map.blocked
        
        frontier=[start]
        path={}

        def draw_minimap():
            if show_minimap:
                self.map.update(current, explored, blocked)
                self.map.save('images/minimap.jpg')
                self.map.show()

        def succeeded():
            path[neighbour] = current
            explored.append(neighbour)
            frontier.append(neighbour)

        def failed():
            blocked.append(neighbour)

        def backtracked():
            frontier.append(parent)

        def debug(message):
            if show_debug:
                base = f'explored={len(explored)+len(blocked)}, depth={depth}, current={current},'
                print(base, message)

        while frontier and depth <= limit:
            current=frontier.pop()

            unavailable = set(explored).union(blocked)
            adj = self.__adj(current)
            neighbours = [n for n in adj if n not in unavailable]
            
            debug('neighbours={}'.format(neighbours))

            for neighbour in neighbours:

                if self.move((current, neighbour)):
                    debug(f'moved to {neighbour}')
                    succeeded()
                    depth+=1
                    current = neighbour
                    draw_minimap()
                    break
                else:
                    debug(f'blocked at {neighbour}')                        
                    failed()
                    draw_minimap()

            parent = path[current]

            if depth > 0 and set(neighbours).issubset(set(blocked)) and parent:
                if self.move((current,parent)):
                    debug(f'backtracked to {parent}')
                    backtracked()
                    depth-=1
                    draw_minimap()
                else:                        
                    debug(f'failed to backtrack to {parent}')
                    frontier.append(current)
                                    
        return explored, blocked, path, depth, start, current

    def move(self, dir, retry=True, debug=False, threshold=50):

        step_duration = 0.23
        cooldown_duration = 0.23
        
        if type(dir) != str:
            current, next = dir[:2]
            dir = self.__calculate_direction(current, next)
        
        frames = []
        def get_screenshots():
            while len(frames) < 8:
                frames.append(self.vision.get_screenshot())
                sleep(0.043)

        def diff_percentage(diff):
            copy = diff.copy()
            copy.astype(np.uint8)
            return np.count_nonzero(copy)/copy.size * 100
        
        def attempt_move():
            s = threading.Thread(target=get_screenshots, args=(), daemon=True)
            s.start()
            self.control.walk(dir,1,cooldown_duration,step_duration)
            s.join()
    
            trust = 0
            if debug: print(f'len(frames)={len(frames)}')
            if len(frames) == 8:
                for i in range(5,8):
                    d = cv.absdiff(frames[0], frames[i])
                    t = diff_percentage(d)
                    if t > trust: trust = t
            if debug: print (f'moved from ({current} to ({next}), trust={trust}')
            return trust > threshold

        success = attempt_move()
        if success: return success
        if retry: 
            frames = []
            success = attempt_move()

        return success
    
    def __adj(self, node):
        x, y = node[:2]
        vertices = {
            'W': (x,y+1),
            'A': (x-1,y),
            'S': (x,y-1),
            'D': (x+1,y)
        }     
        return vertices.values()

    def __calculate_direction(self, current, neighbour):
        t = tuple(np.subtract(neighbour, current))
        directions = {
            ( 0, 1):'W',
            (-1, 0):'A',
            ( 0,-1):'S',
            ( 1, 0):'D',
        }
        return directions[t]

    def display_multiple_img(self,images, rows = 1, cols=1):
        fig, ax = plt.subplots(nrows=rows,ncols=cols )
        for i,image in enumerate(images):
            ax.ravel()[i].imshow(image[1])
            ax.ravel()[i].set_title(image[0])
            ax.ravel()[i].set_axis_off()
        plt.tight_layout()
        plt.show()

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
        

def main():
    env = Environment('BlueStacks')
    t = time()
    env.map.load_map('images/d1_minimap.jpg')
    print(f'time={time()-t}')
    # env.map.current = (35, 44)
    # walkable = list(set(env.map.walkable).difference(env.map.catchable))
    print(f'consumable={env.map.consumable}')
    for c in env.map.consumable:
        print(f'pos={c} -> h={env.h(env.map.current,c)}')
    t = time()
    env.map.show()

    # start = (0,0)
    # goals = [(26,13),(13,29),(34,44),(19,51),(3,47),(-5,51),(-27,43),(-21,22),(26,13),(0,0)]
    # path = []
    # for i,g in enumerate(goals):
    #     s = start if i == 0 else goals[i-1]
    #     path.extend(env.a_star_search(s, g))
    # print(len(path),path)
    # env.map.set_path(path)
    # env.map.show()
    # print(f'time={time()-t}')

    # for i,next in enumerate(path):
    #     current = start if i == 0 else path[i-1]
    #     env.move((current,next))
    #     env.map.set_current(next)
    #     env.map.show()

    # start = (0,0)
    # depth_limit = 1000
    # t = time()
    # # explored, blocked, path, depth, _, current = env.dfs(start,blocked,highlights,depth_limit,True,True,True,depth_limit)
    # explored, blocked, path, depth, _, current = env.explore(start, depth_limit)
    # print('current={}, time={}'.format(current,time()-t))
    # state = {
    #     'player':{
    #         'depth': depth,
    #         'start': start,
    #         'current': current
    #     },
    #     'explored': explored,
    #     'blocked': blocked,
    #     'path': path
    # }
    # f=open('state.txt','wb')  #opened the file in write and binary mode 
    # pickle.dump(state,f) #dumping the content in the variable 'content' into the file
    # f.close()
    # user presses a key
    cv.waitKey(0)
    
    # Destroying present windows on screen
    cv.destroyAllWindows()

main()


