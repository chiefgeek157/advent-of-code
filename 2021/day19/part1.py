import scanner as sc

# filename = '2021/day19/test1.txt'
# filename = '2021/day19/test2.txt'
# filename = '2021/day19/test3.txt'
filename = '2021/day19/input.txt'

sa = sc.ScannerArray()
sa.read_file(filename)

beacons = sa.combine()
print(f'beacons\n{beacons}')
print(f'Answer: {len(beacons)}')
