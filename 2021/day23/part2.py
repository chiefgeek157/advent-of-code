from modules.a_star import a_star

move_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000, 'a': 1, 'b': 10, 'c': 100, 'd': 1000}
home_cols = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'a':0, 'b': 1, 'c': 2, 'd': 3}

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

def classify(node):
    """Return a new node string with piece changed to lowercase
    if NOT in their home positions already."""
    num_rows = int((len(node) - 11) / 4)
    new_node = ''
    for pos in reversed(range(len(node))):
        c = node[pos]
        if pos < 11:
            # No pieces can be in their home posisitons if in the hallway
            new_node += c.lower()
        else:
            row = int((pos - 11) / 4) + 1
            col = (pos - 11) % 4
            if (c != '.' and col == home_cols[c]
                and (row == num_rows or new_node[len(node) - pos - 5].isupper())):
                new_node += c.upper()
            else:
                new_node += c.lower()
    return new_node[::-1]

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
    return classify(''.join(node_list))

def get_nodes(node):
    """Return a list of tuples (node, dist)"""
    nodes = []
    for pos in range(len(node)):
        piece = node[pos]
        if piece != '.':
            # See how we can move the piece at pos
            if pos < 11:
                # In the hallway, can only move to the bottom of the
                # assigned column above only other homed items and only
                # if the path is clear
                clear = True
                steps = 0
                top_pos = 2 + 2 * home_cols[piece]
                if pos < top_pos:
                    iter = range(pos + 1, top_pos + 1)
                else:
                    iter = reversed(range(top_pos, pos))
                for hall_pos in iter:
                    hall_piece = node[hall_pos]
                    steps += 1
                    if hall_piece != '.':
                        clear = False
                        break
                if clear:
                    # now move down the column
                    col_pos = 11 + home_cols[piece]
                    num_rows = int((len(node) - 11) / 4)
                    new_pos = None
                    for row in range(num_rows):
                        col_piece = node[col_pos]
                        if col_piece == '.':
                            # This is a candidate
                            new_pos = col_pos
                            steps += 1
                        elif col_piece == piece.upper():
                            # OK for next spot to be occupied by the same piece if row
                            # greater than zero
                            if row == 0:
                                clear = False
                                break
                            else:
                                # Next piece down is already home, so place in
                                # the row above
                                break
                        else:
                            # Found a piece that is not the same
                            clear = False
                            break
                        col_pos += 4
                    if clear:
                        new_node = move_piece(node, pos, new_pos)
                        dist = steps * move_costs[piece]
                        nodes.append((new_node, dist))
            elif piece.islower():
                # Only applicable for nodes NOT in the home position
                # In a column, can only move into the hallway to one
                # of the available spots if the path above is clear
                for new_pos in [0, 1, 3, 5, 7, 9, 10]:
                    clear = True
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

start = classify('...........BACDABCDABCDABCD')
start = classify('...........BACDABCDABCDABCD')
# print_board(start)
final = classify('...........ABCDABCDABCDABCD')
# print_board(final)

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

# node = classify('A.........B..CDABCDABCDABDC')
# print_board(node)
# neighbors = get_nodes(node)
# print(f'get_nodes({node})')
# for node, score in neighbors:
#     print_board(node)
#     print(f'Score: {score}')

min_score, min_path = a_star(start, final, get_nodes, heuristic)
print(f'Part 2: {min_score}')