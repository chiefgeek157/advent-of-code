import re

# filename = '2015/day06/test1.txt'
filename = '2015/day06/input.txt'

parse = re.compile(r'(toggle|turn off|turn on) (\d{1,3}),(\d{1,3}) through (\d{1,3}),(\d{1,3})')
patches = set()
patches.add((0,((0,0),(999,999))))

# a is a rectangle, p is a patch with a status and rectangle
def intersect(verb: str, area: tuple, patch: tuple):
    # print(f'area {area} patch {patch}')
    r1 = area
    r2 = patch[1]
    xmax = min(r1[1][0], r2[1][0])
    xmin = max(r1[0][0], r2[0][0])
    ymax = min(r1[1][1], r2[1][1])
    ymin = max(r1[0][1], r2[0][1])
    patches = [None, None, None, None, None]

    if xmin > xmax or ymin > ymax:
        # No intersection, return existing patch
        patches[4] = patch
    else:
        # Bottom
        if r2[0][1] < ymin: patches[0] = (patch[0], ((r2[0][0], r2[0][1]), (r2[1][0], ymin - 1)))
        # Top
        if r2[1][1] > ymax: patches[1] = (patch[0], ((r2[0][0], ymax + 1), (r2[1][0], r2[1][1])))
        # Left
        if r2[0][0] < xmin: patches[2] = (patch[0], ((r2[0][0], ymin), (xmin - 1, ymax)))
        # Right
        if r2[1][0] > xmax: patches[3] = (patch[0], (((xmax + 1, ymin), (r2[1][0], ymax))))
        # Center
        bright = patch[0]
        if verb == 'turn on':
            bright += 1
        elif verb == 'turn off':
            bright = max(0, bright - 1)
        else:
            bright += 2
        patches[4] = (bright, ((xmin, ymin), (xmax, ymax)))

    return patches

def apply(patches: set, verb: str, area: tuple):
    new_patches = set()
    for patch in patches:
        subpatches = intersect(verb, area, patch)
        # print(f'Subpatches {subpatches}')
        for subpatch in subpatches:
            if subpatch is not None:
                new_patches.add(subpatch)
    return new_patches

def area(patch: tuple):
    return (patch[1][0] - patch[0][0] + 1) * (patch[1][1] - patch[0][1] + 1)

with open(filename, 'r') as f:
    line = f.readline()
    while line:
        print(f'\nline {line} num patches {len(patches)}')
        # for patch in patches:
        #     print(f'Patch {patch}')
        match = parse.match(line)
        patches = apply(patches, match[1], ((int(match[2]), int(match[3])), (int(match[4]), int(match[5]))))
        line = f.readline()

print(f'\nFINAL')
total_brightness = 0
for patch in patches:
    # print(f'Patch {patch}')
    total_brightness += area(patch[1]) * patch[0]

print(f'Total brightness {total_brightness}')