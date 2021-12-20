import colorama
from colorama import Fore
from colorama import Back
from colorama import Style
import math

#filename = "test.txt"
filename = "input.txt"

points = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

colorama.init()

def score_line(line):
    print(f"Line: {line}")
    score = 0
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
        while len(state) > 0:
            char = state.pop()
            score = score * 5 + points[char]
    print(f"Score {score}")
    return score

scores = []
with open(filename, "r") as f:
    line = f.readline()
    while line:
        score = score_line(line.strip())
        if score > 0:
            scores.append(score)

        line = f.readline()

scores.sort()
print(f"Scores {scores}")
score = scores[int(len(scores)/2)]

print(f"Answer: {score}")