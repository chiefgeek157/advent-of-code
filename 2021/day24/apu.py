# filename = '2021/day24/test1.txt'
filename = '2021/day24/input.txt'

reg = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

inst = []
part2 = False
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        inst = [fields[0]]
        match fields[0]:
            case 'inp':
                pass
            case _:
                inst.append(fields[1])
                inst.append(fields[2])
        line = f.readline()

model = '1' * 14
while len(model) == 14:
    if '0' not in model:
        pass
    model = str(int(model) + 1)