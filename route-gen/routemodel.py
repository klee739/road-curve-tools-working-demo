from curvemodel import GPS
from enum import Enum
import copy

class RoutePosition:
    def __init__(self):
        self.coordinates=GPS()
        self.direction=-1

    def __init__(self, gpsPosition, travelDirection):
        self.coordinates = copy.deepcopy(gpsPosition)
        self.direction = copy.deepcopy(travelDirection)

class RoadSectionType(Enum):
    START = 0
    LINE = 1
    CURVE = 2

class TurnDirection(Enum):
    LEFT = 0
    RIGHT = 1

class RoadSection:
    def __init__(self):
        self.type=RoadSectionType.LINE
        self.length=-1

class RoadSectionStart(RoadSection):
    def __init__(self):
        self.type = RoadSectionType.START
        self.coordinates=GPS()
        self.direction= -1

    def __init__(self, coordinates, travelDirection):
        self.type = RoadSectionType.START
        self.coordinates=copy.deepcopy(coordinates)
        self.direction=copy.deepcopy(travelDirection)

class RoadSectionLine(RoadSection):
    def __init__(self):
        self.type = RoadSectionType.LINE
        self.length = -1

    def __init__(self, length):
        self.type = RoadSectionType.LINE
        self.length = copy.deepcopy(length)

class RoadSectionCurve(RoadSection):
    def __init__(self):
        self.type = RoadSectionType.CURVE
        self.turn = TurnDirection.LEFT
        self.radius = -1
        self.length = -1

    def __init__(self, turnDirection, radius, length):
        self.type = RoadSectionType.CURVE
        self.turn = copy.deepcopy(turnDirection)
        self.radius = copy.deepcopy(radius)
        self.length = copy.deepcopy(length)
