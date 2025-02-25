from point import Point
from utils import cross_product


def line_intersection(line1_start: Point, line1_end: Point, line2_start: Point, line2_end: Point) -> Point | None:
    a, b = line1_start, line1_end
    c, d = line2_start, line2_end

    ccw1 = cross_product(a, b, c)
    ccw2 = cross_product(a, b, d)
    ccw3 = cross_product(c, d, a)
    ccw4 = cross_product(c, d, b)

    if ((ccw1 * ccw2) < 0) and ((ccw3 * ccw4) < 0):
        x1, y1, _ = a
        x2, y2, _ = b
        x3, y3, _ = c
        x4, y4, _ = d

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None

        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
        return Point(x, y)
    return None
