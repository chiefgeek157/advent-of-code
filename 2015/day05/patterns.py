import re

filename = '2015/day05/input.txt'

bad_combos = r'(ab|cd|pq|xy)'
double_letter = r'(.)\1'
vowels = r'([aeiou])'

repeat_pair = r'(..).*\1'
sandwich = r'(.).\1'

def is_nice(value: str):
    if re.search(bad_combos, value): return False
    if not re.search(double_letter, value): return False
    if len(re.findall(vowels, value)) < 3: return False
    return True

def also_nice(value: str):
    if not re.search(repeat_pair, value): return False
    if not re.search(sandwich, value): return False
    return True

nice = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        # if is_nice(line): nice.append(line)
        if also_nice(line): nice.append(line)
        line = f.readline()

print(f'Num nice {len(nice)}')