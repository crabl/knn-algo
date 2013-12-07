#!/usr/bin/env python

# Perform Hilbert & Z-orderings on a set of vectors in n-dimensional
# space and find k-nearest neighbors based on this ordering

# CPSC 4110 - Approximation Algorithms
# Camara Lerner & Chris Rabl

import numpy
import sys
import math
import bitstring
import numpy as np 
import time
import warnings

# Ignore exponent divide-by-zero warning
#warnings.simplefilter("ignore", RuntimeWarning) 

from point import *

V_CONSTANT = 4 # Platform-dependent constant

# Euclidean distance between two points
def distance(a, b):
    return math.sqrt(((a - b) ** 2).sum())

# Find the indices of the k smallest items in a set S, assuming that S contains a zero element
def k_smallest_indices(k, S):
    # We have to look at [1:k+1] because we assume that S contains the point
    # that we are looking for
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
    return distance(point, box_center) - box_radius # This is roughly incorrect... Although it's a circle. So yeah.

# The radius of a set is the largest distance between any two points in the set S
def set_radius(S):
    distances = [distance(p0, p1) for p0 in S for p1 in S]
    return np.max(distances)

def csearch(point, A_i, i, k, low, hi):
    if (hi-low) < V_CONSTANT:
        return set_knn(point[i], k, list(set(A_i + point[low:hi+1])))

    mid = int((hi + low) / 2)
    A_i = set_knn(point[i], k, list(set(A_i + [point[mid]])))
    if box_dist(point[i], point[low], distance(point[low], point[hi])) > set_radius(A_i):
        return A_i
    if point[i] < point[mid]:
        A_i = csearch(point, A_i, i, k, low, mid - 1)
        if point[mid] < point[i].shift(np.ceil(set_radius(A_i))):
            A_i = csearch(point, A_i, i, k, mid + 1, hi)
    else:
        A_i = csearch(point, A_i, i, k, mid + 1, hi)
        if point[i].shift(-1 * np.ceil(set_radius(A_i))) < point[mid]:
            A_i = csearch(point, A_i, k, i, low, mid - 1)

    return A_i

def construct(points, i, k):
    A_i = set_knn(points[i], k, points[max(0,i-k):min(len(points),i+k)])
    if len(A_i) < k:
        A_i.append(points[i])
    upper = 0
    lower = 0
        
    #print "Iteration:", i
    #print "point_i:", points[i]
    #print "A_i:", A_i
    # if p_i^ceil(rad(A_i)) < p_i+k
    if points[i].shift(math.ceil(set_radius(A_i))) < points[min(len(points)-1, i+k)]:
        upper = i
    else:
        I = 0
        while points[i].shift(math.ceil(set_radius(A_i))) < points[i+2**I-1]:
            I += 1
        upper = min(i + 2**I, len(points)-1)

    # if p_i^-ceil(rad(A_i)) > p_i-k
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
        

def main(file_name, k):
    dataset = [(x,y) for x in range(20) for y in range(20)]
    #dataset = np.genfromtxt(str(file_name), delimiter="\t", dtype=np.uint32)

    HP = [Point(item, sftype='hilbert') for item in dataset]
    HP.sort(cmp=cmp_hilbert)
    MP = [Point(item, sftype='morton') for item in dataset]

    t_cum_aknn = 0
    t_cum_knn = 0
    k = int(k)
    precision = 32
    """
    print "Running Z-order AKNN comparison on", len(P), "points..."
    average_distance_from_opt = 0
    for i in range(len(P)):
        iter_fraction = float(i) / len(P)

        # Progress bar
        amtDone = iter_fraction * 100
        sys.stdout.write("\r%.1f%%" %amtDone)
        sys.stdout.flush()

        t0_aknn = time.time()
        AKNN_i = construct_morton(P, i, k)
        tf_aknn = time.time() - t0_aknn
        t_cum_aknn += tf_aknn

        t0_knn = time.time()
        KNN_i = set_knn(P[i], k, P)
        tf_knn = time.time() - t0_knn
        t_cum_knn += tf_knn
        
        average_distance_from_opt += set_radius(AKNN_i) / set_radius(KNN_i)
    print ""
    print "Time Morton AKNN:", t_cum_aknn
    print "Time OPT:", t_cum_knn
    print "Average times distance from OPT:", average_distance_from_opt / len(P)
    """
    t_cum_aknn = 0
    t_cum_knn = 0
    print ""
    print "Running Hilbert AKNN comparison on", len(HP), "points..."
    average_distance_from_opt = 0
    for i in range(len(HP)):
        iter_fraction = float(i) / len(HP)

        # Progress bar
        amtDone = iter_fraction * 100
        sys.stdout.write("\r%.1f%%" %amtDone)
        sys.stdout.flush()

        t0_aknn = time.time()
        AKNN_i = construct(HP, i, k)
        tf_aknn = time.time() - t0_aknn
        t_cum_aknn += tf_aknn

        t0_knn = time.time()
        KNN_i = set_knn(HP[i], k, HP)
        tf_knn = time.time() - t0_knn
        t_cum_knn += tf_knn
        
        average_distance_from_opt += set_radius(AKNN_i) / set_radius(KNN_i)
        print HP[i], "\tAKNN:", AKNN_i, "\tOPT:", KNN_i
    print ""
    print "Time Hilbert AKNN:", t_cum_aknn
    print "Time OPT:", t_cum_knn
    print "Average times distance from OPT:", average_distance_from_opt / len(HP)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
