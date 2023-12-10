filename = '2023/day07/input.txt'
# filename = '2023/day07/test1.txt'

# The stength of a hand is based on the poker strength
#   7: 5 of a kind
#   6: four of a kind
#   5: full house
#   4; three of a kind
#   3: two pair
#   2: one pair
#   1: highest card
#
# The order of cards is a base 13 number converted to decimal
CARD_VALUES = { 'A': 13, 'K': 12, 'Q': 11, 'J': 10, 'T': 9, '9': 8, '8': 7,
               '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1 }

OFFSET = pow(13, 5)

def main() -> int:
    # A hand is a tuple (cards, bid, strength, order)
    hands = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            fields = line.strip().split()
            hand = fields[0]
            bid = int(fields[1])

            counts = {}
            order = 0
            for i in range(5):
                counts[hand[i]] = counts.get(hand[i], 0) + 1
                order = order * 13 + CARD_VALUES[hand[i]]
            # print(f'Counts: {counts}')
            card_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            # print(f'Card counts: {card_counts}')
            if card_counts[0][1] == 5:
                strength = 7
            elif card_counts[0][1] == 4:
                strength = 6
            elif card_counts[0][1] == 3:
                if card_counts[1][1] == 2:
                    strength = 5
                else:
                    strength = 4
            elif card_counts[0][1] == 2:
                if card_counts[1][1] == 2:
                    strength = 3
                else:
                    strength = 2
            else:
                strength = 1

            item = (hand, bid, strength, order)
            print(f'Adding item {item}')
            hands.append(item)

            line = f.readline()

    hands = sorted(hands, key=lambda x: x[2] * OFFSET + x[3])
    print(f'Sorted hands {hands}')

    score = 0
    for i in range(1, len(hands) + 1):
            score += i * hands[i-1][1]
    return score

if __name__ == '__main__':
    print(f'Answer: {main()}')
