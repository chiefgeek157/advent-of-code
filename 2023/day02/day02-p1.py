filename = '2023/day02/input.txt'
# filename = '2023/day02/test1.txt'
# filename = '2023/day02/test2.txt'

max_cubes = {
    'red': 12, 'green': 13, 'blue': 14
}

def vaidate_game(line: str) -> bool:
    grabs = line.split(';')
    for grab in grabs:
        groups = grab.strip().split(',')
        for group in groups:
            fields = group.strip().split(' ')
            count = int(fields[0])
            color = fields[1]
            if count > max_cubes[color]:
                return False
    return True

sum_ids = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        fields1 = line.split(':')
        fields2 = fields1[0].split(' ')
        id = int(fields2[1])
        sum_ids += id if vaidate_game(fields1[1]) else 0
        line = f.readline()

print(f'\nPart 1: {sum_ids}')
