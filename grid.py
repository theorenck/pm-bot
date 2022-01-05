from typing import Dict, List, Iterator, Tuple

Location = Tuple[int, int]

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.walkable: List[Location] = []
        self.blocked: List[Location] = []
        # self.weights: Dict[Location, float] = {}
    
    def in_bounds(self, id: Location) -> bool:
        (x, y) = id
        return abs(x) <= self.width and abs(y) <= self.height
    
    def passable(self, id: Location) -> bool:
        return id in self.walkable
    
    def neighbors(self, id: Location) -> List[Location]:
        (x, y) = id
        neighbors = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)] # E N W S
        # see "Ugly paths" section for an explanation:
        # if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return list(results)
    
    def cost(self, current: Location, goal: Location) -> float:
        # return self.weights.get(next, 1)
        return 1

# def main():
#     g = Grid(55,55)
#     g.walkable = [(-55, -54)]
#     print(g.neighbors((-55,-55)))
# main()