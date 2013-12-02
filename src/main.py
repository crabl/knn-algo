#!/usr/bin/env python

# Perform Hilbert ordering on a set of vectors in n-dimensional space
# and find k-nearest neighbors based on this ordering

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
        self.point = np.array(point)
    
    def __lt__(self, other):
        if cmp_zorder(self.point, other.point) < 0:
            return True
        return False

    def __eq__(self, other):
        if cmp_zorder(self.point, other.point) == 0:
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
    distance_array = [distance(p,s) for s in S]

    # Find the indices of the k smallest items in S
    smallest_indices = k_smallest_indices(k, distance_array)

    # Find the points corresponding to those indices
    nearest_neighbors = [S[i] for i in smallest_indices]
    return nearest_neighbors

# The radius of a set is the largest distance between any two points in the set S
def set_radius(S):
    distance_matrix = np.zeros(len(S), len(S))
    distance_matrix.flat = [distance(p0, p1) for p0 in S for p1 in S]
    return np.max(distance_matrix)

def csearch(point, low, hi):
    if (hi-low) < V_CONSTANT:
        

def construct_morton(points, k):
    for i in range(len(points)):
        A_i = [points[i-k:i+k][index] for index in set_knn(points[i], points[i-k:i+k])]
        upper = 0
        lower = 0

        # if p_i^ceil(rad(A_i)) < p_i+k
        if MortonPoint(np.array(points[i]) ** np.ceil(set_radius(A_i))) < MortonPoint(np.array(points[i+k])):
            upper = i
        else:
            I = 0
            while MortonPoint(np.array(points[i]) ** np.ceil(set_radius(A_i))) < MortonPoint(np.array(points[i+2**I])):
                I += 1
            upper = np.min(i + 2**I, len(points))

        # if p_i^-ceil(rad(A_i)) > p_i-k
        if MortonPoint(np.array(points[i]) ** (-1 * np.ceil(set_radius(A_i)))) > MortonPoint(np.array(points[i-k])):
            lower = i
        else:
            I = 0
            while MortonPoint(np.array(points[i] ** (-1 * np.ceil(set_radius(A_i))))) > MortonPoint(np.array(points[i-2**I])):
                I += 1
            lower = np.max(i - 2**I, 0)
        
        if lower != upper:
            csearch(points[i], lower, upper)

        

def main():
    P = [(3,2),(1,7),(4,4),(6,1),(7,2),(2,5),(1,1)]
    hilbert_ordered = hilbert_index(P, 2, 8)

    print hilbert_ordered
    
    print "Hello, world!"


if __name__ == "__main__":
    main()
