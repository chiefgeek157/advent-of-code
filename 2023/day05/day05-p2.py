import os

print(f'Current directory: {os.getcwd()}')

import aoc.segment as sg

# filename = '2023/day05/input.txt'
filename = '2023/day05/test1.txt'

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

MAX = 10000000000000

def insert_segment(segs, new_seg) -> list:
    '''Inserts a new segment into the list of segements, splitting as needed.

    Segments are (start, end, offset) tuples.

    Returns the new list of segments.'''
    print(f'Inserting {new_seg}')
    results = []
    for i in range(len(segs)):
        seg = segs[i]
        split_segs = sg.split((seg[0], seg[1]), (new_seg[0], new_seg[1]))
        for split_seg in split_segs:
            if split_seg[1] == 1:
                offset = seg[2]
            elif split_seg[1] == 2:
                offset = new_seg[2]
            else:
                offset = seg[2] + new_seg[2]
            results.append((split_seg[0], split_seg[1], offset))
        print(f'   Results {results}')
    return results

def main():
    # Seeds are tuples of (start, end, 0)
    seeds = []

    # Maps are arrays of tuples of (start, end, offset)
    maps = []

    with open(filename, 'r') as f:
        # Read seeds
        line = f.readline()
        seed_fields = line.split(':')[1].strip().split(' ')
        for i in range(0, len(seed_fields), 2):
            start = int(seed_fields[i])
            end = start + int(seed_fields[i+1]) - 1
            seeds.append((start, end, 0))
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

    # Segemnts is an array of tuples
    # Each tuple has a start and end num and an offset
    segs = [(0, MAX, 0)]

    # Add the seed segments
    for seed in seeds:
        insert_segment(segs, seed)

    # Now, for each seed, apply the maps in order
    min_location = MAX
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

    print(f'\nPart 2: {min_location}')

if __name__ == '__main__':
    main()
