import sys

# filename = '2021/day23/test1.txt'
# filename = '2021/day23/test2.txt'
# filename = '2021/day23/test3.txt'
filename = '2021/day23/input.txt'

# Board positions
#
# 00 01 .. 02 .. 03 .. 04 .. 05 06
#       07    08    09    10
#       11    12    13    14

NUM_POS = 15

FINAL_STATE = (' ', ' ', ' ', ' ', ' ', ' ', ' ', 'A', 'B', 'C', 'D', 'A', 'B', 'C', 'D')

MOVE_COSTS = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

# Home positions by piece type
HOME_POS = {
    'A': [7, 11],
    'B': [8, 12],
    'C': [9, 13],
    'D': [10, 14]
}

# Distance to the first possible home for each piece type from each position
HOME_DISTS = {
    #     0  1  2  3  4  5  6  7  8  9  0  1  2  3  4
    'A': [3, 2, 2, 4, 6, 8, 9, 0, 4, 6, 8, 0, 5, 7, 9],
    'B': [5, 4, 2, 2, 4, 6, 7, 4, 0, 4, 6, 5, 0, 5, 7],
    'C': [7, 6, 4, 2, 2, 4, 5, 6, 4, 0, 4, 7, 5, 0, 5],
    'D': [9, 8, 6, 4, 2, 2, 3, 8, 6, 4, 0, 9, 7, 5, 0]
}

# Adjacencies [neighbor, cost multiplier]
ADJS = [
    [(1, 1)],                          # 0
    [(0, 1), (2, 2), (7, 2)],          # 1
    [(1, 2), (3, 2), (7, 2), (8, 2)],  # 2
    [(2, 2), (4, 2), (8, 2), (9, 2)],  # 3
    [(3, 2), (5, 2), (9, 2), (10, 2)], # 4
    [(4, 2), (6, 1), (10, 2)],         # 5
    [(5, 1)],                          # 6
    [(1, 2), (2, 2), (11, 1)],         # 7
    [(2, 2), (3, 2), (12, 1)],         # 8
    [(3, 2), (4, 2), (13, 1)],         # 9
    [(4, 2), (5, 2), (14, 1)],         # 10
    [(7, 1)],                          # 11
    [(8, 1)],                          # 12
    [(9, 1)],                          # 13
    [(10, 1)]                          # 14
]

