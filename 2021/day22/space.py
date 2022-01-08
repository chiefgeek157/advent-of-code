import itertools as it
import math

class Prism():

    def sortby(p1, p2, c, getmin):
        if getmin:
            if p1.pmin[c] < p2.pmin[c]:
                return p1, p2
            else:
                return p2, p1
        else:
            if p1.pmax[c] > p2.pmax[c]:
                return p1.pmax[c], p2.pmax[c], p1.state
            else:
                return p2.pmax[c], p1.pmax[c], p2.state

    def volume(self):
        # Compute coordMax - coordMin for each coord, then return the product
        return math.prod(map(lambda c1, c2: c2 - c1, self.pmin, self.pmax))

    def combine(self, other):
        prisms = []

        if other.pmin in self and other.pmax in self and other:
            # Special case: p2 inside p1 and p2 is state is True
            # Return self (which is True and subsumes other)
            print(f'p2 in p1 and True')
            return [self]
        elif self.pmin in other and self.pmax in other:
            # Special case: p1 inside p2
            # Return other regardless of state
            print(f'p1 in p2 and True')
            return [other]
        elif    self.pmin not in other and self.pmax not in other \
                and other.pmin not in self and other.pmax not in self:
            # No intersection
            print(f'No intersection')
            prisms.append(self)
            if other.state: prisms.append(other)
            return prisms

        # Find intersection int1 to int2
        i1 = tuple([max(c) for c in list(zip(self.pmin, other.pmin))])
        i2 = tuple([min(c) for c in list(zip(self.pmax, other.pmax))])
        print(f'i1={i1} i2={i2}')

        # Decompose into new prisms
        # The intersection prism
        pi = Prism(i1, i2, other.state)
        print(f'pi={pi}, vol={pi.volume()}')
        if pi.volume() > 0: prisms.append(pi)

        # The min x slab
        pbyx = sorted([self, other], key=lambda p: p.pmin[0])
        pmin = (pbyx[0].pmin[0], pbyx[0].pmin[1], pbyx[0].pmin[2])
        pmax = (          i1[0], pbyx[0].pmax[1], pbyx[0].pmax[2])
        px1 = Prism(pmin, pmax, pbyx[0].state)
        print(f'px1={px1}, vol={px1.volume()}')
        if px1.volume() > 0: prisms.append(px1)

        # The max x slab
        pmin = (          i2[0], pbyx[1].pmin[1], pbyx[1].pmin[2])
        pmax = (pbyx[1].pmax[0], pbyx[1].pmax[1], pbyx[1].pmax[2])
        px2 = Prism(pmin, pmax, pbyx[1].state)
        print(f'px2={px2}, vol={px2.volume()}')
        if px2.volume() > 0: prisms.append(px2)

        # The min y column
        pbyy = sorted([self, other], key=lambda p: p.pmin[1])
        pmin = (i1[0], pbyy[0].pmin[1], pbyy[0].pmin[2])
        pmax = (i2[0],           i1[1], pbyy[0].pmax[2])
        py1 = Prism(pmin, pmax, pbyy[0].state)
        print(f'py1={py1}, vol={py1.volume()}')
        if py1.volume() > 0: prisms.append(py1)

        # The max y slab
        pmin = (i1[0],           i2[1], pbyy[1].pmin[2])
        pmax = (i2[0], pbyy[1].pmax[1], pbyy[1].pmax[2])
        py2 = Prism(pmin, pmax, pbyy[1].state)
        print(f'py2={py2}, vol={py2.volume()}')
        if py2.volume() > 0: prisms.append(py2)

        # The min z cuboid
        pbyz = sorted([self, other], key=lambda p: p.pmin[2])
        pmin = (i1[0],           i1[1], pbyz[0].pmin[2])
        pmax = (i2[0],           i2[1],           i1[2])
        pz1 = Prism(pmin, pmax, pbyz[0].state)
        print(f'pz1={pz1}, vol={pz1.volume()}')
        if pz1.volume() > 0: prisms.append(pz1)

        # The max z cuboid
        pmin = (i1[0],           i1[1],           i2[2])
        pmax = (i2[0],           i2[1], pbyz[1].pmax[2])
        pz2 = Prism(pmin, pmax, pbyz[1].state)
        print(f'pz2={pz2}, vol={pz2.volume()}')
        if pz2.volume() > 0: prisms.append(pz2)

        return prisms

    # Extents are a 6-tuple in the order x1, y1, z1, x2, y2, z2
    # State is true is this is a positive space, False is a negative space
    def __init__(self, pmin, pmax, state):
        self.pmin = pmin
        self.pmax = pmax
        self.state = state

    def __contains__(self, p):
        x, y, z = p
        x1, y1, z1 = self.pmin
        x2, y2, z2 = self.pmax
        return self.state and x in range(x1, x2 + 1) and y in range(y1, y2 + 1) and z in range(z1, z2 + 1)

    def __str__(self):
        return f'min={self.pmin} max={self.pmax}, state={self.state}'

    def __repr__(self):
        return str(self)

class Space():

    def add(self, extents, state):
        new_prism = Prism(extents, state)
        if self.prisms is None:
            self.prisms = [new_prism]
        else:
            new_prisms = None
            for prism in self.prisms:
                if new_prisms is None:
                    new_prisms = [prism]
                else:
                    new_prisms = prism.combine(new_prism)
            new_prisms.append(prism)
            self.prisms = new_prisms

    def __init__(self):
        self.prisms = None