filename = "test.txt"
#filename = "input.txt"

board_size = 5

def read_draws(f):
    line = f.readline().strip()
    draws = []
    for value in line.split(","):
        draws.append(int(value))
    print(f"draws {draws}")
    return draws

def read_board(f):
    board = []
    for row_num in range(board_size):
        #print(f"reading row num {row_num}")
        line = f.readline()
        values = line.strip().split()
        #print(f"row values {values}")
        row = []
        for value in values:
            row.append(int(value))
        board.append(row)
    print(f"{board}")
    return board

def read_boards(f):
    boards = [[[], []]]
    # boards are separated by a blank line
    line = f.readline()
    while line:
        print(f"reading board {len(boards)}")
        boards.append(read_board(f))
        line = f.readline()

def apply_draw(draw, boards):
    for board in boards:
        for row in board:
            for col in range(board_size):
                if row[col] == draw:
                    row[col] *= -1
    return boards

draws = []
boards = [[[],[]]]
with open(filename, "r") as f:
    draws = read_draws(f)
    boards = read_boards(f)

for draw in draws:
    boards = apply_draw(draw, boards)

undrawn_values = []
winning_board = [[], []]
last_draw = 0

undrawn_sum = sum(undrawn_values)
print(f"winning board {winning_board} undrawn_values {undrawn_values} sum {undrawn_sum} last draw {last_draw}")
print(f"answer {undrawn_sum * last_draw}")


