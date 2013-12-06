#!/usr/bin/env python
# Stolen from Wikipedia

import numpy as np

def less_msb(x, y):
    return x < y and x < (x ^ y)

def cmp_zorder(a, b):
    j = 0
    k = 0
    x = 0
    dim = len(a)
    for k in range(dim):
        y = a[k] ^ b[k]
        if less_msb(x, y):
            j = k
            x = y
    return a[j] - b[j]

def morton_index(points):
    return sorted(points, cmp=cmp_zorder)

class MortonPoint:
    def __init__(self, point):
        self.point = np.array(point, dtype=np.uint32)
    
    def __lt__(self, other):
        if cmp_zorder(self.point, other.point) < 0:
            return True
        return False

    def __eq__(self, other):
        if cmp_zorder(self.point, other.point) == 0:
            return True
        return False