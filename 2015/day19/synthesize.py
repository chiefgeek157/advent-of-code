from sys import maxsize

filename = '2015/day19/input.txt'
# filename = '2015/day19/test3.txt'
# filename = '2015/day19/test4.txt'

OUTCOME = 'e'

replacements = []
molecule = None
with open(filename, 'r') as f:
    line = f.readline().strip()
    while line:
        if len(line) < 1:
            break
        fields = line.split()
        replacements.append((fields[2].strip(), fields[0].strip()))

        line = f.readline().strip()

    # read the last line
    molecule = f.readline().strip()
print(f'Replacements: {replacements}')
print(f'Molecule: {molecule}')

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.cost = maxsize
        self.visited = False

    def __repr__(self) -> str:
        return f'({self.value},{self.cost})'

nodes = {}
def get_node(value):
    global nodes
    if value in nodes:
        return nodes[value]
    node = Node(value)
    nodes[value] = node
    return node

len_outcome = len(OUTCOME)

node = get_node(molecule)
node.cost = 0

work = set()
work.add(node)

# sort the work (only one)

while work:
    # print(f'\nWork: {work}')
    print(f'\nWork: {len(work)}')
    # Sort work based on lowest cost
    node = sorted(work, key=lambda x: x.cost + len(x.value))[0]
    if node.value == OUTCOME:
        break
    # print(f'Node: {node}')
    work.remove(node)
    node.visited = True

    # Generate neighbors
    for i in range(len(node.value)):
        # print(f'Starting at char {i}')

        left = node.value[:i]
        right = node.value[i:]
        # print(f'left:right {left}:{right}')
        for repl in replacements:
            if right.startswith(repl[0]):
                new_value = left + right.replace(repl[0], repl[1], 1)
                # print(f'For {repl} new: {new_value}')
                neighbor = get_node(new_value)
                if not neighbor.visited:
                    if node.cost + 1 < neighbor.cost:
                        # Update lower cost
                        neighbor.cost = node.cost + 1
                    work.add(neighbor)

print(f'Ans: {nodes[OUTCOME]}')