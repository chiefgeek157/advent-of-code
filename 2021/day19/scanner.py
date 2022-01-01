import colorama
from colorama import Fore, Style
import networkx as nx
import numpy as np
import transformer as tr
from utils import Utils

class ScannerArray():

    DEFAULT_THRESHHOLD = 12

    def __init__(self):
        self._scanners = []

    def read_file(self, filename):
        with open(filename, 'r') as f:
            s = self.read_from(f)
            while s:
                self._scanners.append(s)
                s = self.read_from(f)

    def read_from(self, f):
        id = None
        beacons = []
        line = f.readline()
        # Empty line means EOF
        while line:
            l = line.strip()
            if not l:
                # Blank line means the end of a scanner but more follow
                break
            if l.startswith('--- '):
                id = int(l.split(' ')[2])
            else:
                coords = l.split(',')
                # Points are tuples
                beacons.append((int(coords[0]), int(coords[1]), int(coords[2])))
            line = f.readline()
        if len(beacons) > 0: return Scanner(id, beacons)
        return False

    # Combine all into a single set of beacons relative to scanner 0
    def combine(self):

        # Algorithm:
        # 1) Create a newtwork of scanners based on sufficient overlap
        # 2) Start at a given scanner
        # 3) Visit each scanner depth-first and only once, transforming all beacons into the coordinates of the starting scanner

        # A directed graph to represent the network of Scanners
        graph = nx.DiGraph()
        t = tr.Transformer()

        # Create a network of all scanner overlaps with all other scanners with the rotation and offset
        # on the arcs. Order is not important as all overlaps are needed to complete the graph.
        # NOTE: count is not strictly needed, but is interesting
        # NOTE: arcs are only created for cases where there is a match to keep the graph simple
        for s1 in self._scanners:
            for s2 in self._scanners:
                if s1 != s2:
                    print(f'combine: comparing scanner {s1.id} to {s2.id}')
                    matches, count, rot, origin = t.best_alignment(s1.beacons, s2.beacons, ScannerArray.DEFAULT_THRESHHOLD)
                    if matches:
                        print(f'combine: matched scanner {s1.id} to {s2.id} with rot {rot} and origin {origin}')
                        graph.add_edge(s2, s1, count=count, rot=rot, origin=origin)

        # Start at Scanner 0 by convention
        parent = self._scanners[0]
        transform = t.affine(0, (0,0,0))
        beacons = set()
        visited = []
        self.__visit(parent, transform, graph, visited, beacons)

        return beacons

    def __visit(self, parent, transform, graph, visited, beacons):
        t = tr.Transformer()
        visited.append(parent)
        print(f'visit: visiting {parent.id}')

        # Visit unvisited children first
        for p, child, data in graph.out_edges(parent, data=True):
            if child in visited: continue
            print(f'visit: using child rot {data["rot"]} origin {data["origin"]}')
            child_transform = t.append_affine(transform, data['rot'], data['origin'])
            beacons = self.__visit(child, child_transform, graph, visited, beacons)

        # Now process this node and add to the set of beacons
        print(f'visit: adding becaons from {parent.id}')
        bt = t.transform_points(parent.beacons, transform)
        for b in bt:
            beacons.add(b)

        return beacons

