filename = '2022/day03/input.txt'
# filename = '2022/day03/test1.txt'

char_values = {}
for i in range(1,27):
    char_values[chr(i+64)] = i + 26
for i in range(1,27):
    char_values[chr(i+96)] = i
print(f'Char values: {char_values}')

sum_chars = 0
ord_a = ord('a')
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        # print(f'{line} {len(line)}')
        h1 = line[:int(len(line)/2)]
        h2 = line[int(len(line)/2):]
        print(f'{h1} | {h2}')

        dup_chars = set()
        for char in h1:
            if char in h2 and char not in dup_chars:
                print(f'Duplicate cahr {char}')
                dup_chars.add(char)
                sum_chars += char_values[char]
        line = f.readline()

print(f'Ans: {sum_chars}')
