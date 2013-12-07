import math

import hilbert
import morton

class Point(object):
    def __init__(self, coordinates, precision=32, sftype='hilbert'):
        self.coordinates = tuple([int(item) for item in coordinates]) # Tuple of point coordinates
        self.dimension = len(coordinates)
        self.precision = precision
        self.sftype = sftype.lower()
        if not self.sftype in ['hilbert', 'morton']:
            raise ValueError('Point type must be either Hilbert or Morton')
        
    def check_valid(self):
        if any([x < 0 for x in self.coordinates]):
            #raise ValueError('Cannot get Hilbert index of negative point')
            return False
        return True

    def index_hilbert(self):
        if not self.check_valid():
            return -1
        return hilbert.hilbert_index(self.dimension, self.precision, self.coordinates)

    def sum(self):
        return sum(self.coordinates)

    def shift(self, amount):
        result = Point(tuple([x + amount for x in self.coordinates]), precision=self.precision, sftype=self.sftype)
        return result
    
    def __len__(self):
        return self.dimension

    def __lt__(self, other):
        self.check_valid()
        if self.sftype == 'hilbert':
            return self.index_hilbert() < other.index_hilbert()
        return morton.cmp_zorder(self.coordinates, other.coordinates) < 0

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __pow__(self, power):
        result = Point(tuple([x ** power for x in self.coordinates]), precision=self.precision, sftype=self.sftype)
        return result

    def __add__(self, other):
        return Point(tuple([self[i] - other[i] for i in range(self.dimension)]), precision=self.precision, sftype=self.sftype)
    
    def __sub__(self, other):
        return Point(tuple([self[i] - other[i] for i in range(self.dimension)]), precision=self.precision, sftype=self.sftype)

    def __getitem__(self, i):
            return self.coordinates[i]

    def __repr__(self):
        return str(self.coordinates)

def cmp_hilbert(a, b):
    return a.index_hilbert() - b.index_hilbert()

def cmp_zorder(a, b):
    return morton.cmp_zorder(a.coordinates, b.coordinates)
