import numpy as np
import scanner as sc
import transformer as tr
import unittest
from utils import Utils

class TransformerTests(unittest.TestCase):

    def test_transformer_rots(self):
        t = tr.Transformer()
        for i in range(t.num_rots()):
            for j in range(t.num_rots()):
                if i != j:
                    self.assertFalse(np.allclose(t.rot(i), t.rot(j)))

    def test_transformer_affine(self):
        t = tr.Transformer()
        a = t.affine(0)
        self.assertTrue(np.all(a == [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]))

        a = t.affine(1, (1, 2, 3))
        self.assertTrue(np.all(a == [[0,-1,0,1],[1,0,0,2],[0,0,1,3],[0,0,0,1]]))

    def test_transformer_append_affine(self):
        t = tr.Transformer()
        a1 = t.affine(0)
        a2 = t.append_affine(a1, 1, (1, 2, 3))
        self.assertTrue(np.all(a2 == [[0,-1,0,1],[1,0,0,2],[0,0,1,3],[0,0,0,1]]))

        a3 = t.affine(2, (1,2,3))
        a4 = t.append_affine(a3, 2, (1,2,3))
        self.assertTrue(np.all(a4 == [[1,0,0,0],[0,1,0,0],[0,0,1,6],[0,0,0,1]]))

    def test_transformer_transform(self):
        t = tr.Transformer()
        self.assertEqual(t.transform((1, 2, 3), t.affine( 0)), ( 1,  2,  3))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 1)), (-2,  1,  3))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 2)), (-1, -2,  3))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 3)), ( 2, -1,  3))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 4)), ( 1, -3,  2))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 5)), ( 3,  1,  2))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 6)), (-1,  3,  2))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 7)), (-3, -1,  2))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 8)), ( 1, -2, -3))
        self.assertEqual(t.transform((1, 2, 3), t.affine( 9)), ( 2,  1, -3))
        self.assertEqual(t.transform((1, 2, 3), t.affine(10)), (-1,  2, -3))
        self.assertEqual(t.transform((1, 2, 3), t.affine(11)), (-2, -1, -3))
        self.assertEqual(t.transform((1, 2, 3), t.affine(12)), ( 1,  3, -2))
        self.assertEqual(t.transform((1, 2, 3), t.affine(13)), (-3,  1, -2))
        self.assertEqual(t.transform((1, 2, 3), t.affine(14)), (-1, -3, -2))
        self.assertEqual(t.transform((1, 2, 3), t.affine(15)), ( 3, -1, -2))
        self.assertEqual(t.transform((1, 2, 3), t.affine(16)), ( 3,  2, -1))
        self.assertEqual(t.transform((1, 2, 3), t.affine(17)), (-2,  3, -1))
        self.assertEqual(t.transform((1, 2, 3), t.affine(18)), (-3, -2, -1))
        self.assertEqual(t.transform((1, 2, 3), t.affine(19)), ( 2, -3, -1))
        self.assertEqual(t.transform((1, 2, 3), t.affine(20)), (-3,  2,  1))
        self.assertEqual(t.transform((1, 2, 3), t.affine(21)), (-2, -3,  1))
        self.assertEqual(t.transform((1, 2, 3), t.affine(22)), ( 3, -2,  1))
        self.assertEqual(t.transform((1, 2, 3), t.affine(23)), ( 2,  3,  1))

    def test_transformer_transform_points(self):
        t = tr.Transformer()
        points = Utils.tuplearray([(1, 2, 3), (4, 5, 6)])
        pointst = t.transform_points(points, t.affine(1))
        self.assertEqual(pointst[0], (-2, 1, 3))
        self.assertEqual(pointst[1], (-5, 4, 6))

        pointst = t.transform_points(points, t.affine(1, (10, 20, 30)))
        self.assertEqual(pointst[0], (8, 21, 33))
        self.assertEqual(pointst[1], (5, 24, 36))

    def test_scannerarray_best_alignment(self):
        sa = sc.ScannerArray()
        sa.read_file('2021/day19/test1.txt')
        t = tr.Transformer()
        match, count, rot, origin = t.best_alignment(sa._scanners[1].beacons, sa._scanners[0].beacons, sc.ScannerArray.DEFAULT_THRESHHOLD)
        self.assertTrue(match)
        self.assertEqual(count, 12)
        self.assertEqual(rot, 10)
        self.assertEqual(origin, (68, -1246, -43))

if __name__ == '__main__':
    unittest.main()