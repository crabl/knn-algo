import numpy as np
from zorder import *

def morton_order(points):
    order_map = dict(zip(range(1, len(points)+1), points))
    dims = len(points[0])
    matrix_size = max([max(item) for item in zip(*points)])+1
    M = np.zeros([matrix_size for i in range(dims)], dtype=int)
    for key in order_map:
        M[order_map[key]] = key
    print M
    zorder(M)
    zordered_array = []
    for m in M.flat:
        if m != 0:
            zordered_array.append(order_map[m])

    return zordered_array


    
    
