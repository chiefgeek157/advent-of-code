from aoc.utils import bound1d, bound2d, union1d
from aoc.utils import manhattan_dist

# filename = '2022/day15/test1.txt'
# y_test = 10
# c_min = 0
# c_max = 20

filename = '2022/day15/input.txt'
y_test = 2000000
c_min = 0
c_max = 4000000

part2 = False

def intersect(point, dist, y_line):
    """Return the x-extents of the intersection of the diamond
    region centered on point with rectiliear radius dist and the
    given y-line."""
    seg = None
    if point[1] - dist <= y_line and point[1] + dist >= y_line:
        x_dist = dist - abs(point[1] - y_line)
        seg = (point[0] - x_dist, point[0] + x_dist)
    return seg

limit = 1000000000
extents = (
    (limit, limit),
    (-limit, -limit)
)

sensors = {}
beacons = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split(':')
        s_fields = fields[0].split()
        sx_fields = s_fields[2][:-1].split('=')
        sy_fields = s_fields[3].split('=')
        sensor = (int(sx_fields[1]), int(sy_fields[1]))
        b_fields = fields[1].split()
        bx_fields = b_fields[4][:-1].split('=')
        by_fields = b_fields[5].split('=')
        beacon = (int(bx_fields[1]), int(by_fields[1]))
        beacons.append(beacon)
        print(f'Sensor {sensor} closest beacon {beacon}')

        sensors[sensor] = [beacon, manhattan_dist(sensor, beacon)]

        extents = bound2d(extents, sensor)
        extents = bound2d(extents, beacon)

        line = f.readline()
print(f'Extents:\n{extents}')

line_extents = []
remove = set()
for sensor_loc, sensor_info in sensors.items():
    beacon = sensor_info[0]
    dist = sensor_info[1]
    # print(f'Visiting sensor at {sensor_loc} dist {dist} beacon {beacon}')
    seg = intersect(sensor_loc, dist, y_test)
    # print(f'Sensor seg {seg}')
    line_extents = union1d(line_extents, seg)
    # print(f'Line extents now: {line_extents}')
    if sensor_loc[1] == y_test:
        # print(f'Removing sensor at {sensor_loc}')
        remove.add(sensor_loc)
    if beacon[1] == y_test:
        # print(f'Removing beacon at {beacon}')
        remove.add(beacon)

count = 0
for extent in line_extents:
    count += extent[1] - extent[0] + 1
print(f'\nCount {count} remove {remove}')
print(f'\nPart 1: {count - len(remove)}')

# PART 2

hidden = None
for y in range(c_min, c_max + 1):
    # print(f'Evaluating line {y}')
    line = []
    for sensor_loc, sensor_info in sensors.items():
        if len(line) == 1 and line[0][0] <= c_min and line[0][1] >= c_max:
            # This line cannot have a candidate
            # print(f'Line {y} is wider than sample area {line}')
            break
        # f'  - Line {y}: {line}'
        beacon = sensor_info[0]
        dist = sensor_info[1]
        # print(f'    - Visiting sensor at {sensor_loc} dist {dist} beacon {beacon}')
        seg = intersect(sensor_loc, dist, y)
        # print(f'    - Sensor seg {seg}')
        line = union1d(line, seg)
        # print(f'    - Line now: {line}')
    if len(line) > 1:
        hidden = (line[0][1] + 1, y)
        print(f'  - Found candidate at {hidden})')
        break

if hidden is not None:
    value = hidden[0] * 4000000 + hidden[1]
    print(f'Part 2: {value}')
else:
    print('FOUND NO SOLUTION')