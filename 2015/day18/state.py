import numpy as np

filename = '2015/day18/input.txt'
MAX_ITER = 100
CORNERS = True

# filename = '2015/day18/test1.txt'
# MAX_ITER = 4
# CORNERS = True

def lights_on(g):
    if CORNERS:
        g[0][0] = True
        g[0][g.shape[1] - 1] = True
        g[g.shape[0] - 1][0] = True
        g[g.shape[0] - 1][g.shape[1] - 1] = True

def render(g):
    for i in range(g.shape[0]):
        line = ''
        for j in range(g.shape[1]):
            if g[i][j]:
                line += '#'
            else:
                line += '.'
        print(line)

grid = None
with open(filename, 'r') as f:
    line = f.readline()
    row = 0
    while line:
        line = line.strip()
        if grid is None:
            grid = np.full((len(line), len(line)), False)
        for i in range(len(line)):
            if line[i] == '#':
                grid[row][i] = True
        row += 1

        line = f.readline()
lights_on(grid)
print('Initial grid')
render(grid)

for iter in range(1,MAX_ITER + 1):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # print(f'Visiting [{i},{j}]')

            # Count neighbors
            ncount = 0
            for ii in range(i - 1, i + 2):
                for jj in range(j - 1, j + 2):
                    if ii < 0 or ii >= grid.shape[0] or jj < 0 or jj >= grid.shape[1] or (ii == i and jj == j) or not grid[ii][jj]:
                        # print(f'Skipping [{ii},{jj}]')
                        continue
                    # print(f'Counting [{ii},{jj}]')
                    ncount += 1
            # print(f'[{i},{j}]: count {ncount}')

            # Adjust this location
            if grid[i][j]:
                if ncount < 2 or ncount > 3:
                    # print(f'[{i},{j}]: setting to False')
                    new_grid[i][j] = False
            else:
                if ncount == 3:
                    # print(f'[{i},{j}]: setting to True')
                    new_grid[i][j] = True
    grid = new_grid
    lights_on(grid)

    print(f'\nIter {iter}')
    render(grid)

print(f'\nAns: {(grid).sum()}')