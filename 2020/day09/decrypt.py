# filename = '2020/day09/test1.txt'
filename = '2020/day09/input.txt'

preamble = 0
nums = []
with open(filename, 'r') as f:
    line = f.readline()
    preamble = int(line.split(':')[1])
    print(f'Preamble is {preamble}')
    line = f.readline()
    while line:
        nums.append(int(line))
        line = f.readline()

bad_num = None
bad_i = None
for i in range(preamble, len(nums)):
    num = nums[i]
    found = False
    for j in range(i - preamble, i - 1):
        part1 = nums[j]
        part2 = num - part1
        if part2 in nums[j + 1:i]:
            found = True
            break
    if not found:
        bad_num = num
        bad_i = i
        break

print(f'\nPart 1: {bad_num}\n')

start_pos = None
end_pos = None
for i in range(bad_i - 1):
    sum = 0
    j = i
    while sum <= bad_num:
        sum += nums[j]
        if sum == bad_num:
            start_pos = i
            end_pos = j
            print(f'Start pos {start_pos} end pos {end_pos}')
            break
        j += 1
    if start_pos is not None:
        break

part2 = None
if start_pos is not None:
    subset = nums[start_pos:end_pos + 1]
    print(f'Range {subset}')
    min_num = min(subset)
    max_num = max(subset)
    part2 = min_num + max_num
print(f'\nPart 2: {part2}')
