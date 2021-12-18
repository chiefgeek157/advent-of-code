import colorama
from colorama import Fore
from colorama import Back
from colorama import Style

#filename = "test1.txt"
#filename = "test.txt"
filename = "input.txt"

colorama.init()

# segs_counts = [6, 2, 5, 5, 4, 5, 6, 3, 7, 6]
# segs = [
#     0b1110111,
#     0b0010010,
#     0b1011101,
#     0b1011011,
#     0b0111010,
#     0b1101011,
#     0b1101111,
#     0b1010010,
#     0b1111111,
#     0b1111011
#     # 8687487
# ]
# d bin       #
#
# 1    c  f
# 7  a c  f (7 - 1) = a
# 4   bcd f
# 8  abcdefg
# 2  a cde g
# 3  a cd fg
# 5  ab d fg
# 0  abc efg
# 6  ab defg
# 9  abcd fg
#     |  ||
#    8687497
#     b  ef
#
# 1    c  .  -> c
# 7  . c  .  -> c
# 4   .cd .
# 8  ..cd..g
# 2  . cd. g
# 3  . cd .g
# 5  .. d .g
# 0  ..c ..g
# 6  .. d..g
# 9  ..cd .g
#      |
#      87  7
#      c
#
# 1    .  .
# 7  . .  .
# 4   ..d .  -> d
# 8  ...d..g
# 2  . .d. g
# 3  . .d .g
# 5  .. d .g
# 0  ... ..g -> g
# 6  .. d..g
# 9  ...d .g
#       7  7
#
# Done

digits = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9"
}

sum = 0
with open(filename, "r") as fin:
    line = fin.readline()
    while line:
        map = {}
        counts = {}
        remainder = set(["a", "b", "c", "d", "e", "f", "g"])
        parts = line.strip().split("|")
        inputs = parts[0].split()
        outputs = parts[1].split()
        print(f"inputs {inputs} outputs {outputs}")
        lengths = {}
        for i in range(len(inputs)):
            length = len(inputs[i])
            if length not in lengths.keys():
                lengths[length] = []
            lengths[length].append(i)            
        print(f"lengths {lengths}")

        for input in inputs:
            for c in input:
                if c not in counts.keys():
                    counts[c] = 0
                counts[c] += 1
        print(f"counts {counts}")
        counts = {value: key for (key, value) in counts.items()}
        print(f"counts {counts}")

        # counts[6] = b
        # counts[4] = e
        # counts[9] = f
        b = counts[6]
        e = counts[4]
        f = counts[9]
        map[b] = "b"
        map[e] = "e"
        map[f] = "f"
        remainder = remainder - set([b, e, f])
        print(f"map {map}")
        print(f"remainder {remainder}")

        # d7 - d1 = a
        d1 = set(inputs[lengths[2][0]])
        d7 = set(inputs[lengths[3][0]])
        print(f"d1 {d1} d7 {d7}")
        a = (d7 - d1).pop()
        map[a] = "a"
        remainder = remainder - set(a)
        print(f"map {map}")
        print(f"remainder {remainder}")

        # d1 - f = c
        c = (d1 - set(f)).pop()
        map[c] = "c"
        remainder = remainder - set(c)
        print(f"map {map}")
        print(f"remainder {remainder}")

        # d = d4 - bcf
        d4 = set(inputs[lengths[4][0]])
        d = (d4 - set([b, c, f])).pop()
        map[d] = "d"
        remainder = remainder - set(d)
        print(f"map {map}")
        print(f"remainder {remainder}")

        # g is the last unassigned value
        if len(remainder) != 1:
            print(f"ERROR: remainder has {len(remainder)} values")
            exit(1)
        g = remainder.pop()
        map[g] = "g"
        print(f"map {map}")

        numlist = []
        for output in outputs:
            charlist = []
            for c in output:
                charlist.append(map[c])
            charlist.sort()
            chars = ''.join(charlist)
            print(f"chars {chars}")
            digit = digits[chars]
            numlist.append(digit)
        num = int(''.join(numlist))
            
        print(f"num {num}")
        sum += num

        line = fin.readline()

print(f"Answer: {sum}")