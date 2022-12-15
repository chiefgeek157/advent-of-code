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
ADD_CONST = 1
ADD_REG = 2
MUL_CONST = 3
MUL_REG = 4
DIV_CONST = 5
DIV_REG = 6
MOD_CONST = 7
MOD_REG = 8
EQL_CONST = 9
EQL_REG = 10

def alu(instructions, input):
    reg = [0] * 4
    i = 0
    for inst in instructions:
        print(f'  - Executing instruction {inst} with reg {reg}')
        if inst[0] == INP:
            reg[inst[1]] = int(input[i])
            i += 1
        elif inst[0] == ADD_CONST:
            reg[inst[1]] += inst[2]
        elif inst[0] == ADD_REG:
            reg[inst[1]] += reg[inst[2]]
        elif inst[0] == MUL_CONST:
            reg[inst[1]] *= inst[2]
        elif inst[0] == MUL_REG:
            reg[inst[1]] *= reg[inst[2]]
        elif inst[0] == DIV_CONST:
            reg[inst[1]] = int(np.fix(reg[inst[1]] / inst[2]))
        elif inst[0] == DIV_REG:
            reg[inst[1]] *= int(np.fix(reg[inst[1]] / reg[inst[2]]))
        elif inst[0] == MOD_CONST:
            reg[inst[1]] = reg[inst[1]] % inst[2]
        elif inst[0] == MOD_REG:
            reg[inst[1]] = reg[inst[1]] % reg[inst[2]]
        elif inst[0] == EQL_CONST:
            reg[inst[1]] = 1 if reg[inst[1]] == inst[2] else 0
        elif inst[0] == EQL_REG:
            reg[inst[1]] = 1 if reg[inst[1]] == reg[inst[2]] else 0
        print(f'    - {reg}')
    return reg


max_iter = 1
iter = 0
found = False
while not found and iter < max_iter:
    iter += 1
    model = str(model_num)
    if '0' not in model:
        print(f'Iter {iter:07} model {model}')
        reg = alu(instructions, model)
        print(f'  - reg {reg}')

    model_num -= 1
