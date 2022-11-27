"""A function to compute the Traveling Salesman Problem solution."""

from itertools import permutations

def traveling_salesman(dists: list[list[float]], start: int=None,
        home: bool=False, maxdist: bool=False) -> tuple:
    """Compute the extreme route touching every stop.

    dists: a square array with the distance between every pair of nodes
    start: the starting node, default is 0
    home: True if the salesman should return home at the end, default is False
    maxdist: True is maximum distance is desired, default is False

    Returns the tuple (min distance: float, min route: list[float])
    """

    nodes = list(range(len(dists)))
    print(f'Nodes: {nodes}')
    if start is not None:
        print(f'Removing start node: {start}')
        nodes.remove(start)

    save_dist = None
    save_route = None
    for route in permutations(nodes):
        # print(f'Route: {route}')
        dist = 0
        if start is not None:
            route = start + route

        node = None
        for next_node in route:
            if node is not None:
                dist += dists[node][next_node]
            node = next_node
        if home:
            dist += [node][start]

        if (save_dist is None or (maxdist and dist > save_dist) or
                (not maxdist and dist < save_dist)):
            save_dist = dist
            save_route = route
            print(f'New save_dist {save_dist} for route {route}')

    save_route = list(save_route)

    return (save_dist, save_route)