filename = '2015/day19/input.txt'
# filename = '2015/day19/test1.txt'
# filename = '2015/day19/test2.txt'

replacements = []
molecule = None
with open(filename, 'r') as f:
    line = f.readline().strip()
    while line:
        if len(line) < 1:
            break
        fields = line.split()
        replacements.append((fields[0].strip(), fields[2].strip()))

        line = f.readline().strip()

    # read the last line
    molecule = f.readline().strip()
print(f'Replacements: {replacements}')
print(f'Molecule: {molecule}')

outcomes = {}

for i in range(len(molecule)):
    print(f'Starting at char {i}')

    left = molecule[:i]
    right = molecule[i:]
    print(f'left:right {left}:{right}')
    for repl in replacements:
        if right.startswith(repl[0]):
            new_mol = left + right.replace(repl[0], repl[1], 1)
            print(f'For {repl} new: {new_mol}')
            if new_mol not in outcomes:
                outcomes[new_mol] = 1
            else:
                outcomes[new_mol] += 1

print(f'Ans: {len(outcomes)}')