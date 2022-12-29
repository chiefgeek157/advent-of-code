from aoc.utils import bound, contains

# filename = '2022/day18/test1.txt'
filename = '2022/day18/input.txt'


# def turn_off(v):
#     if v not in voxels:
#         if v not in voids:
#             print(f'Adding void {v} with count 5')
#             voids[v] = 5
#         else:
#             voids[v] -= 1
#             print(f'Setting void {v} to {voids[v]}')
#     else:
#         print(f'Voxel {v} is a voxel so not a void')

# def check_side(v):
#     return not voxels[v]

# voids = {}
voxels = []
voids = set()
extents = None
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split(',')

        v = tuple([int(f) for f in fields])
        voxels.append(v)
        print(f'Added voxel {v}')
        extents = bound(extents, v)

        line = f.readline()

total = 0
for v in voxels:
    print(f'Visiting voxel {v}')
    count = 6
    for p in [
            ((v[0] + 1, v[1], v[2])),
            ((v[0] - 1, v[1], v[2])),
            ((v[0], v[1] + 1, v[2])),
            ((v[0], v[1] - 1, v[2])),
            ((v[0], v[1], v[2] + 1)),
            ((v[0], v[1], v[2] - 1))]:
        if p in voxels:
            count -= 1
        else:
            voids.add(p)
    total += count

print(f'\nPart 1: {total}\n')

# Start with a voxel known to be outside and continue until
# all contiguous voids are found
# All other voids are internal
limits = (
    (extents[0][0] - 1, extents[0][1] - 1, extents[0][2] - 1),
    (extents[1][0] + 1, extents[1][1] + 1, extents[1][2] + 1)
)
outside = []
work = [limits[0]]
while work:
    v = work.pop()
    outside.append(v)
    for p in [
            ((v[0] + 1, v[1], v[2])),
            ((v[0] - 1, v[1], v[2])),
            ((v[0], v[1] + 1, v[2])),
            ((v[0], v[1] - 1, v[2])),
            ((v[0], v[1], v[2] + 1)),
            ((v[0], v[1], v[2] - 1))]:
        if p not in work and p not in outside and p not in voxels and contains(limits, p):
            work.append(p)

total = 0
for v in voxels:
    print(f'Visiting voxel {v}')
    count = 6
    for p in [
            ((v[0] + 1, v[1], v[2])),
            ((v[0] - 1, v[1], v[2])),
            ((v[0], v[1] + 1, v[2])),
            ((v[0], v[1] - 1, v[2])),
            ((v[0], v[1], v[2] + 1)),
            ((v[0], v[1], v[2] - 1))]:
        if p in voxels or p not in outside:
            count -= 1
    total += count

print(f'\nPart 2: {total}')
