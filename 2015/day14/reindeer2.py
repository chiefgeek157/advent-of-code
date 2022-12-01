from operator import attrgetter
from types import SimpleNamespace

filename = '2015/day14/input.txt'
# filename = '2015/day14/test1.txt'

time_limit = 2503
# time_limit = 1000

herd = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        deer = SimpleNamespace()
        herd.append(deer)

        deer.name = fields[0]
        deer.speed = int(fields[3])
        deer.dur = int(fields[6])
        deer.rest = int(fields[13])
        deer.counter = deer.dur
        deer.points = 0
        deer.dist = 0

        print(f'Added {deer}')
        line = f.readline()

for t in range(1, time_limit + 1):
    max_dist = 0
    max_deer = None
    for deer in herd:
        if deer.counter > 0:
            deer.dist += deer.speed
            deer.counter -= 1
            if deer.counter == 0:
                deer.counter = -deer.rest
        else:
            deer.counter += 1
            if deer.counter == 0:
                deer.counter = deer.dur
        if deer.dist > max_dist:
            max_dist = deer.dist
            max_deer = deer
        # print(f'Deer: {deer}')
    max_deer.points += 1

print(f'Herd: {herd}')

print(f'Ans: {max(herd, key=attrgetter("points"))}')
