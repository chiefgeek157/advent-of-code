import colorama
from colorama import Fore, Style
from math import pi
import numpy as np
import operator as op
import transforms3d.affines as aff
import transforms3d.euler as eul

class Transformer():

    def rot(self, n):
        return Transformer.__rots[n]

    def num_rots(self):
        return len(Transformer.__rots)

    def affine(self, rot, trans=(0, 0, 0)):
        return aff.compose(trans, self.rot(rot), np.ones(3))

    def append_affine(self, affine, rot, trans):
        post = self.affine(rot, trans)
        # print(f'\npre\n{pre}\naff\n{affine}\ndot\n{np.dot(pre,affine)}')
        if affine is None: return post
        return np.dot(affine, post)

    # Transform a point tuple
    # Return the transformed point tuple
    def transform(self, point, affine):
        # print(f'{self.rots[n]}, t {t} p {s1.beacons[i]}')
        v = np.empty(4)
        v[:3] = point
        v[3] = 1
        vt = np.dot(affine, v)
        # print(f'{a} . {v} = {vt}')
        return tuple(vt[:3])

    # Transform an np.array of point tuples by applying a rotation r then a translation
    # Return a new np.array with the transformed point tuples
    def transform_points(self, points, affine):
        res = np.empty(len(points), dtype=object)
        for i in range(len(points)):
            res[i] = self.transform(points[i], affine)
        return res

    # Find the best alignment of a given set of points to a second set of points
    def best_alignment(self, points1, points2, threshhold):
        matches = False
        best_count = 0
        best_rot = None
        best_offset = None

        # For each possible rotation, compute the offset to maximize the number of aligned beacons
        #
        # For each beacon is this set, compute the offset to every beacon in the other set and
        # count how many times each offset occurs. Find the offset and rotation with the maximal number of
        # occurances.

        for r in range(self.num_rots()):
            # print(f'\nChecking rot {r}')
            # v_counts is the count of each difference vector
            d_counts = {}

            # Transform these beacons by rot r
            p1t = self.transform_points(points1, self.affine(r))

            # Count vectors from every transformed beacon in this scanner to every beacon in the given set
            for p1 in p1t:
                for p2 in points2:

                    # d is the vector from b1 to b2
                    d = tuple(map(op.sub, p2, p1))
                    # print(f'b1={b1}, b2={b2}, d={d}')
                    if d not in d_counts: d_counts[d] = 0
                    d_counts[d] += 1

            # Get the vector counts in reverse order
            for d in sorted(d_counts, key=d_counts.get, reverse=True):
                count = d_counts[d]
                if count >= threshhold:
                    matches = True
                    # print(f'{Fore.GREEN}FOUND MATCH with {count} matches at rot {r} and offset {d}{Style.RESET_ALL}')
                    if count >= best_count:
                        if best_count > 0: print(f'{Fore.MAGENTA}BETTER COUNT{Style.RESET_ALL}')
                        best_count = count
                        best_offset = d
                        best_rot = r
                    break
            # input("enter...")

        return matches, best_count, best_rot, best_offset
    def __init__(self):
        Transformer.__initailize_rots()

    __rots = None

    def __initailize_rots():
        if Transformer.__rots == None:
            rots = []
            round_vec = np.vectorize(lambda x: round(x))
            rots.append(round_vec(eul.euler2mat(   0  ,   0  ,   0  )))
            rots.append(round_vec(eul.euler2mat(   0  ,   0  ,  pi/2)))
            rots.append(round_vec(eul.euler2mat(   0  ,   0  ,  pi  )))
            rots.append(round_vec(eul.euler2mat(   0  ,   0  , -pi/2)))
            rots.append(round_vec(eul.euler2mat(  pi/2,   0  ,   0  )))
            rots.append(round_vec(eul.euler2mat(  pi/2,   0  ,  pi/2)))
            rots.append(round_vec(eul.euler2mat(  pi/2,   0  ,  pi  )))
            rots.append(round_vec(eul.euler2mat(  pi/2,   0  , -pi/2)))
            rots.append(round_vec(eul.euler2mat(  pi  ,   0  ,   0  )))
            rots.append(round_vec(eul.euler2mat(  pi  ,   0  ,  pi/2)))
            rots.append(round_vec(eul.euler2mat(  pi  ,   0  ,  pi  )))
            rots.append(round_vec(eul.euler2mat(  pi  ,   0  , -pi/2)))
            rots.append(round_vec(eul.euler2mat( -pi/2,   0  ,   0  )))
            rots.append(round_vec(eul.euler2mat( -pi/2,   0  ,  pi/2)))
            rots.append(round_vec(eul.euler2mat( -pi/2,   0  ,  pi  )))
            rots.append(round_vec(eul.euler2mat( -pi/2,   0  , -pi/2)))
            rots.append(round_vec(eul.euler2mat(   0  ,  pi/2,   0  )))
            rots.append(round_vec(eul.euler2mat(   0  ,  pi/2,  pi/2)))
            rots.append(round_vec(eul.euler2mat(   0  ,  pi/2,  pi  )))
            rots.append(round_vec(eul.euler2mat(   0  ,  pi/2, -pi/2)))
            rots.append(round_vec(eul.euler2mat(   0  , -pi/2,   0  )))
            rots.append(round_vec(eul.euler2mat(   0  , -pi/2,  pi/2)))
            rots.append(round_vec(eul.euler2mat(   0  , -pi/2,  pi  )))
            rots.append(round_vec(eul.euler2mat(   0  , -pi/2, -pi/2)))
            for rot in rots:
                round_vec(rot)
            Transformer.__rots = rots

colorama.init()