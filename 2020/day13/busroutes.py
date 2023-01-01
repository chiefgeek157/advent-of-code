# import math

from aoc.utils import chinese_remainder

# filename = '2020/day13/test1.txt'
filename = '2020/day13/input.txt'

routes = []
offsets = []
with open(filename, 'r') as f:
    line = f.readline()
    start_time = int(line.strip())
    line = f.readline()
    while line:
        fields = line.split(',')
        for i in range(len(fields)):
            if fields[i] != 'x':
                routes.append(int(fields[i]))
                offsets.append(i)
        line = f.readline()
print(f'Start time {start_time}')
print(f'Routes {routes}')
print(f'Offsets {offsets}')

min_next = start_time * 10
min_route = None
for route in routes:
    next_time = (int(start_time / route) + 1) * route
    print(f'Route {route} next time is {next_time}')
    if next_time < min_next:
        min_next = next_time
        min_route = route

part1 = (min_next - start_time) * min_route
print(f'\nPart 1: {part1}\n')

# Since the solution is to have the busses leave later, the remainder is
# the difference between the offset and the bus route
#
#  7 |-------|-------|---//---|-------|----
#  x
#  x
# 11 |-----------|----//-----|========X--|----
#  x                 remainder ---^     ^--- offset
#  ...
# 37 |-------//-----------------------X---------//-----------------|

remainders = []
for i in range(len(routes)):
    remainder = ((int(offsets[i] / routes[i]) + 1) * routes[i] - offsets[i]) % routes[i]
    print(f'Remainder for {routes[i]} and offset {offsets[i]} is {remainder}')
    remainders.append(remainder)
part2 = chinese_remainder(routes, remainders)
print(f'\nPart 2: {part2}')
