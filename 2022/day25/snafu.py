import math

def s2d(s):
    d = 0
    x = len(s) - 1
    for c in s:
        if c == '=':
            d -= 2 * 5**x
        elif c == '-':
            d -= 5**x
        else:
            d += int(c) * 5**x
        x -= 1
    return d

def d2s(d):
    if d == 0:
        return '0'
    num_digits = int(math.log(d, 5))
    digits = []
    for x in range(num_digits, -1, -1):
        n = int(d / 5**x)
        digits.append(n)
        d -= n * 5**x
    digits = digits[::-1]
    digits.append(0)
    s = ''
    for i in range(len(digits)):
        n = digits[i]
        carry = False
        if n == 3:
            s += '='
            carry = True
        elif n == 4:
            s += '-'
            carry = True
        else:
            s += str(n)
        if carry:
            j = i
            while digits[j+1] == 4:
                digits[j+1] = 0
                j += 1
            digits[j+1] += 1
    s = s[::-1]
    if s.startswith('0'):
        s = s[1:]
    return s

def test1():
    filename = '2022/day25/unittest1.txt'
    with open(filename, 'r') as f:
        line = f.readline()
        line = f.readline()
        while line:
            fields = line.split()
            res = s2d(fields[0])
            print(f'{fields[0]} == {fields[1]}: {res} {res == int(fields[1])}')
            line = f.readline()

def test2():
    filename = '2022/day25/unittest2.txt'
    with open(filename, 'r') as f:
        line = f.readline()
        line = f.readline()
        while line:
            fields = line.split()
            res = d2s(int(fields[0]))
            print(f'{fields[0]} == {fields[1]}: {res} {res == fields[1]}')
            line = f.readline()

# filename = '2022/day25/test1.txt'
filename = '2022/day25/input.txt'

test1()
test2()

sum_s = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        s = line.strip()
        print(f'Converting {s}')
        res = s2d(s)
        sum_s += res
        line = f.readline()

print(f'\nSum: {sum_s}')
res = d2s(sum_s)

print(f'\nPart 1: {res}')
