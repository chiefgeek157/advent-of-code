import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
import sys

#filename = "test.txt"
filename = "input.txt"

colorama.init()

map = []

with open(filename, "r") as f:
    line = f.readline()
    while line:
        row = [int(c) for c in list(line.strip())]
        print(f"row {row}")
        map.append(row)
        line = f.readline()

def get_map_value(map, x, y):
    if x < 0 or x > (len(map) - 1) or y < 0 or y > (len(map[x]) - 1):
        return sys.maxsize
    else:
        return map[x][y]

def is_local_min(map, x, y):
    pc = get_map_value(map, x    , y    )
    pu = get_map_value(map, x    , y - 1)
    pd = get_map_value(map, x    , y + 1)
    pl = get_map_value(map, x - 1, y    )
    pr = get_map_value(map, x + 1, y    )
    print(f"({x},{y}: {pc} {pu} {pd} {pl} {pr}")
    return (pc < min(pu, pd, pl, pr))

minima = []
for x in range(len(map)):
    for y in range(len(map[x])):
        if is_local_min(map, x, y):
            print(f"Found minimum at {x} {y}: {map[x][y]}")
            minima.append((x, y, map[x][y]))

print(f"minima {minima}")
sum = 0
for minimum in minima:
    sum += minimum[2] + 1

print(f"Answer: {sum}")