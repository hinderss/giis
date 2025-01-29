import math
from point import Point


def wu_algorithm(x1, y1, x2, y2) -> list[Point]:
    points = []

    def plot(x, y, intensity, debug=None):
        intensity = max(0, min(1, intensity))
        r = g = b = int(255 * (1 - intensity))
        points.append(Point(x, y, (r, g, b), debug=debug))

    def fpart(x):
        return x - math.floor(x)

    def rfpart(x):
        return 1 - fpart(x)

    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1
    gradient = dy / dx if dx != 0 else 1

    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = xend
    ypxl1 = math.floor(yend)

    debug_info = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "steep": steep,
        "dx": dx,
        "dy": dy,
        "gradient": gradient,
        "xend": xend,
        "yend": yend,
        "xgap": xgap,
        "xpxl1": xpxl1,
        "ypxl1": ypxl1,
    }

    if steep:
        plot(ypxl1, xpxl1, rfpart(yend) * xgap, debug_info)
        plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap, debug_info)
    else:
        plot(xpxl1, ypxl1, rfpart(yend) * xgap, debug_info)
        plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap, debug_info)

    intery = yend + gradient

    # Вторая точка
    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend
    ypxl2 = math.floor(yend)

    debug_info = {
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "steep": steep,
        "dx": dx,
        "dy": dy,
        "gradient": gradient,
        "xend": xend,
        "yend": yend,
        "xgap": xgap,
        "xpxl2": xpxl2,
        "ypxl2": ypxl2,
    }

    if steep:
        plot(ypxl2, xpxl2, rfpart(yend) * xgap, debug_info)
        plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap, debug_info)
    else:
        plot(xpxl2, ypxl2, rfpart(yend) * xgap, debug_info)
        plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap, debug_info)

    if steep:
        for x in range(xpxl1 + 1, xpxl2):
            debug_info = {
                "x": x,
                "intery": intery,
                "floor_intery": math.floor(intery),
                "rfpart_intery": rfpart(intery),
                "fpart_intery": fpart(intery),
            }
            plot(math.floor(intery), x, rfpart(intery), debug_info)
            plot(math.floor(intery) + 1, x, fpart(intery), debug_info)
            intery += gradient
    else:
        for x in range(xpxl1 + 1, xpxl2):
            debug_info = {
                "x": x,
                "intery": intery,
                "floor_intery": math.floor(intery),
                "rfpart_intery": rfpart(intery),
                "fpart_intery": fpart(intery),
            }
            plot(x, math.floor(intery), rfpart(intery), debug_info)
            plot(x, math.floor(intery) + 1, fpart(intery), debug_info)
            intery += gradient

    return points