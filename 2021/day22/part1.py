from space import Prism, Space

# filename = '2021/day22/test1.txt'
# filename = '2021/day22/test2.txt'
# filename = '2021/day22/test3.txt'
filename = '2021/day22/input.txt'

# part1 = True
part1 = False
minlimit = -50
maxlimit = 50

space = Space()
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        values = line.strip().split()
        state = (values[0] == 'on')
        coords = values[1].split(',')
        minmaxes = []
        for i in range(3):
            temp = coords[i].split('=')
            minmax = temp[1].split('..')
            minmaxes.append([int(minmax[0]), int(minmax[1])])
        print(f'state={state} minmax={minmaxes}')
        if part1 and (\
                any([minmaxes[i][0] < -50 or minmaxes[i][0] > 50 for i in range(3)]) or \
                any([minmaxes[i][1] < -50 or minmaxes[i][1] > 50 for i in range(3)])
            ):
            print(f'Skipping out of bounds prism')
        else:
            space.add((minmaxes[0][0], minmaxes[1][0], minmaxes[2][0]), \
                (minmaxes[0][1], minmaxes[1][1], minmaxes[2][1]), state)
        line = f.readline()

print(f'space={space}')