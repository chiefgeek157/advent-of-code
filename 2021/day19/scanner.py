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
        self.graph = None

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
        self.graph = nx.DiGraph()
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
                        self.graph.add_edge(s2, s1, count=count, rot=rot, origin=origin)

        # Start at Scanner 0 by convention
        parent = self._scanners[0]
        transform = t.affine(0, (0,0,0))
        beacons = set()
        visited = []
        self.__visit(parent, transform, visited, beacons)

        return beacons

    def __visit(self, parent, transform, visited, beacons):
        t = tr.Transformer()
        visited.append(parent)
        print(f'visit: visiting {parent.id}')

        # Visit unvisited children first
        for p, child, data in self.graph.out_edges(parent, data=True):
            if child in visited: continue
            print(f'visit: using child rot {data["rot"]} origin {data["origin"]}')
            child_transform = t.append_affine(transform, data['rot'], data['origin'])
            beacons = self.__visit(child, child_transform, visited, beacons)

        # Now process this node and add to the set of beacons
        print(f'visit: adding becaons from {parent.id}')
        parent.transform = transform
        bt = t.transform_points(parent.beacons, transform)
        for b in bt:
            beacons.add(b)

        return beacons

    # Calculate the maximum rectilinear distance ("taxicab distance") between any two scanners
    def max_taxi_distance(self):
        if self.graph is None: self.combine()
        t = tr.Transformer()

        d_max = 0
        for s1 in self._scanners:
            for s2 in self._scanners:
                if s1 != s2:
                    o1, r, z, s = t.decompose(s1.transform)
                    o2, r, z, s = t.decompose(s2.transform)
                    d = abs(o2[0] - o1[0]) + abs(o2[1] - o1[1]) + abs(o2[2] - o1[2])
                    d_max = max(d_max, d)
        return d_max

class Scanner():

    def __init__(self, id=None, beacons=None):
        self.id = id
        self.transform = None
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

colorama.init()

