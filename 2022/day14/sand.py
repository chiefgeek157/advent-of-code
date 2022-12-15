from modules.utils import print_vert_header

# filename = '2022/day14/test1.txt'
filename = '2022/day14/input.txt'
part2 = True

AIR = 0
ROCK = 1
SAND = 2

cave_chars = ['.', '#', 'o']

entry = (500,0)

def get_point(point):
    global cave, cave_min, cave_max
    if point[0] < cave_min[0]:
        cave_min = (point[0], cave_min[1])
    if point[0] > cave_max[0]:
        cave_max = (point[0], cave_max[1])
    if part2 and point[1] == cave_max[1]:
        return ROCK
    return cave[point] if point in cave else AIR

def draw():
    print_vert_header(cave_min[0], cave_max[0], '    ')
    for y in range(cave_min[1],cave_max[1] + 1):
        line = f'{y:03} '
        for x in range(cave_min[0], cave_max[0] + 1):
            if (x,y) == entry:
                line += '+'
            else:
                line += cave_chars[get_point((x,y))]
        print(line)

cave = {}
cave_min = entry
cave_max = entry
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        point1 = None
        point2 = None
        fields = line.split(' -> ')
        for spot in fields:
            coords = spot.split(',')
            point2 = (int(coords[0]), int(coords[1]))
            cave_min = (min(cave_min[0], point2[0]), min(cave_min[1], point2[1]))
            cave_max = (max(cave_max[0], point2[0]), max(cave_max[1], point2[1]))
            if point1:
                print(f'Rock from {point1} to {point2}')
                dx = point2[0] - point1[0]
                dy = point2[1] - point1[1]
                stepx = 0 if dx == 0 else int(dx / abs(dx))
                stepy = 0 if dy == 0 else int(dy / abs(dy))
                point = point1
                for step in range(max(abs(dx), abs(dy)) + 1):
                    cave[point] = ROCK
                    point = (point[0] + stepx, point[1] + stepy)
            point1 = point2
        line = f.readline()

if part2:
    cave_max = (cave_max[0], cave_max[1] + 2)
draw()

sand_count = 0
filled = False
while not filled:
    sand = entry
    while True:
        if sand[1] > cave_max[1]:
            filled = True
            break
        d_sand = (sand[0], sand[1] + 1)
        l_sand = (sand[0] - 1, sand[1] + 1)
        r_sand = (sand[0] + 1, sand[1] + 1)
        if get_point(d_sand) == AIR:
            next_sand = d_sand
        elif get_point(l_sand) == AIR:
            next_sand = l_sand
        elif get_point(r_sand) == AIR:
            next_sand = r_sand
        else:
            cave[sand] = SAND
            sand_count += 1
            if sand == entry:
                filled = True
            # print(f'Sand {sand_count} set at {sand}')
            # print(f'After {sand_count} sand:')
            # draw()
            # print()
            break
        sand = next_sand

draw()
print(f'Part 1/2: {sand_count}')