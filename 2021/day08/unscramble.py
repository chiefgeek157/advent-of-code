import colorama
from colorama import Fore
from colorama import Back
from colorama import Style

filename = "test.txt"
#filename = "input.txt"

colorama.init()

segs_counts = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
segs = [
    0b1110111,
    0b0010010,
    0b1011101,
    0b1011011,
    0b0111010,
    0b1101011,
    0b1101111,
    0b1010010,
    0b1111111,
    0b1111011
    # 8687487
]
# d bin       #

# 7 1010010
# 1 0010010 -
#   1000000 b0
#     
# 7 1010010
# 6 1101111
#   *111100 b2
#     
# 6 1101111
# 0 1110111 -
#   *0*1000 b3

# 1 0010010 2
# 4 0111010 4

# 6 1101111 6 7 - 6 -> b2
# 7 1010010
# 8 1111111 7

# 2 1011101 5
# 3 1011011 5
# 5 1101011 5

# 0 1110111 6
# 9 1111011 6

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
