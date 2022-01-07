# TODO: Move it to a proper unit test suite
# import unittest
# class TestStringMethods(unittest.TestCase):

from models import Colors
from models import Annotation
from models import Minimap

def main():
    legend = [
        Annotation('warpable', Colors.BLUE),
        Annotation('catchable', Colors.MAGENTA, weight=2),
        Annotation('consumable', Colors.ORANGE, weight=10),
    ]
    m = Minimap.load('images/d1_minimap_annotated.jpg', 'Mortyland', legend)
    # m.map_width = m.map_width * 2 
    # m.grid.warpable.locations = []
    # m.grid.annotations = {}
    # m.save('images/minimap.jpg')
    m.show(True)
    m.grid.warpable.locations = []
    m.map = None
    m.show(True)
    # Minimap.load('images/d1_minimap_annotated.jpg','Mortyland', legend).show(True)
    pass

main()