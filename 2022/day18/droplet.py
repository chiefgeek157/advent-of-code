# filename = '2022/day18/test1.txt'
filename = '2022/day18/input.txt'


def turn_off(v):
    if v not in voxels:
        if v not in voids:
            print(f'Adding void {v} with count 5')
            voids[v] = 5
        else:
            voids[v] -= 1
            print(f'Setting void {v} to {voids[v]}')
    else:
        print(f'Voxel {v} is a voxel so not a void')

def check_side(v):
    return not voxels[v]

voids = {}
voxels = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split(',')

        v = tuple([int(f) for f in fields])
        voxels.append(v)
        print(f'Added voxel {v}')

        line = f.readline()

total = 0
for v in voxels:
    print(f'Visiting voxel {v}')
    count = 6
    if (v[0] + 1, v[1] + 0, v[2] + 0) in voxels:
        count -= 1
    if (v[0] - 1, v[1] + 0, v[2] + 0) in voxels:
        count -= 1
    if (v[0] + 0, v[1] + 1, v[2] + 0) in voxels:
        count -= 1
    if (v[0] + 0, v[1] - 1, v[2] + 0) in voxels:
        count -= 1
    if (v[0] + 0, v[1] + 0, v[2] + 1) in voxels:
        count -= 1
    if (v[0] + 0, v[1] + 0, v[2] - 1) in voxels:
        count -= 1

    turn_off((v[0] + 1, v[1], v[2]))
    turn_off((v[0] - 1, v[1], v[2]))
    turn_off((v[0], v[1] + 1, v[2]))
    turn_off((v[0], v[1] - 1, v[2]))
    turn_off((v[0], v[1], v[2] + 1))
    turn_off((v[0], v[1], v[2] - 1))

    total += count

print(f'Part 1: {total}')

bubbles = list(filter(lambda k: voids[k] == 0, voids))
print(f'Bubbles: {bubbles}')

total_bubble = 0
for v in voxels:
    print(f'Visiting voxel {v}')
    count = 0
    if (v[0] + 1, v[1] + 0, v[2] + 0) in bubbles:
        count += 1
    if (v[0] - 1, v[1] + 0, v[2] + 0) in bubbles:
        count += 1
    if (v[0] + 0, v[1] + 1, v[2] + 0) in bubbles:
        count += 1
    if (v[0] + 0, v[1] - 1, v[2] + 0) in bubbles:
        count += 1
    if (v[0] + 0, v[1] + 0, v[2] + 1) in bubbles:
        count += 1
    if (v[0] + 0, v[1] + 0, v[2] - 1) in bubbles:
        count += 1

    print(f'Voxel {v} has bubble side count {count}')
    total_bubble += count
print(f'Total bubble sides: {total_bubble}')
print(f'Part 2: {total - total_bubble}')

# 3284 is too high