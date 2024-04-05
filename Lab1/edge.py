import math

from point import Point


class Edge:

    def __init__(self, start: Point, end: Point, weight: int):
        self.start = start
        self.end = end
        self.weight = weight
        self.rotation = math.atan2(end.y - start.y, end.x - start.x)
