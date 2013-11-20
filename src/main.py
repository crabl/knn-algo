#!/usr/bin/env python

# Perform Hilbert ordering on a set of vectors in n-dimensional space
# and find k-nearest neighbors based on this ordering

# CPSC 4110 - Approximation Algorithms
# Camara Lerner & Chris Rabl

import numpy
import sys

import lattice
import basis

def main():
    file_name = str(sys.argv[1])
    k = int(sys.argv[2])

    data_set = np.genfromtxt(file_name, delimiter="\t") # Get from CSV
    basis_vectors = basis.get_basis(dataset)
    lattice_points = lattice.from_vectors(data_set, basis_vectors)


if __name__ == "__main__":
    main()
