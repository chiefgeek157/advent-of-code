import copy as cp
import math
from math import pi
import numpy as np
import transforms3d.affines as aff
import transforms3d.axangles as axa
import transforms3d.euler as eul

class Scanner():

    def read(f):
        beacons = []
        id = None
        pnts = None
        line = f.readline()
        while line:
            l = line.strip()
            if not l:
                break
            if l.startswith('--- '):
                id = int(l.split(' ')[2])
            else:
                pnts = l.split(',')
                beacons.append([int(x) for x in pnts])
            line = f.readline()
        return Scanner(id, beacons) if len(beacons) > 0 else False

    def __init__(self, id=None, beacons=None):
        self.id = id
        if beacons is None:
            self.beacons = None
        else:
            self.beacons = np.array(beacons)

    def __str__(self):
        s = ''
        for b in self.beacons:
            s += f'{b}\n'
        return s

class Combiner():

    def __init__(self):
        self.rots = []
        round_vec = np.vectorize(lambda x: round(x))
        self.rots.append(round_vec(eul.euler2mat(   0  ,   0  ,   0  )))
        self.rots.append(round_vec(eul.euler2mat(   0  ,   0  ,  pi/2)))
        self.rots.append(round_vec(eul.euler2mat(   0  ,   0  ,  pi  )))
        self.rots.append(round_vec(eul.euler2mat(   0  ,   0  , -pi/2)))
        self.rots.append(round_vec(eul.euler2mat(  pi/2,   0  ,   0  )))
        self.rots.append(round_vec(eul.euler2mat(  pi/2,   0  ,  pi/2)))
        self.rots.append(round_vec(eul.euler2mat(  pi/2,   0  ,  pi  )))
        self.rots.append(round_vec(eul.euler2mat(  pi/2,   0  , -pi/2)))
        self.rots.append(round_vec(eul.euler2mat(  pi  ,   0  ,   0  )))
        self.rots.append(round_vec(eul.euler2mat(  pi  ,   0  ,  pi/2)))
        self.rots.append(round_vec(eul.euler2mat(  pi  ,   0  ,  pi  )))
        self.rots.append(round_vec(eul.euler2mat(  pi  ,   0  , -pi/2)))
        self.rots.append(round_vec(eul.euler2mat( -pi/2,   0  ,   0  )))
        self.rots.append(round_vec(eul.euler2mat( -pi/2,   0  ,  pi/2)))
        self.rots.append(round_vec(eul.euler2mat( -pi/2,   0  ,  pi  )))
        self.rots.append(round_vec(eul.euler2mat( -pi/2,   0  , -pi/2)))
        self.rots.append(round_vec(eul.euler2mat(   0  ,  pi/2,   0  )))
        self.rots.append(round_vec(eul.euler2mat(   0  ,  pi/2,  pi/2)))
        self.rots.append(round_vec(eul.euler2mat(   0  ,  pi/2,  pi  )))
        self.rots.append(round_vec(eul.euler2mat(   0  ,  pi/2, -pi/2)))
        self.rots.append(round_vec(eul.euler2mat(   0  , -pi/2,   0  )))
        self.rots.append(round_vec(eul.euler2mat(   0  , -pi/2,  pi/2)))
        self.rots.append(round_vec(eul.euler2mat(   0  , -pi/2,  pi  )))
        self.rots.append(round_vec(eul.euler2mat(   0  , -pi/2, -pi/2)))
        for rot in self.rots:
            round_vec(rot)

    def overlap(self, s1, s2):
        match = False
        match_r = None
        origin = [None, None, None]
        for r in range(len(self.rots)):
            # print(f'Checking rot {r}')
            s2b = self.transform(s2.beacons, r)
            axis_match = [False, False, False]
            for axis in range(3):
                s1p = s1.beacons[:, axis]
                # print(f's1[{axis}] {s1p}')
                s2p = s2b[:, axis]
                # print(f's2[{axis}] {s2p}')

                diffs = {}
                for i in range(len(s1p)):
                    for j in range(len(s2p)):
                        d = round(s1p[i] - s2p[j])
                        if d in diffs:
                            diffs[d] += 1
                            if diffs[d] >= 12:
                                # print(f'rot {r} axis {axis} has 12 matches at {d}')
                                axis_match[axis] = True
                                origin[axis] = d
                                match_r = r
                                break
                        else:
                            diffs[d] = 1
                    if axis_match[axis]: break

            if all(x for x in axis_match):
                print(f'All axes matched for rot {r} and origin {origin}')
                match = True
                break
            else:
                # print(f'Not all axes matched')
                pass
            # input('Enter...')
        return match, match_r, origin

    # Cascade downward to first match
    # Repeat until at the bottom, at which point all
    # will be combined into scanners[0]
    def combine(self, scanners):
        for i in reversed(range(1, len(scanners))):
            s2 = scanners[i]
            print(f'\nMerging s[{s2.id}]({len(s2.beacons)})')
            for j in reversed(range(i)):
                s1 = scanners[j]
                print(f'Checking against s[{s1.id}]({len(s1.beacons)})')
                match, r, o = self.overlap(s1, s2)
                if match:
                    b = self.transform(s2.beacons, r, o)
                    s1.beacons = np.unique(np.vstack((s1.beacons, b)), axis=0)
                    print(f's[{s2.id}] merged into s[{s1.id}]({len(s1.beacons)})')
                    break

    def transform(self, b, n=0, t=[0, 0, 0]):
        b = b.copy()
        a = aff.compose(t, self.rots[n], np.ones(3))
        for i in range(len(b)):
            # print(f'{self.rots[n]}, t {t} p {s1.beacons[i]}')
            v = np.append(np.array(b[i]), 1)
            p = np.dot(a, v)
            # print(f'{a} . {v} = {p}')
            b[i] = p[:3]
        return b
