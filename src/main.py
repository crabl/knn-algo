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

from hilbert_index import *
from morton_index import *

V_CONSTANT = 4 # Platform-dependent constant

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

class HilbertPoint:
    def __init__(self, point, precision):
        self.point = np.array(point, dtype=np.uint32)
        self.dimension = len(point)
        self.precision = precision
    
    def __lt__(self, other):
        if cmp_hilbert(self.point, other.point, self.dimension, self.precision) < 0:
            return True
        return False

    def __eq__(self, other):
        if cmp_hilbert(self.point, other.point, self.dimension, self.precision) == 0:
            return True
        return False

# Euclidean distance between two points
def distance(a, b):
    return np.sqrt(((np.array(a)-np.array(b))**2).sum())

# Find the indices of the k smallest items in a set S, assuming that S contains a zero element
def k_smallest_indices(k, S):
    # We have to look at [1:k+1] because we assume that S contains the point
    # that we are looking for
    return [idx for (s, idx) in sorted(zip(S,range(len(S))))][1:k+1]

# Find the k nearest neighbors to a point in a given set S
def set_knn(point, k, S):
    distance_array = [distance(point,s) for s in S]

    # Find the indices of the k smallest items in S
    smallest_indices = k_smallest_indices(k, distance_array)

    # Find the points corresponding to those indices
    nearest_neighbors = [S[i] for i in smallest_indices]
    return nearest_neighbors

def box_dist(point, box_center, box_radius):
    return distance(point, box_center) - box_radius # This is roughly incorrect... Although it's a circle. So yeah.

# The radius of a set is the largest distance between any two points in the set S
def set_radius(S):
    distance_matrix = np.zeros((len(S), len(S)))
    distance_matrix.flat = [distance(p0, p1) for p0 in S for p1 in S]
    return np.max(distance_matrix)

def csearch(point, A_i, i, k, low, hi):
    if (hi-low) < V_CONSTANT:
        return set_knn(point[i], k, list(set(A_i + point[low:hi])))
    mid = int((hi + low) / 2)
    A_i = set_knn(point[i], k, list(set(A_i + point[mid])))
    if box_dist(point[i], point[low], dist(point[low], point[hi])) > set_radius(A_i):
        return A_i
    if MortonPoint(point[i]) < MortonPoint(point[m]):
        A_i = csearch(point, A_i, i, k, low, mid - 1)
        if MortonPoint(point[m]) < MortonPoint(point[i] ** np.ceil(set_radius(A_i))):
            A_i = csearch(point, A_i, i, k, mid + 1, hi)
    else:
        A_i = csearch(point, A_i, i, k, mid + 1, hi)
        if MortonPoint(point[i] ** (-1 * np.ceil(set_radius(A_i)))):
            A_i = csearch(point, A_i, i, low, mid - 1)
    return A_i

def construct_morton(points, i, k):
    A_i = set_knn(points[i], k, points[max(0,i-k):min(len(points),i+k)])
    if len(A_i) < k:
        A_i.append(points[i])
    upper = 0
    lower = 0
        
    #print "Iteration:", i
    #print "point_i:", points[i]
    #print "A_i:", A_i
    # if p_i^ceil(rad(A_i)) < p_i+k
    if MortonPoint(np.array(points[i]) ** np.ceil(set_radius(A_i))) < MortonPoint(np.array(points[min(i+k, len(points)-1)])):
        upper = i
    else:
        I = 0
        while MortonPoint(np.array(points[i]) ** np.ceil(set_radius(A_i))) < MortonPoint(np.array(points[min(len(points)-1, i+2**I)])):
            I += 1
        upper = min(i + 2**I, len(points)-1)

    # if p_i^-ceil(rad(A_i)) > p_i-k
    if MortonPoint(np.array(points[i]) ** (-1 * np.ceil(set_radius(A_i)))) > MortonPoint(np.array(points[max(0, i-k)])):
        lower = i
    else:
        I = 0
        while MortonPoint(np.array(points[i] ** (-1 * np.ceil(set_radius(A_i))))) > MortonPoint(np.array(points[max(0, i-2**I)])):
            I += 1
        lower = np.max(i - 2**I, 0)

    if lower != upper:
        csearch(points, A_i, i, k, lower, upper)

        

def main():
    P = [(x,y) for x in range(16) for y in range(16)]
    for i in range(len(P)):
        print P[i], "NN:", construct_morton(P, i, 4)
    


if __name__ == "__main__":
    main()
