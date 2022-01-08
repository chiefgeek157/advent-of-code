from space import Prism, Space
import unittest
from unittest import TestCase

class PrismTests(TestCase):
    def test_combine(self):
        p1 = Prism((0,0,0),(1,1,1),True)
        p2 = Prism((0,0,0),(1,1,1),True)
        new = p1.combine(p2)
        print(f'new={new}')
        self.assertEqual(len(new), 1)
        self.assertEqual(new[0].pmin, (0,0,0))
        self.assertEqual(new[0].pmax, (1,1,1))
        self.assertTrue(new[0].state)

        p3 = Prism((0,0,0),(2,2,2),True)
        new = p1.combine(p3)
        print(f'new={new}')
        # self.assertEqual(len(new), 1)
        # self.assertEqual(new[0].pmin, (0,0,0))
        # self.assertEqual(new[0].pmax, (1,1,1))
        # self.assertTrue(new[0].state)

        p4 = Prism((1,1,1),(2,2,2),True)
        new = p1.combine(p4)
        print(f'new={new}')

        p5 = Prism((-1,-1,-1),(0,0,0),True)
        new = p1.combine(p5)
        print(f'new={new}')

        p6 = Prism((-2,-2,-2),(-1,-1,-1),True)
        new = p1.combine(p6)
        print(f'new={new}')

        p7 = Prism((-2,-2,-2),(-1,-1,-1),True)
        new = p1.combine(p6)
        print(f'new={new}')

if __name__ == '__main__':
    unittest.main()