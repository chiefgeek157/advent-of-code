import math
import numpy as np
from numpy.core.numeric import allclose
import scanner as sc
import unittest

class ScannerTests(unittest.TestCase):

    def test_scanner_create(self):
        s = sc.Scanner()
        self.assertEqual(s.id, None)
        self.assertEqual(s.beacons, None)

        s = sc.Scanner(10)
        self.assertEqual(s.id, 10)
        self.assertEqual(s.beacons, None)

        s = sc.Scanner(10, [1, 2, 3])
        self.assertEqual(s.id, 10)
        self.assertTrue(np.allclose(s.beacons, np.array([1, 2, 3])))

        s = sc.Scanner(10, [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(s.id, 10)
        self.assertEqual(len(s.beacons), 2)
        self.assertTrue(np.allclose(s.beacons, np.array([[1, 2, 3], [4, 5, 6]])))

    def test_scanner_read(self):
        s1 = None
        with open('2021/day19/test-s0.txt', 'r') as f:
            s1 = sc.Scanner.read(f)
        self.assertEqual(s1.id, 0)
        self.assertEqual(len(s1.beacons), 25)
        self.assertTrue((s1.beacons[0] == np.array([404, -588, -901])).all())
        self.assertTrue((s1.beacons[24] == np.array([459, -707, 401])).all())

    def test_combiner_rots(self):
        c = sc.Combiner()
        for i in range(len(c.rots)):
            for j in range(len(c.rots)):
                if i != j:
                    self.assertFalse(np.allclose(c.rots[i], c.rots[j]))

    def test_combiner_transform(self):
        c = sc.Combiner()
        s = sc.Scanner(0, [[1, 2, 3]])
        self.assertTrue(np.allclose(c.transform(s,  0).beacons[0], [ 1,  2,  3]))
        self.assertTrue(np.allclose(c.transform(s,  1).beacons[0], [-2,  1,  3]))
        self.assertTrue(np.allclose(c.transform(s,  2).beacons[0], [-1, -2,  3]))
        self.assertTrue(np.allclose(c.transform(s,  3).beacons[0], [ 2, -1,  3]))
        self.assertTrue(np.allclose(c.transform(s,  4).beacons[0], [ 1, -3,  2]))
        self.assertTrue(np.allclose(c.transform(s,  5).beacons[0], [ 3,  1,  2]))
        self.assertTrue(np.allclose(c.transform(s,  6).beacons[0], [-1,  3,  2]))
        self.assertTrue(np.allclose(c.transform(s,  7).beacons[0], [-3, -1,  2]))
        self.assertTrue(np.allclose(c.transform(s,  8).beacons[0], [ 1, -2, -3]))
        self.assertTrue(np.allclose(c.transform(s,  9).beacons[0], [ 2,  1, -3]))
        self.assertTrue(np.allclose(c.transform(s, 10).beacons[0], [-1,  2, -3]))
        self.assertTrue(np.allclose(c.transform(s, 11).beacons[0], [-2, -1, -3]))
        self.assertTrue(np.allclose(c.transform(s, 12).beacons[0], [ 1,  3, -2]))
        self.assertTrue(np.allclose(c.transform(s, 13).beacons[0], [-3,  1, -2]))
        self.assertTrue(np.allclose(c.transform(s, 14).beacons[0], [-1, -3, -2]))
        self.assertTrue(np.allclose(c.transform(s, 15).beacons[0], [ 3, -1, -2]))
        self.assertTrue(np.allclose(c.transform(s, 16).beacons[0], [ 3,  2, -1]))
        self.assertTrue(np.allclose(c.transform(s, 17).beacons[0], [-2,  3, -1]))
        self.assertTrue(np.allclose(c.transform(s, 18).beacons[0], [-3, -2, -1]))
        self.assertTrue(np.allclose(c.transform(s, 19).beacons[0], [ 2, -3, -1]))
        self.assertTrue(np.allclose(c.transform(s, 20).beacons[0], [-3,  2,  1]))
        self.assertTrue(np.allclose(c.transform(s, 21).beacons[0], [-2, -3,  1]))
        self.assertTrue(np.allclose(c.transform(s, 22).beacons[0], [ 3, -2,  1]))
        self.assertTrue(np.allclose(c.transform(s, 23).beacons[0], [ 2,  3,  1]))

    def test_combiner_xform_scanner(self):
        c = sc.Combiner()
        s = sc.Scanner(0, [[1, 2, 3], [4, 5, 6]])
        # print(f's {s}')
        s1 = c.transform(s, 1)
        # print(f's1 {s1}')
        self.assertTrue(np.allclose(s1.beacons[0], [-2, 1, 3]))
        self.assertTrue(np.allclose(s1.beacons[1], [-5, 4, 6]))

    def test_rotation(self):
        c = sc.Combiner()
        s1 = sc.Scanner(0, [[-1,-1, 1],[-2,-2, 2],[-3,-3, 3],[-2,-3, 1],[ 5, 6,-4],[ 8, 0, 7]])
        others = []
        others.append(sc.Scanner(0, \
            [[ 1,-1, 1],[ 2,-2, 2],[ 3,-3, 3],[ 2,-1, 3],[-5, 4,-6],[-8,-7, 0]]))
        others.append(sc.Scanner(0, \
            [[-1,-1,-1],[-2,-2,-2],[-3,-3,-3],[-1,-3,-2],[ 4, 6, 5],[-7, 0, 8]]))
        others.append(sc.Scanner(0, \
            [[ 1, 1,-1],[ 2, 2,-2],[ 3, 3,-3],[ 1, 3,-2],[-4,-6, 5],[ 7, 0, 8]]))
        others.append(sc.Scanner(0, \
            [[ 1, 1, 1],[ 2, 2, 2],[ 3, 3, 3],[ 3, 1, 2],[-6,-4,-5],[ 0, 7,-8]]))
        # print(f's1 \n{s1.beacons}')
        rots = [14, 16, 22, 7]
        for o in range(len(others)):
            for i in range(len(c.rots)):
                # print(f'rot[{i}]')
                s = c.transform(others[o], i)
                # print(f's\n{s.beacons}')
                if np.allclose(s1.beacons, s.beacons):
                    self.assertEqual(i, rots[o])

    def test_rot_trans(self):
        c = sc.Combiner()
        s = []
        with open('2021/day19/test-s0.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s1.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        match = False
        rot = None
        for i in range(len(c.rots)):
            # print(f'Applying rot {i}')
            st = c.transform(s[1], i, [68, -1246, -43])
            match_count = 0
            for j in range(len(s[0].beacons)):
                p1 = s[0].beacons[j]
                # if p1[0] == -618: print(f'p1 {p1}')
                for k in range(len(st.beacons)):
                    p2 = st.beacons[k]
                    # if p2[0] == -618: print(f'p2 {s.beacons[k]}')
                    if p1[0] == p2[0] and p1[1] == p2[1] and p1[2] == p2[2]:
                        match_count += 1
                        # print(f'Match point at rot {i} {s1.beacons[j]}')
                        if match_count >= 12:
                            match = True
                            rot = i
                            break
                if match: break
            if match: break
        self.assertTrue(match)
        self.assertEqual(rot, 10)

    def test_combiner_overlap(self):
        c = sc.Combiner()
        s = []
        with open('2021/day19/test-s0.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s1.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        match, n, origin = c.overlap(s[0], s[1])
        self.assertTrue(match)
        self.assertEqual(n, 10)
        self.assertEqual(origin, [68, -1246, -43])

        with open('2021/day19/test-s4.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        match, n, origin = c.overlap(s[1], s[2])
        self.assertTrue(match)
        self.assertEqual(n, 19)
        self.assertEqual(origin, [88, 113, -1104])

    def test_combiner_combine(self):
        c = sc.Combiner()
        s = []
        with open('2021/day19/test-s0.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s1.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        c.combine(s)
        self.assertEqual(len(s[0].beacons), 38)

    def test_combiner_double(self):
        c = sc.Combiner()
        s = []
        with open('2021/day19/test-s0.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s1.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s4.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        c.combine(s)
        self.assertEqual(len(s[0].beacons), 52)

    def test_combiner_all(self):
        c = sc.Combiner()
        s = []
        with open('2021/day19/test-s0.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s1.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s2.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s3.txt', 'r') as f:
            s.append(sc.Scanner.read(f))
        with open('2021/day19/test-s4.txt', 'r') as f:
            s.append(sc.Scanner.read(f))

        c.combine(s)

        results = []
        with open('2021/day19/test-results.txt', 'r') as f:
            line = f.readline()
            while line:
                values = line.strip().split(',')
                results.append([int(values[0]), int(values[1]), int(values[2])])
                line = f.readline()
        results = np.array(results)

        self.assertEqual(len(s[0].beacons), len(results))
        self.assertTrue(np.all(np.array([p in results for p in s[0].beacons])))

if __name__ == '__main__':
    unittest.main()