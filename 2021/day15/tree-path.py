import anytree as any
import colorama as clr
from typing import List, Tuple
import sys
import networkx as nx

filename = "test1.txt"
#filename = "test2.txt"
#filename = "test3.txt"
#filename = "input.txt"

clr.init()

grid_x = 0
grid_y = 0

class Node(any.NodeMixin):
    def __init__(self, parent:"Node", pos:Tuple, value:int):
        self.parent = parent
        self.pos = pos
        self.value = value
    
    def adjacents(self, grid:List[List[int]]):
        width = len(grid[0])
        height = len(grid)
        adj = []
        # Right
        if self.pos[0] <  - 1:
            adj.append((self.pos[0]+1, self.pos[1]))
        # Down
        if self.pos[1] < height - 1:
            adj.append((self.pos[0], self.pos[1]+1))
        # Left
        if self.pos[0] > 0:
            adj.append((self.pos[0]-1, self.pos[1]))
        # Up
        if self.pos[1] > 0:
            adj.append((self.pos[0], self.pos[1]-1))
        return adj

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.pos == other.pos
        if isinstance(other, tuple):
            return self.pos == other
        return NotImplemented

def print_grid(grid:List[List[int]], path:List[Node], min_path:List[Node], current:Node):
    print(f"{clr.Cursor.POS(0, 0)}{clr.Fore.LIGHTMAGENTA_EX}{clr.Style.BRIGHT}GRID:{Style.RESET_ALL}")
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            pos = (x, y)
            if current == pos:
                print(f"{Fore.RED}{Style.BRIGHT}", end="")
            if pos in path:
                print(f"{Fore.YELLOW}{Style.BRIGHT}", end="")
            elif pos in min_path:
                print(f"{Fore.YELLOW}{Style.BRIGHT}", end="")
            else:
                print(f"{Fore.WHITE}{Style.DIM}", end="")
            print(f"{grid[x][y]}{Style.RESET_ALL}", end="")
        print()

def sum_path(path:List[Node]):
    return sum([node.value for node in path])

def clear_screen():
    print(f"\033[2J", end="")

def pause(line:int):
    print(f"{Cursor.POS(0, line)}{Fore.RED}", end="")
    input("Press enter to continue...")
    print(f"{Style.RESET_ALL}")

def print_sum(line:int, sum:int):
    print(f"{Cursor.POS(0, line)}{Fore.CYAN}SUM: {sum}{Style.RESET_ALL}")

def print_work(line:int, work:List[Node]):
    print(f"{Cursor.POS(0, line)}{Fore.LIGHTGREEN_EX}WORK:")
    count = 0
    for pos in work:
        print(f"[{pos[0]:2},{pos[1]:2}] ", end="")
        count += 1
        if count > 10:
            print()
            count = 0
    print(f"{Style.RESET_ALL}")

clear_screen()

grid = []
with open(filename, "r") as f:
    line = f.readline()
    while line:
        row = []
        for char in line.strip():
            value = int(char)
            row.append(value)
        grid.append(row)
        line = f.readline()

grid_line = 0
sum_line = len(grid) + 2
input_line = sum_line + 1
work_line = input_line + 1

start_pos = (0,0)
end_pos = (len(grid[0]) - 1, len(grid) - 1)
path = []
min_path = []
min_sum = sys.maxsize
print_grid(grid, path, min_path, start_pos)

root = Node(None, start_pos, grid[start_pos[0]][start_pos[1]])
work = [root]
while len(work) > 0:
    node = work.pop()
    print_work(work_line, work)
    path.append(node)
    print_grid(grid, path, min_path, node)
    if node == end_pos:
        break
    adjs = node.adjacents(grid)
    for adj in adjs:
        if adj not in path:
            work.append(adj)
            print_work(work_line, work)
    print_sum(sum_line, sum_path(grid, path))
    pause(input_line)

pause(input_line)
