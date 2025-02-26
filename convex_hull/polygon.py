from colors import BLUE, RED, GREEN, YELLOW
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

    def scanline_fill(self, fill_color=BLUE):
        min_y = min(point.y for point in self.points)
        max_y = max(point.y for point in self.points)
        filled_points = []

        for y in range(min_y, max_y + 1):
            intersections = []
            for point1, point2 in zip(self.points, self.points[1:] + [self.points[0]]):  # Обход по ребрам
                x1, y1 = point1.x, point1.y
                x2, y2 = point2.x, point2.y

                if y1 == y2:
                    continue

                if min(y1, y2) <= y < max(y1, y2):
                    x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersections.append(x)

            intersections.sort()

            for i in range(0, len(intersections) - 1, 2):
                x_start = round(intersections[i])
                x_end = round(intersections[i + 1])

                for x in range(x_start, x_end + 1):
                    filled_points.append(Point(x, y, color=fill_color))

        return filled_points

    def active_edge_fill(self, fill_color=RED):
        min_y = min(point.y for point in self.points)
        max_y = max(point.y for point in self.points)
        filled_points = []

        edges = []
        for point1, point2 in self:
            if point1.y != point2.y:
                edges.append((point1, point2))

        edges.sort(key=lambda edge: min(edge[0].y, edge[1].y))

        ael = []
        current_y = min_y

        while current_y <= max_y:
            for edge in edges:
                if min(edge[0].y, edge[1].y) == current_y:
                    ael.append(edge)

            ael = [edge for edge in ael if max(edge[0].y, edge[1].y) > current_y]

            ael.sort(key=lambda edge: edge[0].x + (current_y - edge[0].y) * (edge[1].x - edge[0].x) / (edge[1].y - edge[0].y))

            for i in range(0, len(ael), 2):
                x_start = int(ael[i][0].x + (current_y - ael[i][0].y) * (ael[i][1].x - ael[i][0].x) / (ael[i][1].y - ael[i][0].y))
                x_end = int(ael[i + 1][0].x + (current_y - ael[i + 1][0].y) * (ael[i + 1][1].x - ael[i + 1][0].x) / (ael[i + 1][1].y - ael[i + 1][0].y))
                for x in range(x_start, x_end + 1):
                    debug_info = {
                        "current_y": current_y,
                        "x_start": x_start,
                        "x_end": x_end,
                    }
                    filled_points.append(Point(x, current_y, debug=debug_info, color=fill_color))

            current_y += 1

        return filled_points

    def flood_fill(self, start_x, start_y, fill_color=GREEN):
        filled_points = []
        filled = set()
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack.pop()
            if (x, y) not in filled and self.point_in_polygon(x, y):
                # Добавляем точку в список
                debug_info = {
                    "in_poly?": self.point_in_polygon(x, y),
                    "x": x,
                    "y": y,
                }
                filled_points.append(Point(x, y, color=GREEN, debug=debug_info))
                filled.add((x, y))
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

        return filled_points

    def scanline_flood_fill(self, start_x, start_y, width, height, fill_color=YELLOW):
        filled_points = []
        filled = set()
        stack = [(start_x, start_y)]

        while stack:
            x, y = stack.pop()
            if (x, y) not in filled and self.point_in_polygon(x, y):
                left = x
                while left >= 0 and (left, y) not in filled and self.point_in_polygon(left, y):
                    debug_info = {
                        "x=left": left,
                        "y": y,
                    }
                    filled_points.append(Point(left, y, color=fill_color, debug=debug_info))
                    filled.add((left, y))
                    left -= 1
                right = x + 1
                while right < width and (right, y) not in filled and self.point_in_polygon(right, y):
                    debug_info = {
                        "x=right": right,
                        "y": y,
                    }
                    filled_points.append(Point(right, y, color=fill_color, debug=debug_info))
                    filled.add((right, y))
                    right += 1
                for i in range(left + 1, right):
                    if y + 1 < height and (i, y + 1) not in filled and self.point_in_polygon(i, y + 1):
                        stack.append((i, y + 1))
                    if y - 1 >= 0 and (i, y - 1) not in filled and self.point_in_polygon(i, y - 1):
                        stack.append((i, y - 1))

        return filled_points


class ConvexHull(Polygon):
    def __init__(self, points: list[(int, int)], algorithm="Jarvis"):
        algorithm_func = algorithms.get(algorithm)
        if not algorithm_func:
            raise Exception(f"No such convex hull algorithm: `{algorithm}`")
        hull = algorithm_func(points)
        super().__init__(hull)

    def is_convex(self) -> bool:
        return True


