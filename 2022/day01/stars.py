filename = '2022/day01/input.txt'
# filename = '2022/day01/test1.txt'

elves = []
with open(filename, 'r') as f:
    elf = []
    elves.append(elf)
    line = f.readline()
    while line:
        line = line.strip()
        if len(line) > 0:
            elf.append(int(line))
        else:
            elf = []
            elves.append(elf)
        line = f.readline()
print(f'Elves: {elves}')

sorted_elves = sorted(elves, key=lambda x: sum(x), reverse=True)
sum_calories = 0
for i in range(3):
    sum_calories += sum(sorted_elves[i])

print(f'\nAns: {sum_calories}')