from point import Point


class Line:
    def __init__(self, point1: (int, int), point2: (int, int)):
        self.start: Point = Point(*point1)
        self.end: Point = Point(*point2)

    def __iter__(self):
        return iter((self.start, self.end))
