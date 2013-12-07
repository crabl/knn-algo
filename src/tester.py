# Application Unit Tests
# Copyright (C) 2013 Christopher Rabl

import unittest

from point import *
from main import *

class PointTests(unittest.TestCase):
    a = Point((1,1,1))
    b = Point((1,1,2))

    def create_invalid(self):
        return Point((0,0,0), sftype='invalid')
    
    def test_create_invalid(self):
        self.assertRaises(ValueError, self.create_invalid)

    def test_not_equal(self):
        self.assertEqual(self.a != self.b, True)

class HilbertPointTests(unittest.TestCase):
    a = Point((1,0,1), sftype='hilbert')
    b = Point((0,1,1), sftype='hilbert')

    def test_index_comp(self):
        self.assertEqual(self.a > self.b, False)
        self.assertEqual(self.a == self.b, False)
        self.assertEqual(self.a < self.b, True)

    def test_correct_order(self):
        self.assertEqual(self.a.index_hilbert(), 2)
        self.assertEqual(self.b.index_hilbert(), 4)

class MortonPointTests(unittest.TestCase):
    a = Point((1,0,1), sftype='morton')
    b = Point((1,1,0), sftype='morton')
    
    def test_index_comp(self):
        self.assertEqual(self.a < self.b, True)
        self.assertEqual(self.a == self.b, False)
        self.assertEqual(self.a > self.b, False)

class AlgorithmCorrectnessTests(unittest.TestCase):
    dataset = [(x,y) for x in range(4) for y in range(4)]

    # Generate and sort Hilbert points
    HP = [Point(item, sftype='hilbert') for item in dataset]
    HP.sort(key=lambda h: h.index_hilbert()) # Have to use this or we run into issues with 'long'

    # Generate and sort Morton points
    MP = [Point(item, sftype='morton') for item in dataset]
    MP.sort(cmp=cmp_zorder)

    k = 4

    def test_hilbert_construct(self):
        # First case will only return us k-1 results because it is the bottom corner
        correct = [[(0, 1), (1, 0), (1, 1)], 
        [(0, 0), (1, 1), (1, 0), (2, 0)],
        [(0, 1), (1, 0), (2, 0), (0, 0)],
        [(2, 0), (0, 0), (1, 1), (0, 1)],
        [(1, 0), (2, 1), (3, 0), (1, 1)],
        [(2, 0), (3, 1), (2, 1), (1, 0)],
        [(3, 0), (2, 1), (3, 2), (2, 0)],
        [(2, 0), (3, 1), (2, 2), (1, 0)],
        [(3, 2), (2, 1), (2, 3), (3, 1)],
        [(2, 2), (3, 1), (3, 3), (2, 1)],
        [(3, 2), (2, 3), (2, 2), (3, 1)],
        [(2, 2), (3, 3), (1, 3), (3, 2)],
        [(1, 2), (2, 3), (0, 3), (2, 2)],
        [(0, 2), (1, 3), (0, 3), (2, 3)],
        [(1, 2), (0, 3), (1, 3), (2, 3)],
        [(0, 2), (1, 3), (1, 2), (2, 3)]]

        valid = []
        for arr in correct:
            temp_arr = []
            for p in arr:
                temp_arr.append(Point(p, sftype='hilbert'))
            valid.append(temp_arr)

        for i in range(len(self.HP)):
            self.assertEqual(all([p in valid[i] for p in construct(self.HP, i, self.k)]), True)
    
    def test_morton_construct(self):
        # First case will only return us k-1 results because it is the bottom corner
        correct = [[(0, 1), (1, 0), (1, 1)],
        [(1, 1), (0, 0), (0, 2), (1, 0)],
        [(1, 1), (0, 0), (0, 1), (0, 2)],
        [(0, 1), (1, 0), (1, 2), (0, 2)],
        [(0, 1), (1, 2), (0, 3), (1, 1)],
        [(0, 2), (1, 3), (1, 2), (0, 1)],
        [(1, 1), (0, 2), (1, 3), (0, 3)],
        [(0, 3), (1, 2), (0, 2), (1, 1)],
        [(2, 1), (3, 0), (3, 1), (1, 2)],
        [(2, 0), (3, 1), (2, 2), (3, 0)],
        [(2, 0), (3, 1), (2, 1), (2, 2)],
        [(3, 2), (2, 1), (3, 0), (2, 2)],
        [(3, 2), (2, 1), (2, 3), (3, 1)],
        [(2, 2), (3, 3), (3, 2), (2, 1)],
        [(2, 2), (3, 1), (3, 3), (2, 3)],
        [(3, 2), (2, 3), (2, 2), (3, 1)]]
        valid = []
        for arr in correct:
            temp_arr = []
            for p in arr:
                temp_arr.append(Point(p, sftype='morton'))
            valid.append(temp_arr)

        for i in range(len(self.MP)):
            self.assertEqual(all([p in valid[i] for p in construct(self.MP, i, self.k)]), True)



if __name__ == "__main__":
    unittest.main()
