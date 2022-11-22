filename = '2015/day02/input.txt'

total = 0

with open(filename, 'r') as f:
    data = f.readline()
    while data:
        dims = tuple(int(x) for x in data.split('x'))
        s1 = dims[0] * dims[1]
        s2 = dims[0] * dims[2]
        s3 = dims[1] * dims[2]
        area = 2 * (s1 + s2 + s3) + min(s1, s2, s3)
        print(f'{dims}, s1={s1} s2={s2} s3={s3} min={min(s1,s2,s3)} area={area}')
        total += area
        data = f.readline()

print(f'Total area {total}')