import numpy as np
import scanner as sc
import transformer as tr
import unittest

class ScannerTests(unittest.TestCase):

    def test_scanner_create(self):
        s = sc.Scanner()
        self.assertEqual(s.id, None)
        self.assertEqual(s.beacons, None)

        s = sc.Scanner(10)
        self.assertEqual(s.id, 10)
        self.assertEqual(s.beacons, None)

        s = sc.Scanner(10, (1, 2, 3))
        self.assertEqual(s.id, 10)
        self.assertTrue(s.beacons.dtype == 'object')

        s = sc.Scanner(10, [(1, 2, 3), (4, 5, 6)])
        self.assertEqual(s.id, 10)
        self.assertEqual(len(s.beacons), 2)
        self.assertTrue(s.beacons.dtype == 'object')

    def test_scannerarray_read_from(self):
        with open('2021/day19/test1.txt', 'r') as f:
            sa = sc.ScannerArray()
            s1 = sa.read_from(f)
            self.assertEqual(s1.id, 0)
            self.assertEqual(len(s1.beacons), 25)
            self.assertTrue(s1.beacons[0] == (404,-588,-901))
            self.assertTrue(s1.beacons[24] == (459,-707,401))

            s2 = sa.read_from(f)
            self.assertEqual(s2.id, 1)
            self.assertEqual(len(s2.beacons), 25)
            self.assertTrue(s2.beacons[0] == (686,422,578))
            self.assertTrue(s2.beacons[24] == (553,889,-390))

    def test_scannerarray_read(self):
        sa = sc.ScannerArray()
        sa.read_file('2021/day19/test1.txt')
        self.assertEqual(len(sa._scanners), 5)
        self.assertEqual(sa._scanners[0].id, 0)
        self.assertEqual(len(sa._scanners[0].beacons), 25)
        self.assertTrue(sa._scanners[0].beacons[0] == (404, -588, -901))
        self.assertTrue(sa._scanners[0].beacons[24] == (459, -707, 401))
        self.assertEqual(len(sa._scanners[4].beacons), 26)
        self.assertTrue(sa._scanners[4].beacons[0] == (727,592,562))
        self.assertTrue(sa._scanners[4].beacons[25] == (30,-46,-14))

    def test_scannerarray_combine(self):
        sa = sc.ScannerArray()
        sa.read_file('2021/day19/test1.txt')
        beacons = sa.combine()
        self.assertEqual(len(beacons), 79)

    # def test_scanner_set_parents(self):
    #     s = []
    #     with open('2021/day19/test-s0.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s1.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))

    #     sc.Scanner.set_parents(s)
    #     self.assertEqual(s[1].parent.id, s[0].id)

    # def test_scanner_find_matching_beacons(self):
    #     s = []
    #     with open('2021/day19/test-s0.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s1.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))

    #     s[1].find_matching_beacons(s[0])

    # def test_scanner_combine(self):
    #     s = []
    #     with open('2021/day19/test-s0.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s1.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s2.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s3.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s4.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))

    #     beacons = sc.Scanner.combine(s)
    #     # print(f'beacons {sorted(beacons)}')
    #     # print(f'count {len(beacons)}')
    #     self.assertEqual(len(beacons), 79)

    # def test_combiner_xform_scanner(self):
    #     c = sc.Combiner()
    #     s = sc.Scanner(0, [[1, 2, 3], [4, 5, 6]])
    #     # print(f's {s}')
    #     s1 = c.transform(s, 1)
    #     # print(f's1 {s1}')
    #     self.assertTrue(np.allclose(s1.beacons[0], [-2, 1, 3]))
    #     self.assertTrue(np.allclose(s1.beacons[1], [-5, 4, 6]))

    # def test_rotation(self):
    #     c = sc.Combiner()
    #     s1 = sc.Scanner(0, [[-1,-1, 1],[-2,-2, 2],[-3,-3, 3],[-2,-3, 1],[ 5, 6,-4],[ 8, 0, 7]])
    #     others = []
    #     others.append(sc.Scanner(0, \
    #         [[ 1,-1, 1],[ 2,-2, 2],[ 3,-3, 3],[ 2,-1, 3],[-5, 4,-6],[-8,-7, 0]]))
    #     others.append(sc.Scanner(0, \
    #         [[-1,-1,-1],[-2,-2,-2],[-3,-3,-3],[-1,-3,-2],[ 4, 6, 5],[-7, 0, 8]]))
    #     others.append(sc.Scanner(0, \
    #         [[ 1, 1,-1],[ 2, 2,-2],[ 3, 3,-3],[ 1, 3,-2],[-4,-6, 5],[ 7, 0, 8]]))
    #     others.append(sc.Scanner(0, \
    #         [[ 1, 1, 1],[ 2, 2, 2],[ 3, 3, 3],[ 3, 1, 2],[-6,-4,-5],[ 0, 7,-8]]))
    #     # print(f's1 \n{s1.beacons}')
    #     rots = [14, 16, 22, 7]
    #     for o in range(len(others)):
    #         for i in range(len(c.rots)):
    #             # print(f'rot[{i}]')
    #             s = c.transform(others[o], i)
    #             # print(f's\n{s.beacons}')
    #             if np.allclose(s1.beacons, s.beacons):
    #                 self.assertEqual(i, rots[o])

    # def test_rot_trans(self):
    #     c = sc.Combiner()
    #     s = []
    #     with open('2021/day19/test-s0.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s1.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     match = False
    #     rot = None
    #     for i in range(len(c.rots)):
    #         # print(f'Applying rot {i}')
    #         st = c.transform(s[1], i, [68, -1246, -43])
    #         match_count = 0
    #         for j in range(len(s[0].beacons)):
    #             p1 = s[0].beacons[j]
    #             # if p1[0] == -618: print(f'p1 {p1}')
    #             for k in range(len(st.beacons)):
    #                 p2 = st.beacons[k]
    #                 # if p2[0] == -618: print(f'p2 {s.beacons[k]}')
    #                 if p1[0] == p2[0] and p1[1] == p2[1] and p1[2] == p2[2]:
    #                     match_count += 1
    #                     # print(f'Match point at rot {i} {s1.beacons[j]}')
    #                     if match_count >= 12:
    #                         match = True
    #                         rot = i
    #                         break
    #             if match: break
    #         if match: break
    #     self.assertTrue(match)
    #     self.assertEqual(rot, 10)

    # def test_combiner_overlap(self):
    #     c = sc.Combiner()
    #     s = []
    #     with open('2021/day19/test-s0.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s1.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     match, n, origin = c.overlap(s[0], s[1])
    #     self.assertTrue(match)
    #     self.assertEqual(n, 10)
    #     self.assertEqual(origin, [68, -1246, -43])

    #     with open('2021/day19/test-s4.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     match, n, origin = c.overlap(s[1], s[2])
    #     self.assertTrue(match)
    #     self.assertEqual(n, 19)
    #     self.assertEqual(origin, [88, 113, -1104])

    # def test_combiner_combine(self):
    #     c = sc.Combiner()
    #     s = []
    #     with open('2021/day19/test-s0.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s1.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     c.combine(s)
    #     self.assertEqual(len(s[0].beacons), 38)

    # def test_combiner_double(self):
    #     c = sc.Combiner()
    #     s = []
    #     with open('2021/day19/test-s0.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s1.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s4.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     c.combine(s)
    #     self.assertEqual(len(s[0].beacons), 52)

    # def test_combiner_all(self):
    #     c = sc.Combiner()
    #     s = []
    #     with open('2021/day19/test-s0.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s1.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s2.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s3.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))
    #     with open('2021/day19/test-s4.txt', 'r') as f:
    #         s.append(sc.Scanner.read(f))

    #     c.combine(s)

    #     results = []
    #     with open('2021/day19/test-results.txt', 'r') as f:
    #         line = f.readline()
    #         while line:
    #             values = line.strip().split(',')
    #             results.append([int(values[0]), int(values[1]), int(values[2])])
    #             line = f.readline()
    #     results = np.array(results)

    #     self.assertEqual(len(s[0].beacons), len(results))
    #     self.assertTrue(np.all(np.array([p in results for p in s[0].beacons])))

if __name__ == '__main__':
    unittest.main()