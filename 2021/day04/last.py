import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
import math

#filename = "test.txt"
filename = "input.txt"

board_size = 5

def read_draws(f):
    line = f.readline().strip()
    draws = []
    for value in line.split(","):
        draws.append(int(value))
    print(f"There are {len(draws)} draws {draws}")
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
    print(f"There are {len(boards)} boards")
    return boards, marks

def print_boards(in_boards, in_marks):
    boards = in_boards.copy()
    marks = in_marks.copy()
    rows = math.ceil(len(boards) / 5)
    b = 0
    for row in range(rows):
        print()
        cols = min(5, len(boards))
        # Print headers
        for col in range(cols):
            print(f"{Fore.BLUE}Board {Style.BRIGHT}{b + col:2}{Style.RESET_ALL}          ", end="")
        print()
        for r in range(board_size):
            for col in range(cols):
                for c in range(board_size):
                    if marks[col][r][c]:
                        color = Fore.RED + Style.BRIGHT
                    else:
                        color = Fore.WHITE + Style.NORMAL
                    print(f"{color}{boards[col][r][c]:2}{Style.RESET_ALL} ", end='')
                print("   ", end="")
            print()
        print()
        for col in range(cols):
            boards.pop(0)
            marks.pop(0)
        b += cols

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

def remove_bingo_boards(boards, marks):
    out_boards = []
    out_marks = []
    rem_boards = []
    rem_marks = []
    for b in range(len(boards)):
        if check_mark(marks[b]):
            print(f"BINGO! removing index {b}")
            rem_boards.append(boards[b])
            rem_marks.append(marks[b])
        else:
            out_boards.append(boards[b])
            out_marks.append(marks[b])
    return out_boards, out_marks, rem_boards, rem_marks

colorama.init()

draws = None
boards = None
marks = None
with open(filename, "r") as f:
    draws = read_draws(f)
    boards, marks = read_boards(f)

winning_draw = None
removed_boards = None
removed_marks = None
for draw in draws:
    print(f"\n{Fore.YELLOW}Draw {Style.BRIGHT}{draw}{Style.RESET_ALL}")
    marks = apply_draw(draw, boards, marks)
    print_boards(boards, marks)
    boards, marks, removed_boards, removed_marks = remove_bingo_boards(boards, marks)
    if len(boards) == 0:
        print("Last board finished")
        winning_draw = draw
        break
    # input("Press Enter to continue...")

undrawn_values = []
for r in range(board_size):
    for c in range(board_size):
        if not removed_marks[0][r][c]:
            undrawn_values.append(removed_boards[0][r][c])

undrawn_sum = sum(undrawn_values)
print(f"undrawn_values {undrawn_values} sum {undrawn_sum} winning draw {winning_draw}")
print(f"answer {undrawn_sum * winning_draw}")
