from aoc.search import a_star

# filename = '2022/day16/test1.txt'
filename = '2022/day16/input.txt'

# graph[node] = [rate, [neighbors]]
graph = {}
with open(filename, 'r') as f:
    # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    line = f.readline()
    while line:
        fields = line.split()
        name = fields[1]
        rate = int(fields[4][:-1].split('=')[1])
        neighbors = []
        for i in range(9, len(fields)):
            neighbors.append(fields[i].split(',')[0])
        graph[name] = (rate, neighbors)
        line = f.readline()

max_flow = 0
for name, values in graph.items():
    max_flow += values[0]
    print(f'Node {name} has rate {values[0]:2} and links to {values[1]}')

def is_final(node):
    name, counter, open, open_valves, open_rate = node
    return (open_rate == max_flow)

def heuristic(node):
    name, counter, open, open_valves, open_rate = node
    return (max_flow - open_rate)

def get_neighbors(node):
    # print(f'Visiting node {node}')
    # Results are (node, dist)
    # Node is (name, counter, open, open_valves, open_rate)
    # Dist is max_flow - (sum(open_values) * counter)
    name, counter, open, open_valves, open_rate = node
    results = []
    if counter == 0:
        return results
    next_counter = counter - 1
    rate = graph[name][0]
    neighbors = graph[name][1]
    next_open_valves = open_valves
    next_open_rate = open_rate
    # Dist is the lost opportunity. As we get closer to the target
    # the distance becomes less
    dist = max_flow - open_rate
    if open:
        # We need to open the valve
        next_open_valves = tuple(list(next_open_valves) + [name])
        next_open_rate += rate
        dist -= rate
    else:
        # We moved to this node, see if it can be opened in the next turn
        if name not in open_valves and rate > 0:
            # This valve can be opened as a next action
            next_node = (name, next_counter, True, tuple(next_open_valves), next_open_rate)
            result = (next_node, dist)
            results.append(result)

    # Now add neighbors
    for next_name in neighbors:
        next_node = (next_name, next_counter, False, tuple(next_open_valves), next_open_rate)
        result = (next_node, dist)
        results.append(result)

    return results

# A node is (name, timer, open, open_valves, open_rate)
start = ('AA', 30, False, tuple(['AA']), 0)
min_score, min_path = a_star(start, is_final, get_neighbors, heuristic)

print(f'Min score {min_score}')
cum_flow = 0
for node in min_path:
    name, counter, open, open_valves, open_rate = node
    if open:
        print(f'At time {counter} open valve {name}')
    else:
        print(f'At time {counter} move to {name}')
    print(f'  - Flow now {open_rate} with open valves {open_valves}')
    cum_flow += open_rate
print(f'Counter left {counter} with flow rate {open_rate}')
cum_flow += counter * open_rate
print(f'Total flow {cum_flow}')
# def pop_work(work):
#     """Sort and pop the last one (max) by rate

#     work entry contains (total, name, timer, [path])
#     """
#     work = sorted(work, key=lambda x: x[0])
#     return (work.pop(), work)

# min_score, min_path = djikstra('AA', get_neighbors)

# best_total = 0
# best_path = None

# max_open = len([x for x in graph.values() if x[0] > 0])

# # A queue of nodes to visit
# # [score, node, move, timer, total, [open], [path]]
# # move = True if this is a move, False if an open
# # Score = total + timer * rate (if not open)
# work = []
# work.append([0, 'AA', True, 30, 0, [], ['AA']])

# while work:

#     entry, work = pop_work(work)
#     score, node, move, timer, total, open, path = entry
#     print(f'Visiting {"move" if move else "open"} node {node}'
#         f' with score {score} timer {timer} total {total} open {open}'
#         f' and path {path}')

#     if total > best_total:
#         best_total = total
#         best_path = path
#         print(f'  - New best total {total} with path {path}')

#     if len(open) == max_open:
#         # If all valves are open, we know the total
#         print(f'  - All valves are open, nothing to do')
#         continue
#     else:
#         next_timer = timer - 1
#         if next_timer > 0:
#             for next_node in graph[node][1]:
#                 # Move to next_node
#                 next_rate = graph[next_node][0]
#                 next_total = total
#                 next_score = next_total
#                 next_open = open
#                 next_path = path + [node]
#                 print(f'  - Adding to work {next_node} with total '
#                     f'{next_total} timer {next_timer} and path {next_path}')
#                 entry = [next_score, next_node, True, next_timer, next_total,
#                     next_open, next_path]
#                 work.append(entry)

#                 if node not in open and rate > 0:
#                     # This node value is not yet open, so add an entry
#                     # to prioritize doing that next
#                     value = rate * (next_timer - 1)
#                     print(f'  - Opening valve {node} for a value of {value}')
#                     next_total = total + value
#                     next_score = next_total
#                     next_open = open + [node]
#                     next_path = path + [node]
#                     if next_timer > 0:
#                         print(f'  - Adding to work {node} with total '
#                             f'{next_total} timer {next_timer} open {next_open} '
#                             f'and path {next_path}')
#                         entry = [next_score, next_node, False, next_timer, next_total,
#                             next_open, next_path]
#                         work.append(entry)
#         else:
#             print(f'  - Ran out of time for path {path + [node]}')

# print(f'Best total {best_total} with path {best_path}')