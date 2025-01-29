import math


def sort_points_clockwise(points):
    points = list(set(points))
    center_x = sum(x for x, y, _ in points) / len(points)
    center_y = sum(y for x, y, _ in points) / len(points)
    center = (center_x, center_y)

    def calculate_angle(point):
        x, y, _ = point
        angle = math.atan2(y - center_y, x - center_x)
        return -angle

    sorted_points = sorted(points, key=calculate_angle)
    return sorted_points
