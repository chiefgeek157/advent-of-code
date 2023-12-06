import re

filename = '2023/day05/input.txt'
# filename = '2023/day05/test1.txt'

# convert the comment below to a map
# Maps:
MAPS = {
    0: 'seed to soil',
    1: 'soil to fertilizer',
    2: 'fertilizer to water',
    3: 'water to light',
    4: 'light to temperature',
    5: 'temperature to humidity',
    6: 'humidity to location'
}

def main():
    seeds = None
    maps = []

    with open(filename, 'r') as f:
        # Read seeds
        line = f.readline()
        seeds = list(int(x) for x in line.split(':')[1].strip().split(' '))
        print(f'Seeds: {seeds}')

        # Read maps
        map_type = -1
        line = f.readline()
        while line:
            line = line.strip()
            if len(line) == 0:
                line = f.readline()
                map_type += 1
                maps.append([])
                print(f'Reading map type {MAPS[map_type]}')
            else:
                fields = line.split(' ')
                dst = int(fields[0])
                src = int(fields[1])
                cnt = int(fields[2])

                # Each map entry is a tuple with source start num, source end num,
                # and the offset to the destination num
                entry = (src, src + cnt - 1, dst - src)
                maps[map_type].append(entry)
                print(f'   Read {fields} => {entry}')

            line = f.readline()

    # Sort each map by the source start num
    for i in range(len(maps)):
        maps[i] = sorted(maps[i], key=lambda x: x[0])
        print(f'Sorted map {MAPS[i]}: {maps[i]}')

    # Now, for each seed, apply the maps in order
    min_location = 1000000000000
    for seed in seeds:
        print(f'Seed: {seed}', end=' ')
        for i in range(len(maps)):
            for entry in maps[i]:
                if seed >= entry[0] and seed <= entry[1]:
                    seed += entry[2]
                    break
            print(f'=> {seed}', end=' ')
        print()
        if seed < min_location:
            min_location = seed
            print(f'New min location: {min_location}')

    print(f'\nPart 1: {min_location}')

if __name__ == '__main__':
    main()
