import colorama
from colorama import Back, Cursor, Fore, Style
import networkx as nx
from typing import Dict, List, Tuple
import sys

#filename = 'test1.txt'
#filename = 'test2.txt'
#filename = 'test3.txt'
filename = 'input.txt'

colorama.init()

use_screen = False

def move_to(r:int, c:int):
    if use_screen and r is not None and c is not None:
        print(f'{Cursor.POS(c, r)}', end='')

def print_grid(nodes, width:int, height:int,
        work:List[Tuple]=None, current:Tuple=None, path:List[Tuple]=None):
    move_to(grid_line, 0)
    print(f'{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}GRID:{Style.RESET_ALL}')
    for y in range(height):
        for x in range(width):
            pos = (x, y)
            if current is not None and current == pos:
                print(f'{Fore.RED}{Style.BRIGHT}', end='')
            elif work is not None and pos in work:
                print(f'{Fore.BLUE}{Style.BRIGHT}', end='')
            elif path is not None and pos in path:
                print(f'{Fore.YELLOW}{Style.BRIGHT}', end='')
            else:
                print(f'{Fore.WHITE}{Style.DIM}', end='')
            score = f'{nodes[pos]["score"]:03}'
            if len(score) > 3:
                score = '###'
            print(f'{nodes[pos]["risk"]}-{score} {Style.RESET_ALL}', end='')
        print()

def clear_screen():
    if use_screen:
        print(f'\033[2J', end='')

def pause(line:int=None):
    move_to(line, 0)
    print(f'{Fore.RED}', end='')
    input('Press enter to continue...')
    print(f'{Style.RESET_ALL}')

def print_sum(line:int, sum:int):
    move_to(line, 0)
    print(f'{Fore.CYAN}SUM: {sum}{Style.RESET_ALL}')

def print_work(line:int, work:List[Tuple]):
    move_to(line, 0)
    print(f'{Fore.LIGHTGREEN_EX}WORK [{len(work)}]')
    count = 0
    for pos in work:
        print(f'[{pos[0]:2},{pos[1]:2}] ', end='')
        count += 1
        if count > 10:
            print()
            count = 0
    print(f'{Style.RESET_ALL}')

def print_path(path:List[Tuple]):
    print(f'path: {path}')

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
            graph.add_node((x, y), risk=int(line[x]), visited=False, score=sys.maxsize, prev=None)
        line = f.readline()
        y += 1
        height += 1

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
start_pos = (0,0)
end_pos = (width - 1, height - 1)

clear_screen()

# Add start to the working list
work = [start_pos]
nodes[start_pos]['visited'] = True
nodes[start_pos]['score'] = 0
# print_grid(nodes, width, height)

# Continue until the work list is empty, or we reach
# the end position
while work:
    # print_work(work_line, work)

    # Find the node in work with the lowest score
    curr_pos = None
    for pos in work:
        if curr_pos is None or nodes[pos]['score'] < nodes[curr_pos]['score']:
            curr_pos = pos
    work.remove(curr_pos)
    # print(f'curr_pos: {curr_pos}')
    # print(f'nodes[curr_pos]={nodes[curr_pos]}')

    curr_risk = nodes[curr_pos]['risk'] if curr_pos != start_pos else 0
    # print(f'curr_risk: {curr_risk}')

    # Add the position to the path and increment the total sum
    # print_grid(nodes, width, height, work, curr_pos)

    # If we are at the end, we are done
    if curr_pos == end_pos:
        break
 
    # Get list of unvisited neighbor positions:
    #  - mark as visited
    #  - update the score as the path score + the risk score
    #  - add to the work list
    unvisited = [n for n in graph.neighbors(curr_pos) if not nodes[n]['visited']]
    curr_score = nodes[curr_pos]['score']
    for neighbor_pos in unvisited:
        neighbor = nodes[neighbor_pos]
        # Mark adjacent nodes as visited
        neighbor['visited'] = True
        # Update score of adjacent nodes
        new_score = curr_score + neighbor['risk']
        if new_score < neighbor['score']:
            neighbor['score'] = new_score
            # Set the neighbor's previous path position
            neighbor['prev'] = curr_pos
        # Add the neighbor to the work list
        work.append(neighbor_pos)

    # pause(input_line)

pos = end_pos
path = []
while pos != start_pos:
    path.append(pos)
    pos = nodes[pos]['prev']
path.append(start_pos)
path.reverse()

print_grid(nodes, width, height, None, None, path)
print(f'total risk={nodes[end_pos]["score"]}')
