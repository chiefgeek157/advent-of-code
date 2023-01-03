import unittest

import aoc.grid as ag

class UtilUnitTests(unittest.TestCase):

    def test_get_adjacent_2d_unbounded_no_diag(self):
        p = [2, 5]
        a = ag.get_adjacent(p)
        self.assertEqual(a, [(1, 5), (2, 4), (2, 6), (3, 5)])

        p = (2, 5)
        a = ag.get_adjacent(p)
        self.assertEqual(a, [(1, 5), (2, 4), (2, 6), (3, 5)])

    def test_get_adjacent_2d_unbounded_with_diag(self):
        p = [2, 5]
        a = ag.get_adjacent(p, diag=True)
        self.assertEqual(a, [(1, 4), (1, 5), (1, 6), (2, 4), (2, 6), (3, 4), (3, 5), (3, 6)])

    def test_get_adjacent_2d_bounded_with_diag(self):
        p = [0, 0]
        bounds = [(0, 0), (5, 5)]
        a = ag.get_adjacent(p, diag=True, bounds=bounds)
        self.assertEqual(a, [(0, 1), (1, 0), (1, 1)])

    def test_get_adjacent_3d_unbounded_no_diag(self):
        p = [2, 5, 7]
        a = ag.get_adjacent(p)
        self.assertSetEqual(set(a), set([
            (1, 5, 7), (3, 5, 7),
            (2, 4, 7), (2, 6, 7),
            (2, 5, 6), (2, 5, 8)]))

        p = (2, 5, 7)
        a = ag.get_adjacent(p)
        self.assertSetEqual(set(a), set([
            (1, 5, 7), (3, 5, 7),
            (2, 4, 7), (2, 6, 7),
            (2, 5, 6), (2, 5, 8)]))

    def test_get_adjacent_3d_unbounded_with_diag(self):
        p = [2, 5, 7]
        a = ag.get_adjacent(p, diag=True)
        self.assertSetEqual(set(a), set([
            (1, 4, 6), (1, 4, 7), (1, 4, 8),
            (1, 5, 6), (1, 5, 7), (1, 5, 8),
            (1, 6, 6), (1, 6, 7), (1, 6, 8),
            (2, 4, 6), (2, 4, 7), (2, 4, 8),
            (2, 5, 6),            (2, 5, 8),
            (2, 6, 6), (2, 6, 7), (2, 6, 8),
            (3, 4, 6), (3, 4, 7), (3, 4, 8),
            (3, 5, 6), (3, 5, 7), (3, 5, 8),
            (3, 6, 6), (3, 6, 7), (3, 6, 8)]))

    def test_get_adjacent_3d_bounded_with_diag(self):
        p = [0, 0, 0]
        bounds = [(0, 0, 0), (5, 5, 5)]
        a = ag.get_adjacent(p, diag=True, bounds=bounds)
        self.assertSetEqual(set(a), set([
                                  (0, 0, 1),
                       (0, 1, 0), (0, 1, 1),
                       (1, 0, 0), (1, 0, 1),
                       (1, 1, 0), (1, 1, 1)]))

if __name__ == '__main__':
    unittest.main()
