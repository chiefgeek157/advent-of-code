import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
from typing import Dict, List, Set, Tuple

#filename = "test1.txt"
#filename = "test2.txt"
#filename = "test3.txt"
filename = "input.txt"

def insert(pairs:Dict, counts:Dict, transforms:Dict):
    for pair, count in pairs.copy().items():
        if count > 0:
            transform = transforms[pair]
            new1 = pair[0] + transform
            new2 = transform + pair[1]
            pairs[pair] -= count
            pairs[new1] = count + (pairs[new1] if new1 in pairs else 0)
            pairs[new2] = count + (pairs[new2] if new2 in pairs else 0)
            print(f"{pair}={pairs[pair]} -> {new1}={pairs[new1]} {new2}={pairs[new2]}")
            counts[transform] += count

pairs = {}
transforms = {}
counts = {}
with open(filename, "r") as f:
    poly = f.readline().strip()
    f.readline()
    print(f"Polymer template: {poly}")

    line = f.readline()
    while line:
        values = line.strip().split()
        transforms[values[0]] = values[2]
        pairs[values[0]] = 0
        for char in values[0]:
            counts[char] = 0
        line = f.readline()

    for i in range(len(poly) - 1):
        pair = f"{poly[i]}{poly[i+1]}"
        pairs[pair] += 1

    for char in poly:
        counts[char] += 1
    
    print(f"Transforms: {transforms}")
    print(f"Pairs: {pairs}")
    print(f"Counts: {counts}")

limit = 40
target_sum = sum(counts.values())
for i in range(limit):
    insert(pairs, counts, transforms)
    target_sum = (target_sum - 1) * 2 + 1
    check_sum = sum(pairs.values()) + 1
    print(f"({i+1:2}/{limit}) Pairs {pairs} total pair counts {check_sum}")
    assert check_sum == target_sum, f"target({target_sum}) != check({check_sum})"
    print(f"Counts: {counts}")
    # print(f"Polymer: {poly}")
    # input("Press enter to continue...")

# print(f"Counts: {counts}")
reversed = {v: k for k, v in counts.items()}
print(f"Reversed: {reversed}")
min_count = min(reversed.keys())
max_count = max(reversed.keys())
print(f"Answer: {reversed[max_count]}:{max_count} - {reversed[min_count]}:{min_count} = {max_count - min_count}")


