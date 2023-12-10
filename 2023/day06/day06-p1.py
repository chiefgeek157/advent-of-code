import re

filename = '2023/day06/input.txt'
# filename = '2023/day06/test1.txt'

def main() -> int:
    races = []

    with open(filename, 'r') as f:
        # Read seeds
        line = f.readline()
        lengths = list(int(x) for x in re.split(' +', line.strip().split(':')[1].strip()))
        line = f.readline()
        max_dists = list(int(x) for x in re.split(' +', line.strip().split(':')[1].strip()))

        races = list(zip(lengths, max_dists))
        print(f'Races: {races}')

        total = 1
        for race in races:
            count = 0
            length, max_dist = race
            for hold_time in range(1, length):
                dist = (length - hold_time) * hold_time
                if dist > max_dist:
                    count += 1
            print(f'Race {race} count {count}')
            total *= count

    return total

if __name__ == '__main__':
    print(f'Answer: {main()}')
