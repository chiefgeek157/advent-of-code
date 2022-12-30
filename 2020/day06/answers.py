# filename = '2020/day06/test1.txt'
filename = '2020/day06/input.txt'

unique = 0
all = 0
with open(filename, 'r') as f:
    line = f.readline()
    group = set()
    inter = None
    while line:
        line = line.strip()
        if len(line) == 0:
            unique += len(group)
            # print(f'Inter is: {inter}')
            all += len(inter)
            group = set()
            inter = None
        else:
            group.update(line)
            if inter is None:
                inter = set(line)
            else:
                inter = inter.intersection(set(line))
            # print(f'Intersectiion now {inter}')
        line = f.readline()
    unique += len(group)
    # print(f'Inter is: {inter}')
    all += len(inter)

print(f'Part 1: {unique}')
print(f'Part 2: {all}')
