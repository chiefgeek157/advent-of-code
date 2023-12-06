filename = '2023/day02/input.txt'
# filename = '2023/day02/test1.txt'

def sum_power(line: str) -> bool:
    return True

sum_power = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        fields = line.split(':')
        grabs = fields[1].split(';')
        maxs = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        for grab in grabs:
            groups = grab.strip().split(',')
            for group in groups:
                cubes = group.strip().split(' ')
                count = int(cubes[0])
                color = cubes[1]
                maxs[color] = max(maxs[color], count)
        power = maxs['red'] * maxs['green'] * maxs['blue']
        print(f'{fields[0]}: {maxs} -> {power}')
        sum_power += power
        line = f.readline()

print(f'\nPart 2: {sum_power}')
