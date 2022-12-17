"""An implementation of search algorithms.
"""
import heapq as hq
import math
from typing import Callable, Hashable

# Type aliases for clarity
Node = Hashable
SearchResult = tuple[int, list[Node]]
NeighborFunc = Callable[[Node, int], list[tuple[Node, int|float]]]
HeuristicFunc = Callable[[Node, int], int|float]

def djikstra(start: Node, f_neighbors: NeighborFunc) -> SearchResult:
    """Return the min score and min path from start node to final node.

    The score function, f, for a given node, x, is given by:

        f(x) = g(x) + h(x)

    where f is the score of node x, g is the cumulatrive score for the path
    leading from start to x, and h is a heuristic estimate of the distance
    from x to final.

    start: the starting node, not eveluated except it must be hashable.
    final: the final node to seek, not eveluated except it must be hashable.
    f_neighbors: a function that will return a list of all neighbors of the
        given state as a tuple (node, d). d is any non-negative value
        reflecting the distance from node to the neighbor.
    f_heuristic: the h function that will compute the heuristic value for
        the given node, which must be a non-negative value. Note that this
        function does not cache the heuristic values locally.
    """
    # A cache of scores for each node so they can be found and compared
    # when a node is visited


    # priority_queue is the working set of nodes to explore
    #   entries in the prioirity queue are lists [score, depth, node]
    #   where score is used by the queue to sort the heap.
    #   priority_queue[0] is always the prioirity (min_heap)
    #   Nodes can be replaced by setting the node to None
    #   and adding the repolacement to the queue
    #
    # queued_entries is a dict of entries keyed by node so that we can
    #     find entries in the queue by value
    #
    # scores is a cache of scores by node
    #
    # predecessors is the link from a node to its predecessor
    #     predecessor[node] = prior_node
    #
    priority_queue = []
    queued_entries = {}
    scores = {}
    predecessors = {}

    # visited_nodes is the set of nodes already visited that should not be
    #   added to the priority queue again
    # removed_entries are queue entries which were replaced in the priority
    #   queue so should be ignored (score, depth, node)

    entry = [0, 0, start]
    hq.heappush(priority_queue, entry)
    queued_entries[start] = entry
    predecessors[start] = None
    scores[start] = 0

    min_score = math.inf
    final = None
    while priority_queue:

        print(f'Prirotiy queue length {len(priority_queue)}')

        # The min heap always return the lowest item in the queue
        # If node is None, it means this node was replaced in the priority
        # queue, so just skip this one
        score, depth, node = hq.heappop(priority_queue)
        if node is not None:
            queued_entries.pop(node)
            print(f'Visiting node {node} with score {scores[node]}')

            if score < min_score:
                # This is the best candidate found so far
                print(f'  - New best score {score} at node {node}')
                min_score = score
                final = node

            neighbors = f_neighbors(node, depth)
            for next_node, dist in neighbors:

                # Compute the trial score for f(y) = f(x) + d(x, y)
                next_score = scores[node] + dist
                next_depth = depth + 1

                # Initialize the cached score to infinity if needed
                if next_node not in scores:
                    scores[next_node] = math.inf
                if next_score < scores[next_node]:

                    # This is a better (or perhaps first) score for next_node
                    print(f'  - Setting score of node {next_node} to '
                        f'{next_score} and predecessor {node}')
                    scores[next_node] = next_score

                    # Set predecessor to node
                    predecessors[next_node] = node

                    next_entry = [next_score, next_depth, next_node]
                    add_entry = False
                    if next_node not in queued_entries:
                        add_entry = True
                    else:
                        # This node is already queued, so check if the
                        # queued item should be replaced
                        queued_entry = queued_entries[next_node]
                        if next_score < queued_entry[1]:
                            # This is a better score for this node
                            # Mark the queued entry as removed and add
                            # the new item
                            print(f'  - Replacing entry for node {next_node} '
                                f'from {queued_entry[1]} to {next_score}')
                            queued_entry[2] = None
                            add_entry = True
                    if add_entry:
                        print(f'  - Adding node {next_node} to queue with '
                            f'score {next_score} and depth {next_depth}')
                        hq.heappush(priority_queue, next_entry)
                        queued_entries[next_node] = next_entry

    print(f'Priority queue empty, building min path')
    # Reconstruct the path from start to final
    min_path = []
    min_path.append(final)
    next = predecessors[final]
    while next:
        min_path.append(next)
        next = predecessors[next]
    min_path = min_path[::-1]

    return (min_score, min_path)

