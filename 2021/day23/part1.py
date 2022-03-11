from amphipod import Piece, Board, State
import copy as cp

# filename = '2021/day23/test1.txt'
filename = '2021/day23/test2.txt'
# filename = '2021/day22/input.txt'

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