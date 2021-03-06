#!/usr/bin/env python

# Perform Hilbert & Z-orderings on a set of vectors in n-dimensional
# space and find k-nearest neighbors based on this ordering

# CPSC 4110 - Approximation Algorithms
# Implemented by:
# Camara Lerner - https://github.com/lernerc
# Christopher Rabl - https://github.com/crabl 

# Based on algorithm detailed by Michael Connor and Piyush Kumar
# http://doi.ieeecomputersociety.org/10.1109/TVCG.2010.9

import numpy as np
import sys
import math
import time

from point import *

V_CONSTANT = 4 # Platform-dependent constant

# Euclidean distance between two points
def distance(a, b):
    return math.sqrt(((a - b) ** 2).sum())

# Find the indices of the k smallest items in a set S, assuming that S contains a zero element
def k_smallest_indices(k, S):
    # We have to look at [1:k+1] because we assume that S contains the point that we are looking for
    return [idx for (s, idx) in sorted(zip(S,range(len(S))))][1:k+1]

# Find the k nearest neighbors to a point in a given set S
def set_knn(point, k, S):
    distances = [distance(point,s) for s in S]

    # Find the indices of the k smallest items in S
    smallest_indices = k_smallest_indices(k, distances)

    # Find the points corresponding to those indices
    nearest_neighbors = []
    for i in smallest_indices:
        if S[i] != point:
            nearest_neighbors.append(S[i])

    return nearest_neighbors

def box_dist(point, box_center, box_radius):
    return distance(point, box_center) - box_radius # This is correct... Although it's a circle. So yeah.

# The radius of a set is the largest distance between any two points in the set S
def set_radius(S):
    distances = [distance(p0, p1) for p0 in S for p1 in S]
    return max(distances)

def csearch(point, A_i, i, k, low, hi):
    if (hi-low) < V_CONSTANT:
        return set_knn(point[i], k, list(set(A_i + point[low:hi+1])))

    mid = int((hi + low) / 2)
    A_i = set_knn(point[i], k, list(set(A_i + [point[mid]])))
    if box_dist(point[i], point[low], distance(point[low], point[hi])) > set_radius(A_i):
        return A_i
    if point[i] < point[mid]:
        A_i = csearch(point, A_i, i, k, low, mid - 1)
        if point[mid] < point[i].shift(math.ceil(set_radius(A_i))):
            A_i = csearch(point, A_i, i, k, mid + 1, hi)
    else:
        A_i = csearch(point, A_i, i, k, mid + 1, hi)
        if point[i].shift(-1 * math.ceil(set_radius(A_i))) < point[mid]:
            A_i = csearch(point, A_i, k, i, low, mid - 1)

    return A_i

def construct(points, i, k):
    A_i = set_knn(points[i], k, points[max(0,i-k):min(len(points),i+k)])
    if len(A_i) < k:
        A_i.append(points[i])
    upper = 0
    lower = 0

    if points[i].shift(math.ceil(set_radius(A_i))) < points[min(len(points)-1, i+k)]:
        upper = i
    else:
        I = 0
        while points[i].shift(math.ceil(set_radius(A_i))) < points[i+2**I-1]:
            I += 1
        upper = min(i + 2**I, len(points)-1)

    if points[i].shift(-1 * math.ceil(set_radius(A_i))) > points[i-k]:
        lower = i
    else:
        I = 0
        while points[i].shift(-1 * math.ceil(set_radius(A_i))) > points[i-2**I]:
            I += 1
        lower = max(i - 2**I, 0)

    if lower != upper:
        A_i = csearch(points, A_i, i, k, lower, upper)

    return A_i
        

def main(file_name, k, validate):
    #dataset = [(x,y) for x in range(20) for y in range(20)]
    dataset = np.genfromtxt(str(file_name), delimiter="\t", dtype=np.uint32)

    print "Generating Hilbert ordering:",
    HP = [Point(item, sftype='hilbert') for item in dataset]
    print "Sorting..."
    HP.sort(key=lambda h: h.index_hilbert()) # Have to use this or we run into issues with 'long'

    print "Generating Morton ordering:",
    MP = [Point(item, sftype='morton') for item in dataset]
    print "Sorting..."
    MP.sort(cmp=cmp_zorder)


    k = int(k)
    precision = 32
    t_cum_hilbert = 0
    t_cum_morton = 0
    t_cum_naive0 = 0
    t_cum_naive1 = 0

    print ""
    print "Approximate", str(k)+"-Nearest Neighbours"
    print "Running AKNN comparison on", len(HP), "points in", len(HP[0]), "dimensions..."
    distance_ratio_hilbert = 0
    distance_ratio_morton = 0
    for i in range(len(HP)):
        iter_fraction = float(i) / len(HP)

        # Progress bar
        amtDone = iter_fraction * 100
        if not validate:
            sys.stdout.write("\r%.1f%%" %amtDone)
            sys.stdout.flush()

        t0_hilbert = time.time()
        AKNN_hilbert = construct(HP, i, k)
        tf_hilbert = time.time() - t0_hilbert
        t_cum_hilbert += tf_hilbert

        t0_morton = time.time()
        AKNN_morton = construct(MP, i, k)
        tf_morton = time.time() - t0_morton
        t_cum_morton += tf_morton

        t0_naive0 = time.time()
        KNN_i0 = set_knn(HP[i], k, HP)
        tf_naive0 = time.time() - t0_naive0
        t_cum_naive0 += tf_naive0

        t0_naive1 = time.time()
        KNN_i1 = set_knn(MP[i], k, MP)
        tf_naive1 = time.time() - t0_naive1
        t_cum_naive1 += tf_naive1

        if(validate):
            print "========== Iteration",i,"=========="
            print "Hilbert Point:", HP[i]
            print "Z-Order Point:", MP[i]
            print "Hilbert AKNN:", AKNN_hilbert
            print " Naive KNN 0:", KNN_i0
            print "Z-Order AKNN:", AKNN_morton
            print " Naive KNN 1:", KNN_i1

        
        distance_ratio_hilbert += set_radius(AKNN_hilbert) / set_radius(KNN_i0)
        distance_ratio_morton += set_radius(AKNN_morton) / set_radius(KNN_i1)

    print ""
    print "Time Hilbert AKNN:", t_cum_hilbert
    print "Time Z-Order AKNN:", t_cum_morton
    print "Time Naive KNN 0:", t_cum_naive0
    print "Time Naive KNN 1:", t_cum_naive1
    print "Average radius ratio Hilbert from OPT:", distance_ratio_hilbert / len(HP)
    print "Average radius ratio Z-Order from OPT:", distance_ratio_morton / len(MP)

if __name__ == "__main__":
    validate = False
    try:
        if sys.argv[3] == "validate":
            validate = True
    except:
        pass
    main(sys.argv[1], sys.argv[2], validate)
