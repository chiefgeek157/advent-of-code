# filename = '2020/day08/test1.txt'
filename = '2020/day08/input.txt'

ops = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        ops.append((fields[0], int(fields[1])))
        line = f.readline()

visited = set()
pos = 0
acum = 0
while True:
    op, v = ops[pos]
    visited.add(pos)
    new_pos = pos
    if op == 'acc':
        acum += v
        new_pos += 1
    elif op == 'jmp':
        new_pos += v
    else:
        new_pos += 1
    if new_pos in visited:
        break
    pos = new_pos

print(f'\nPart 1: {acum}')

for swap in range(len(ops)):
    visited = set()
    pos = 0
    acum = 0
    ended = False
    while True:
        op, v = ops[pos]
        visited.add(pos)
        new_pos = pos
        if op == 'acc':
            acum += v
            new_pos += 1
        elif (pos == swap and op == 'nop'
                or pos != swap and op == 'jmp'):
            new_pos += v
        else:
            new_pos += 1
        if new_pos == len(ops):
            print(f'Needed to swap pos {swap}')
            ended = True
            break
        if new_pos in visited or new_pos > len(ops):
            break
        pos = new_pos
    if ended:
        break

print(f'\nPart 2: {acum}')
