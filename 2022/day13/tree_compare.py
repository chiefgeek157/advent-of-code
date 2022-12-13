from functools import cmp_to_key

# filename = '2022/day13/test1.txt'
filename = '2022/day13/input.txt'

def parse(line, parent):
    while len(line) > 0:
        if line[0] == '[':
            child = []
            parent.append(child)
            line = parse(line[1:], child)
        elif line[0] == ']':
            # End of the parent
            line = line[1:]
            break
        elif line[0] == ',':
            # End of this member
            line = line[1:]
        else:
            # A non-group member
            i = 0
            while line[i] in '0123456789':
                i += 1
            val = int(line[:i])
            parent.append(val)
            line = line[i:]
    return line

def parse_line(line):
    parent = []
    line = parse(line, parent)
    return parent[0]

# tests = [
#     '[]',
#     '[1]',
#     '[1,2]',
#     '[[]]',
#     '[[1]]',
#     '[[1],2]',
#     '[[1],[2]]'
# ]
# for test in tests:
#     item = parse_line(test)
#     print(f'parse({test}): {item}')

# exit()

def compare(p1, p2, level=0):
    print(f'{"  "*level}- Compare {p1} vs {p2}')
    matched = None
    if isinstance(p1, list):
        if isinstance(p2, list):
            # Both are lists
            i = 0
            while matched is None:
                if i == len(p1) and i < len(p2):
                    print(f'{"  "*(level+1)}- Left side ran out of items, so inputs are in the right order')
                    matched = -1
                elif i == len(p2) and i < len(p1):
                    print(f'{"  "*(level+1)}- Right side ran out of items, so inputs are NOT in the right order')
                    matched = 1
                elif i < len(p1) and i < len(p2):
                    c1 = p1[i]
                    c2 = p2[i]
                    matched = compare(c1, c2, level + 1)
                    i += 1
                else:
                    break
        else:
            # p1 is a list, p2 is a value
            print(f'{"  "*(level+1)}- Mixed types; convert right to {[p2]} and retry comparison')
            matched = compare(p1, [p2], level + 1)
    else:
        if isinstance(p2, list):
            # p1 is a value, p2 is a list
            print(f'{"  "*(level+1)}- Mixed types; convert left to {[p1]} and retry comparison')
            matched = compare([p1], p2, level + 1)
        else:
            # Both are values
            if p1 < p2:
                print(f'{"  "*(level+1)}- Left side is smaller, so inputs are in the right order')
                matched = -1
            elif p1 > p2:
                print(f'{"  "*(level+1)}- Right side is smaller, so inputs are NOT in the right order')
                matched = 1
            # Else keep going

    return matched

sum_indices = 0
i = 0
packets = []
with open(filename, 'r') as f:
    line1 = f.readline()
    if line1:
        line2 = f.readline()
    while line1:
        line1 = line1.strip()
        line2 = line2.strip()

        i += 1
        print(f'\n== Pair {i} ==')
        p1 = parse_line(line1)
        p2 = parse_line(line2)
        packets.append(p1)
        packets.append(p2)
        if compare(p1, p2, 0) < 0:
            sum_indices += i

        line1 = f.readline()
        if line1:
            if len(line1.strip()) == 0:
                line1 = f.readline()
            line2 = f.readline()

print(f'Part1: {sum_indices}')

packets.append([[2]])
packets.append([[6]])

sorted_packets = sorted(packets, key=cmp_to_key(compare))

print(f'Sorted packets:')
product = 1
i = 1
for packet in sorted_packets:
    if packet == [[2]] or packet == [[6]]:
        product *= i
    print(packet)
    i += 1

print(f'Part 2: {product}')