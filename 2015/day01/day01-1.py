# from amphipod import Piece, Board, State
# import copy as cp

# filename = '2021/day23/test1.txt'
# filename = '2021/day23/test2.txt'
filename = '2015/day01/input.txt'

data = ""

with open(filename, 'r') as f:
    data = f.readline()

floor = 0
for c in data:
    if c == "(":
        floor += 1
    elif c == ")":
        floor -= 1

print(f'Final floor {floor}')