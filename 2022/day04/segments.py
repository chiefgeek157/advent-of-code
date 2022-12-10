filename = '2022/day04/input.txt'
# filename = '2022/day04/test1.txt'

part2 = True
overlaps = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        fields = line.split(',')
        subfields = fields[0].split('-')
        range1 = (int(subfields[0]), int(subfields[1]))
        subfields = fields[1].split('-')
        range2 = (int(subfields[0]), int(subfields[1]))
        print(f'{range1} | {range2}')

        if part2:
            if (range1[1] >= range2[0] and range1[0] <= range2[1]):
                print('Overlap')
                overlaps += 1
        else:
            if (range1[0] <= range2[0] and range1[1] >= range2[1]
                or range2[0] <= range1[0] and range2[1] >= range1[1]):
                print('Overlap')
                overlaps += 1

        line = f.readline()

print(f'Ans: {overlaps}')
