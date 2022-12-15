"""A bunch of utilities"""

from copy import copy

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
