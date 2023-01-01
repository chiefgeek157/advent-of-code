"""A bunch of utilities"""

from copy import copy
import math

def print_vert_header(h_min, h_max, leader='', l_pad='', r_pad=''):
    labels = []
    for h in range(h_min, h_max + 1):
        labels.append(str(h))
    rows = len(max(labels, key=len))
    for i in range(rows):
        line = leader
        for label in labels:
            line += l_pad + label[i] + r_pad
        print(line)

def manhattan_dist(p1, p2):
    """Return the reciliear (Manhattan) between two points.

    The arguments can be any objects that can be subscripted
    including lists, tuples, and numpy arrays.
    """
    return (abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]))

def bound1d(extents, point):
    """Expand the given extents tuple with the given point.

    Extents are any subscriptable type [min, max]
    Point is a subscriptable type [x]

    Returns a tuple (min, max)
    """
    return (min(extents[0], point[0]), max(extents[1], point[1]))

def bound2d(extents, point):
    """Expand the given extents tuple with the given point.

    Extents are any subscriptable type [[min_x, min_y], [max_x, max_y]]
    Point is a subscriptable type [x, y]

    Returns a tuple ((min_x, min_y), (max_x, max_y))
    """
    return (
        (min(extents[0][0], point[0]), min(extents[0][1], point[1])),
        (max(extents[1][0], point[0]), max(extents[1][1], point[1]))
    )

def bound(extents, point):
    """Expand the given extents tuple with the given point.

    Extents are any subscriptable type [[min_x, min_y], [max_x, max_y]]
    Point is a subscriptable type [x, y]

    Returns a tuple ((min_x, min_y), (max_x, max_y))
    """
    if extents is None:
        return (tuple(point), tuple(point))

    mins = []
    maxs = []
    for i in range(len(point)):
        mins.append(min(extents[0][i], point[i]))
        maxs.append(max(extents[1][i], point[i]))
    return (tuple(mins), tuple(maxs))

def contains(extents, point):
    """Return True if the point is within the extents."""
    if extents is None:
        return False
    for i in range(len(point)):
        if point[i] < extents[0][i] or point[i] > extents[1][i]:
            return False
    return True

def union1d(extents, seg):
    """Return the union of extents and seg in 1 dimension.

    extents is a list of segments as tuples.
    seg is a tuple.

    Returns a list of non-overlapping tuples.
    """
    if seg is None:
        return extents
    if len(extents) == 0:
        return [seg]
    if seg[1] < extents[0][0]:
        return [seg] + extents
    if seg[0] > extents[-1][1]:
        return extents + [seg]
    if seg[0] <= extents[0][0] and seg[1] >= extents[-1][1]:
        return [seg]

    new_extents = []
    seg_state = 0
    if seg[0] < extents[0][0]:
        seg_state = 1
        seg_start = seg[0]
    for i in range(len(extents)):
        if seg_state == 0:
            if seg[0] <= extents[i][1]:
                # Seg starts before this extent ends
                seg_start = min(seg[0], extents[i][0])
                if seg[1] <= extents[i][1]:
                    # Seg ends within this extent as well
                    seg_state = 2
                    new_extents.append((seg_start, extents[i][1]))
                else:
                    seg_state = 1
            else:
                # This extent is entirely less than the seg
                new_extents.append(extents[i])
        elif seg_state == 1:
            if seg[1] < extents[i][0]:
                # Seg ended before this extent started
                seg_state = 2
                new_extents.append((seg_start, seg[1]))
                new_extents.append(extents[i])
            elif seg[1] <= extents[i][1]:
                # Seg ends within this extent
                seg_state = 2
                new_extents.append((seg_start, extents[i][1]))
        else:
            # Seg already done, just copy in
            new_extents.append(extents[i])
    if seg_state == 1:
        # Close out the final segment
        new_extents.append((seg_start, max(seg[1], extents[-1][1])))

    return new_extents

# def subtract1d(extents, seg):
#     """Return the extents minus the seg in 1 dimension."""
#     new_extents = []
#     if seg[1] < extents[0] or seg[0] > extents[1]:
#         new_extents = [extents]
#     el:
#         extents = bound1d(extents, seg[0])
#         extents = bound1d(extents, seg[1])
#         new_extents = [extents]
#     return new_extents

def complex_min(*args: complex) -> complex:
    """Return a complex number that is the min of each component.

    This treats complex numbers as cartesian coordiantes.
    """
    return complex(min([c.real for c in args]), min([c.imag for c in args]))

def complex_max(*args: complex) -> complex:
    """Return a complex number that is the max of each component.

    This treats complex numbers as cartesian coordiantes.
    """
    return complex(max([c.real for c in args]), max([c.imag for c in args]))

def complex_bounds(b: tuple[complex, complex], p: complex):
    """Update the given bounds to include p.

    If b is None, returns (p, p)
    """
    if b is None:
        return (p, p)
    return (complex_min(b[0], p), complex_max(b[1], p))

def complex_area(b: tuple[complex, complex]) -> int:
    """Return the area enclosed by the given bounds."""
    return int(b[1].real - b[0].real + 1) * int(b[1].imag - b[0].imag + 1)

def round_int(x: float) -> int:
    if x < 0:
        return math.trunc(x) if -x % 1 < 0.5 else math.floor(x)
    else:
        return math.trunc(x) if  x % 1 < 0.5 else math.ceil(x)

def round_complex(c: complex) -> complex:
    return complex(round_int(c.real), round_int(c.imag))

def mod_inverse(a: int, m: int) -> int:
    """Return the inverse mod for m given b.

    FInd x such that
    a * x === 1 mod m
    """
    a1 = a % m
    for i in range(m):
        if (i * a1) % m == 1:
            print(f'Found mod inverse of {a} and {m}: {i}')
            return i
    print(f'NO mod inverse of {a} and {m}')
    return 0

def chinese_remainder(n: list[int], b: list[int]) -> int:
    """Return the lowest number, n, such that n % n[i] = b[i].

    See https://www.youtube.com/watch?v=zIFehsBHB8o

    Bases must be co-prime.
    """
    print(f'Finding Chinese Reaminder of {n} with remainders {b}')
    count = len(n)
    N0 = math.prod(n)
    print(f'   - N0: {N0}')
    N = []
    for i in range(count):
        N.append(int(N0 / n[i]))
        print(f'   - N[{i}]: {N[-1]}')
    sum_bNx = 0
    for i in range(count):
        xi = mod_inverse(N[i], n[i])
        sum_bNx += b[i] * N[i] * xi
    result = sum_bNx % N0
    print(f'  - Found solution at {result}')
    for i in range(count):
        print(f'    - Check that {result} % {n[i]} = {b[i]}: {result % n[i] == b[i]}')
    return result
