from line.algorithms.bresenham import bresenham_algorithm
from line.algorithms.dda import dda_algorithm
from line.algorithms.wu import wu_algorithm

algorithms = {
    "DDA": dda_algorithm,
    "Bresenham": bresenham_algorithm,
    "Wu": wu_algorithm,
}
