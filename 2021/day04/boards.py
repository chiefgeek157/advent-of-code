import colorama
from colorama import Fore
from colorama import Back
from colorama import Style

#filename = "test.txt"
filename = "input.txt"

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
    mark = []
    for r in range(board_size):
        #print(f"reading row num {row_num}")
        line = f.readline()
        values = line.strip().split()
        #print(f"row values {values}")
        value_row = []
        mark_row = []
        for c in range(board_size):
            value_row.append(int(values[c]))
            mark_row.append(False)
        board.append(value_row)
        mark.append(mark_row)
    print_board(board, mark)
    return board, mark

def read_boards(f):
    boards = []
    marks = []
    # boards are separated by a blank line
    line = f.readline()
    while line:
        print(f"{Fore.BLUE}Reading board {Style.BRIGHT}{len(boards)}{Style.RESET_ALL}")
        board, mark = read_board(f)
        boards.append(board)
        marks.append(mark)
        line = f.readline()
    return boards, marks

def print_board(board, mark):
    for r in range(board_size):
        for c in range(board_size):
            if mark[r][c]:
                color = Fore.RED + Style.BRIGHT
            else:
                color = Fore.WHITE + Style.NORMAL
            print(f"{color}{board[r][c]:3}{Style.RESET_ALL}", end='')
        print()

def print_boards(boards, marks):
    for b in range(len(boards)):
        print()
        print(f"{Fore.BLUE}Board {Style.BRIGHT}{b}{Style.RESET_ALL}")
        print_board(boards[b], marks[b])

def apply_draw(draw, boards, marks):
    for b in range(len(boards)):
        for r in range(board_size):
            for c in range(board_size):
                if boards[b][r][c] == draw:
                    marks[b][r][c] = True
    return marks

def check_mark(mark):
    for i in range(board_size):
        found_row = True
        found_col = True
        for j in range(board_size):
            # Check rows
            if not mark[i][j]:
                found_row = False
            if not mark[j][i]:
                found_col = False
            if not found_row and not found_col:
                # This row and col both failed
                break
        if found_row or found_col:
            print(f"Found bingo: found row {found_row} found col {found_col}")
            return True
    return False

def check_boards(boards, marks):
    for b in range(len(boards)):
        if check_mark(marks[b]):
            return b
    return False

colorama.init()

draws = None
boards = None
marks = None
with open(filename, "r") as f:
    draws = read_draws(f)
    boards, marks = read_boards(f)

winning_index = None
winning_draw = None
for draw in draws:
    print(f"\n{Fore.YELLOW}Draw {Style.BRIGHT}{draw}{Style.RESET_ALL}")
    marks = apply_draw(draw, boards, marks)
    print_boards(boards, marks)
    winning_index = check_boards(boards, marks)
    if winning_index:
        winning_draw = draw
        print(f"BINGO! draw {draw}")
        print_board(boards[winning_index], marks[winning_index])
        break

if winning_index is None:
    print("NO WINNER :(")
    exit(1)

undrawn_values = []
for r in range(board_size):
    for c in range(board_size):
        if not marks[winning_index][r][c]:
            undrawn_values.append(boards[winning_index][r][c])

undrawn_sum = sum(undrawn_values)
print(f"undrawn_values {undrawn_values} sum {undrawn_sum} winning draw {winning_draw}")
print(f"answer {undrawn_sum * winning_draw}")
