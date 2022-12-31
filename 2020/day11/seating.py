from copy import deepcopy

# filename = '2020/day11/test1.txt'
filename = '2020/day11/input.txt'

grid = []
h = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        grid.append(list(line.strip()))
        h += 1
        line = f.readline()
w = len(grid[0])

part2_grid = deepcopy(grid)

def print_grid(g):
    for y in range(h):
        print(f'{"".join(g[y])}')

print(f'\n=== Part 1 initial grid ===')
print_grid(grid)
part1 = None
iter = 1
changed = True
while changed:
    changed = False
    new_grid = deepcopy(grid)
    for y in range(h):
        for x in range(w):
            count = 0
            if grid[y][x] == '.':
                continue
            for xn, yn in [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                    (x - 1, y), (x + 1, y),
                    (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]:
                if (xn >=0 and xn < w and yn >= 0 and yn < h
                        and grid[yn][xn] == '#'):
                    count += 1
            if grid[y][x] == 'L' and count == 0:
                new_grid[y][x] = '#'
                changed = True
            elif grid[y][x] == '#' and count >= 4:
                new_grid[y][x] = 'L'
                changed = True
    grid = new_grid
    # print(f'\n=== After iter {iter} ===')
    # print_grid(grid)
    iter += 1

print(f'\n=== Part 1 final grid ===')
print_grid(grid)
part1 = 0
for row in grid:
    part1 += row.count('#')
print(f'\nPart 1: {part1}\n')

def is_occupied(x, y, dx, dy):
    xn = x
    yn = y
    while True:
        xn += dx
        yn += dy
        if xn < 0 or xn == w or yn < 0 or yn == h:
            return False
        if grid[yn][xn] == '#':
            return True
        if grid[yn][xn] == 'L':
            return False

grid = part2_grid
print(f'\n=== Part 2 initial grid ===')
print_grid(grid)
part2 = None
iter = 1
changed = True
while changed:
    changed = False
    new_grid = deepcopy(grid)
    for y in range(h):
        for x in range(w):
            count = 0
            if grid[y][x] == '.':
                continue
            for dx, dy in [(-1,-1), (0,-1), (1,-1),
                    (-1,0), (1,0),
                    (-1, 1), (0,1), (1, 1)]:
                if is_occupied(x, y, dx, dy):
                    count += 1
            if grid[y][x] == 'L' and count == 0:
                new_grid[y][x] = '#'
                changed = True
            elif grid[y][x] == '#' and count >= 5:
                new_grid[y][x] = 'L'
                changed = True
    grid = new_grid
    # print(f'\n=== After iter {iter} ===')
    # print_grid(grid)
    iter += 1

print(f'\n=== Part 2 final grid ===')
print_grid(grid)
part2 = 0
for row in grid:
    part2 += row.count('#')
print(f'\nPart 2: {part2}')
