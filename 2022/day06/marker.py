filename = '2022/day06/input.txt'
# filename = '2022/day06/test1.txt'
part2 = False

def find_marker(line, size) -> int:
    print(f'{line}')
    for i in range(size - 1, len(line)):
        seg = line[i - size + 1:i + 1]
        # print(f'Seg {seg}')
        marker = True
        for j in range(size - 1):
            # print(f'seg[{j}]: {seg[j]} find: {seg.find(seg[j], j + 1)}')
            if seg.find(seg[j], j + 1) >= 0:
                marker = False
                break
        if marker:
            print('Marker')
            break
    return i

with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line[:-1]
        print(f'Part 1: {find_marker(line, 4) + 1}')
        print(f'Part 2: {find_marker(line, 14) + 1}')
        line = f.readline()

