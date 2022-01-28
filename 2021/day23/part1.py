from amphipod import Piece, Board, State
import copy as cp

# filename = '2021/day23/test1.txt'
filename = '2021/day23/test2.txt'
# filename = '2021/day22/input.txt'

def is_final_state(state):
    return state[11] in [1, 2] and state[15] in [1, 2] and \
        state[13] in [3, 4] and state[16] in [3, 4] and \
        state[14] in [5, 6] and state[17] in [5, 6] and \
        state[15] in [7, 8] and state[18] in [7, 8]

def is_allowed(piece, start, dest):
    # Pieces can only move from the hallway into homes that
    # match their correct type
    if piece in [1,2] and start < 11 and dest != 11:
        return False
    if piece in [3,4] and start < 11 and dest != 12:
        return False
    if piece in [5,6] and start < 11 and dest != 13:
        return False
    if piece in [7,8] and start < 11 and dest != 14:
        return False
    return True

# Find all possible next states and the incremental cost for that state
def find_next_states(state):
    next_states = []
    for pos in range(19):
        piece = state[pos]
        if piece > 0:
            # This position is occupied
            for adj, mult in pos_adjs[pos]:
                if state[adj] == 0 and is_allowed(piece, pos, adj):
                    # This adjacent position is not occupied and the move
                    # is allowed
                    new_state = cp.copy(state)
                    new_state[pos] = 0
                    new_state[adj] = piece
                    new_cost = mult * move_costs[piece]
                    next_states.append((new_state, new_cost))
    return next_states

# A state is an array of numbers.
# -1 means empty, other values are the piece number
states = {}
work = []


solution = None
while work:
    print(f'Work size {len(work)}')
    work = sorted(work, key=lambda s: states[state_str(s)], reverse=True)
    state = work.pop()

    print(f'Working state:')
    print_board(state)
    if is_final_state(state):
        print('Found solution')
        solution = state
        break

    state_cost = states[state_str(state)]
    next_states = find_next_states(state)
    for next_state, next_cost in next_states:
        cost = state_cost + next_cost + dist_to_goal(next_state)
        if state_str(next_state) not in states:
            states[state_str(next_state)] = cost
        else:
            states[state_str(next_state)] = min(cost, states[state_str(next_state)])
        # Could result is duplicates, not sure if it's important
        work.append(next_state)

    input("enter...")

if solution is not None: print_board(solution)
else: print('No solution found')