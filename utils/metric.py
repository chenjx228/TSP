from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import math

def euclidean_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return dist
