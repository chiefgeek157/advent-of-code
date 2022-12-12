from modules.a_star import a_star

start = '...........BACDABCDABCDABCD'
final = '...........ABCDABCDABCDABCD'

move_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
home_cols = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

def print_board(node):
    print("\n#############")
    print(f'#{node[:11]}#')
    for i in range(int((len(node) - 11) / 4)):
        line = '  '
        for j in range(4):
            line += f'#{node[11 + 4 * i + j]}'
        line += '#'
        print(line)
    print('  #########')

def heuristic(node):
    global home_cols, move_costs
    score = 0
    for i in range(len(node)):
        if node[i] != '.':
            if i <= 10:
                # Hallway nodes
                score += (abs(home_cols[node[i]] * 2 + 2 - i) + 1) * move_costs[node[i]]
            else:
                # Home nodes
                row = int((i - 11) / 4)
                col = (i - 11) % 4
                if col != home_cols[node[i]]:
                    score += (abs(home_cols[node[i]] - col) * 2 + row + 2) * move_costs[node[i]]
    return score

def move_piece(node, pos, new_pos):
    node_list = list(node)
    node_list[new_pos] = node[pos]
    node_list[pos] = '.'
    return ''.join(node_list)

def check_path(node, col_start, hall_end, homes=False):
    """Check a path from a pos in a column to a pos in the
    hall.

    If homes is True, do not count positions with the correct
    home piece already present, which is used when moving from the
    hall into the home.
    """
    clear = True
    steps = 0

    # Check path to top of column
    steps = 0
    j = col_start - 4
    while j > 10:
        if node[j] != '.':
            if homes and node[j] != node[hall_end]:
            clear = False
            break
        j -= 4
        steps += 1
    j = j - 2 - (10 - j)
    if clear:
        # Check path from j (position in hall) to new_pos
        if new_pos < j:
            iter = reversed(range(new_pos, j + 1))
        else:
            iter = range(j, new_pos + 1)
        for k in iter:
            steps += 1
            if node[k] != '.':
                clear = False
                break
    return (clear, steps)

def get_nodes(node):
    """Return a list of tuples (node, dist)"""
    nodes = []
    for pos in range(len(node)):
        if node[pos] != '.':
            if pos < 11:
                # In the hallway, can only move to the bottom of the
                # assigned column above only other homed items and only
                # if the path is clear
                clear = True
                hall_pos = 2 + 2 * home_cols[node[pos]]
                if pos < hall_pos:
                    iter = reversed(range(pos, hall_pos + 1))
                else:
                    iter = range(j, new_pos + 1)
                for k in iter:
                    steps += 1
                    if node[k] != '.':
                        clear = False
                        break
            else:
                # In a column, can only move into the hallway to one
                # of the available spots if the path above is clear
                clear = True
                for new_pos in [0, 1, 3, 5, 7, 9, 10]:
                    # Check path to top of column
                    steps = 0
                    j = pos - 4
                    while j > 10:
                        if node[j] != '.':
                            clear = False
                            break
                        j -= 4
                        steps += 1
                    j = j - 2 - (10 - j)
                    if clear:
                        # Check path from j (position in hall) to new_pos
                        if new_pos < j:
                            iter = reversed(range(new_pos, j + 1))
                        else:
                            iter = range(j, new_pos + 1)
                        for k in iter:
                            steps += 1
                            if node[k] != '.':
                                clear = False
                                break
                    if clear:
                        new_node = move_piece(node, pos, new_pos)
                        dist = steps * move_costs[node[pos]]
                        nodes.append((new_node, dist))
    return nodes

# print_board(start)
# print_board(final)
# print(f'heuristic({final}): {heuristic(final)}')
# print(f'heuristic({start}): {heuristic(start)}')
# node = '...........DDDDCCCCBBBBAAAA'
# print(f'heuristic({node}): {heuristic(node)}')
# node = '...........DCBADCBADCBADCBA'
# print(f'heuristic({node}): {heuristic(node)}')
# node = 'DC.......BCC...C..ADAABDDAB'
# print_board(node)
# print(f'heuristic({node}): {heuristic(node)}')

print(f'get_nodes({start}): {get_nodes(start)}')

# min_score, min_path = a_star(start, final, neighbors, heuristic)
# print(f'Part 2: {min_score}')