def a_star(start: Node, final: Node, f_neighbors: NeighborFunc,
        f_heuristic: HeuristicFunc) -> SearchResult:
    """Return the min score and min path from start node to final node.

    The score function, f, for a given node, x, is given by:

        f(x) = g(x) + h(x)

    where f is the score of node x, g is the cumulatrive score for the path
    leading from start to x, and h is a heuristic estimate of the distance
    from x to final.

    start: the starting node, not eveluated except it must be hashable.
    final: the final node to seek, not eveluated except it must be hashable.
    f_neighbors: a function that will return a list of all neighbors of the
        given state as a tuple (node, d). d is any non-negative value
        reflecting the distance from node to the neighbor.
    f_heuristic: the h function that will compute the heuristic value for
        the given node, which must be a non-negative value. Note that this
        function does not cache the heuristic values locally.
    """
    # A cache of g_scores for each node so they can be found and compared
    # when a node is visited
    g_scores = {}
    g_score = 0
    g_scores[start] = g_score

    h_score = f_heuristic(start)
    f_score = g_score + h_score

    # priority_queue is the working set of nodes to explore
    # priority_queue[0] is always the prioirity (min_heap)
    # Items on the heap are tuples (f_score, node)
    priority_queue = []
    hq.heappush(priority_queue, (f_score, start))

    # We keep a second set to ascertain if a node is already in the priority
    # queue
    queued_nodes = set()
    queued_nodes.add(start)

    # The dict of predecessors of each node
    predecessors = {}
    predecessors[start] = None

    min_score = None
    while priority_queue:

        # The min heap always return the lowest item in the queue
        f_score, node = hq.heappop(priority_queue)
        queued_nodes.remove(node)

        if node == final:
            # Found the solution
            min_score = f_score
            break

        neighbors = f_neighbors(node)
        for next_node, dist in neighbors:

            # Compute the trial score for g(y) = g(x) + d(x, y)
            next_g_score = g_scores[node] + dist

            # Initialize the cached g_score to infinity if needed
            if next_node not in g_scores:
                g_scores[next_node] = math.inf

            if next_g_score < g_scores[next_node]:

                # This is a better (or perhaps first) path to next_node
                g_scores[next_node] = next_g_score

                # Compute f_score
                next_h_score = f_heuristic(next_node)
                next_f_score = next_g_score + next_h_score

                # Set predecessor to node
                predecessors[next_node] = node

                # Make sure we do not queue twice at the same time
                # Potentially queued again later
                if next_node not in queued_nodes:
                    hq.heappush(priority_queue, (next_f_score, next_node))
                    queued_nodes.add(next_node)

    # Failed to find the final node before we ran out of nodes to visit
    if min_score is None:
        return (None, None)

    # Reconstruct the path from start to final
    min_path = []
    min_path.append(final)
    next = predecessors[final]
    while next:
        min_path.append(next)
        next = predecessors[next]
    min_path = min_path[::-1]

    return (min_score, min_path)

