filename = '2021/day23/test1.txt'
# filename = '2021/day22/input.txt'

# Board positions
#
# 00 01 02 03 04 05 06 07 08 09 10
#       11    12    13    14
#       15    16    17    18

# Pieces
piece_names = ['..', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D1', 'D2']

# Distance to the first possible home for each piece from each position
home_dists = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 4, 6, 8, 0, 5, 7, 9],
    [3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 4, 6, 8, 0, 5, 7, 9],
    [5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 4, 0, 4, 6, 5, 0, 5, 7],
    [5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 4, 0, 4, 6, 5, 0, 5, 7],
    [7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 4, 0, 4, 7, 5, 0, 5],
    [7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 4, 0, 4, 7, 5, 0, 5],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 8, 6, 4, 0, 9, 7, 5, 0],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 8, 6, 4, 0, 9, 7, 5, 0]
]

# Move costs
move_costs = [0, 1, 1, 10, 10, 100, 100, 1000, 1000]

# No stops
no_step_poss = [2, 4, 6, 8]

# Adjacencies
pos_adjs = [
    [1],
    [0, 2],
    [1, 3, 11],
    [2, 4],
    [3, 5, 12],
    [4, 6],
    [5, 7, 13],
    [6, 8],
    [7, 9, 14],
    [8, 10],
    [9],
    [2, 15],
    [4, 16],
    [6, 17],
    [8, 18],
    [11],
    [12],
    [13],
    [17]
]

def read_line(line, pos, piece_pos, state):
    for c in line.strip():
        if c != '#':
            if c == '.':
                state[pos] = 0
            else:
                match c:
                    case 'A':
                        if not piece_pos[0]:
                            state[pos] = 1
                            piece_pos[0] = True
                        else:
                            state[pos] = 2
                    case 'B':
                        if not piece_pos[1]:
                            state[pos] = 3
                            piece_pos[1] = True
                        else:
                            state[pos] = 4
                    case 'C':
                        if not piece_pos[2]:
                            state[pos] = 5
                            piece_pos[2] = True
                        else:
                            state[pos] = 6
                    case 'D':
                        if not piece_pos[3]:
                            state[pos] = 7
                            piece_pos[3] = True
                        else:
                            state[pos] = 8
                    case _:
                        raise ValueError(f'Unexpected char {c}')
            pos += 1
    return pos

def print_board(state):
    for i in range(11):
        print(f'{piece_names[state[i]]} ', end='')
    print('\n      ', end='')
    for i in range(11, 15):
        print(f'{piece_names[state[i]]}    ', end='')
    print('\n      ', end='')
    for i in range(15, 19):
        print(f'{piece_names[state[i]]}    ', end='')
    print()

def state_str(state):
    s = ''
    for i in state: s += str(i)
    return s

def is_final_state(state):
    return state[11] in [1, 2] and state[15] in [1, 2] and \
        state[13] in [3, 4] and state[16] in [3, 4] and \
        state[14] in [5, 6] and state[17] in [5, 6] and \
        state[15] in [7, 8] and state[18] in [7, 8]

def dist_to_goal(state):
    d = 0
    for pos in range(19):
        d += home_dists[state[pos]][pos]

def find_next_states(state):
    next_states = []

    return next_states

# A state is an array of numbers.
# -1 means empty, other values are the piece number
states = {}
work = []

with open(filename, 'r') as f:
    # Discard first line
    f.readline()

    state = [0] * 19
    piece_pos = [False] * 4
    pos = 0
    pos = read_line(f.readline().strip(), pos, piece_pos, state)
    pos = read_line(f.readline().strip(), pos, piece_pos, state)
    pos = read_line(f.readline().strip(), pos, piece_pos, state)
    print_board(state)
    states[state_str(state)] = 0
    work.append(state)

solution = None
while work:
    work = sorted(work, key=lambda s: states[state_str(s)], reverse=True)
    state = work.pop()
    if is_final_state(state):
        print('Found solution')
        solution = state
        break

    state_cost = states[state_str(state)]
    next_states = find_next_states(state)
    for next_state, next_cost in next_states:
        if state_str(next_state) not in states:
            states[state_str(next_state)] = state_cost + next_cost + dist_to_goal(next_state)
            work.append(next_state)

if solution is not None: print_board(solution)
else: print('No solution found')