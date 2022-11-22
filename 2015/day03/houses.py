filename = '2015/day03/input.txt'

houses = {}

path=""
with open(filename, 'r') as f:
    path = f.readline()

pos = (0,0)
houses[pos] = 1
for c in path:
    if c == '^':
        pos = (pos[0], pos[1] + 1)
    elif c == 'v':
        pos = (pos[0], pos[1] - 1)
    if c == '>':
        pos = (pos[0] + 1, pos[1])
    if c == '<':
        pos = (pos[0] - 1, pos[1])
    if pos in houses:
        houses[pos] += 1
    else:
        houses[pos] = 1

print(f'Total visited houses {len(houses)}')