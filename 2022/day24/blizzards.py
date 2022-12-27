import math

from aoc.search import a_star
from aoc.utils import manhattan_dist

# filename = '2022/day24/test1.txt'
filename = '2022/day24/input.txt'

moves = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1)
}

def print_grid(g):
    print(f'#.{"#" * w}')
    for y in range(h):
        line = '#'
        for x in range(w):
            if (x, y) in g:
                blizzs = g[(x, y)]
                if len(blizzs) == 1:
                    line += directions[blizzs[0]]
                else:
                    line += str(len(blizzs))
            else:
                line += '.'
        line += '#'
        print(line)
    print(f'{"#" * w}.#')

def print_state(state, node=None):
    for y in range(h):
        line = ''
        for x in range(w):
            if node is not None and (node[1], node[2]) == (x, y):
                line += '#'
            elif (x, y) in state:
                line += 'O'
            else:
                line += '.'
        print(line)

blizzards = []
directions = []
w = None
h = None
with open(filename, 'r') as f:
    line = f.readline()
    w = len(line) - 3
    line = f.readline()
    y = 0
    while line:
        if line.startswith('##'):
            break
        x = 0
        for c in line.strip()[1:-1]:
            if c != '.':
                # print(f'Blizzard at [{x}, {y}] in direction {c}')
                blizzards.append((x, y))
                directions.append(c)
            x += 1
        line = f.readline()
        y += 1
    h = y

num_states = math.lcm(w, h)
print(f'Size: {w} x {h}, num_states = {num_states} ')

def blow(b, d):
    # print(f'Blowing {b} in {d}')
    bx = (b[0] + moves[d][0]) % w
    by = (b[1] + moves[d][1]) % h
    return (bx, by)

states = []
for t in range(num_states):
    # print(f'\n=== Time {t} ===')
    grid = {}
    state = []
    for i in range(len(blizzards)):
        bliz = blizzards[i]
        dir = directions[i]
        if bliz not in grid:
            grid[bliz] = []
        grid[bliz].append(i)
        blizzards[i] = blow(bliz, dir)

    # print_grid(grid)

    for x in range(w):
        for y in range(h):
            if (x, y) not in grid:
                # print(f'Empty spot at {(x,y)}')
                state.append((x, y))
    state.append((0, -1))
    state.append((w - 1, h))

    # print_state(state)
    states.append(state)

# for i in range(len(states)):
    # print(f'\nState {i}')
    # print_state(states[i])

# A node is a tuple
# (x, y)

def is_final(node):
    return ((node[1], node[2]) == final)

def get_next_nodes(node):
    print(f'Visiting [{node[1]},{node[2]}] in state {node[0]}')
    nodes = []
    next_state = (node[0] + 1) % num_states
    state = states[next_state]
    # print_state(state, node)
    for next in [
        (node[1]    , node[2]    ),
        (node[1]    , node[2] - 1),
        (node[1] + 1, node[2]    ),
        (node[1]    , node[2] + 1),
        (node[1] - 1, node[2]    ),
    ]:
        if next in state:
            nodes.append(((next_state, next[0], next[1]), 1))

    print(f'  - Can move to: {nodes}')
    return nodes

def heuristic(node):
    return manhattan_dist((node[1], node[2]), final)

start_node = (0, 0, -1)
final = (w - 1, h)
min_dist, min_path = a_star(start_node, is_final, get_next_nodes, heuristic)

print(f'Min path: {min_path}')
print(f'\nPart 1: {len(min_path) - 1}\n')

total_time = len(min_path) - 1

# Part 2, back home and to final again

start = (w - 1, h)
final = (0, -1)
min_dist, min_path = a_star(min_path[-1], is_final, get_next_nodes, heuristic)

print(f'Min path: {min_path}')
print(f'\nPart 2a: {len(min_path) - 1}\n')

total_time += len(min_path) - 1

start = (0, -1)
final = (w - 1, h)
min_dist, min_path = a_star(min_path[-1], is_final, get_next_nodes, heuristic)

print(f'Min path: {min_path}')
print(f'\nPart 2b: {len(min_path) - 1}')

total_time += len(min_path) - 1
print(f'\nPart 2: {total_time}')
