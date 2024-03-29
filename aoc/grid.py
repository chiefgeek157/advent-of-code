"""A bunch of grid-related utilities."""

from collections.abc import Collection, Iterable, Sequence
from itertools import combinations, permutations, product

Extents = Collection[Collection[int]]
Point = Collection[int]

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

def print_sparse_grid(w, h, active):
    for y in range(h):
        line = ''
        for x in range(w):
            line += '#' if (x, y) in active else '.'
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

def extents_include(extents: Extents, point: Point):
    """Expand the given extents to include the given point.

    If extents is None, returns a new extents containing point.
    """
    if extents is None:
        return (tuple(point), tuple(point))

    mins = []
    maxs = []
    for i in range(len(point)):
        mins.append(min(extents[0][i], point[i]))
        maxs.append(max(extents[1][i], point[i]))
    return (tuple(mins), tuple(maxs))

def extents_include_all(extents: Extents, points: list[Point]):
    """Expand the given extents to include all the given points.

    If extents is None, returns a new extents containing points.
    """
    for point in points:
        extents = extents_include(extents, point)
    return extents

def extents_contains(extents: Extents, point: Point):
    """Return True if the point is within the extents."""
    if extents is None:
        return False
    for i in range(len(point)):
        if point[i] < extents[0][i] or point[i] > extents[1][i]:
            return False
    return True

def extents_expand(extents: Extents, dist: int) -> Extents:
    """Return an Extents expanded by dist in every direction."""
    return tuple([tuple([x - dist for x in extents[0]]),
        tuple([p + dist for p in extents[1]])])

def extents_range(extents: Extents, dim: int) -> Iterable[int]:
    """Return a range iterator for the given dimension."""
    return range(extents[0][dim], extents[1][dim] + 1)

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

def get_adjacent(p: Collection[int], bounds: Sequence[Sequence[int]]=None,
        diag=False) -> Collection[int]:
    adjs = []
    dim = len(p)
    for offsets in product([-1, 0, 1], repeat=dim):
        if any(x != 0 for x in offsets):
            count_0 = sum(1 for x in offsets if x == 0)
            if diag or (not diag and count_0 == dim - 1):
                adj = tuple([p[i] + offsets[i] for i in range(dim)])
                if (bounds is None
                    or all([adj[i] >= bounds[0][i]
                        and adj[i] <= bounds[1][i]
                        for i in range(dim)])):
                    adjs.append(adj)
    return adjs

def print_sparse_n_grid(active: list[Point], extents: Extents):
    """Print an n-dimensional grid with active cells.

    Prints as many x-y slices as needed to cover the
    other dimensions. Dimensions are named:
      x, y, z, w, t, dim_num>, ...
    """
    dims = len(extents[0])

    known_dim_labels = ['x', 'y', 'z', 'w', 't']
    labels = []
    for i in range(dims):
        labels.append(known_dim_labels[i] if i < len(known_dim_labels) else i)

    # Iterate dims from last to first to we print y then x
    pos = [0] * dims
    iters = [None] * dims
    dim = dims - 1
    iters[dim] = iter(extents_range(extents, dim))
    while iters[-1] is not None:
        if dim == 1:
            line = ''
        try:
            n = next(iters[dim])
            pos[dim] = n
            if dim == 2:
                line = '\n'
                for i in range(2, dims):
                    line += f'{labels[i]}={pos[i]} '
                print(line)
            if dim > 0:
                dim -= 1
                iters[dim] = iter(extents_range(extents, dim))
            else:
                line += '#' if tuple(pos) in active else '.'
        except StopIteration:
            iters[dim] = None
            dim += 1
            if dim == 1:
                print(line)
