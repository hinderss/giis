from typing import Iterable

from colors import BLACK


class Point:
    def __init__(self, x, y, color: Iterable[int] = BLACK, debug: dict | None = None):
        self.x = x
        self.y = y
        self.color = tuple(color)
        self.debug: dict | None = debug

    def __iter__(self):
        return iter((self.x, self.y, self.color))

    def __str__(self):
        return f"({self.x}, {self.y}, {self.color})"

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.color})"

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x, self.y, self.color) == (other.x, other.y, other.color)
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.color))
