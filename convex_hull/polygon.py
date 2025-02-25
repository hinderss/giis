from convex_hull.algorithms import algorithms
from convex_hull.algorithms.line_intersection import line_intersection
from point import Point

import uuid

from utils import cross_product


class Polygon:
    def __init__(self, points):
        self.points = []
        self.tag = None
        if len(points) < 3:
            raise Exception("Полигон должен иметь хотя бы 3 вершины.")
        if points and isinstance(points[0], Point):
            self.points = points
        elif points and isinstance(points[0], (tuple, list)):
            self.points = [Point(x, y) for x, y in points]

    def __iter__(self):
        n = len(self.points)
        for i in range(n):
            yield self.points[i], self.points[(i + 1) % n]

    def point_in_polygon(self, x, y):
        inside = False
        for point1, point2 in self:
            x1, y1, _ = point1
            x2, y2, _ = point2
            if y > min(y1, y2):
                if y <= max(y1, y2):
                    if x <= max(x1, x2):
                        if y1 != y2:
                            xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                        if y1 == y2 or x <= xinters:
                            inside = not inside
        return inside

    def line_polygon_intersection(self, line_start: Point, line_end: Point):
        intersections = []
        for point1, point2 in self:
            intersection = line_intersection(line_start, line_end, point1, point2)
            if intersection:
                intersections.append(intersection)
        return intersections

    def draw(self, canvas):
        self.tag = uuid.uuid4()
        for point1, point2 in self:
            x1, y1, _ = point1
            x2, y2, _ = point2
            canvas.create_line(x1, y1, x2, y2, fill="blue", tags=self.tag)
        return self.tag

    def is_convex(self) -> bool:
        if len(self.points) < 3:
            raise Exception("Полигон должен иметь хотя бы 3 вершины.")

        n = len(self.points)
        if n == 3:
            return True

        sign = 0
        for i in range(n):
            a = self.points[i]
            b = self.points[(i + 1) % n]
            c = self.points[(i + 2) % n]
            cp = cross_product(a, b, c)
            if cp == 0:
                continue
            if sign == 0:
                sign = 1 if cp > 0 else -1
            elif (cp > 0 and sign == -1) or (cp < 0 and sign == 1):
                return False
        return True


class ConvexHull(Polygon):
    def __init__(self, points: list[(int, int)], algorithm="Jarvis"):
        algorithm_func = algorithms.get(algorithm)
        if not algorithm_func:
            raise Exception(f"No such convex hull algorithm: `{algorithm}`")
        hull = algorithm_func(points)
        super().__init__(hull)

    def is_convex(self) -> bool:
        return True


