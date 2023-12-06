import re

filename = '2023/day04/input.txt'
# filename = '2023/day04/test1.txt'

sum_points = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        fields1 = line.split(':')
        fields2 = fields1[1].strip().split('|')
        winners = list(int(x) for x in re.split(' +', fields2[0].strip()))
        nums = list(int(x) for x in re.split(' +', fields2[1].strip()))
        winner_count = 0
        for winner in winners:
            if winner in nums:
                winner_count += 1
        print(f'{fields1[0]} winner count {winner_count}')
        if winner_count > 0:
            sum_points += 2 ** (winner_count - 1)
        line = f.readline()

print(f'\nPart 1: {sum_points}')
