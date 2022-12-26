from aoc.utils import complex_bounds, complex_area

# filename = '2022/day23/test1.txt'
# filename = '2022/day23/test2.txt'
filename = '2022/day23/input.txt'

def print_grid():
    print(f'Bounds: {bounds}')
    for y in range(int(bounds[0].imag), int(bounds[1].imag) + 1):
        if y == 0:
            line = ''
            for x in range(int(bounds[0].real), int(bounds[1].real) + 1):
                if x == 0:
                    line += '+'
                line += '-'
            print(line)
        line = ''
        for x in range(int(bounds[0].real), int(bounds[1].real) + 1):
            if x == 0:
                line += '|'
            line += '#' if complex(x, y) in grid else '.'
        print(line)

grid = []
bounds = None
with open(filename, 'r') as f:
    line = f.readline()
    y = 0
    while line:
        x = 0
        for c in line.strip():
            if c == '#':
                p = complex(x, y)
                grid.append(p)
                bounds = complex_bounds(bounds, p)
            x += 1
        line = f.readline()
        y += 1

checks = [
    [(-1 - 1j), ( 0 - 1j), ( 1 - 1j)],
    [(-1 + 1j), ( 0 + 1j), ( 1 + 1j)],
    [(-1 - 1j), (-1 + 0j), (-1 + 1j)],
    [( 1 - 1j), ( 1 + 0j), ( 1 + 1j)],
]

neighbors = [
    (-1 - 1j), (0 - 1j), (1 - 1j),
    (-1 + 0j),           (1 + 0j),
    (-1 + 1j), (0 + 1j), (1 + 1j)
]

print('== Initial Grid ==')
print_grid()

count = 10000
start_check = 0
for round in range(count):
    print(f'\n== Round {round + 1} ==')
    # print(f'  - Start move is {start_check}')
    proposed = {}
    any_need_to_move = False
    for elf in grid:
        # print(f'  - Checking Elf at {elf}')
        need_to_move = False
        for neighbor in neighbors:
            if (elf + neighbor) in grid:
                # print(f'    - Elf at {elf} has neighbor at {elf + neighbor}')
                need_to_move = True
                any_need_to_move = True
                break
        if need_to_move:
            # print(f'    - {elf} needs to move')
            can_move = False
            for i in range(4):
                check = (start_check + i) % 4
                clear = True
                for j in range(3):
                    if (elf + checks[check][j]) in grid:
                        # print(f'    - Cannot move in dir {check}')
                        clear = False
                        need_to_move = True
                        break
                if clear:
                    # print(f'    - {elf} can move in dir {check}')
                    can_move = True
                    new_elf = elf + checks[check][1]
                    if new_elf in proposed:
                        proposed[new_elf].append(elf)
                    else:
                        proposed[new_elf] = [elf]
                    break
            else:
                # print(f'    - {elf} cannot move at all')
                proposed[elf] = [elf]
        else:
            # print(f'    - No need to move')
            proposed[elf] = [elf]

    if not any_need_to_move:
        print(f'\nNo elves need to move')
        break

    new_grid = []
    bounds = None
    for new_elf, old_elves in proposed.items():
        if len(old_elves) == 1:
            # print(f'  - Elf {old_elves[0]} moved to {new_elf}')
            new_grid.append(new_elf)
            bounds = complex_bounds(bounds, new_elf)
            any_moves = True
        else:
            # print(f'  - Elves proposed same move {old_elves}')
            for old_elf in old_elves:
                new_grid.append(old_elf)
                bounds = complex_bounds(bounds, old_elf)
    grid = new_grid
    # print(f'\n== End of Round {round + 1} ==')
    # print_grid()

    start_check = (start_check + 1) % 4

count_empty = complex_area(bounds) - len(grid)

print(f'\nPart 1: {count_empty}')

if not any_need_to_move:
    print_grid()
    print(f'\nPart 2: {round + 1}')
else:
    print(f'Moves still needed after {round + 1} rounds')