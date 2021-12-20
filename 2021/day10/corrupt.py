import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
import sys

#filename = "test.txt"
filename = "input.txt"

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

colorama.init()

def is_corrupt(line):
    print(f"Line: {line}")
    corrupt = False
    state = []
    for char in line:
        match char:
            case "(":
                state.append(char)
            case "[":
                state.append(char)
            case "{":
                state.append(char)
            case "<":
                state.append(char)
            case ")":
                if state[-1] == "(":
                    state.pop()
                else:
                    corrupt = True
                    break
            case "]":
                if state[-1] == "[":
                    state.pop()
                else:
                    corrupt = True
                    break
            case "}":
                if state[-1] == "{":
                    state.pop()
                else:
                    corrupt = True
                    break
            case ">":
                if state[-1] == "<":
                    state.pop()
                else:
                    corrupt = True
                    break
        print(f"State: {state}")
    if corrupt:
        print(f"Corrupt at {char}")
    elif len(state) > 0:
        print(f"Incomplete")
    return corrupt, char

score = 0
with open(filename, "r") as f:
    line = f.readline()
    while line:
        corrupt, bad_char = is_corrupt(line.strip())
        if corrupt:
            score += scores[bad_char]

        line = f.readline()

print(f"Answer: {score}")