# The possible moves
# ([allowed for], steps, cost)
MOVES = {
    ( 0,  7): (['A'], [ 1,  7],                  3),
    ( 0, 11): (['A'], [ 1,  7, 11],              4),
    ( 0,  8): (['B'], [ 1,  2,  8],              5),
    ( 0, 12): (['B'], [ 1,  2,  8, 12],          6),
    ( 0,  9): (['C'], [ 1,  2,  3,  9],          7),
    ( 0, 13): (['C'], [ 1,  2,  3,  9,  13],     8),
    ( 0, 10): (['D'], [ 1,  2,  3,  4,  10],     9),
    ( 0, 14): (['D'], [ 1,  2,  3,  4,  10, 14],10),
    ( 1,  7): (['A'], [ 7],                      2),
    ( 1, 11): (['A'], [ 7, 11],                  3),
    ( 1,  8): (['B'], [ 2,  8],                  4),
    ( 1, 12): (['B'], [ 2,  8, 12],              5),
    ( 1,  9): (['C'], [ 2,  3,  9],              6),
    ( 1, 13): (['C'], [ 2,  3,  9,  13],         7),
    ( 1, 10): (['D'], [ 2,  3,  4,  10],         8),
    ( 1, 14): (['D'], [ 2,  3,  4,  10, 14],     9),
    ( 2,  7): (['A'], [ 7],                      2),
    ( 2, 11): (['A'], [ 7, 11],                  3),
    ( 2,  8): (['B'], [ 8],                      2),
    ( 2, 12): (['B'], [ 8, 12],                  3),
    ( 2,  9): (['C'], [ 3,  9],                  4),
    ( 2, 13): (['C'], [ 3,  9,  13],             5),
    ( 2, 10): (['D'], [ 3,  4,  10],             6),
    ( 2, 14): (['D'], [ 3,  4,  10, 14],         7),
    ( 3,  7): (['A'], [ 2,  7],                  4),
    ( 3, 11): (['A'], [ 2,  7, 11],              5),
    ( 3,  8): (['B'], [ 8],                      2),
    ( 3, 12): (['B'], [ 8, 12],                  3),
    ( 3,  9): (['C'], [ 9],                      2),
    ( 3, 13): (['C'], [ 9,  13],                 3),
    ( 3, 10): (['D'], [ 4,  10],                 4),
    ( 3, 14): (['D'], [ 4,  10, 14],             5),
    ( 4,  7): (['A'], [ 3,  2,  7],              6),
    ( 4, 11): (['A'], [ 3,  2,  7, 11],          7),
    ( 4,  8): (['B'], [ 3,  8],                  4),
    ( 4, 12): (['B'], [ 3,  8, 12],              5),
    ( 4,  9): (['C'], [ 9],                      2),
    ( 4, 13): (['C'], [ 9,  13],                 3),
    ( 4, 10): (['D'], [ 10],                     2),
    ( 4, 14): (['D'], [ 10, 14],                 3),
    ( 5,  7): (['A'], [ 4,  3,  2,  7],          8),
    ( 5, 11): (['A'], [ 4,  3,  2,  7, 11],      9),
    ( 5,  8): (['B'], [ 4,  3,  8],              6),
    ( 5, 12): (['B'], [ 4,  3,  8, 12],          7),
    ( 5,  9): (['C'], [ 4,  9],                  4),
    ( 5, 13): (['C'], [ 4,  9,  13],             5),
    ( 5, 10): (['D'], [ 4,  10],                 2),
    ( 5, 14): (['D'], [ 4,  10, 14],             3),
    ( 6,  7): (['A'], [ 5,  4,  3,  2,  7],      9),
    ( 6, 11): (['A'], [ 5,  4,  3,  2,  7, 11], 10),
    ( 6,  8): (['B'], [ 5,  4,  3,  8],          7),
    ( 6, 12): (['B'], [ 5,  4,  3,  8, 12],      8),
    ( 6,  9): (['C'], [ 5,  4,  9],              5),
    ( 6, 13): (['C'], [ 5,  4,  9,  13],         6),
    ( 6, 10): (['D'], [ 5,  4,  10],             3),
    ( 6, 14): (['D'], [ 5,  4,  10, 14],         4),
    ( 7,  0): (['A', 'B', 'C', 'D'], [ 1,  0],                  3),
    ( 7,  1): (['A', 'B', 'C', 'D'], [ 1],                      2),
    ( 7,  2): (['A', 'B', 'C', 'D'], [ 2],                      2),
    ( 7,  3): (['A', 'B', 'C', 'D'], [ 2,  3],                  4),
    ( 7,  4): (['A', 'B', 'C', 'D'], [ 2,  3,  4],              6),
    ( 7,  5): (['A', 'B', 'C', 'D'], [ 2,  3,  4,  5],          8),
    ( 7,  6): (['A', 'B', 'C', 'D'], [ 2,  3,  4,  5,  6],      9),
    ( 8,  0): (['A', 'B', 'C', 'D'], [ 2,  1,  0],              5),
    ( 8,  1): (['A', 'B', 'C', 'D'], [ 2,  1],                  4),
    ( 8,  2): (['A', 'B', 'C', 'D'], [ 2],                      2),
    ( 8,  3): (['A', 'B', 'C', 'D'], [ 3],                      2),
    ( 8,  4): (['A', 'B', 'C', 'D'], [ 3,  4],                  4),
    ( 8,  5): (['A', 'B', 'C', 'D'], [ 3,  4,  5],              6),
    ( 8,  6): (['A', 'B', 'C', 'D'], [ 3,  4,  5,  6],          7),
    ( 9,  0): (['A', 'B', 'C', 'D'], [ 3,  2,  1,  0],          7),
    ( 9,  1): (['A', 'B', 'C', 'D'], [ 3,  2,  1],              6),
    ( 9,  2): (['A', 'B', 'C', 'D'], [ 3,  2],                  4),
    ( 9,  3): (['A', 'B', 'C', 'D'], [ 3],                      2),
    ( 9,  4): (['A', 'B', 'C', 'D'], [ 4],                      2),
    ( 9,  5): (['A', 'B', 'C', 'D'], [ 4,  5],                  4),
    ( 9,  6): (['A', 'B', 'C', 'D'], [ 4,  5,  6],              5),
    (10,  0): (['A', 'B', 'C', 'D'], [ 4,  3,  2,  1,  0],      9),
    (10,  1): (['A', 'B', 'C', 'D'], [ 4,  3,  2,  1],          8),
    (10,  2): (['A', 'B', 'C', 'D'], [ 4,  3,  2],              6),
    (10,  3): (['A', 'B', 'C', 'D'], [ 4,  3],                  4),
    (10,  4): (['A', 'B', 'C', 'D'], [ 4],                      2),
    (10,  5): (['A', 'B', 'C', 'D'], [ 5],                      2),
    (10,  6): (['A', 'B', 'C', 'D'], [ 5,  6],                  3),
    (11,  0): (['A', 'B', 'C', 'D'], [ 7,  1,  0],              4),
    (11,  1): (['A', 'B', 'C', 'D'], [ 7,  1],                  3),
    (11,  2): (['A', 'B', 'C', 'D'], [ 7,  2],                  3),
    (11,  3): (['A', 'B', 'C', 'D'], [ 7,  2,  3],              5),
    (11,  4): (['A', 'B', 'C', 'D'], [ 7,  2,  3,  4],          7),
    (11,  5): (['A', 'B', 'C', 'D'], [ 7,  2,  3,  4,  5],      9),
    (11,  6): (['A', 'B', 'C', 'D'], [ 7,  2,  3,  4,  5,  6], 10),
    (12,  0): (['A', 'B', 'C', 'D'], [ 8,  2,  1,  0],          6),
    (12,  1): (['A', 'B', 'C', 'D'], [ 8,  2,  1],              5),
    (12,  2): (['A', 'B', 'C', 'D'], [ 8,  2],                  3),
    (12,  3): (['A', 'B', 'C', 'D'], [ 8,  3],                  3),
    (12,  4): (['A', 'B', 'C', 'D'], [ 8,  3,  4],              5),
    (12,  5): (['A', 'B', 'C', 'D'], [ 8,  3,  4,  5],          7),
    (12,  6): (['A', 'B', 'C', 'D'], [ 8,  3,  4,  5,  6],      8),
    (13,  0): (['A', 'B', 'C', 'D'], [ 9,  3,  2,  1,  0],      8),
    (13,  1): (['A', 'B', 'C', 'D'], [ 9,  3,  2,  1],          7),
    (13,  2): (['A', 'B', 'C', 'D'], [ 9,  3,  2],              5),
    (13,  3): (['A', 'B', 'C', 'D'], [ 9,  3],                  3),
    (13,  4): (['A', 'B', 'C', 'D'], [ 9,  4],                  3),
    (13,  5): (['A', 'B', 'C', 'D'], [ 9,  4,  5],              5),
    (13,  6): (['A', 'B', 'C', 'D'], [ 9,  4,  5,  6],          6),
    (14,  0): (['A', 'B', 'C', 'D'], [10,  4,  3,  2,  1,  0], 10),
    (14,  1): (['A', 'B', 'C', 'D'], [10,  4,  3,  2,  1],      9),
    (14,  2): (['A', 'B', 'C', 'D'], [10,  4,  3,  2],          7),
    (14,  3): (['A', 'B', 'C', 'D'], [10,  4,  3],              5),
    (14,  4): (['A', 'B', 'C', 'D'], [10,  4],                  3),
    (14,  5): (['A', 'B', 'C', 'D'], [10,  5],                  3),
    (14,  6): (['A', 'B', 'C', 'D'], [10,  5,  6],              4)
}