def djikstra_max(start: Node, f_neighbors: NeighborFunc) -> SearchResult:
    """Return the min score and min path from start node to final node.

    The score function, f, for a given node, x, is given by:

        f(x) = g(x) + h(x)

    where f is the score of node x, g is the cumulatrive score for the path
    leading from start to x, and h is a heuristic estimate of the distance
    from x to final.

    start: the starting node, not eveluated except it must be hashable.
    final: the final node to seek, not eveluated except it must be hashable.
    f_neighbors: a function that will return a list of all neighbors of the
        given state as a tuple (node, d). d is any non-negative value
        reflecting the distance from node to the neighbor.
    f_heuristic: the h function that will compute the heuristic value for
        the given node, which must be a non-negative value. Note that this
        function does not cache the heuristic values locally.
    """
    max_score = int(1000000000)

    # priority_queue is the working set of nodes to explore
    #   entries in the prioirity queue are lists [score, depth, node]
    #   where score is used by the queue to sort the heap.
    #   priority_queue[0] is always the prioirity (min_heap)
    #   Nodes can be replaced by setting the node to None
    #   and adding the repolacement to the queue
    #
    # queued_entries is a dict of entries keyed by node so that we can
    #     find entries in the queue by value
    #
    # scores is a cache of scores by node
    #
    # predecessors is the link from a node to its predecessor
    #     predecessor[node] = prior_node
    #
    priority_queue = []
    queued_entries = {}
    scores = {}
    predecessors = {}

    # visited_nodes is the set of nodes already visited that should not be
    #   added to the priority queue again
    # removed_entries are queue entries which were replaced in the priority
    #   queue so should be ignored (score, depth, node)

    entry = [max_score, 0, start]
    hq.heappush(priority_queue, entry)
    queued_entries[start] = entry
    predecessors[start] = None
    scores[start] = max_score

    best_score = max_score
    final = None
    while priority_queue:

        print(f'Prirotiy queue length {len(priority_queue)}')

        # The min heap always return the lowest item in the queue
        # If node is None, it means this node was replaced in the priority
        # queue, so just skip this one
        score, depth, node = hq.heappop(priority_queue)
        if node is not None:
            queued_entries.pop(node)
            print(f'Visiting node {node} with score {max_score - scores[node]}')

            if score < best_score:
                # This is the best candidate found so far
                print(f'  - New best score {max_score - score} at node {node}')
                best_score = score
                final = node

            neighbors = f_neighbors(node, depth)
            for next_node, dist in neighbors:

                # Compute the trial score for f(y) = f(x) + d(x, y)
                next_score = scores[node] + dist
                next_depth = depth + 1

                # Initialize the cached score to infinity if needed
                if next_node not in scores:
                    scores[next_node] = math.inf
                if next_score < scores[next_node]:

                    # This is a better (or perhaps first) score for next_node
                    print(f'  - Setting score of node {next_node} to '
                        f'{max_score - next_score} and predecessor {node}')
                    scores[next_node] = max_score - next_score

                    # Set predecessor to node
                    predecessors[next_node] = node

                    next_entry = [next_score, next_depth, next_node]
                    add_entry = False
                    if next_node not in queued_entries:
                        add_entry = True
                    else:
                        # This node is already queued, so check if the
                        # queued item should be replaced
                        queued_entry = queued_entries[next_node]
                        if next_score < queued_entry[1]:
                            # This is a better score for this node
                            # Mark the queued entry as removed and add
                            # the new item
                            print(f'  - Replacing entry for node {next_node} '
                                f'from {max_score - queued_entry[1]} to '
                                f'{max_score - next_score}')
                            queued_entry[2] = None
                            add_entry = True
                    if add_entry:
                        print(f'  - Adding node {next_node} to queue with '
                            f'score {max_score - next_score} and depth {next_depth}')
                        hq.heappush(priority_queue, next_entry)
                        queued_entries[next_node] = next_entry

    print(f'Priority queue empty, building min path')
    # Reconstruct the path from start to final
    best_path = []
    best_path.append(final)
    next = predecessors[final]
    while next:
        best_path.append(next)
        next = predecessors[next]
    best_path = best_path[::-1]

    return (best_score, best_path)
