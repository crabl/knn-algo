#!/usr/bin/env python
# Snap n-dimensional points to an n-dimensional integer lattice
# CPSC 4110 - Approximation Algorithms
# Camara Lerner & Chris Rabl

import numpy as np

# vectors: set of vectors in R^n that we want to convert to V^n
# vector: vector in R^n
# basis_vectors: n linearly-independent vectors in R^n
def from_vectors(vectors, basis_vectors):
    A_inverse = np.linalg.inv(np.matrix(basis_vectors).transpose())
    new_vectors = []
    for vector in vectors:
        v = A_inverse * np.matrix(vector).transpose()
        v = np.round(v)
        new_vectors.append(v)

    return np.array(new_vectors)
