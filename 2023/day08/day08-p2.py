filename = '2023/day08/input.txt'
# filename = '2023/day08/test1.txt'
# filename = '2023/day08/test2.txt'
# filename = '2023/day08/test3.txt'

def is_done(nodes: map, curr: list) -> bool:
    for node in curr:
        if not nodes[node][2]:
            return False
    print(f'All done {curr}')
    return True

def main() -> int:
    nodes = {}
    current_nodes = []
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
            if node[2] == 'A':
                current_nodes.append(node)
            is_end = (node[2] == 'Z')
            value = (left, right, is_end)
            print(f'{node} = {value}')
            nodes[node] = value
            line = f.readline()

    visited_states = set()
    step = 1
    i = 0
    while not is_done(nodes, current_nodes):
        state = (*current_nodes, i)
        if state in visited_states:
            print('Loop at {state}')
            exit(1)
        else:
            visited_states.add(state)
        if step % 10000 == 0:
            print(f'Step {step}')
        # print(f'Current nodes: {current_nodes}')
        dir = path[i]
        # print(f'  Step {step} next dir is {i}: {dir}')
        for j in range(len(current_nodes)):
            node = current_nodes[j]
            # print(f'    Visiting current_nodes[{j}]:{node} = {nodes[node]}', end=' ')
            if dir == 'L':
                current_nodes[j] = nodes[node][0]
            else:
                current_nodes[j] = nodes[node][1]
            # print(f'=> {current_nodes[j]}')
        i = (i + 1) % len(path)
        step += 1
    score = step - 1
    return score

if __name__ == '__main__':
    print(f'Answer: {main()}')
