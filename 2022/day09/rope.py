import math
filename = '2022/day09/input.txt'
# filename = '2022/day09/test1.txt'
# filename = '2022/day09/test2.txt'
part2 = True

def print_grid():
    global grid_min, grid_max, h, t, ts, rope
    print(f'-----------------------')
    for y in range(grid_max[1], grid_min[1] - 1, -1):
        line = ''
        for x in range(grid_min[0], grid_max[0] + 1):
            char = '.'
            if (x, y) in ts:
                char = '#'
            if x == 0 and y == 0:
                char = 's'
            if (x, y) == rope[-1]:
                char = 'T'
            for i in reversed(range(1, len(rope) - 1)):
                if (x, y) == rope[i]:
                    char = str(i)
            if (x, y) == rope[0]:
                char = 'H'
            line += char
        print(line)
    print(f'-----------------------')

def minmax(p):
    global grid_min, grid_max
    grid_min = (min(grid_min[0], p[0]), min(grid_min[1], p[1]))
    grid_max = (max(grid_max[0], p[0]), max(grid_max[1], p[1]))

def add_h(h):
    global ts, grid_min, grid_max
    minmax(h)

def add_t(t):
    global ts, grid_min, grid_max
    ts.add(t)
    minmax(t)

def rnd(x):
    if x < 0:
        return math.floor(x)
    return math.ceil(x)

rope_len = 2
if part2:
    rope_len = 10

ts = set()
grid_min = (0,0)
grid_max = (0,0)
rope = []
for i in range(rope_len):
    rope.append((0, 0))
add_t((0, 0))

print_grid()
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        dir = fields[0]
        dist = int(fields[1])
        # print(f'--- MOVE {dir} for {dist}')
        match(dir):
            case 'R':
                x_incr = 1
                y_incr = 0
            case 'L':
                x_incr = -1
                y_incr = 0
            case 'U':
                x_incr = 0
                y_incr = 1
            case 'D':
                x_incr = 0
                y_incr = -1
        for i in range(dist):
            rope[0] = (rope[0][0] + x_incr, rope[0][1] + y_incr)
            add_h(rope[0])
            for i in range(1, len(rope)):
                dx = rope[i - 1][0] - rope[i][0]
                dy = rope[i - 1][1] - rope[i][1]
                # print(f'dx:{dx} dy:{dy}')
                if abs(dx) > 1 or abs(dy) > 1:
                    # print(f'Need to move {i}')
                    dt = math.sqrt(dx*dx + dy*dy)
                    mx = rnd(dx / dt)
                    my = rnd(dy / dt)
                    # print(f'dt:{dt} mx:{mx} my:{my}')
                    rope[i] = (rope[i][0] + mx, rope[i][1] + my)
                    # print(f'Rope: {rope}')
                add_t(rope[-1])
            # print(f'H:{rope[0]} T:{rope[-1]}')
            # print_grid()
        # print_grid()
        line = f.readline()

print_grid()
print(f'Part 1: {len(ts)}')