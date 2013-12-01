#!/usr/bin/env python

# Perform Hilbert ordering on a set of vectors in n-dimensional space
# and find k-nearest neighbors based on this ordering

# CPSC 4110 - Approximation Algorithms
# Camara Lerner & Chris Rabl

import numpy
import sys
import math
import bitstring
from hilbertIndex import *

class MortonPoint:
    def __init__(self, point):
        self.point = point

    # Override len to give us the number of dimensions in the point
    def __len__(self):
        return len(self.point)

    # Override array subscript operator
    def __getitem__(self, key):
        return self.point[key]

    # Test if two points have the same Morton order
    def __eq__(self, other):
        return self.point == other.point
        
    # Test for less than in terms of Morton ordering
    def __lt__(self, other):
        x = 0
        dim = 0
        for j in range(0, len(self)):
            y = self.xor_msb(self[j], other[j])
            if x < y:
                x = y
                dim = j
    
        return self[dim] < other[dim]

    # Return the Most Significant Differing Bit of two integers
    def msdb(self, a, b):
        bit_num = 0
        num = a ^ b # Bitwise XOR on a and b

        # Shift until we reach the most significant bit
        while num != 0:
            bit_num += 1
            num = num >> 1

        return bit_num

    # Return XOR of most significant bit between two floating point numbers
    def xor_msb(self, a, b):
        a = float(a)
        b = float(b)
        mantissa_a, exponent_a = math.frexp(a)
        mantissa_b, exponent_b = math.frexp(b)
        
        if exponent_a == exponent_b:
            # Need to get the integer mantissa, since math.frexp
            # gives it to us as a float
            int_mantissa_a = int(str(mantissa_a)[2:])
            int_mantissa_b = int(str(mantissa_b)[2:])
            most_sig_dif_bit = self.msdb(int_mantissa_a, int_mantissa_b)
            return exponent_a - most_sig_dif_bit
        
        if exponent_b < exponent_a:
            return exponent_a

        return exponent_b

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

def main():
    P = [(3,2),(1,7),(4,4),(6,1),(7,2),(2,5),(1,1)]
    H = [hilbertIndex(2,8,point) for point in P]
    hilbert_ordered = [p for (h,p) in sorted(zip(H, P))] # Sort the points in Hilbert order

    print hilbert_ordered
    
    print "Hello, world!"


if __name__ == "__main__":
    main()
