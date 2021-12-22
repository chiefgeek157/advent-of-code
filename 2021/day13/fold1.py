import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
from typing import Dict, List, Set, Tuple

#filename = "test1.txt"
#filename = "test2.txt"
#filename = "test3.txt"
filename = "input.txt"

def print_points(width, height, points):
    print(f"\nSize: {width} x {height}")
    for y in range(height):
        for x in range(width):
            point = (x, y)
            if point in points:
                print(f"{Fore.BLUE}#{Style.RESET_ALL}", end="")
            else:
                print(f".", end="")
        print()

def fold(width:int, height:int, action:Dict, points:Set[Tuple]):
    folded = set()
    dir = action["dir"]
    line = action["line"]
    print(f"Folding along {dir} = {line}")
    match dir:
        case "x":
            width = int((width - 1) / 2)
        case "y":
            height = int((height - 1) / 2)
    for point in points:
        p = (point[0], point[1])
        match dir:
            case "x":
                if point[0] > line:
                    p = (line - (point[0] - line), point[1])
            case "y":
                if point[1] > line:
                    p = (point[0], line - (point[1] - line))
        folded.add(p)
    return width, height, folded

points = set()
actions = []
width = 0
height = 0
with open(filename, "r") as f:
    line = f.readline()
    while line and len(line.strip()) > 0:
        values = line.strip().split(",")
        points.add((int(values[0]), int(values[1])))
        line = f.readline()

    line = f.readline()
    while line:
        values = line.strip().split()[2].split("=")
        dir = values[0]
        line = int(values[1])
        match dir:
            case "x":
                width = max(width, line * 2 + 1)
            case "y":
                height = max(height, line * 2 + 1)
        actions.append({"dir": dir, "line": line})
        line = f.readline()
    print_points(width, height, points)
    print(f"Actions: {actions}")

for action in actions:
    width, height, points = fold(width, height, action, points)
    print_points(width, height, points)

print(f"Answer: {len(points)}")
