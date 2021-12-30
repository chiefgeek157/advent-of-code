import scanner as sc

# filename = '2021/day19/test1.txt'
# filename = '2021/day19/test2.txt'
# filename = '2021/day19/test3.txt'
filename = '2021/day19/input.txt'

scanners = []
with open(filename, 'r') as f:
    s = sc.Scanner.read(f)
    while s:
        scanners.append(s)
        s = sc.Scanner.read(f)
for s in scanners: print(f'Scanner[{s.id}]:\n{s}')

c = sc.Combiner()
c.combine(scanners)
# print(f'Scanner[{scanners[0].id}]:\n{scanners[0]}')
print(f'Answer: {len(scanners[0].beacons)}')
