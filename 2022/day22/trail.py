# filename = '2022/day22/test1.txt'
filename = '2022/day22/input.txt'

moves = {
    0: (1, 0),
    1: (0, 1),
    2: (-1, 0),
    3: (0, -1)
}

chars = {
    0: '>',
    1: 'v',
    2: '<',
    3: '^'
}

lines = []
action_line = None
w = 0
h = 0
with open(filename, 'r') as f:
    line = f.readline()[:-1]
    while line:
        lines.append(line)
        w = max(w, len(line))
        h += 1
        line = f.readline()[:-1]
    action_line = f.readline().strip()

actions = []
pos = 0
while True:
    # print(f'Action line: {action_line}')
    if pos == len(action_line):
        # print(f'End of actions: {action_line}')
        actions.append(int(action_line[:pos]))
        break
    if action_line[pos] in '0123456789':
        # print(f'Skipping digit: {action_line[pos]}')
        pos += 1
        continue
    else:
        # print(f'Reading dist: {action_line[:pos]}')
        actions.append(int(action_line[:pos]))
        # print(f'Reading turn: {action_line[pos]}')
        actions.append(action_line[pos])
        action_line = action_line[pos + 1:]
        pos = 0

print(f'Actions: {actions}')

grid = []
for y in range(h):
    line = lines[y]
    row = [' '] * w
    for x in range(len(line)):
        row[x] = line[x]
    grid.append(row)

start_x = 0
for x in range(w):
    if grid[0][x] == '.':
        start_x = x
        break

def print_grid():
    for y in range(h):
        line = ''
        for x in range(w):
            line += grid[y][x]
        print(line)

def get_next(x, y, d):
    move = moves[d]
    nx = x + move[0]
    ny = y + move[1]
    if nx == w or (d == 0 and grid[ny][nx] == ' '):
        nx = 0
        while grid[ny][nx] == ' ':
            nx += 1
        if grid[ny][nx] == '#':
            return (x, y, True)
        return (nx, ny, False)
    elif nx == -1 or (d == 2 and grid[ny][nx] == ' '):
        nx = w - 1
        while grid[ny][nx] == ' ':
            nx -= 1
        if grid[ny][nx] == '#':
            return (x, y, True)
        return (nx, ny, False)
    elif ny == h or (d == 1 and grid[ny][nx] == ' '):
        ny = 0
        while grid[ny][nx] == ' ':
            ny += 1
        if grid[ny][nx] == '#':
            return (x, y, True)
        return (nx, ny, False)
    elif ny == -1 or (d == 3 and grid[ny][nx] == ' '):
        ny = h - 1
        while grid[ny][nx] == ' ':
            ny -= 1
        if grid[ny][nx] == '#':
            return (x, y, True)
        return (nx, ny, False)
    elif grid[ny][nx] == '#':
        return (x, y, True)
    return (nx, ny, False)

x = start_x
y = 0
d = 0

print(f'Start: [{x}, {y}], {d}')
grid[y][x] = 'S'
print_grid()

path = [(x, y)]
for action in actions:
    print(f'Action: {action}')
    if isinstance(action, int):
        count = action
        while count:
            nx, ny, stopped = get_next(x, y, d)
            if stopped:
                print(f'Stopped at [{nx}, {ny}]')
                break
            x = nx
            y = ny
            print(f'Moved to [{x}, {y}]')
            grid[y][x] = chars[d]
            path.append((x, y))
            count -= 1
        print_grid()
    else:
        d = (d + (1 if action == 'R' else -1)) % 4
        print(f'New direction is {d}')

print(f'Final [{x}, {y}] {d}')
val = 1000 * (y + 1) + 4 * (x + 1) + d
print(f'Part 1: {val}')

print(f'Start: [{x}, {y}], {d}')
grid[y][x] = 'S'
print_grid()

# Part 2

#      +-1-+-2-+
#      |   |   |
#      5 K 6 R 7
#      |   |   |
#      +-9-+-10+
#      |   |
#     12 B 10
#      |   |
#  +-12+-11+
#  |   |   |
#  5 L 8 F 7
#  |   |   |
#  +-4-+-3-+
#  |   |
#  1 T 3
#  |   |
#  +-2-+

# edge, detect xy min, detect xy max, new xy start, xy incr, new dir
edges = [
    [ 1, [ 50,  -1], [100,   0], [  0, 150], [ 0,  1], 0],
    [ 2, [100,  -1], [150,   0], [  0, 199], [ 1,  0], 3],
    [ 7, [150,   0], [150,  49], [ 99, 149], [ 0, -1], 2],
    [10, [100,  50], [150,  51], [ 99,  99], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
    [10, [150,   0], [150,  49], [ 99, 149], [ 9,  9], 2],
]

def get_next_2(x, y, d):
    move = moves[d]
    nx = x + move[0]
    ny = y + move[1]
    if nx == w or (d == 0 and grid[ny][nx] == ' '):
        nx = 0
        while grid[ny][nx] == ' ':
            nx += 1
        if grid[ny][nx] == '#':
            return (x, y, True)
        return (nx, ny, False)
    elif nx == -1 or (d == 2 and grid[ny][nx] == ' '):
        nx = w - 1
        while grid[ny][nx] == ' ':
            nx -= 1
        if grid[ny][nx] == '#':
            return (x, y, True)
        return (nx, ny, False)
    elif ny == h or (d == 1 and grid[ny][nx] == ' '):
        ny = 0
        while grid[ny][nx] == ' ':
            ny += 1
        if grid[ny][nx] == '#':
            return (x, y, True)
        return (nx, ny, False)
    elif ny == -1 or (d == 3 and grid[ny][nx] == ' '):
        ny = h - 1
        while grid[ny][nx] == ' ':
            ny -= 1
        if grid[ny][nx] == '#':
            return (x, y, True)
        return (nx, ny, False)
    elif grid[ny][nx] == '#':
        return (x, y, True)
    return (nx, ny, False)

path = [(x, y)]
for action in actions:
    print(f'Action: {action}')
    if isinstance(action, int):
        count = action
        while count:
            nx, ny, stopped = get_next_2(x, y, d)
            if stopped:
                print(f'Stopped at [{nx}, {ny}]')
                break
            x = nx
            y = ny
            print(f'Moved to [{x}, {y}]')
            grid[y][x] = chars[d]
            path.append((x, y))
            count -= 1
        print_grid()
    else:
        d = (d + (1 if action == 'R' else -1)) % 4
        print(f'New direction is {d}')
