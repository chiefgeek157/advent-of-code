# filename = '2020/day03/test1.txt'
filename = '2020/day03/input.txt'

grid = []
w = 0
h = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        grid.append(line.strip())
        line = f.readline()
w = len(grid[0])
h = len(grid)

x_incr = 3
y_incr = 1

x = 0
y = 0
count = 0
while y < h:
    if grid[y][x] == '#':
        count += 1
    x = (x + x_incr) % w
    y += y_incr

print(f'Part 1: {count}')

slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

counts = 1
for slope in slopes:
    x = 0
    y = 0
    count = 0
    while y < h:
        if grid[y][x] == '#':
            count += 1
        x = (x + slope[0]) % w
        y += slope[1]
    print(f'For slope {slope} count {count}')
    counts *= count

print(f'Part 2: {counts}')