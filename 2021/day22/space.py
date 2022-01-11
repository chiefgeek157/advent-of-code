import itertools as it
import math

class Prism():

    def volume(self):
        # Compute coordMax - coordMin for each coord, then return the product
        return math.prod(map(lambda c1, c2: c2 - c1 + 1, self.pmin, self.pmax))

    def intersection(self, other):
        i1 = tuple([max(c) for c in list(zip(self.pmin, other.pmin))])
        i2 = tuple([min(c) for c in list(zip(self.pmax, other.pmax))])
        # print(f'intersection({self}, {other}): i1={i1} i2={i2}')
        if all([i <= j for i, j in zip(i1, i2)]): return i1, i2
        else: return None

    # Returns the subset of this prism not overlapping with other
    # Returns True if other is subsumed by this prism (and should not be added later)
    def combine(self, other):
        # print(f'combining self={self} with other={other}')
        prisms = []

        inter = self.intersection(other)
        if inter == None:
            # No intersection
            # Return self and not subsumed
            # print(f'   No intersection')
            return [self], False

        if other in self and other.state:
            # Special case: other inside self and other is True
            # Return self and subsumed
            # print(f'   other in self and True')
            return [self], True

        if self in other:
            # Special case: self inside other
            # Return nothing and  not subsumed
            # print(f'   self in other')
            return [], False

        # Decompose self into new prisms outside of other

        i1, i2 = inter

        # The min x slab
        if self.pmin[0] < i1[0]:
            pmin = (self.pmin[0]    , self.pmin[1], self.pmin[2])
            pmax = (       i1[0] - 1, self.pmax[1], self.pmax[2])
            px1 = Prism(pmin, pmax, True)
            # print(f'   px1={px1}')
            prisms.append(px1)

        # The max x slab
        if self.pmax[0] > i2[0]:
            pmin = (       i2[0] + 1, self.pmin[1], self.pmin[2])
            pmax = (self.pmax[0]    , self.pmax[1], self.pmax[2])
            px2 = Prism(pmin, pmax, True)
            # print(f'   px2={px2}')
            prisms.append(px2)

        # The min y column
        if self.pmin[1] < i1[1]:
            pmin = (i1[0], self.pmin[1]    , self.pmin[2])
            pmax = (i2[0],        i1[1] - 1, self.pmax[2])
            py1 = Prism(pmin, pmax, True)
            # print(f'   py1={py1}')
            prisms.append(py1)

        # The max y column
        if self.pmax[1] > i2[1]:
            pmin = (i1[0],        i2[1] + 1, self.pmin[2])
            pmax = (i2[0], self.pmax[1]    , self.pmax[2])
            py2 = Prism(pmin, pmax, True)
            # print(f'   py2={py2}')
            prisms.append(py2)

        # The min z cuboid
        if self.pmin[2] < i1[2]:
            pmin = (i1[0], i1[1], self.pmin[2]    )
            pmax = (i2[0], i2[1],        i1[2] - 1)
            pz1 = Prism(pmin, pmax, True)
            # print(f'   pz1={pz1}')
            prisms.append(pz1)

        # The max z cuboid
        if self.pmax[2] > i2[2]:
            pmin = (i1[0], i1[1],        i2[2] + 1)
            pmax = (i2[0], i2[1], self.pmax[2]    )
            pz2 = Prism(pmin, pmax, True)
            # print(f'   pz2={pz2}')
            prisms.append(pz2)

        return prisms, False

    # Extents are a 6-tuple in the order x1, y1, z1, x2, y2, z2
    # State is true is this is a positive space, False is a negative space
    def __init__(self, pmin, pmax, state):
        self.pmin = pmin
        self.pmax = pmax
        self.state = state
        if not all([i <= j for i, j in zip(pmin, pmax)]):
            raise ValueError('pmin must be <= pmax')

    def __contains__(self, p):
        if isinstance(p, tuple) and len(p) == 3:
            # Testing one point
            return all([i >= j for i, j in zip(p, self.pmin)]) and \
                all([i <= j for i, j in zip(p, self.pmax)])
        elif isinstance(p, Prism):
            # Testing the other prism's min and max
            return (p.pmin in self and p.pmax in self)
        else:
            return NotImplemented

    def __str__(self):
        return f'min={self.pmin} max={self.pmax}, state={self.state}, volume={self.volume()}'

    def __repr__(self):
        return str(self)

class Space():

    def add(self, pmin, pmax, state):
        # print(f'space adding pmin={pmin}, pmax={pmax}, state={state}')
        new_prism = Prism(pmin, pmax, state)
        if self.prisms is None:
            self.prisms = [new_prism]
        else:
            new_prisms = []
            add_new_prism = True
            for prism in self.prisms:
                subprisms, subsumed = prism.combine(new_prism)
                new_prisms += subprisms
                if subsumed: add_new_prism = False
            # print(f'adding {len(new_prisms)} prisms add_new_prism={add_new_prism}')
            self.prisms = new_prisms
            if add_new_prism and new_prism.state:
                # Append the new prism if it has not been subsumed and it is 'on'
                self.prisms.append(new_prism)
        # print(f'space num prisms {len(self.prisms)}')
        # input('enter')

        # # Sanity check for no overlapping prisms
        # for p1 in self.prisms:
        #     if not p1.state:
        #         print(f'ERROR prism not on {p1}')
        #     for p2 in self.prisms:
        #         if p1 != p2 and p1.intersection(p2) is not None:
        #             print(f'ERROR: intersection between {p1} and {p2}')

    def volume(self):
        v = 0
        for prism in self.prisms:
            v += prism.volume()
        return v

    def __init__(self):
        self.prisms = None

    def __str__(self):
        s = f'space: volume={self.volume()}'
        # for prism in self.prisms:
        #     s += f'\n   {prism}'
        return s