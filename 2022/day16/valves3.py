from aoc.search import djikstra

filename = '2022/day16/test1.txt'
# filename = '2022/day16/input.txt'

# graph[node] = [rate, [neighbors]]
graph = {}
flow_nodes = []
sum_rates = 0
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
        if rate > 0:
            flow_nodes.append(name)
        sum_rates += rate
        line = f.readline()
flow_nodes.append('AA')

# Compact the graph by converting nodes with zero flow into
# segments along a path

network = {}
for flow_node in flow_nodes:
    rate, neighbors = graph[flow_node]
    work_nodes = []
    work_paths = {flow_node: flow_node}
    for neighbor in neighbors:
        work_nodes.append(neighbor)
        work_paths[neighbor] = [neighbor]
    while work_nodes:
        node = work_nodes.pop()
        node_path = work_paths[node]
        node_rate, node_neighbors = graph[node]
        if node_rate == 0:
            for node_neighbor in node_neighbors:
                node_neighbor_path = node_path + [node_neighbor]
                if node_neighbor in work_paths:
                    curr_node_neighbor_path = work_paths[node_neighbor]
                    if len(node_neighbor_path) < len(curr_node_neighbor_path):
                        # This path to the neighbor is shorter
                        work_paths[node_neighbor] = node_neighbor_path
                elif node_neighbor not in work_nodes:
                    # This neighbor has never been queued
                    work_nodes.append(node_neighbor)
                    work_paths[node_neighbor] = node_neighbor_path
    paths = []
    for node, path in work_paths.items():
        if node != flow_node and node != 'AA' and node in flow_nodes:
            paths.append(path)
    network[flow_node] = (rate, paths)

for node in sorted(network):
    rate, paths = network[node]
    line = f'Network node {node} has rate {rate} and connects to:'
    for path in paths:
        line += f' {path[-1]}(d:{len(path)})'
    print(line)

def get_neighbors(node, depth):
    """return [((name, counter), dist)]

    dist: (sum_rate - active_rate) * len(path_to_neighbor)
    """
    neighbors = []
    name, counter, path, active_rate, open_valves = node
    if counter <= 1:
        # Cannot proceed any further
        return neighbors

    rate, links = network[name]
    if name != 'AA' and name not in open_valves:
        # Add a step to open this valve
        next_counter = counter - 1
        next_path = tuple(list(path) + [name])
        next_active_rate = active_rate + rate
        next_open_valves = tuple(list(open_valves) + [name])
        next_node = (name, next_counter, next_path, next_active_rate, next_open_valves)
        dist = sum_rates - active_rate
        neighbor = (next_node, dist)
        neighbors.append(neighbor)

    # Add neighbors
    for link in links:
        next_name = link[-1]
        steps = len(link)
        next_counter = counter - steps
        if next_counter >= 1:
            next_path = tuple(list(path) + link)
            dist = (sum_rates - active_rate) * steps
            next_node = (next_name, next_counter, next_path, active_rate, open_valves)
            neighbor = (next_node, dist)
            neighbors.append(neighbor)
    return neighbors

start = ('AA', 30, tuple(['AA']), 0, tuple())
min_dist, min_path = djikstra(start, get_neighbors)

# Node = (name, counter, path, cum_dist, cum_flow, flow_rate, open_valves)
# start = ('AA', ['AA'], 30, 0, 0, 0, ['AA'])
# work = []
# work_dists = {}
# max_total_flow = 0
# max_path = []
# work.append(start)
# while work:
#     name, counter, cum_dist, path, cum_flow, flow_rate, open_valves = work.pop(0)
#     print(f'Visiting {name} at {counter} with cum dist {cum_dist} and cum flow {cum_flow}'
#         f' flow rate {flow_rate} and open valves {open_valves} via path {path}')
#     if counter == 1:
#         total_flow = cum_flow + flow_rate
#         if total_flow > max_total_flow:
#             print(f'New max total flow {total_flow} with path {path}')
#             max_total_flow = total_flow
#             max_path = path
#     else:
#         rate, links = network[name]
#         for link in links:
#             dest = link[-1]
#             new_counter = counter - len(link)
#             new_node = (dest, new_counter, )