class Scanner():

    def __init__(self, id=None, beacons=None):
        self.id = id
        # self.parent = None
        # self.children = []
        # self.origin = None
        # self.rot = None
        if beacons is None:
            self.beacons = None
        elif isinstance(beacons, tuple) or isinstance(beacons, list):
            self.beacons = Utils.tuplearray(beacons)
        elif isinstance(beacons, np.ndarray):
            self.beacons = beacons
        else:
            raise ValueError('Invalid type given for beacons')

    def __str__(self):
        s = ''
        for b in self.beacons:
            s += f'{b}\n'
        return s

    # # Create an np.array or tuples from a list of tuples
    # # if given an ndarray, just return it
    # def tuplearray(tlist):
    #     if isinstance(tlist, tuple):
    #         tlist = [tlist]
    #     elif isinstance(tlist, np.ndarray):
    #         return tlist
    #     arr = np.empty(len(tlist), dtype=object)
    #     arr[:] = tlist
    #     return arr

    # def find_matching_beacons(self, scanner):
    #     match, count, rot, origin = self.best_alignment(scanner)
    #     if not match:
    #         return False
    #     t = tr.Transformer()
    #     a = t.affine(rot, origin)
    #     bt = t.transform_points(self.beacons, a)
    #     b_match = []
    #     for b in bt:
    #         ba = np.empty(1, dtype=object)
    #         ba[0] = b
    #         if np.isin(ba, scanner.beacons)[0]: b_match.append(b)
    #     print(f'b_match: {b_match}')

    # def combine_with(self, scanners, visited=None):
    #     if visited is None:
    #         visited = [self]
    #     print(f'Visiting s-{self.id}')
    #     # print(f's-{self.id} rot {self.rot} origin {self.origin} parent_afffine\n{parent_affine}')
    #     t = tr.Transformer()
    #     affine = t.append_affine(parent_affine, self.rot, self.origin)
    #     # print(f's-{self.id} afffine\n{affine}')

    #     # First transform children passing along this affine map
    #     for child in self.children:
    #         child.combine_into(affine, beacons)

    #     # No transform these points and add them in
    #     # print(f's-{self.id} b\n{self.beacons}')
    #     bt = t.transform_points(self.beacons, affine)
    #     # print(f's-{self.id} bt\n{bt}')
    #     for b in bt:
    #         beacons.add(b)
    #     # print(f'After {self.id} beacons now\n{beacons}')

    # # For ease, beacons is a set of tuples
    # def combine_into(self, parent_affine, beacons):
    #     print(f'Visiting s-{self.id}')
    #     # print(f's-{self.id} rot {self.rot} origin {self.origin} parent_afffine\n{parent_affine}')
    #     t = tr.Transformer()
    #     affine = t.append_affine(parent_affine, self.rot, self.origin)
    #     # print(f's-{self.id} afffine\n{affine}')

    #     # First transform children passing along this affine map
    #     for child in self.children:
    #         child.combine_into(affine, beacons)

    #     # No transform these points and add them in
    #     # print(f's-{self.id} b\n{self.beacons}')
    #     bt = t.transform_points(self.beacons, affine)
    #     # print(f's-{self.id} bt\n{bt}')
    #     for b in bt:
    #         beacons.add(b)
    #     # print(f'After {self.id} beacons now\n{beacons}')

    # # Given a set of scanners, set the parent of each scanner
    # def set_parents(scanners):
    #     # Scanner[0] get the identity rot and translation
    #     scanners[0].set_alignment(None, 0, (0,0,0))

    #     # Visit scanners in reverse order since we want scanner 0 to be the top of the chain
    #     for child in reversed(range(1, len(scanners))):
    #         print(f'Setting parent of scanner {scanners[child].id}')
    #         # Visit potential parents in order so that lower parents have more children, if possible
    #         matched = False
    #         best_count = 0
    #         best_parent = None
    #         best_rot = None
    #         best_origin = None
    #         for parent in range(len(scanners)):
    #             if parent != child:
    #                 print(f'Matching against parent scanner {scanners[parent].id}')
    #                 match, count, rot, origin = scanners[child].best_alignment(scanners[parent])
    #                 if match:
    #                     matched = True
    #                     if count > best_count:
    #                         best_count = count
    #                         best_parent = parent
    #                         best_rot = rot
    #                         best_origin = origin
    #         if not matched:
    #             raise ValueError(f'{Fore.RED}{Style.BRIGHT}NO MATCHES{Style.RESET_ALL}')
    #         else:
    #             print(f'Setting scanner {scanners[child].id} parent to {scanners[best_parent].id}')
    #             scanners[child].set_alignment(scanners[best_parent], best_rot, best_origin)

    # def set_alignment(self, parent, rot, origin):
    #     self.parent = parent
    #     if parent is not None: parent.children.append(self)
    #     self.rot = rot
    #     if isinstance(origin, tuple) and len(origin) == 3:
    #         self.origin = origin
    #     else:
    #         raise ValueError('Origin is not a 3-tuple')

