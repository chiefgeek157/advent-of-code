from itertools import permutations

filename = '2015/day13/input.txt'
# filename = '2015/day13/test1.txt'

data = {}

with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        if fields[0] in data:
            name_data = data[fields[0]]
        else:
            name_data = {}
            data[fields[0]] = name_data
        name_data[fields[10][:-1]] = int(fields[3]) * (
            1 if fields[2] == 'gain' else -1)
        line = f.readline()
print(f'Data: {data}')

data['me'] = {}
for guest in data:
    data[guest]['me'] = 0
    data['me'][guest] = 0

max_sum = 0
for perm in permutations(data.keys()):
    # print(f'Perm: {perm}')
    sum = 0
    prev_guest = None
    for guest in perm:
        if prev_guest is not None:
            sum += data[prev_guest][guest]
            sum += data[guest][prev_guest]
        prev_guest = guest
    sum += data[prev_guest][perm[0]]
    sum += data[perm[0]][prev_guest]
    # print(f'Sum: {sum}')
    if sum > max_sum:
        print(f'New max {sum}')
        max_sum = sum

print(f'Ans: {max_sum}')
