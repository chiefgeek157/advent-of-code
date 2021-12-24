import colorama
from colorama import Back, Cursor, Fore, Style
import networkx as nx
from typing import Dict, List, Tuple
import sys

filename = 'test1.txt'
#filename = 'test2.txt'
#filename = 'test3.txt'
#filename = 'input.txt'

colorama.init()

def print_grid(nodes, width:int, height:int, path:List[Tuple],
        work:List[Tuple]=None, current:Tuple=None):
    print(f'{Cursor.POS(0, 0)}{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}GRID:{Style.RESET_ALL}')
    for y in range(height):
        for x in range(width):
            pos = (x, y)
            if current is not None and current == pos:
                print(f'{Fore.RED}{Style.BRIGHT}', end='')
            elif pos in path:
                print(f'{Fore.YELLOW}{Style.BRIGHT}', end='')
            elif work is not None and pos in work:
                print(f'{Fore.BLUE}{Style.BRIGHT}', end='')
            else:
                print(f'{Fore.WHITE}{Style.DIM}', end='')
            print(f'{nodes[pos]["risk"]}{Style.RESET_ALL}', end='')
        print()

def clear_screen():
    print(f'\033[2J', end='')

def pause(line:int=None):
    if line is not None:
        print(f'{Cursor.POS(0, line)}', end='')
    print(f'{Fore.RED}', end='')
    input('Press enter to continue...')
    print(f'{Style.RESET_ALL}')

def print_sum(line:int, sum:int):
    print(f'{Cursor.POS(0, line)}{Fore.CYAN}SUM: {sum}{Style.RESET_ALL}')

def print_work(line:int, work:List[Tuple]):
    print(f'{Cursor.POS(0, line)}{Fore.LIGHTGREEN_EX}WORK:')
    count = 0
    for pos in work:
        print(f'[{pos[0]:2},{pos[1]:2}] ', end='')
        count += 1
        if count > 10:
            print()
            count = 0
    print(f'{Style.RESET_ALL}')

# Graph nodes are position tuples (x,y)
# The graph holds additional attributes for the nodes
width = 0
height = 0
graph = nx.Graph()
with open(filename, 'r') as f:
    line = f.readline()
    y = 0
    while line:
        line = line.strip()
        width = len(line)
        x = 0
        for x in range(len(line)):
            # Add a node the the graph at (x,y) with initial values
            graph.add_node((x, y), risk=int(line[x]), visited=False, score=0)
        line = f.readline()
        y += 1
        height += 1
height -= 1

# Add edges to the graph
for x in range(width):
    for y in range(height):
        if x > 0:
            graph.add_edge((x, y), (x-1, y))
        if x < width - 1:
            graph.add_edge((x, y), (x+1, y))
        if y > 0:
            graph.add_edge((x, y), (x, y-1))
        if y < height - 1:
            graph.add_edge((x, y), (x, y+1))

# For convenience
nodes = graph.nodes

# Display lines for printing
grid_line = 0
sum_line = height + 2
input_line = sum_line + 1
work_line = input_line + 1

# Initialize the search
start = (0,0)
end = (width - 1, height - 1)
path = []
path_sum = 0

clear_screen()

# Add start to the working list
work = [start]
print_grid(nodes, width, height, path)

# Continue until the work list is empty, or we reach
# the end position
while work:
    print_work(work_line, work)

    # Find the node in work with the lowest score
    curr = None
    for pos in work:
        if curr is None or nodes[pos]['score'] < nodes[curr]['score']:
            curr = pos
    work.remove(curr)

    curr_risk = nodes[curr]['risk'] if curr != start else 0

    # Add the position to the path and increment the total sum
    path.append(curr)
    path_sum += curr_risk
    print_grid(nodes, width, height, path)
    print_sum(sum_line, path_sum)

    # If we are at the end, we are done
    if curr == end:
        break
 
    # Get list of unvisited neighbor positions:
    #  - mark as visited
    #  - update the score as the path score + the risk score
    #  - add to the work list
    unvisited = [n for n in graph.neighbors(curr) if not nodes[n]['visited']]
    for pos in unvisited:
        neighbor = nodes[pos]
        # Mark adjacent nodes as visited
        neighbor['visited'] = True
        # Update score of adjacent nodes
        neighbor['score'] = neighbor['risk'] + curr_risk
        # Add the neighbor to the work list
        work.append(neighbor)

    pause(input_line)

pause(input_line)
