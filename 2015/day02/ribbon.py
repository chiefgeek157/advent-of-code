filename = '2015/day02/input.txt'

total = 0

with open(filename, 'r') as f:
    data = f.readline()
    while data:
        dims = tuple(int(x) for x in data.split('x'))
        min_perim = 2 * (dims[0] + dims[1] + dims[2] - max(dims))
        vol = dims[0] * dims[1] * dims[2]
        len = min_perim + vol
        print(f'{dims}, min_perim={min_perim} vol={vol}, len={len}')
        total += len
        data = f.readline()

print(f'Total len {total}')