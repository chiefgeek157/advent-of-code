# filename = '2022/day17/test1.txt'
filename = '2022/day17/input.txt'

blocks = [
    [(0+0j), (1+0j), (2+0j), (3+0j)],
    [(1+0j), (0+1j), (1+1j), (2+1j), (1+2j)],
    [(0+0j), (1+0j), (2+0j), (2+1j), (2+2j)],
    [(0+0j), (0+1j), (0+2j), (0+3j)],
    [(0+0j), (1+0j), (0+1j), (1+1j)]
]

jets = ''
with open(filename, 'r') as f:
    jets = f.readline()

# # Find patterns in jets
# for l in range(2, int(len(jets) / 2) + 1):
#     print(f'Checking repeat at length {l}')
#     if len(jets) % l != 0:
#         print(f'{l} is not a factor of {len(jets)}')
#         continue
#     matches = True
#     for i in range(int(len(jets) / l)):
#         for j in range(l):
#             if jets[j] != jets[i * l + j]:
#                 print(f'For pattern length {l}, [{j}] {jets[j]} != [{i * l + j}] {jets[i * l + j]}')
#                 matches = False
#                 break
#         if not matches:
#             break
#     if matches:
#         print(f'Found a repeat at length {l}')

def intersects(board, block):
    return (b in board for b in block)

def fix(board, block):
    for b in block:
        board.add(block)

def print_window(block=[]):
    y_max = int(max([b.imag for b in (board + block)]))
    y_min = int(max(-1, min(top.imag,
        min([b.imag for b in block], default=top.imag)) - 8))
    for y in range(y_max, y_min - 1, -1):
        if y == -1:
            line = '+-------+'
        else:
            line = '|'
            for x in range(7):
                pos = complex(x, y)
                line += '@' if pos in block else '#' if pos in board else '.'
            line += '|'
        print(line)

def print_all(block=[]):
    y_max = int(max([b.imag for b in (board + block)]))
    for y in range(y_max, -1 - 1, -1):
        if y == -1:
            line = '+-------+'
        else:
            line = '|'
            for x in range(7):
                pos = complex(x, y)
                line += '@' if pos in block else '#' if pos in board else '.'
            line += '|'
        print(line)

board = []
count = 0
top = (0-0j)
jet_uses = 0
states = []
repeats = []
repeat_tops = []
filled_repeats = False
repeating = False
# A state is (block, jet, col_depth) where col_depth is the count
# down from top
while count < 2022 and not filled_repeats:
    block = blocks[count % len(blocks)]
    pos = top + (2+3j)
    block = [b + pos for b in block]

    # print(f'\nA new block falls')
    # print_window(block)
    while True:

        # Move left of right
        move = (1+0j) if jets[jet_uses % len(jets)] == '>' else (-1+0j)
        new_block = [b + move for b in block]
        if not any([b in board or b.real < 0 or b.real > 6 for b in new_block]):
            block = new_block
        # print(f'\nAfter jet')
        # print_window(block)

        # Now move down
        new_block = [b + (0-1j) for b in block]
        if not any([b in board or b.imag < 0 for b in new_block]):
            block = new_block
            # print(f'\nAfter down')
            # print_window(block)
        else:
            # Block can no longer move
            board += block
            top = complex(0, max([b.imag for b in board]) + 1)
            # print(f'\nAfter block stops, top now {top}')
            # print_window()

            # Look for a repeating pattern
            cols = [list(filter(lambda p: p.real == x, board)) for x in range(7)]
            col_depths = [int(top.imag - max([p.imag for p in cols[x]], default=0) - 1) for x in range(7)]
            state = ((count % len(blocks)), jets[jet_uses % len(jets)], col_depths)
            if state in states:
                if repeating:
                    if state in repeats:
                        print(f'Found first repeat of repeats {state}')
                        filled_repeats = True
                    else:
                else:
                    print(f'Starting list of repeats {state}')
                    repeating = True
                    repeats.append(state)
                    repeat_tops.append(int(top.imag))
            else:
                print(f'Adding new state {state}')
                states.append(state)
            break

        jet_uses += 1
    count += 1

# print_all()
# print(f'Part 1: {int(top.imag)}')

print(f'Ready to fill the remainder with repeats from {count}')

print(f'Repeats: {repeats}')
print(f'Tops: {repeat_tops}')