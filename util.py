from dataclasses import dataclass, field
from typing import Any
from enum import Enum


def manhattan_dist(point_a, point_b):
    return (abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1]))


# https://stackoverflow.com/questions/66448588/is-there-a-way-to-make-a-priority-queue-sort-by-the-priority-value-in-a-tuple-on?noredirect=1&lq=1
@dataclass(order=True)
class PrioGame:
    priority: int
    item: Any=field(compare=False)

    def get_item(self):
        return self.item


class Direction(Enum): 
    DOWN = (1, 0)
    UP = (-1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)

if __name__ == '__main__':
    pass