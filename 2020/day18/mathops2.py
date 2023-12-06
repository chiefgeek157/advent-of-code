import binarytree as bt

filename = '2020/day18/test1.txt'
# filename = '2020/day18/input.txt'

part1 = None
part2 = None

funcs = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y
}

def eval_node(node) -> int:
    print(f'Evaluating {node}')
    if isinstance(node, int):
        print(f'   Node is a const {node}')
        return node
    left = eval_node(node[0])
    right = eval_node(node[2])
    print(f'   Node has operator {node[1]}')
    val = funcs[node[1]](left, right)
    print(f'   Node has value {val}')
    return val

# Parse a string as a mathematical expression and evaluate the result
def parse_line_ai(line: str) -> int:
    stack = []
    node = []
    for c in line:
        if c == ' ':
            continue
        print(f'Char is "{c}"')
        if c == '(':
            print(f'Pushing node {node}')
            stack.append(node)
            node = []
        elif c == ')':
            child = node
            node = stack.pop()
            print(f'Popped node {node}')
            node.append(child)
        elif c == '+':
            if len(node) == 3:
                child = node
                node = [child]
            node.append(c)
        elif c == '*':
            if len(node) == 3:
                child = node
                node = [child]
            node.append(c)
        else:
            node.append(int(c))
        print(f'Node now: {node}, stack is {stack}')
    return eval_node(node)


def parse_line(line: str) -> int:
    stack = []
    node = []
    in_plus = False
    for c in line:
        if c == ' ':
            continue
        print(f'Char is "{c}"')
        if c == '(':
            print(f'Pushing node {node}')
            stack.append(node)
            node = []
        elif c == ')':
            child = node
            node = stack.pop()
            print(f'Popped node {node}')
            node.append(child)
        elif c == '+':
            if part2:
                right = [node.pop()]
                right.append(c)
                print(f'Pushing {right}, node now {node}')
                stack.append(right)
                in_plus = True
            else:
                if len(node) == 3:
                    child = node
                    node = [child]
                node.append(c)
        elif c == '*':
            if len(node) == 3:
                child = node
                node = [child]
            node.append(c)
        else:
            if in_plus:
                print('Ending plus sequence')
                left = stack.pop()
                left.append(int(c))
                node.append(left)
                in_plus = False
            else:
                node.append(int(c))
        print(f'Node now: {node}, stack is {stack}')
    return eval_node(node)

# sum_results:int = 0
# with open(filename, 'r') as f:
#     line: str = f.readline()
#     while line:
#         print(f'Eval: {line.strip()}')
#         sum_results += parse_line(line.strip())
#         line = f.readline()

# part1 = sum_results
# print(f'\nPart 1: {part1}\n')

part2 = True
sum_results = 0
with open(filename, 'r') as f:
    line: str = f.readline()
    while line:
        print(f'Eval: {line.strip()}')
        sum_results += parse_line(line.strip())
        line = f.readline()

part2 = sum_results
print(f'\nPart 2: {part2}')
