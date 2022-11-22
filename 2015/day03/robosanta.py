filename = '2015/day03/input.txt'

houses = {}

path=""
with open(filename, 'r') as f:
    path = f.readline()

santas = [(0,0), (0,0)]
houses[santas[0]] = 1
houses[santas[1]] += 1
santa = 0
for c in path:
    pos = santas[santa]
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

    santas[santa] = pos

    santa = 0 if santa == 1 else 1

print(f'Total visited houses {len(houses)}')