# filename = '2022/day17/test1.txt'
filename = '2022/day17/input.txt'

blocks = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]]
]

jets = ''
with open(filename, 'r') as f:
    jets = f.readline()

def intersects(block, pos):
    h = len(block)
    w = len(block[0])
    if pos[1] < 0:
        # Hit the bottom
        return True
    if pos[1] >= len(board):
        # Have not hit the top of the board yet
        return False
    for i in range(h):
        y = pos[1] + i
        if y >= len(board):
            return False
        for j in range(w):
            x = pos[0] + j
            if block[i][j] == 1 and board[y][x] == 1:
                return True
    return False

def fix(block, pos):
    h = len(block)
    w = len(block[0])
    for i in range(h):
        y = pos[1] + i
        if y == len(board):
            board.append([0] * 7)
        for j in range(w):
            x = pos[0] + j
            board[y][x] = block[i][j]

def print_all(block, pos):
    y_max = max(len(board), pos[1] + len(block))
    for y in range(y_max - 1, -1, -1):
        line = '|'
        for x in range(7):
            if (x >= pos[0] and x < pos[0] + len(block[0])
                and y >= pos[1] and y < pos[1] + len(block)):
                if block[y - pos[1]][x - pos[0]] == 1:
                    line += '@'
                else:
                    if y < len(board):
                        if board[y][x] == 1:
                            line += '#'
                        else:
                            line += '.'
                    else:
                        line += '.'
            elif y < len(board):
                if board[y][x] == 1:
                    line += '#'
                else:
                    line += '.'
            else:
                line += '.'
        line += '|'
        print(line)
    print('+-------+')

board = []
count = 0
block_num = 0
jet_uses = 0
while count < 2022:
    block = blocks[count % len(blocks)]
    h = len(block)
    w = len(block[0])
    pos = (2, len(board) + 3)
    # print(f'\nA new block falls')
    # print_all(block, pos)
    down = False
    while True:
        if down:
            new_pos = (pos[0], pos[1] - 1)
            if intersects(block, new_pos):
                # print(f'\nBlock stops falling')
                fix(block, pos)
                # print_all(block, pos)
                break
            # print(f'\nBlock falls 1 unit')
            down = False
        else:
            jet = jets[jet_uses % len(jets)]
            if jet == '>':
                # print(f'\nJet pushes right')
                new_pos = (min(7 - w, pos[0] + 1), pos[1])
            else:
                # print(f'\nJet pushes left')
                new_pos = (max(0, pos[0] -1), pos[1])
            if intersects(block, new_pos):
                # print(f'\nCannot move due to another block')
                fix(block, pos)
                break
                # new_pos = pos
            down = True
            jet_uses += 1
        pos = new_pos
        # print_all(block, pos)
    count += 1

print(f'Part 1: {len(board)}')

# 3129 was too low
# 3394 was too high difference was whether sliding into a block prevents vertical motion
# ry detecting if vertical motion is still allowed (the '+' in particlar)