# class Combiner():

#     # Cascade downward to first match
#     # Repeat until at the bottom, at which point all
#     # will be combined into scanners[0]
#     def combine(self, scanners):
#         for i in reversed(range(1, len(scanners))):
#             s2 = scanners[i]
#             print(f'\nMerging s[{s2.id}]({len(s2.beacons)})')
#             for j in reversed(range(i)):
#                 s1 = scanners[j]
#                 print(f'Checking against s[{s1.id}]({len(s1.beacons)})')
#                 match, r, o = self.overlap(s1, s2)
#                 if match:
#                     b = self.transform(s2.beacons, r, o)
#                     s1.beacons = np.unique(np.vstack((s1.beacons, b)), axis=0)
#                     print(f's[{s2.id}] merged into s[{s1.id}]({len(s1.beacons)})')
#                     break

#     def overlap(self, s1, s2):
#         match = False
#         origin = [None, None, None]
#         count_max = [None, None, None]
#         rot_max = None
#         for rot in range(len(self.rots)):
#             # print(f'Checking rot {rot}')
#             s2b = self.transform(s2.beacons, rot)
#             axis_match = [False, False, False]
#             d_match = [None, None, None]
#             d_count_match = [None, None, None]
#             for axis in range(3):
#                 s1p = s1.beacons[:, axis]
#                 # print(f's1[{axis}] {s1p}')
#                 s2p = s2b[:, axis]
#                 # print(f's2[{axis}] {s2p}')

#                 diffs = {}
#                 for i in range(len(s1p)):
#                     for j in range(len(s2p)):
#                         d = round(s1p[i] - s2p[j])
#                         if d in diffs:
#                             diffs[d] += 1
#                             # if diffs[d] >= 12:
#                             #     # print(f'rot {rot} axis {axis} has 12 matches at {d}')
#                             #     axis_match[axis] = True
#                             #     origin[axis] = d
#                             #     match_rot = rot
#                             #     break
#                         else:
#                             diffs[d] = 1
#                     # if axis_match[axis]: break

#                 # Get distance with maximum overlap
#                 d_max = max(diffs, key=diffs.get)
#                 d_max_count = diffs[d_max]
#                 if d_max_count >= 12:
#                     print(f'rot {rot} axis {axis} has {d_max_count} matches at distance {d_max}')
#                     axis_match[axis] = True
#                     d_match[axis] = d_max
#                     d_count_match[axis] = d_max_count
#             if all(x for x in axis_match):
#                 print(f'{Fore.YELLOW}All axes matched with counts {d_count_match} for rot {rot} and origin {d_match}{Style.RESET_ALL}')
#                 match = True
#                 bigger = True
#                 if count_max[0] is not None:
#                     for axis in range(3):
#                         if d_count_match[axis] < count_max[axis]: bigger = False
#                 if bigger:
#                     print(f'{Fore.BLUE}Counts are bigger {d_count_match}{Style.RESET_ALL}')
#                     origin = d_match
#                     count_max = d_count_match
#                     if rot_max is None:
#                         rot_max = rot
#                     elif rot != rot_max:
#                         print(f'{Fore.RED}PROBLEM: max d count at different rotations on differnt axes{Style.RESET_ALL}')
#             else:
#                 # print(f'Not all axes matched')
#                 pass
#             # input('Enter...')
#         return match, rot_max, origin

#     def __init__(self):
#         self.__initailize_rots()



colorama.init()

