import numpy as np
import unittest
from utils import Utils

class UtilsTests(unittest.TestCase):

    def test_tuplearray(self):
        a = Utils.tuplearray()
        self.assertEqual(len(a), 0)
        self.assertIsInstance(a, np.ndarray)

        b = Utils.tuplearray(a)
        self.assertEqual(len(b), 0)
        self.assertIsInstance(b, np.ndarray)

        a = Utils.tuplearray(None)
        self.assertEqual(len(a), 0)
        self.assertIsInstance(a, np.ndarray)

        a = Utils.tuplearray([])
        self.assertEqual(len(a), 0)
        self.assertIsInstance(a, np.ndarray)

        a = Utils.tuplearray([1, 2, 3])
        self.assertEqual(len(a), 1)
        self.assertIsInstance(a, np.ndarray)
        self.assertEqual(a[0], (1, 2, 3))

        a = Utils.tuplearray([[1, 2, 3]])
        self.assertEqual(len(a), 1)
        self.assertIsInstance(a, np.ndarray)
        self.assertEqual(a[0], (1, 2, 3))

        a = Utils.tuplearray((1, 2, 3))
        self.assertEqual(len(a), 1)
        self.assertIsInstance(a, np.ndarray)
        self.assertEqual(a[0], (1, 2, 3))

        a = Utils.tuplearray([(1, 2, 3)])
        self.assertEqual(len(a), 1)
        self.assertIsInstance(a, np.ndarray)
        self.assertEqual(a[0], (1, 2, 3))

        b = Utils.tuplearray(a)
        self.assertEqual(len(b), 1)
        self.assertIsInstance(b, np.ndarray)
        self.assertEqual(b[0], (1, 2, 3))

if __name__ == '__main__':
    unittest.main()