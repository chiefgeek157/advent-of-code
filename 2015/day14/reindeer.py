filename = '2015/day14/input.txt'
# filename = '2015/day14/test1.txt'

time_limit = 2503
# time_limit = 1000

max_dist = 0
max_deer = None
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        name = fields[0]
        speed = int(fields[3])
        dur = int(fields[6])
        rest = int(fields[13])

        periods = int(time_limit / (dur + rest))
        last_period = time_limit % (dur + rest)
        dist = (periods * dur + min(dur, last_period)) * speed
        print(f'{name} speed {speed} dur {dur} rest {rest} pers {periods} last {last_period} dist {dist}')

        if dist > max_dist:
            max_dist = dist
            max_deer = name

        line = f.readline()

print(f'Ans: {max_deer} at {max_dist}')
