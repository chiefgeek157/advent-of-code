from copy import copy, deepcopy

# filename = '2021/day25/test1.txt'
filename = '2021/day25/input.txt'

def print_grid(step, grid):
    print(f'\nAfter {step} step{"s" if step > 1 else ""}')
    for row in grid:
        print(''.join(row))

grid = []
w = 0
h = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        row = []
        w = len(line.strip())
        for c in line.strip():
            row.append(c)
        grid.append(row)
        line = f.readline()
        h += 1
print_grid(0, grid)

def get_row(grid, y):
    return copy(grid[y])

def put_row(grid, y, row):
    grid[y] = row

def get_col(grid, x):
    col = [''] * h
    for y in range(h):
        col[y] = grid[y][x]
    return col

def put_col(grid, x, col):
    for y in range(h):
        grid[y][x] = col[y]

moved = True
step = 0
while moved:
    moved = False
    step += 1

    # Move east
    for y in range(h):
        row = get_row(grid, y)
        # print(f'  - Checking row {row}')
        for x in range(w - 1, -1, -1):
            # print(f'    - Checking [{x},{y}]: {grid[y][x]}')
            if grid[y][x] == '>':
                next_x = (x + 1) % w
                if grid[y][next_x] == '.':
                    # print(f'      - Moving to {next_x}')
                    row[next_x] = '>'
                    row[x] = '.'
                    moved = True
            # print(f'    - Row now {row}')
        put_row(grid, y, row)

    # print_grid(step, grid)

    # Move south
    for x in range(w):
        col = get_col(grid, x)
        # print(f'  - Checking col {col}')
        for y in range(h - 1, -1, -1):
            # print(f'    - Checking [{x},{y}]: {grid[y][x]}')
            if grid[y][x] == 'v':
                next_y = (y + 1) % h
                if grid[next_y][x] == '.':
                    # print(f'      - Moving to {next_y}')
                    col[next_y] = 'v'
                    col[y] = '.'
                    moved = True
            # print(f'    - Col now {col}')
        put_col(grid, x, col)

    # print_grid(step, grid)

print_grid(step, grid)
print(f'Part 1: {step}')
