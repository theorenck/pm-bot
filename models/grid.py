from math import inf as infinity
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

from models import Colors, Color

Location = Tuple[int, int]

@dataclass
class Annotation:
    name: str
    color: Color = Colors.BLUE
    locations: List[Location] = None
    weight: float = infinity

Annotations = Optional[Dict[str, Annotation]]

class Grid(object):

    __annotations: Annotations = None

    def __init__(self, width: int, height: int, current: Location = (0,0), 
        traversable: List[Location] = [], blocked: List[Location] = [],
        annotations: Annotations = {}, weights: Dict[Location, float] = {}):
        self.width = width
        self.height = height
        self.current = current
        self.traversable = traversable
        self.blocked = blocked
        self.__weights = weights
        self.__annotations = annotations

    @property
    def annotations(self) -> Annotations:
        return self.__annotations

    @annotations.setter
    def annotations(self, value: Annotations):
        self.__annotations = value

    def __getattr__(self, name: str):
        if self.__annotations and name in self.__annotations.keys():
            return self.__annotations[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def in_bounds(self, id: Location) -> bool:
        x, y = id
        return abs(x) <= self.width and abs(y) <= self.height
    
    def is_traversable(self, id: Location) -> bool:
        return id in self.traversable
    
    def neighbors(self, id: Location) -> List[Location]:
        (x, y) = id
        neighbors = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)] # E N W S
        results = filter(self.in_bounds, neighbors)
        results = filter(self.is_traversable, results)
        return list(results)
    
    def cost(self, current: Location, goal: Location) -> float:
        if self.is_traversable(goal):
            return self.__weights.get(goal, 1.0)
        return infinity