import math

from aoc.utils import round_complex

# filename = '2020/day12/test1.txt'
filename = '2020/day12/input.txt'

headings = [(1+0j), (0+1j), (-1+0j), (0-1j)]
dirs = {
    'E': headings[0],
    'S': headings[1],
    'W': headings[2],
    'N': headings[3]
}

moves = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        moves.append((line[0], int(line[1:])))
        line = f.readline()

part1 = None
pos = (0 + 0j)
heading = 0
for move in moves:
    action, dist = move
    if action in ['N', 'S', 'E', 'W']:
        pos += dist * dirs[action]
    elif action == 'R':
        heading = (heading + int(dist / 90)) % 4
    elif action == 'L':
        heading = (heading - int(dist / 90)) % 4
    else:
        pos += dist * headings[heading]
    print(f'After move {move} pos {pos} head {heading}')

part1 = int(abs(pos.real) + abs(pos.imag))
print(f'\nPart 1: {part1}\n')

# Xnew = Xold x cosθ – Yold x sinθ
# Ynew = Xold x sinθ + Yold x cosθ
def rotate(p, deg):
    return round_complex(complex(
        p.real * math.cos(math.radians(deg)) - p.imag * math.sin(math.radians(deg)),
        p.real * math.sin(math.radians(deg)) + p.imag * math.cos(math.radians(deg))
    ))

part2 = None
pos = (0 + 0j)
waypoint = (10 - 1j)
print(f'Initial pos {pos} waypoint {waypoint}')
for move in moves:
    action, dist = move
    if action in ['N', 'S', 'E', 'W']:
        waypoint += dist * dirs[action]
    elif action == 'R':
        waypoint = rotate(waypoint, dist)
    elif action == 'L':
        waypoint = rotate(waypoint, -dist)
    else:
        pos += dist * waypoint
    print(f'After move {move} pos {pos} waypoint {waypoint}')

part2 = int(abs(pos.real) + abs(pos.imag))
print(f'\nPart 2: {part2}')
