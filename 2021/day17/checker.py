filename = '2021/day17/results1.txt'
results = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        pairs = line.strip().split()
        for pair in pairs:
            coords = pair.split(',')
            results.append((int(coords[0]), int(coords[1])))
        line = f.readline()
print(f'results: {results}')
pairs = sorted(results, key=lambda x:x[0]*100+x[1])
for pair in pairs:
    print(f'{pair}')
