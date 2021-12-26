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

def print_board(line:int, graph:nx.Graph, width:int, height:int,
        work:List[Tuple]=None, current:Tuple=None, path:List[Tuple]=None, risks=True, scores=True, edges=False):
    move_to(line, 0)
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
            score = f'{graph.nodes[pos]["score"]:03}'
            if len(score) > 3:
                score = '###'
            if risks:
                print(f'{graph.nodes[pos]["risk"]}', end='')
            if risks and scores:
                print('-', end='')
            if scores:
                print(f'{score}', end='')
            if x < width - 1:
                if edges and ((x, y), (x+1, y)) in graph.edges:
                    print('-', end='')
                else:
                    print(' ', end='')
            print(f'{Style.RESET_ALL}', end='')
        print()
        if edges and y < height - 1:
            for x in range(width):
                if edges and ((x, y), (x, y+1)) in graph.edges:
                    if risks and not scores:
                        print('| ', end='')
                    elif not risks and scores:
                        print(' |  ', end='')
                    if risks and scores:
                        print('  |   ', end='')
                else:
                    if risks and not scores:
                        print('  ', end='')
                    elif not risks and scores:
                        print('    ', end='')
                    if risks and scores:
                        print('      ', end='')
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

# Add a tile to the board
# Lines are in [y][x] order and are chars (not ints)
# Graph nodes are position tuples (x,y)
# The graph holds additional attributes for the nodes
def add_tile(lines:List[List[int]], width:int, height:int,
        graph:nx.Graph, tile_pos_x:int, tile_pos_y:int, risk_offset:int):
    for tile_x in range(width):
        for tile_y in range(height):
            x = tile_pos_x * width + tile_x
            y = tile_pos_y * height + tile_y
            # Add edges, which will also add the nodes
            if x > 0:
                graph.add_edge((x, y), (x-1, y))
            if tile_x < width - 1:
                graph.add_edge((x, y), (x+1, y))
            if y > 0:
                graph.add_edge((x, y), (x, y-1))
            if tile_y < height - 1:
                graph.add_edge((x, y), (x, y+1))

            # Set the node initial values
            # print(f'Setting initial values for [{x},{y}] risk={lines[tile_y][tile_x]}')
            graph.nodes[(x, y)]['risk'] = (int(lines[tile_y][tile_x]) + risk_offset)
            if graph.nodes[(x, y)]['risk'] > 9:
                graph.nodes[(x, y)]['risk'] -= 9
            graph.nodes[(x, y)]['visited'] = False
            graph.nodes[(x, y)]['score'] = sys.maxsize
            graph.nodes[(x, y)]['prev'] = None

# Tile is in [y][x] order
def print_tile_risks(tile:List[List[int]], width:int, height:int):
    for y in range(height):
        for x in range(width):
            print(f'{tile[y][x]}', end='')
        print()

def print_board_risks(graph:nx.Graph, width:int, height:int):
    for x in range(width):
        for y in range(height):
            print(f'{graph.nodes[(x,y)]["risk"]}', end='')
        print()

# Read lines from file
# y is first dimension, x is second
lines = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        lines.append(line.strip())
        line = f.readline()
tile_width = len(lines[0])
tile_height = len(lines)

print_tile_risks(lines, tile_width, tile_height)

# The board is w x h tiles
num_tiles_x = 5
num_tiles_y = 5
board_width = tile_width * num_tiles_x
board_height = tile_height * num_tiles_y
graph = nx.Graph()
for tile_x in range(num_tiles_x):
    for tile_y in range(num_tiles_y):
        print(f'Adding tile at [{tile_x},{tile_y}] with offset {tile_x + tile_y}')
        add_tile(lines, tile_width, tile_height, graph, tile_x, tile_y, tile_x + tile_y)
lines = None

# Display lines for printing
grid_line = 0
sum_line = board_height + 2
input_line = sum_line + 1
work_line = input_line + 1

print_board(grid_line, graph, board_width, board_height, None, None, None, True, False, True)

# For convenience
nodes = graph.nodes

# Initialize the search
start_pos = (0,0)
end_pos = (board_width - 1, board_height - 1)

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

print_board(grid_line, graph, board_width, board_height, None, None, path, False, True, True)
print(f'total risk={nodes[end_pos]["score"]}')
