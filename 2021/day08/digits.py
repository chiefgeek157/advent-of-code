import colorama
from colorama import Fore
from colorama import Back
from colorama import Style

filename = "test.txt"
#filename = "input.txt"

colorama.init()

segs_counts = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]

inputs = []
outputs = []
with open(filename, "r") as f:
    line = f.readline()
    while line:
        parts = line.strip().split("|")
        input = parts[0].split()
        output = parts[1].split()
        print(f"inputs {input} outputs {output}")
        inputs.append(input)
        outputs.append(output)
        line = f.readline()

count = 0
for output in outputs:
    for digit in output:
        if len(digit) in [2, 3, 4, 7]:
            count += 1

print(f"Answer: {count}")
