import binarytree as bt

filename = '2020/day18/test1.txt'
# filename = '2020/day18/input.txt'

part1 = None
part2 = None

funcs = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y
}

# Node = [type, parent, ...]
# Node types:
# 0: const
#    [value]
# 1: left op right
#    [left, op, right]
# 2: parentheses
#    [child]

def add_child(node, child):
    child[1] = node
    if node[0] == 1 and node[4] is None:
        node[4] = child
    else:
        node[2] = child

def parse_line(line):
    root = [2, None]
    node = root
    for c in line:
        if c == '(':
            child = [2, node, None]
            add_child(node, child)
            node = child
        elif c == ')':
            # move up to parent
            node = node[1]
        elif c == '*' or c == '+':

            node[3] = c
        else:
            d = int(c)
            child = [0, node, d]
            add_child(node, child)
    return root

sum_results = 0
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        print(f'Eval: {line.strip()}')
        args = []
        ops = []
        need_left = 1
        for c in line.strip():
            if c == ' ':
                pass
            elif c == '(':
                need_left += 1
            elif c == ')':
                right = args.pop()
                left = args.pop()
                op = ops.pop()
                result = funcs[op](left, right)
                args.append(result)
            elif c == '*' or c == '+':
                ops.append(c)
            else:
                d = int(c)
                if need_left:
                    args.append(d)
                    need_left -= 1
                else:
                    left = args.pop()
                    op = ops.pop()
                    result = funcs[op](left, d)
                    args.append(result)
        print(f'  - Result: {args[0]}')
        sum_results += args[0]
        line = f.readline()

part1 = sum_results
print(f'\nPart 1: {part1}\n')

print(f'\nPart 2: {part2}')