DISTS = {
    0: {7:3, 11:4, 8:5, 12:6, 9:7, 13:8, 10:9, 14:10},
    1: {7:2, 11:3, 8:4, 12:5, 9:6, 13:7, 10:8, 14:9},
    2: {7:2, 11:3, 8:2, 12:3, 9:4, 13:5, 10:6, 14:7},
    3: {7:4, 11:5, 8:2, 12:3, 9:2, 13:3, 10:4, 14:5},
    4: {7:6, 11:7, 8:4, 12:5, 9:2, 13:3, 10:2, 14:3},
    5: {7:8, 11:9, 8:6, 12:7, 9:4, 13:5, 10:2, 14:3},
    6: {7:9, 11:10, 8:7, 12:8, 9:5, 13:6, 10:3, 14:4},
    7: {0:3, 1:2, 2:2, 3:4, 4:6, 5:8, 6:9},
    8: {0:5, 1:4, 2:2, 3:2, 4:4, 5:6, 6:7},
    9: {0:7, 1:6, 2:4, 3:2, 4:2, 5:4, 6:5},
    10: {0:9, 1:8, 2:6, 3:4, 4:2, 5:2, 6:3},
    11: {0:4, 1:3, 2:3, 3:5, 4:7, 5:9, 6:10},
    12: {0:6, 1:5, 2:3, 3:3, 4:5, 5:7, 6:8},
    13: {0:8, 1:7, 2:5, 3:3, 4:3, 5:5, 6:6},
    14: {0:10, 1:9, 2:7, 3:5, 4:3, 5:3, 6:4}
}

