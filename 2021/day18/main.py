from snailnum import SnailNum

# filename = '2021/day18/test1.txt'
# filename = '2021/day18/test2.txt'
# filename = '2021/day18/test3.txt'
# filename = '2021/day18/test4.txt'
# filename = '2021/day18/test5.txt'
# filename = '2021/day18/test6.txt'
# filename = '2021/day18/test7.txt'
filename = '2021/day18/test8.txt'

nums = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        num = SnailNum.read(line.strip())
        print(f'Read: {num}')
        nums.append(num)
        line = f.readline()

s = None
for num in nums:
    if s is None:
        s = num
    else:
        s += num
print(f'Sum: {s}')
print(f'Magnitude: {s.magnitude()}')
