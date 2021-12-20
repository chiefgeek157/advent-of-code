import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
import sys

#filename = "test.txt"
filename = "input.txt"

# Return the map value at the given coords, or None if off the map
def get_map_value(map, x, y):
    if x < 0 or x > (len(map) - 1) or y < 0 or y > (len(map[x]) - 1):
        return None
    else:
        return map[x][y]

# Return true if the value at the giiven coord is less than all of its
# neighbors (horizontal and vertical)
def is_local_min(map, x, y):
    pc = get_map_value(map, x    , y    )
    pu = get_map_value(map, x    , y - 1)
    pd = get_map_value(map, x    , y + 1)
    pl = get_map_value(map, x - 1, y    )
    pr = get_map_value(map, x + 1, y    )
    # print(f"({x},{y}: {pc} {pu} {pd} {pl} {pr}")
    min_adj = pu if pu is not None else sys.maxsize
    min_adj = pd if pd is not None and pd < min_adj else min_adj
    min_adj = pl if pl is not None and pl < min_adj else min_adj
    min_adj = pr if pr is not None and pr < min_adj else min_adj
    return (pc < min_adj)

# Find all nodes in the basic starting at a given 
def find_basin(map, minimum, visited):
    print(f"\nFindng basin starting at {minimum}")
    if minimum in visited:
        print(f"Already visited {minimum}")
        return None
    basin = set()
    work = set()
    work.add(minimum)
    while len(work) > 0:
        print(f"Work {work}")
        node = work.pop()
        visit_node(node, map, basin, work, visited)
    return basin

def visit_node(node, map, basin, work, visited):
    print(f"Visiting {node}")
    basin.add(node)
    neighbors = get_neighbors(map, node)
    print(f"Neighbors {neighbors}")
    for neighbor in neighbors:
        if neighbor not in visited:
            # A value of 9 is a boundary
            if neighbor[2] < 9:
                work.add(neighbor)
    visited.add(node)

def get_neighbors(map, node):
    x = node[0]
    y = node[1]
    neighbors = set()
    if x > 0:
        neighbors.add((x - 1, y, map[x - 1][y]))
    if x < len(map) - 1:
        neighbors.add((x + 1, y, map[x + 1][y]))
    if y > 0:
        neighbors.add((x, y - 1, map[x][y - 1]))
    if y < len(map[0]) - 1:
        neighbors.add((x, y + 1, map[x][y + 1]))
    return neighbors

def print_map(map, minima, basins):
    for x in range(len(map)):
        for y in range(len(map[x])):
            node = (x, y, map[x][y])
            if node in minima:
                print(f"{Fore.RED}{Style.BRIGHT}", end="")
            elif node in basins:
                print(f"{Fore.BLUE}{Style.BRIGHT}", end="")
            else:
                print(f"{Fore.YELLOW}{Style.DIM}", end="")
            print(f"{map[x][y]}{Style.RESET_ALL}", end="")
        print()

colorama.init()

map = []
with open(filename, "r") as f:
    line = f.readline()
    while line:
        row = [int(c) for c in list(line.strip())]
        # print(f"row {row}")
        map.append(row)
        line = f.readline()

minima = set()
for x in range(len(map)):
    for y in range(len(map[x])):
        if is_local_min(map, x, y):
            # print(f"Found minimum at {x} {y}: {map[x][y]}")
            minima.add((x, y, map[x][y]))

print(f"Minima {minima}")
basins = []
visited = set()
for minimum in minima:
    basin = find_basin(map, minimum, visited)
    if basin is not None:
        basins.append(basin)

basins.sort(key = len, reverse = True)
product = 1
for i in range(3):
    print(f"Basin {i}: {basins[i]}")
    product *= len(basins[i])

all_basins = []
for basin in basins:
    all_basins += list(basin)
print(f"all_basins {all_basins}")

print_map(map, minima, all_basins)

print(f"Answer: {product}")
