import re

filename = '2023/day01/input.txt'
# filename = '2023/day01/test1.txt'
# filename = '2023/day01/test2.txt'

# Function to get first and last digit from a line of text
# using a regular expression for digits
def get_first_last_sum(line):
    digits = re.findall(r'\d', line)
    sum = 10 * int(digits[0]) + int(digits[-1])
    print(f'{line} -> {sum}')
    return sum

# Map of number names to values
number_map = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

# Regular expression to match the names of numbers or a digit
number_names = re.compile(
    r'(?=(zero|one|two|three|four|five|six|seven|eight|nine|\d))')

def get_first_last_sum_names(line):
    digits = re.findall(number_names, line)
    print(f'matches: {digits}')
    dig1 = number_map[digits[0]]
    dig2 = number_map[digits[-1]]
    sum = 10 * dig1 + dig2
    print(f'{line} -> {sum}')
    return sum

# Sum the digits in the input file
sum_digits = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        # sum_digits += get_first_last_sum(line)
        sum_digits += get_first_last_sum_names(line)
        line = f.readline()

# print(f'\nPart 1: {sum_digits}')
print(f'\nPart 2: {sum_digits}')
