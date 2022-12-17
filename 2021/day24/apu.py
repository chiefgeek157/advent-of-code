import numpy as np

# instructions = [
#     [0, 1],
#     [3, 1, -1]
# ]
# instructions = [
#     [0, 3],
#     [0, 1],
#     [3, 3, 3],
#     [10, 3, 1]
# ]
# instructions = [
#     [0, 0],
#     [2, 3, 0],
#     [7, 3, 2],
#     [5, 0, 2],
#     [2, 2, 0],
#     [7, 2, 2],
#     [5, 0, 2],
#     [2, 1, 0],
#     [7, 1, 2],
#     [5, 0, 2],
#     [7, 0, 2]
# ]
filename = '2021/day24/input.txt'

model_num = int('9' * 14)

INP = 0
ADD = 1
MUL = 2
DIV = 3
MOD = 4
EQL = 5

regs = {'w': 0, 'x': 1, 'y': 2, 'z': 3}
regs_inv = 'wxyz'
ops = {'inp': INP, 'add': ADD, 'mul': MUL, 'div': DIV, 'mod': MOD, 'eql': EQL}
ops_inv = ['inp', 'add', 'mul', 'div', 'mod', 'eql']

def inst_str(inst):
    res = f'{ops_inv[inst[0]]} {regs_inv[inst[1]]}'
    if inst[0] != 0:
        res += f' {inst[2] if inst[3] else regs_inv[inst[2]]}'
    return res

def alu(instructions, input):
    """Instructions are [op, arg1, arg2, is_const]"""
    reg = [0] * 4
    i = 0
    for inst in instructions:
        print(f'  - Executing instruction {inst_str(inst)} with {reg} and next input at {i}')
        if inst[0] == INP:
            reg[inst[1]] = int(input[i])
            i += 1
        elif inst[0] == ADD:
            reg[inst[1]] += inst[2] if inst[3] else reg[inst[2]]
        elif inst[0] == MUL:
            reg[inst[1]] *= inst[2] if inst[3] else reg[inst[2]]
        elif inst[0] == DIV:
            reg[inst[1]] = int(np.fix(reg[inst[1]]
                / (inst[2] if inst[3] else reg[inst[2]])))
        elif inst[0] == MOD:
            reg[inst[1]] = reg[inst[1]] % (inst[2] if inst[3] else reg[inst[2]])
        elif inst[0] == EQL:
            reg[inst[1]] = 1 if reg[inst[1]] == (
                inst[2] if inst[3] else reg[inst[2]]) else 0
        print(f'    - Registers now {reg}')
    return reg

instructions = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        fields = line.split()
        if fields[0] == 'inp':
            inst = [INP, regs[fields[1]]]
        else:
            op = ops[fields[0]]
            arg1 = regs[fields[1]]
            if fields[2] in 'wxyz':
                arg2 = regs[fields[2]]
                arg3 = False
            else:
                arg2 = int(fields[2])
                arg3 = True
            inst = [op, arg1, arg2, arg3]

        instructions.append(inst)

        line = f.readline()

# print(f'Using instructions:')
# for inst in instructions:
#     print(inst_str(inst))

# reg = alu(instructions, '12345678912345')

max_iter = 1
iter = 0
min_z = 10000000000000
found = None
while found is None and iter < max_iter:
    iter += 1
    model = str(model_num)
    if '0' not in model:
        # print(f'Iter {iter:07} model {model}')
        reg = alu(instructions, model)
        # print(f'  - reg {reg}')
        # print(f'For {model} -> {reg[3]}')
        min_z = min(min_z, reg[3])
        if reg[3] == 0:
            found = model

    model_num -= 1

print(f'Model {found} minz {min_z}')