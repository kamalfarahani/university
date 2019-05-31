from math import sqrt
from typing import List
from functools import reduce

class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        
        return Point(x, y)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y

        return Point(x, y)
    
    def __truediv__(self, n: float):
        return Point(self.x / n, self.y / n)
    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
    def norm(self):
        return sqrt(self.x**2 + self.y**2)


def euclidean_distance(p1: Point, p2: Point) -> float:
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2


def manhattan_distance(p1: Point, p2: Point) -> float:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def mean_of_points(points: List[Point]) -> Point:
    return reduce(lambda p1, p2: p1 + p2, points) / len(points)
