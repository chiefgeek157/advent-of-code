filename = '2015/day23/input.txt'
# filename = '2015/day23/test3.txt'

registers = {'a': 1, 'b': 0}
instructions = []

with open(filename, 'r') as f:
    line = f.readline().strip()
    while line:
        instructions.append(line)
        line = f.readline().strip()

step = 0
i = 0
while True and step < 10000:
    if i < 0 or i >= len(instructions):
        break

    step +=1
    line = instructions[i]

    print(f'Step {step} {registers} [{i}]: {line}')
    instr = line[:3]
    match instr:
        case 'inc':
            reg = line[4]
            registers[reg] += 1
            i += 1
        case 'tpl':
            reg = line[4]
            registers[reg] *= 3
            i += 1
        case 'hlf':
            reg = line[4]
            registers[reg] = int(registers[reg] / 2)
            i += 1
        case 'jmp':
            dist = int(line[4:])
            i += dist
        case 'jie':
            reg = line[4]
            dist = int(line[7:])
            i += dist if registers[reg] % 2 == 0 else 1
        case 'jio':
            reg = line[4]
            dist = int(line[7:])
            i += dist if registers[reg] == 1 else 1
        case _:
            break
