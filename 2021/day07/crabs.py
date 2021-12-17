import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
import math
import sys

#filename = "test.txt"
filename = "input.txt"

colorama.init()

crabs = []
with open(filename, "r") as f:
    values = f.readline().strip().split(",")
    for value in values:
        crabs.append(int(value))

min_fuel = sys.maxsize
min_x = None
for x in range(min(crabs), max(crabs) + 1):
    fuel = 0
    for crab in crabs:
        d = abs(crab - x)
        fuel += int(d * (d + 1) / 2)
    if fuel < min_fuel:
        min_fuel = fuel
        min_x = x
        print(f"New min {min_fuel} at {min_x}")

print(f"answer {min_fuel} at {min_x}")