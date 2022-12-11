from functools import reduce
from operator import mul

filename = '2022/day11/input.txt'
# filename = '2022/day11/test1.txt'
part2 = True

monkey_items = []
handle_counts = []
operators = []
operands = []
test_values = []
true_monkeys = []
false_monkeys = []

with open(filename, 'r') as f:
    i = None
    line = f.readline()
    while line:
        line = line.strip()
        if len(line) == 0:
            i = None
            print()
        elif i is None:
            fields = line.split()
            i = int(fields[1][:-1])
            monkey_items.append([])
            handle_counts.append(0)
            print(f'Monkey {i}:')
        else:
            if line.startswith('Starting'):
                fields = line.split(':')
                items = fields[1].split(',')
                for item in items:
                    monkey_items[i].append(int(item))
                print(f'   Monkey {i} starts with {monkey_items[i]}')
            elif line.startswith('Operation'):
                fields = line.split(':')
                ops = fields[1].split()
                if ops[3] == '+':
                    val = int(ops[4])
                    operators.append(ops[3])
                    operands.append(val)
                    print(f'   Monkey {i} operation = old + {val}')
                elif ops[4] == 'old':
                    operators.append('^')
                    operands.append(None)
                    print(f'   Monkey {i} operation = old * old')
                else:
                    val = int(ops[4])
                    operators.append(ops[3])
                    operands.append(val)
                    print(f'   Monkey {i} operation = old * {val}')
            elif line.startswith('Test'):
                fields = line.split()
                test_values.append(int(fields[3]))
                print(f'   Monkey {i} test divisible by {fields[3]}:')
            elif line.startswith('If true'):
                fields = line.split()
                true_monkeys.append(int(fields[5]))
                print(f'      Monkey {i} if true  throw to monkey {fields[5]}')
            else:
                fields = line.split()
                false_monkeys.append(int(fields[5]))
                print(f'      Monkey {i} if false throw to monkey {fields[5]}')

        line = f.readline()

max_rounds = 10000 if part2 else 20
num_monkeys = len(monkey_items)
max_val = reduce(mul, test_values)
print(f'Max value: {max_val}')

for round in range(1, max_rounds + 1):
    print(f'\n\n==== ROUND {round} ====')

    for monkey in range(num_monkeys):
        print(f'\nMonkey {monkey}:')
        for val in monkey_items[monkey]:
            handle_counts[monkey] += 1
            print(f'  Monkey inspects an item with a worry level of {val}')
            if operators[monkey] == '+':
                new_val = val + operands[monkey]
                print(f'    Worry level increases by {operands[monkey]} to {new_val}.')
            elif operators[monkey] == '*':
                new_val = val * operands[monkey]
                print(f'    Worry level is multiplied by {operands[monkey]} to {new_val}.')
            else:
                new_val = val * val
                print(f'    Worry level is multiplied by itself to {new_val}.')
            if part2:
                new_val = new_val % max_val
                print(f'    New worry level % {max_val} is {new_val}')
            else:
                new_val = int(new_val / 3)
                print(f'    New worry level / 3 is {new_val}')
            divisiible = (new_val % test_values[monkey] == 0)
            print(f'    New worry level {"is" if divisiible else "is not"} divisible by {test_values[monkey]}')
            new_monkey = true_monkeys[monkey] if divisiible else false_monkeys[monkey]
            monkey_items[new_monkey].append(new_val)
            print(f'    Item with worry level {new_val} is thrown to monkey {new_monkey}')
        monkey_items[monkey] = []

    print(f'\nAfter ROUND {round}\n  Items:')
    for i in range(num_monkeys):
        print(f'    Monkey {i}: {monkey_items[i]}')
    print(f'  Handle counts:')
    for i in range(num_monkeys):
        print(f'    Monkey {i}: {handle_counts[i]}')

sorted_counts = sorted(handle_counts, reverse=True)
monkey_business = sorted_counts[0] * sorted_counts[1]

print(f'Part 1: {monkey_business}')