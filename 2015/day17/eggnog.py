from itertools import combinations

filename = '2015/day17/input.txt'
# filename = '2015/day17/test1.txt'

EGGNOG = 150

bottles = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        bottles.append(int(line.strip()))
        line = f.readline()
print(f'Bottles: {bottles}')

max_bottles = 0
total = 0
for bottle in sorted(bottles):
    if (total + bottle) > EGGNOG:
        break
    total += bottle
    max_bottles += 1
print(f'Max bottles: {max_bottles}')

matches = {}
for num in range(1, max_bottles + 1):
    for combo in combinations(bottles, num):
        # print(f'Combo: {combo}')
        total = sum(combo)
        if total == EGGNOG:
            # print(f'Found match: {combo}')
            if num not in matches:
                match_list = []
                matches[num] = match_list
            else:
                match_list = matches[num]
            match_list.append(combo)

min_size = min(matches.keys())
min_count = len(matches[min_size])
total = sum(len(x) for x in matches.values())
print(f'Ans: {total}, min size {min_size} count {min_count}')