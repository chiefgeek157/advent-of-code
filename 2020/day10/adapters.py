# filename = '2020/day10/test1.txt'
# filename = '2020/day10/test2.txt'
filename = '2020/day10/input.txt'

adapters = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        adapters.append(int(line))
        line = f.readline()
adapters = [0] + adapters
adapters.append(max(adapters) + 3)

part1 = None
adapters = list(sorted(adapters))
diffs = [0] * 4
for i in range(1, len(adapters)):
    diff = adapters[i] - adapters[i - 1]
    diffs[diff] += 1

part1 = diffs[1] * diffs[3]
print(f'\nPart 1: {part1}\n')

counts = {}
for i in range(len(adapters)):
    counts[adapters[i]] = 0
counts[0] = 1

for i in range(len(adapters)):
    node = adapters[i]
    count = counts[node]
    for j in range(1, 4):
        next_adapter = node + j
        if next_adapter in adapters:
            counts[next_adapter] += count

part2 = counts[adapters[-1]]
print(f'\nPart 2: {part2}')
