import copy as cp

filename = '2021/day23/test1.txt'
# filename = '2021/day23/test2.txt'
# filename = '2021/day22/input.txt'

# Board positions
#
# 00 01 .. 02 .. 03 .. 04 .. 05 06
#       07    08    09    10
#       11    12    13    14

POSITIONS = range(0,14)

# Home positions by piece type
HOME_POS = [[7, 11], [8, 12], [9, 13], [10, 14]]

# Distance to the first possible home for each piece type from each position
HOME_DISTS = [
    #0  1  2  3  4  5  6  7  8  9  0  1  2  3  4
    [3, 2, 2, 4, 6, 8, 9, 0, 4, 6, 8, 0, 5, 7, 9],
    [5, 4, 2, 2, 4, 6, 7, 4, 0, 4, 6, 5, 0, 5, 7],
    [7, 6, 4, 2, 2, 4, 5, 6, 4, 0, 4, 7, 5, 0, 5],
    [9, 8, 6, 4, 2, 2, 3, 8, 6, 4, 0, 9, 7, 5, 0]
]

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

# The
PATHS = {
    ( 0,  7): ([ 1,  7], 3),
    ( 0, 11): ([ 1,  7, 11], 4),
    ( 0,  8): ([ 1,  2,  8], 5),
    ( 0, 12): ([ 1,  2,  8, 12], 6),
    ( 0,  7): ([ 1,  7], 3),
    ( 0, 11): ([ 1,  7, 11], 4),
    ( 0,  7): ([ 1,  7], 3),
    ( 0, 11): ([ 1,  7, 11], 4),
}


initial_state = [' '] * 19
with open(filename, 'r') as f:
    # Discard first line
    f.readline()

    pos = 0
    line = f.readline()
    while line:
        print(f'Initial state: {initial_state}')
        for c in line.strip():
            print(f'Read char {c} as pos {pos}')
            if c != '#':
                if c != '.':
                    initial_state[pos] = c
                    print(f'Set pos {pos} to {c}')
                pos += 1
        line = f.readline()
initial_state = [v for i,v in enumerate(initial_state) if i not in frozenset((2, 4 , 6, 8))]
print(f'Initial state: {initial_state}')


# The array of potential next states
work = []

# The array of visited state4s
visited = []

work.append(initial_state)
solution = None
while work:
    print(f'Work size {len(work)} Visited {len(visited)}')
    work = sorted(work, key=lambda s: s.total_cost(), reverse=True)
    # for state in work:
    #     print(f'state cost {state.cost} total cost {state.total_cost()} hash {hash(state)} chain {state.cost_chain()}')
    state = work.pop()
    visited.append(state)

#     print(f'Working state: cost {state.cost} total cost {state.total_cost()} hash {hash(state)}')
#     print(f'{state}')
#     if state.is_final():
#         print('Found solution')
#         solution = state
#         break

#     next_states = board.find_next_states(state)
#     for next_state, incr_cost in next_states:
#         # print(f'{next_state}\nincr_cost {incr_cost} hash {hash(next_state)}')
#         next_state.update(incr_cost, state)
#         if next_state in visited:
#             skip_in_visited += 1
#         elif next_state in work:
#             skip_in_work += 1
#         else:
#             work.append(next_state)
#     print(f'Skipping visited {skip_in_visited} in work {skip_in_work}')

#     # input("enter...")

# if solution is not None: print(f'{solution}')
# else: print('No solution found')