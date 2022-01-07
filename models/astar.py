from typing import Dict, List
from queue import PriorityQueue

from models import Grid, Location

class AStarSearch:

    def __init__(self, grid: Grid):
        self.grid = grid

    @staticmethod
    def heuristic(a, b) -> float:
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)
    
    @staticmethod
    def reconstruct_path(previous, start: Location, goal: Location) -> List[Location]:
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = previous[current]
        path.reverse() # optional
        return path

    def search(self, start: Location, goal: Location):
        frontier: PriorityQueue = PriorityQueue()
        frontier.put((0, start))
        previous: Dict[Location,Location] = {}
        current_cost = {}
        previous[start] = None
        current_cost[start] = 0
        
        while not frontier.empty():
            _, current = frontier.get()
            if current == goal:
                break
            
            for next in self.grid.neighbors(current):
                new_cost = current_cost[current] + self.grid.cost(current, next)
                if next not in current_cost or new_cost < current_cost[next]:
                    current_cost[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put((priority, next))
                    previous[next] = current
        
        return self.reconstruct_path(previous, start, goal)