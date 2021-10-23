from enum import Enum

def manhattan_dist(point_a, point_b):
    return (abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1]))


class Direction(Enum): 
    DOWN = (1, 0)
    UP = (-1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)