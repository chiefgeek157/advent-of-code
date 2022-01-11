from space import Prism, Space
import unittest
from unittest import TestCase

class PrismTests(TestCase):

    def test_interesection(self):
        p1 = Prism((0,0,0),(0,0,0),True)
        p2 = Prism((0,0,0),(0,0,0),True)
        inter = p1.intersection(p2)
        self.assertIsNotNone(inter)
        i1, i2 = inter
        self.assertEqual(i1, (0,0,0))
        self.assertEqual(i2, (0,0,0))

        p3 = Prism((1,0,0),(1,0,0),True)
        inter = p1.intersection(p3)
        self.assertIsNone(inter)

    def test_combine(self):
        p1 = Prism((0,0,0),(1,1,1),True)
        p2 = Prism((0,0,0),(1,1,1),True)
        new, more = p1.combine(p2)
        print(f'more={more} new={new}')
        self.assertEqual(len(new), 1)
        self.assertEqual(new[0].pmin, (0,0,0))
        self.assertEqual(new[0].pmax, (1,1,1))
        self.assertTrue(new[0].state)

        p3 = Prism((0,0,0),(2,2,2),True)
        new, more = p1.combine(p3)
        print(f'new={new}\more={more}')
        # self.assertEqual(len(new), 1)
        # self.assertEqual(new[0].pmin, (0,0,0))
        # self.assertEqual(new[0].pmax, (1,1,1))
        # self.assertTrue(new[0].state)

        p4 = Prism((1,1,1),(2,2,2),True)
        new, more = p1.combine(p4)
        print(f'new={new}\more={more}')

        p5 = Prism((-1,-1,-1),(0,0,0),True)
        new, more = p1.combine(p5)
        print(f'new={new}\more={more}')

        p6 = Prism((-2,-2,-2),(-1,-1,-1),True)
        new, more = p1.combine(p6)
        print(f'new={new}\more={more}')

        p7 = Prism((-2,-2,-2),(-1,-1,-1),True)
        new, more = p1.combine(p6)
        print(f'new={new}\more={more}')

    def test_space_combine(self):
        s = Space()
        s.add((0,0,0), (2,2,2), True)
        print(f'space={s}')

        s.add((1,1,1), (3,3,3), True)
        print(f'space={s}')

        s.add((7,8,9), (10,11,12), True)
        print(f'space={s}')

if __name__ == '__main__':
    unittest.main()