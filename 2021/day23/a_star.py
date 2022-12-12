"""An implementation of the A* search.
"""
import heapq as hq
import math
import sys

def a_star(start, final, f_neighbors, f_heuristic) -> tuple:
    """Return the min score and min path from start node to final node.

    The score function, f, for a given node, x, is given by:

        f(x) = g(x) + h(x)

    where f is the score of node x, g is the cumulatrive score for the path
    leading from start to x, and h is a heuristic estimate of the distance from x
    to final.

    start: the starting node, not eveluated except it must be hashable.
    final: the final node to seek, not eveluated except it must be hashable.
    f_neighbors: a function that will return a list of all neighbors of the given
        state as a tuple (node, d). d is any non-negative value
        reflecting the distance from node to the neighbor.
    f_heuristic: the h function that will compute the heuristic value for the given node,
        which must be a non-negative value. Note that this function does not cache
        the heuristic values unless cache_h is True. It is assumed the caller will
        cache them as needed.
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

    # We keep a second set to ascertain if a node is already in the priority queue
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
                    hq.heappush(priority_queue, (f_score, next_node))
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
    min_path = reversed(min_path)

    return (min_score, min_path)