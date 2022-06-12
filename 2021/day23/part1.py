from amphipod import Piece, Board, State
import copy as cp

filename = '2021/day23/test1.txt'
# filename = '2021/day23/test2.txt'
# filename = '2021/day22/input.txt'

board = Board()
initial_state = State.read(filename, board)

work = []
visited = []
skip_in_work = 0
skip_in_visited = 0

work.append(initial_state)
solution = None
while work:
    print(f'Work size {len(work)} Visited {len(visited)}')
    work = sorted(work, key=lambda s: s.total_cost(), reverse=True)
    # for state in work: print(f'state cost {state.cost} total cost {state.total_cost()} hash {hash(state)} chain {state.cost_chain()}')
    state = work.pop()
    visited.append(state)

    print(f'Working state: cost {state.cost} total cost {state.total_cost()} hash {hash(state)}')
    print(f'{state}')
    if state.is_final():
        print('Found solution')
        solution = state
        break

    next_states = board.find_next_states(state)
    for next_state, incr_cost in next_states:
        # print(f'{next_state}\nincr_cost {incr_cost} hash {hash(next_state)}')
        next_state.update(incr_cost, state)
        if next_state in visited:
            skip_in_visited += 1
        elif next_state in work:
            skip_in_work += 1
        else:
            work.append(next_state)
    print(f'Skipping visited {skip_in_visited} in work {skip_in_work}')

    # input("enter...")

if solution is not None: print(f'{solution}')
else: print('No solution found')