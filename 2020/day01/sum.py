# filename = '2020/day01/test1.txt'
filename = '2020/day01/input.txt'

entries = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        entries.append(int(line.strip()))
        line = f.readline()

entries = list(sorted(entries))

for entry in entries:
    if entry > 1010:
        print(f'Failed')
        break
    if (2020 - entry) in entries:
        e1 = entry
        e2 = 2020 - entry
        print(f'Part 1: {e1 * e2}')
        break

found = False
for e1 in entries:
    for e2 in entries:
        if e2 != e1:
            if e2 > (2020 - e1) / 2:
                break
            if (2020 - e1 - e2) in entries:
                e3 = 2020 - e1 - e2
                print(f'Part 2: {e1 * e2 * e3}')
                found = True
                break
        if found:
            break
