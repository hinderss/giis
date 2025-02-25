import math

from point import Point


def sort_points_clockwise(points):
    points = list(set(points))
    center_x = sum(x for x, y, _ in points) / len(points)
    center_y = sum(y for x, y, _ in points) / len(points)

    def calculate_angle(point):
        x, y, _ = point
        angle = math.atan2(y - center_y, x - center_x)
        return -angle

    sorted_points = sorted(points, key=calculate_angle)
    return sorted_points


def hex_color(color: tuple[int, int, int]):
    r, g, b = color
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("Цветовые значения должны быть в диапазоне от 0 до 255")
    return f"#{r:02x}{g:02x}{b:02x}"


class Arrow:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.width = None
        self.color = None
        self.arrowhead = None
        self.line = None

    def create(self, x1, y1, x2, y2, color="gray", width=1):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.color = color

        self.line = self.canvas.create_line(x1, y1, x2, y2, width=width, fill=color, tags="debug")

        self.draw_arrowhead()

    def draw_arrowhead(self):
        arrow_length = 10
        angle = math.atan2(self.y2 - self.y1, self.x2 - self.x1)

        x3 = self.x2 - arrow_length * math.cos(angle - math.pi / 6)
        y3 = self.y2 - arrow_length * math.sin(angle - math.pi / 6)
        x4 = self.x2 - arrow_length * math.cos(angle + math.pi / 6)
        y4 = self.y2 - arrow_length * math.sin(angle + math.pi / 6)

        self.arrowhead = self.canvas.create_polygon(
            self.x2, self.y2, x3, y3, x4, y4, fill=self.color, outline=self.color, tags="debug",
        )


def cross_product(a: Point, b: Point, c: Point):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
