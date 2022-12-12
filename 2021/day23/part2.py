from a_star import a_star

start = '...........BACDABCDABCDABCD'
FINAL = '...........ABCDABCDABCDABCD'

MOVE_COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
HOME_COLS = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

def neighbors(node):
    return []

def heuristic(node):
    score = 0
    for i in range(len(node)):
        if node[i] != '.':
            if i <= 10:
                # Hallway nodes
                score += (abs(HOME_COLS[node[i]] * 2 + 2 - i) + 1) * MOVE_COSTS[node[i]]
            else:
                # Home nodes
                row = int((i - 11) / 4)
                col = (i - 11) % 4
                if col != HOME_COLS[node[i]]:
                    score += (abs(HOME_COLS[node[i]] - col) * 2 + row + 2) * MOVE_COSTS[node[i]]
    return score

min_score, min_path = a_star(start, FINAL, neighbors, heuristic)
print(f'Part 2: {min_score}')