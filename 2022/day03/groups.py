filename = '2022/day03/input.txt'
# filename = '2022/day03/test1.txt'

char_values = {}
for i in range(1,27):
    char_values[chr(i+64)] = i + 26
for i in range(1,27):
    char_values[chr(i+96)] = i
print(f'Char values: {char_values}')

def read3(f):
    lines = None
    line = f.readline()
    while line:
        if lines is None:
            lines = []
        lines.append(line.strip())
        if len(lines) == 3:
            break
        line = f.readline()
    return lines

sum_chars = 0
ord_a = ord('a')
with open(filename, 'r') as f:
    lines = read3(f)
    while lines:
        print(f'lines: {lines}')
        dup_chars = set()
        for char in lines[0]:
            if char in lines[1] and char in lines[2] and char not in dup_chars:
                print(f'Duplicate char {char}')
                dup_chars.add(char)
                sum_chars += char_values[char]
        lines = read3(f)

print(f'Ans: {sum_chars}')
