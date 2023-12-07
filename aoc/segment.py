'''Utility functions to handle segements as tuples.'''

def intersects(seg1: tuple, seg2: tuple) -> bool:
    '''Returns True if the two segments intersect.'''
    return seg1[0] <= seg2[1] and seg1[1] >= seg2[0]

def intersection(seg1: tuple, seg2: tuple) -> tuple:
    '''Returns the intersection of two segments.

    If the segments do not intersect, returns None.'''
    if not intersects(seg1, seg2):
        return None
    return (max(seg1[0], seg2[0]), min(seg1[1], seg2[1]))

def split(seg1: tuple, seg2: tuple) -> list(tuple):
    '''Returns a list of three segments representing the split of seg1 by seg2.

    The returned array will contain 1-3 tuples of the form ((start, end), overlap)
    where overlap is a combination of bits, 1 for seg1 and 2 for seg2.

                  |---seg1---|
    |---seg2---|
                  |1---------|

         |---seg1---|
    |---seg2---|
    |2--||3----||1--|

    |---seg1---|
    |-seg2--|
    |3------||1|

    |---seg1---|
       |seg2|
    |1||3---||1|

    |---seg1---|
    |---seg2---|
    |3---------|

    |---seg1---|
        |-seg2-|
    |1-||3-----|

    |---seg1---|
          |---seg2---|
    |1---||3---||2---|

    |---seg1---|
                 |---seg2---|
    |1---------|
    '''
    results = []

    if not intersects(seg1, seg2):
        results.append((seg1, 1))
        return results

    inter = intersection(seg1, seg2)
    new1 = ((min(seg1[0], seg2[0]), min(seg1[1], seg2[1]. inter[0] - 1)),
            1 if seg1[0] < seg2[0] else 2)
    new2 = ((inter[0], inter[1]), 3)
    new3 = (max(seg1[0], seg2[0], inter[1] + 1), max(seg1[1], seg2[1]),
            1 if seg1[1] > seg2[1] else 2)
    if new1[0][0] <= new1[0][1]:
        results.append(new1)
    results.append(new2)
    if new3[0][0] <= new3[0][1]:
        results.append(new3)
    return results