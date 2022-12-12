import math

from modules.a_star import a_star

# filename = '2022/day12/test1.txt'
filename = '2022/day12/input.txt'

def add_if_allowed(node1, node2, neighbors):
    global grid
    if node2[0] in range(0, len(grid[0])) and node2[1] in range(0, len(grid)):
        diff = ord(grid[node2[1]][node2[0]]) - ord(grid[node1[1]][node1[0]])
        if diff < 2:
            neighbors.append((node2, diff + 1))

def neighbors(node):
    """Node is a tuple (x, y).

    Returns a list of tuples ((x,y), dist)"""
    neighbors = []
    add_if_allowed(node, (node[0] - 1, node[1]), neighbors)
    add_if_allowed(node, (node[0] + 1, node[1]), neighbors)
    add_if_allowed(node, (node[0], node[1] - 1), neighbors)
    add_if_allowed(node, (node[0], node[1] + 1), neighbors)
    return neighbors

def distance_to_final(node):
    """Distance is the Manhattan distance in x,y plus the difference
    in height (min 0)."""
    global final
    return (
        abs(final[0] - node[0]) + abs(final[1] - node[1])
        + max(0,
            ord(grid[final[1]][final[0]]) - ord(grid[node[1]][node[0]])))

grid = []
start = None
final = None
y = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        row = []
        grid.append(row)
        for x in range(len(line)):
            row.append(line[x])
            if start is None and line[x] == 'S':
                start = (x, y)
                row[-1] = 'a'
            if final is None and line[x] == 'E':
                final = (x, y)
                row[-1] = 'z'
        line = f.readline()
        y += 1
print(f'Grid: {grid}')
print(f'Start: {start} Final: {final}')

min_score, min_path = a_star(start, final, neighbors, distance_to_final)
print(f'Part1: {len(min_path) - 1}')

min_path_len = math.inf
for x in range(len(grid[0])):
    for y in range(len(grid)):
        if grid[y][x] == 'a':
            # print(f'Starting at ({x}, {y})')
            _, min_path = a_star((x, y), final, neighbors, distance_to_final)
            if min_path is None:
                # print(f'Failed to find solution from {x} {y} {grid[y][x]}')
                pass
            else:
                path_len = len(min_path)
                if path_len < min_path_len:
                    print(f'Found new min path len {path_len} at ({x:3},{y:3})')
                    min_path_len = path_len
print(f'Part2: {min_path_len - 1}')