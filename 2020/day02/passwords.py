# filename = '2020/day02/test1.txt'
filename = '2020/day02/input.txt'

good1 = []
good2 = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split(':')
        policy = fields[0].split()
        range = policy[0].split('-')
        min_count = int(range[0])
        max_count = int(range[1])
        char = policy[1]
        password = fields[1].strip()

        count = password.count(char)
        if count >= min_count and count <= max_count:
            good1.append(password)

        if (bool(len(password) >= min_count and password[min_count - 1] == char)
                != bool(len(password) >= max_count and password[max_count - 1] == char)):
            good2.append(password)
        line = f.readline()

print(f'Part 1: {len(good1)}')
print(f'Part 2: {len(good2)}')
