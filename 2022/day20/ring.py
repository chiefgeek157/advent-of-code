from copy import deepcopy

filename = '2022/day20/test1.txt'
# filename = '2022/day20/input.txt'

def print_by_pos():
    line = ''
    for i in sorted(items_by_pos):
        item = items_by_pos[i]
        line += f'{item[0]}[{item[1][0]},{item[2][0]}] '
    print(line)

def append(v):
    global items_by_pos, root_item
    print(f'Appending {v}')
    if root_item is None:
        root_item = [v, None, None]
        root_item[1] = root_item
        root_item[2] = root_item
        items_by_pos[0] = root_item
    else:
        prev_item = root_item[1]
        next_item = root_item
        item = [v, prev_item, next_item]
        prev_item[2] = item
        next_item[1] = item
        items_by_pos[len(items_by_pos)] = item
    # print_by_pos()

def move(item, p1, p2, old_to_new, new_to_old):
    global items_by_pos, root_item

    print(f'Moving {item[0]} from {p1} to {p2}')
    prev1 = item[1]
    next1 = item[2]
    new_prev = items_by_pos[p2]
    new_next = new_prev[2]

    prev1[2] = next1
    next1[1] = prev1

    new_prev[2] = item
    item[1] = new_prev

    new_next[1] = item
    item[2] = new_next

    if item == root_item:
        root_item = next1

    if p1 < p2:
        for i in range(p1, p2):
            items_by_pos[i] = items_by_pos[i + 1]
            old_to_new[i + 1] = i
        items_by_pos[p2] = item
        old_to_new[p1] = p2
    else:
        for i in range(p1, p2, -1):
            items_by_pos[i] = items_by_pos[i - 1]
            old_to_new[i - 1] = i
        items_by_pos[p2 + 1] = item
        old_to_new[p1] = p2 + 1
    print_by_pos()

def rotate():
    global items_by_pos, root_item

    size = len(items_by_pos)
    old_to_new = {}
    new_to_old = {}
    for i in range(size):
        old_to_new[i] = i
        new_to_old[i] = i

    # old = [items_by_pos[v][0] for v in sorted(items_by_pos)]
    # for v in old:
    for i in range(size):
        p1 = old_to_new[i]
        item = items_by_pos[p1]
        v = item[0]
        if v != 0:
            p2 = (p1 + v - (1 if v < 0 else 0)) % size
            move(item, p1, p2,  old_to_new, new_to_old)

# items_by_val = {}
items_by_pos = {}
# pos_by_val = {}
root_item = None
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        append(int(line.strip()))
        line = f.readline()

rotate()

p0 = pos_by_val[0]
p1000 = (p0 + 1000) % len(pos_by_val)
v1000 = items_by_pos[(p0 + 1000) % len(pos_by_val)][0]
v2000 = items_by_pos[(p0 + 2000) % len(pos_by_val)][0]
v3000 = items_by_pos[(p0 + 3000) % len(pos_by_val)][0]
print(f'Part 1: {v1000} + {v2000} + {v3000} = {v1000 + v2000 + v3000}')
