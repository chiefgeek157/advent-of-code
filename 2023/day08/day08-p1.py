filename = '2023/day08/input.txt'
# filename = '2023/day08/test1.txt'
# filename = '2023/day08/test2.txt'

def main() -> int:
    nodes = {}
    with open(filename, 'r') as f:
        line = f.readline()
        path = line.strip()
        print(f'Path is {path}')
        line = f.readline()
        line = f.readline()
        while line:
            node = line[0:3]
            left = line[7:10]
            right = line[12:15]
            print(f'{node} = ({left}, {right})')
            nodes[node] = (left, right)
            line = f.readline()

    node = 'AAA'
    step = 1
    i = 0
    while node != 'ZZZ':
        dir = path[i]
        print(f'Step {step} at node {node}: {nodes[node]}, next step is {i}: {dir}', end=' ')
        if dir == 'L':
            node = nodes[node][0]
        else:
            node = nodes[node][1]
        print(f'=> {node}')
        i = (i + 1) % len(path)
        step += 1
    score = step - 1
    return score

if __name__ == '__main__':
    print(f'Answer: {main()}')
