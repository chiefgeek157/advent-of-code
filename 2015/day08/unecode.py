import re

filename = '2015/day08/input.txt'
# filename = '2015/day08/test1.txt'

ESCRE = r'\\[^"x]|\\"|\\x[0-9a-fA-F]{2}'

reg_chars = 0
esc_chars = 0
with open(filename, 'r') as f:
    line = f.readline().rstrip()
    while line:
        print(f'line: {line}')
        reg_chars += len(line)
        line = re.sub(ESCRE, '_', line)
        print(f'      {line}')
        esc_chars += len(line) - 2
        line = f.readline().rstrip()

print(f'Answer: {reg_chars} - {esc_chars} = {reg_chars - esc_chars}')
