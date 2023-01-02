# filename = '2020/day14/test1.txt'
# filename = '2020/day14/test2.txt'
filename = '2020/day14/input.txt'

bits = 36
masks = []
progs = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        print(f'Reading program {len(progs)}')
        # Read mask
        filter = 0
        setter = 0
        mask_str = line.strip()[7:]
        bit = 1
        for i in reversed(range(bits)):
            if mask_str[i] == '0':
                filter += bit
            elif mask_str[i] == '1':
                setter += bit
                filter += bit
            bit *= 2
        print(f'  - filter {filter:0{bits}b}')
        print(f'  - setter {setter:0{bits}b}')
        masks.append((filter, setter))

        # Read program
        prog = []
        line = f.readline()
        while line and line.startswith('mem'):
            fields = line.split(' = ')
            loc = int(fields[0][4:-1])
            value = int(fields[1])
            print(f'  - Put {value} in {loc}')
            prog.append((loc, value))
            line = f.readline()
        progs.append(prog)

buffer = {}
for i in range(len(progs)):
    print(f'\n=== Executing program {i} ===')
    filter, setter = masks[i]
    for loc, val in progs[i]:
        print(f'  - Executing put {val} in {loc}')
        print(f'    - Unmasked val {val:15}: {val:0{bits}b}')
        print(f'    - Filter       {" " * 15}: {filter:0{bits}b}')
        print(f'    - Setter       {" " * 15}: {setter:0{bits}b}')
        masked = (val & ~filter) | setter
        print(f'    - Masked       {masked:15}: {masked:0{bits}b}')
        buffer[loc] = masked

part1 = sum(buffer.values())
print(f'\nPart1: {part1}\n')

def get_locs(l, m):
    # print(f'    - Get new locs')
    # print(f'      - loc  {l:0{bits}b}')
    # print(f'      - mask {m:0{bits}b}')
    locs = []
    bit_pos = []
    test_bit = 1
    for i in range(bits):
        if ~m & test_bit:
            bit_pos.append(i)
        test_bit <<= 1
    # print(f'      - Mask has {len(bit_pos)} bits for {2**len(bit_pos)} combinations')
    for combo in range(2**len(bit_pos)):
        loc = l
        for j in range(len(bit_pos)):
            # print(f'          - Combo {combo:b} : bit pos {bit_pos[j]}')
            pos_mask = 1 << bit_pos[j]
            # print(f'          - pos mask {pos_mask:0{bits}b}')
            loc &= ~pos_mask
            # print(f'          - Loc after turning off bit {loc:0{bits}b}')
            if combo & 1 << j:
                # print(f'          - Turning on that bit')
                loc |= 1 << bit_pos[j]
                # print(f'          - Loc after turning on bit {loc} {loc:0{bits}b}')
        # print(f'        - Loc {loc} {loc:0{bits}b}')
        locs.append(loc)
    return locs

buffer = {}
for i in range(len(progs)):
    print(f'\n=== Executing program {i} ===')
    filter, setter = masks[i]
    for loc, val in progs[i]:
        print(f'  - Executing put {val} in {loc}')
        # print(f'    - Unmasked val {loc:15}: {loc:0{bits}b}')
        # print(f'    - Filter       {" " * 15}: {filter:0{bits}b}')
        # print(f'    - Setter       {" " * 15}: {setter:0{bits}b}')
        masked = loc | setter
        # print(f'    - Masked       {masked:15}: {masked:0{bits}b}')
        locs = get_locs(masked, filter)
        for new_loc in locs:
            print(f'    - Setting {new_loc} to {val}')
            buffer[new_loc] = val

part2 = sum(buffer.values())
print(f'\nPart 2: {part2}')
