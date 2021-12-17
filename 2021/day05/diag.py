import colorama
from colorama import Fore
from colorama import Back
from colorama import Style

#filename = "test.txt"
filename = "input.txt"

def create_line(p1, p2):
    xinc = 0 if p2[0] - p1[0] == 0 else 1 if p2[0] > p1[0] else -1
    yinc = 0 if p2[1] - p1[1] == 0 else 1 if p2[1] > p1[1] else -1
    length = max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1])) + 1
    p = (p1[0], p1[1])
    line = []
    for i in range(length):
        # print(f"Appending {p}")
        line.append(p)
        p = (p[0] + xinc, p[1] + yinc)
    return line

def apply_line(grid, p1, p2):
    line = create_line(p1, p2)
    for p in line:
        if p in grid.keys():
            grid[p] += 1
        else:
            grid[p] = 1
    return grid

def print_grid(grid, x_max, y_max):
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            if (x,y) in grid.keys():
                print(f"{Fore.RED}{Style.BRIGHT}{grid[(x,y)]:2}{Style.RESET_ALL} ", end="")
            else:
                print(" . ", end="")
        print()

colorama.init()

x_max = 0
y_max = 0
grid = {}
with open(filename, "r") as f:
    line = f.readline()
    while line:
        info = line.strip().split()
        coords = info[0].split(",")
        p1 = (int(coords[0]), int(coords[1]))
        coords = info[2].split(",")
        p2 = (int(coords[0]), int(coords[1]))
        print(f"{p1} -> {p2}")
        x_max = max(x_max, p1[0], p2[0])
        y_max = max(y_max, p1[1], p2[1])

        grid = apply_line(grid, p1, p2)
        # print_grid(grid, x_max, y_max)
        line = f.readline()

#print_grid(grid, x_max, y_max)

total = 0
for value in grid.values():
    if value > 1:
        total += 1

print(f"answer: {total}")

