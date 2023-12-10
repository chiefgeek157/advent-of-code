import math
import re

# The soluition is to solve the quadratic equation
# -h^2 + lh - d
#
# h = (l + sqrt(l^2 + 4d)) / 2
#
# h = (71530 + sqrt(71530^2 + 4*940200)) / 2
#
# d = (l - h) * h
# d = lh - h^2
# h^2 - lh + d = 0
# h = ( l +/- sqrt (l^2 - 4*d) ) / 2

filename = '2023/day06/input.txt'
# filename = '2023/day06/test1.txt'

def main() -> int:
    races = []

    with open(filename, 'r') as f:
        # Read seeds
        line = f.readline()
        length = int(line.split(':')[1].replace(' ', ''))
        line = f.readline()
        max_dist = int(line.split(':')[1].replace(' ', ''))

        print(f'Race: {length}, {max_dist}')

        root1 = int((length + math.sqrt(length*length - 4 * max_dist)) / 2)
        root2 = int((length - math.sqrt(length*length - 4 * max_dist)) / 2)
        print(f'Roots: {root1}, {root2}')

    return root1 - root2

if __name__ == '__main__':
    print(f'Answer: {main()}')
