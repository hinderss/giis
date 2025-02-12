import numpy as np

from point import Point


def hermite_curve(points: tuple) -> list[Point]:
    p1, vend1, p4, vend4 = points

    r1 = (vend1[0] - p1[0], vend1[1] - p1[1])
    r4 = (vend4[0] - p4[0], vend4[1] - p4[1])

    P1 = np.array(p1)
    P4 = np.array(p4)
    R1 = np.array(r1)
    R4 = np.array(r4)

    hermite_matrix = np.array([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
    ])

    parameter_matrix = np.array([P1, P4, R1, R4])

    coefficients = np.dot(hermite_matrix, parameter_matrix)

    curve_points = []
    for t in np.linspace(0, 1, 1000):
        T = np.array([t**3, t**2, t, 1])
        x, y = np.dot(T, coefficients)
        point = Point(round(x), round(y))
        if point not in curve_points:
            matrix_dict = {
                "t3": f"{t ** 3:.3f}",
                "t2": f"{t ** 2:.3f}",
                "t1": f"{t:.3f}",
                "1": "1",
                "": "*",
            }
            max_len = max(len(str(int(coefficients[i, 0]))) for i in range(coefficients.shape[0]))
            for i in range(coefficients.shape[0]):
                matrix_dict[str(int(coefficients[i, 0])).zfill(max_len)] = str(int(coefficients[i, 1])).zfill(max_len)
            point.debug = matrix_dict
            curve_points.append(point)

    return curve_points
