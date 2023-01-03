import aoc.grid as ag

# filename = '2020/day17/test1.txt'
filename = '2020/day17/input.txt'

part1 = None
part2 = None

# cells are (x, y, z)
active_cells = set()
active_cells2 = set()
extents = None
extents2 = None
with open(filename, 'r') as f:
    y = 0
    z = 0
    w = 0
    line = f.readline()
    while line:
        line = line.strip()
        for x in range(len(line)):
            if line[x] == '#':
                p = (x, y, z)
                p2 = (x, y, z, w)
                active_cells.add(p)
                active_cells2.add(p2)
                extents = ag.extents_include(extents, p)
                extents2 = ag.extents_include(extents2, p2)
        y += 1
        line = f.readline()

def activate(active_cells, extents):
    extents = ag.extents_expand(extents, 1)
    new_active = set()
    dims = len(extents[0])
    iters = [None] * dims
    p = [0] * dims
    dim = dims - 1
    iters[dim] = iter(ag.extents_range(extents, dim))
    while iters[-1] is not None:
        try:
            n = next(iters[dim])
            p[dim] = n
            if dim > 0:
                dim -= 1
                iters[dim] = iter(ag.extents_range(extents, dim))
            else:
                active = tuple(p) in active_cells
                adjs = ag.get_adjacent(p, diag=True)
                count = len(list(filter(lambda p: p in active_cells, adjs)))
                # print(f'  - Visiting {p}, active: {active}, count: {count}')
                # print(f'    - adjs  : {adjs}')
                # print(f'    - active: {list(filter(lambda p: p in active_cells, adjs))}')
                if active and count in [2, 3] or not active and count == 3:
                    # print(f'    - change ACTIVE')
                    new_active.add(tuple(p))
                # elif active:
                    # print(f'    - change NOT ACITVE')
        except StopIteration:
            iters[dim] = None
            dim += 1
    # Tighten the extents
    extents = ag.extents_include_all(None, new_active)
    return new_active, extents

print('=== Initial grid ===')
ag.print_sparse_n_grid(active_cells, extents)
# print(f'  - Num active cells: {len(active_cells)}, extents {extents}')

for i in range(1, 7):
    print(f'\n=== Iteration {i} ===')
    active_cells, extents = activate(active_cells, extents)
    ag.print_sparse_n_grid(active_cells, extents)
    # print(f'  - Num active cells: {len(active_cells)}, extents {extents}')

part1 = len(active_cells)
print(f'\nPart 1: {part1}\n')

print('=== Initial grid ===')
ag.print_sparse_n_grid(active_cells2, extents2)
# print(f'  - Num active cells: {len(active_cells)}, extents {extents}')

for i in range(1, 7):
    print(f'\n=== Iteration {i} ===')
    active_cells2, extents2 = activate(active_cells2, extents2)
    ag.print_sparse_n_grid(active_cells2, extents2)
    # print(f'  - Num active cells: {len(active_cells)}, extents {extents}')

part2 = len(active_cells2)
print(f'\nPart 2: {part2}')
