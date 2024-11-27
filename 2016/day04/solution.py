# --- Day 4: Security Through Obscurity ---
# Finally, you come across an information kiosk with a list of rooms. Of
# course, the list is encrypted and full of decoy data, but the instructions
# to decode the list are barely hidden nearby. Better remove the decoy data
# first.
#
# Each room consists of an encrypted name (lowercase letters separated by
# dashes) followed by a dash, a sector ID, and a checksum in square brackets.
#
# A room is real (not a decoy) if the checksum is the five most common letters
# in the encrypted name, in order, with ties broken by alphabetization. For
# example:
#
# aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters
# are a (5), b (3), and then a tie between x, y, and z, which are listed alphabetically.
# a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are
# all tied (1 of each), the first five are listed alphabetically.
# not-a-real-room-404[oarel] is a real room.
# totally-real-room-200[decoy] is not.
# Of the real rooms from the list above, the sum of their sector IDs is 1514.
#
# What is the sum of the sector IDs of the real rooms?

from collections import Counter
from operator import itemgetter

# input = 'test1.txt'
input = 'input.txt'

def main():

    # --- Part One --

    with open(input) as f:
        line = f.readline()
        total = 0
        while line:
            # print(f'\nline: {line}')
            fields = line.split('[')
            groups = fields[0].split('-')
            letters = ''.join(groups[:-1])
            sector = int(groups[-1])
            checksum = fields[1][:-2]
            # print(f'letters: {letters}, sector: {sector}, checksum: {checksum}')

            counts = Counter(letters)
            # print(f'counts: {counts}')

            ordered = {val[0] : val[1] for val in
                       sorted(counts.items(),
                              key = lambda x: (-x[1], x[0]))}
            # print(f'ordered: {ordered}')

            # get the first five keys from ordered
            sum = ''.join(list(ordered.keys())[:5])
            # print(f'sum: {sum}')

            if sum == checksum:
                # print(f'room is real')
                total += sector
            else:
                print(f'letters: {letters}, sector: {sector}, checksum: {checksum}')
                print(f'ordered: {ordered}')
                print(f'sum: {sum}')


            line = f.readline()

        print(f'Part 1: {total}')

if __name__ == '__main__':
    main()