initial_state = [' '] * (NUM_POS + 4)
with open(filename, 'r') as f:
    # Discard first line
    f.readline()

    pos = 0
    line = f.readline()
    while line:
        # print(f'Initial state: {initial_state}')
        for c in line.strip():
            # print(f'Read char {c} as pos {pos}')
            if c != '#':
                if c != '.':
                    initial_state[pos] = c
                    # print(f'Set pos {pos} to {c}')
                pos += 1
        line = f.readline()
initial_state = tuple([v for i,v in enumerate(initial_state) if i not in frozenset((2, 4 , 6, 8))])
print(f'Initial state: {initial_state}')

def get_est_cost(state):
    global NUM_POS, HOME_DISTS, MOVE_COSTS
    cost = 0
    for i in range(NUM_POS):
        if state[i] != ' ':
            cost += HOME_DISTS[state[i]][i] * MOVE_COSTS[state[i]]
    return cost

def get_total_cost(state):
    global costs
    min_cost, est_cost = costs[state]
    return min_cost + est_cost

def get_moves_for(piece, pos, state):
    """Return a list of move consisting (state, cost)"""
    global NUM_POS, MOVES, MOVE_COSTS
    valid_moves = []
    for new_pos in range(NUM_POS):
        if (pos, new_pos) in MOVES:
            valid_for, steps, length = MOVES[(pos, new_pos)]
            if piece in valid_for:
                path_clear = True
                for step in steps:
                    if state[step] != ' ':
                        path_clear = False
                        break
                if path_clear:
                    new_state = list(state)
                    new_state[pos] = ' '
                    new_state[new_pos] = piece
                    valid_moves.append((tuple(new_state), MOVE_COSTS[piece] * length))
    return valid_moves

def is_home(state):
    global NUM_POS
    res = [False] * NUM_POS
    for i in range(7):
        res[i] = (state[i] == ' ')
    res[11] = (state[11] == 'A')
    res[7] = (res[11] and state[7] == 'A')
    res[12] = (state[12] == 'B')
    res[8] = (res[12] and state[8] == 'B')
    res[13] = (state[13] == 'C')
    res[9] = (res[13] and state[9] == 'C')
    res[14] = (state[14] == 'D')
    res[10] = (res[14] and state[10] == 'D')
    return res

# The array of potential next states as tuples
work = []

# The array of visited states as tuples
visited = []

# The minmmum cost of each state so far along with the estimate cost to complete
# The keys are state tuples and the values are tuples of (min_cost, est_cost)
costs = {}

predecessors = {}
predecessors[initial_state] = None

work.append(initial_state)
costs[initial_state] = (0, get_est_cost(initial_state))
found = False
iter = 1
while work and not found:
    work = sorted(work, key=get_total_cost, reverse=True)
    state = work.pop()
    if state not in visited:
        visited.append(state)
    print(f'Iter {iter:07}: Work {len(work):07} state: {state} costs {costs[state][0]:06}, {costs[state][1]:06}')

    # Get next valid states
    homes = is_home(state)
    for i in range(NUM_POS):
        if state[i] != ' ' and not homes[i]:
            next_states = get_moves_for(state[i], i, state)
            for next_state, next_cost in next_states:
                new_cost = costs[state][0] + next_cost
                if next_state not in visited:
                    if next_state not in work:
                        work.append(next_state)
                    if next_state not in costs:
                        costs[next_state] = (sys.maxsize, 0)
                    if new_cost < costs[next_state][0]:
                        predecessors[next_state] = state
                    costs[next_state] = (new_cost, get_est_cost(next_state))
                    if next_state == FINAL_STATE:
                        found = True
                        break
        if found:
            break
    iter += 1

print(f'Part 1: {costs[FINAL_STATE][0]}')
state = FINAL_STATE
while state:
    print(f'State {state}')
    state = predecessors[state]
