from point import *
import unittest

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
    
if __name__ == "__main__":
    unittest.main()
