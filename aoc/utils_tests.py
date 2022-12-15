import unittest

from aoc.utils import union1d

class UtilUnitTests(unittest.TestCase):

    def test_union1d(self):
        # Seg non-overlap to right
        self.assertEqual(union1d([(0,0)], (1,1)), [(0,0), (1,1)])

        # Seg non-overlap to left
        self.assertEqual(union1d([(0,5)], (-2,-1)), [(-2,-1), (0,5)])

        # Seg subsumes all
        self.assertEqual(union1d([(0,1)], (-2,2)), [(-2,2)])
        self.assertEqual(union1d([(0,1), (2,5)], (-2,10)), [(-2,10)])

        # Seg inside one segment
        self.assertEqual(union1d([(-5,5)], (-2,2)), [(-5,5)])
        self.assertEqual(union1d([(1,2), (2,10), (11,15)], (3,5)),
            [(1,2), (2,10), (11,15)])

        # Seg overlaps left with a segment
        self.assertEqual(union1d([(10,20), (30,40), (50,60)], (25,35)),
            [(10,20), (25,40), (50,60)])

        # Seg overlaps right with a segment
        self.assertEqual(union1d([(10,20), (30,40), (50,60)], (35,45)),
            [(10,20), (30,45), (50,60)])

        # Seg overlaps right with a segment
        self.assertEqual(union1d([(10,20), (30,40), (50,60)], (35,45)),
            [(10,20), (30,45), (50,60)])

        # Seg subsumes a middle extent
        self.assertEqual(union1d([(10,20), (30,40), (50,60)], (25,45)),
            [(10,20), (25,45), (50,60)])

if __name__ == '__main__':
    unittest.main()
