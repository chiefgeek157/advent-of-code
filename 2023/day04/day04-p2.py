import re

filename = '2023/day04/input.txt'
# filename = '2023/day04/test1.txt'

num_cards = 0
copies = { 1: 1 }
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        fields1 = line.split(':')
        card = int(fields1[0][4:])
        fields2 = fields1[1].strip().split('|')
        winners = list(int(x) for x in re.split(' +', fields2[0].strip()))
        nums = list(int(x) for x in re.split(' +', fields2[1].strip()))
        winner_count = 0
        for winner in winners:
            if winner in nums:
                winner_count += 1
        card_copies = copies.get(card, 1)
        print(f'{card} has {card_copies} copies')
        num_cards += card_copies
        for i in range(winner_count):
            other_card = card + i + 1
            copies[other_card] = copies.get(other_card, 1) + card_copies
            print(f'copies[{other_card}] = {copies[other_card]}')
        line = f.readline()

print(f'\nPart 2: {num_cards}')
