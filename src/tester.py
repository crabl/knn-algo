from point import *
import unittest

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
    
if __name__ == "__main__":
    unittest.main()
