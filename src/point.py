import math

import hilbert
import morton

class Point(object):
    def __init__(self, coordinates, precision=32, sftype="hilbert"):
        self.coordinates = coordinates # Tuple of point coordinates
        self.dimension = len(coordinates)
        self.precision = precision
        self.sftype = sftype.lower()
        if not self.sftype in ["hilbert", "morton"]:
            raise ValueError("Point type must be either Hilbert or Morton")
        
    def index_hilbert(self):
        return hilbert.hilbert_index(self.dimension, self.precision, self.coordinates)
    
    def __lt__(self, other):
        if self.sftype == "hilbert":
            return self.index_hilbert() < other.index_hilbert()
        return morton.cmp_zorder(self.coordinates, other.coordinates) < 0

    def __eq__(self, other):
        if self.sftype == "hilbert":
            return self.index_hilbert() == other.index_hilbert()
        return morton.cmp_zorder(self.coordinates, other.coordinates) == 0

    def __pow__(self, power):
        result = Point(tuple([x ** power for x in self.coordinates]), precision=self.precision, sftype=self.sftype)
        return result

    def __repr__(self):
        return str(self.coordinates)
