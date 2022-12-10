import math

filename = '2022/day05/input.txt'
# filename = '2022/day05/test1.txt'
part2 = True

def print_stacks(stacks):
    h = len(max(stacks, key=lambda x: len(x)))
    # print(f'Height: {h}')
    for i in range(h - 1, -1, -1):
        row = ''
        for stack in stacks:
            if len(stack) >= i + 1:
                row += f'[{stack[i]}] '
            else:
                row += '    '
        print(row)
    row = ''
    for i in range(len(stacks)):
        row += f' {i + 1}  '
    print(row)

stacks = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        line = line[:-1]

        if len(line) == 0:
            pass
        if line.startswith('move'):
            fields = line.split()
            qty = int(fields[1])
            src = int(fields[3]) - 1
            tgt = int(fields[5]) - 1
            print(f'move {qty} from {src + 1} to {tgt + 1}')
            if not part2:
                for i in range(qty):
                    stacks[tgt].append(stacks[src].pop())
            else:
                substack = stacks[src][-qty:]
                stacks[src] = stacks[src][:len(stacks[src]) - qty]
                stacks[tgt] += substack
            print_stacks(stacks)
        elif line.startswith(' 1'):
            # Reverse the stacks
            for i in range(len(stacks)):
                stacks[i] = stacks[i][::-1]
            print_stacks(stacks)
        else:
            stack_idx = 0
            while line:
                # print(f'Line: {line}')
                box = line[:3][1]
                # print(f'Box {box}')
                if stack_idx >= len(stacks):
                    # print(f'Adding stack {stack_idx}')
                    stacks.append([])
                if box != ' ':
                    # print(f'Adding box {box} to stack {stack_idx}')
                    stacks[stack_idx].append(box)
                line = line[4:]
                stack_idx += 1

        line = f.readline()

tops = ''
for stack in stacks:
    tops += stack[-1]

print(f'Ans: {tops}')
