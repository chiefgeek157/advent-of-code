import aoc.segment as sg

# filename = '2023/day05/input.txt'
filename = "2023/day05/test1.txt"

# convert the comment below to a map
# Maps:
MAPS = {
    0: "seed to soil",
    1: "soil to fertilizer",
    2: "fertilizer to water",
    3: "water to light",
    4: "light to temperature",
    5: "temperature to humidity",
    6: "humidity to location",
}

MAX = 10000000000000


def insert_segment(segs, new_seg) -> list:
    """Inserts a new segment into the list of segements, splitting as needed.

    Segments are (start, end, offset) tuples.

    Returns the new list of segments."""
    # print(f"       Inserting {new_seg}")
    results = []
    used_up_new_seg = False
    for i in range(len(segs)):
        seg = segs[i]
        print(f'      Checking new_seg {new_seg} against {seg}')
        split_segs = sg.split((seg[0], seg[1]), (new_seg[0], new_seg[1]))
        print(f'      Split segs {split_segs}')
        for i in range(len(split_segs) - 1):
            if split_segs[i][2] == 1:
                offset = seg[2]
            elif split_segs[2] == 2:
                offset = new_seg[2]
            else:
                offset = seg[2] + new_seg[2]
            results.append((split_segs[i][0], split_segs[i][1], offset))
            print(f'      Added {results[-1]}')
        if len(split_segs) <= 1:
            used_up_new_seg = True
            break
        new_seg = split_segs[-1]
    if not used_up_new_seg:
        results.append(new_seg)
        print(f'      Added {results[-1]}')
    return results


def main():
    # Segs are tuples of (start, end, offset)
    # Seeds have an offset of 0
    segs = []

    # Maps are arrays of tuples of (start, end, offset)
    maps = []

    with open(filename, "r") as f:
        # Read seeds
        line = f.readline()
        seed_fields = line.split(":")[1].strip().split(" ")
        for i in range(0, len(seed_fields), 2):
            start = int(seed_fields[i])
            end = start + int(seed_fields[i + 1]) - 1
            segs.append((start, end, 0))
        # Sort the seed segments
        segs = sorted(segs, key=lambda x: x[0])
        print(f"Seed segs: {segs}")

        # Read maps
        map_type = -1
        line = f.readline()
        while line:
            line = line.strip()
            if len(line) == 0:
                line = f.readline()
                map_type += 1
                maps.append([])
                # print(f"Reading map type {MAPS[map_type]}")
            else:
                fields = line.split(" ")
                dst = int(fields[0])
                src = int(fields[1])
                cnt = int(fields[2])

                # Each map entry is a tuple with source start num, source end num,
                # and the offset to the destination num
                entry = (src, src + cnt - 1, dst - src)
                maps[map_type].append(entry)
                # print(f"   Read {fields} => {entry}")

            line = f.readline()

    # Sort each map by the source start num
    for i in range(len(maps)):
        maps[i] = sorted(maps[i], key=lambda x: x[0])
        print(f"Sorted map {MAPS[i]}: {maps[i]}")

    # Apply the maps in order
    for i in range(len(maps)):
        print(f'Applying map {MAPS[i]}')
        for entry in maps[i]:
            print(f'   Applying {entry}')
            segs = insert_segment(segs, entry)
            print(f"   segs: {segs}")


if __name__ == "__main__":
    main()
