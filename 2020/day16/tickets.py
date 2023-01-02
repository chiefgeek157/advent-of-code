# filename = '2020/day16/test1.txt'
# filename = '2020/day16/test2.txt'
filename = '2020/day16/input.txt'

part1 = None
part2 = None

fields = {}
tickets = []
with open(filename, 'r') as f:
    print(f'Reading fields')
    line = f.readline().strip()
    while line:
        flds = line.split(':')
        name = flds[0]
        fields[name] = []
        rngs = flds[1].split(' or ')
        for rng in rngs:
            nums = rng.split('-')
            fields[name].append((int(nums[0]), int(nums[1])))
        print(f'  - Field {name} has ranges {fields[name]}')
        line = f.readline().strip()

    print(f'Reading my ticket')
    line = f.readline()
    line = f.readline().strip()
    flds = line.split(',')
    tickets.append([])
    for fld in flds:
        tickets[0].append(int(fld))
    line = f.readline()
    print(f'  - Ticket: {tickets[0]}')

    print(f'Reading other tickets')
    line = f.readline()
    line = f.readline().strip()
    while line:
        flds = line.split(',')
        ticket = []
        tickets.append(ticket)
        for fld in flds:
            ticket.append(int(fld))
        print(f'  - Ticket: {ticket}')
        line = f.readline().strip()

part1 = 0
valid_tickets = [tickets[0]]
print(f'Finding invalid ticket values')
for i in range(1, len(tickets)):
    ticket = tickets[i]
    ticket_valid = True
    for val in ticket:
        val_valid = False
        for name, rngs in fields.items():
            for rng in rngs:
                if val in range(rng[0], rng[1] + 1):
                    val_valid = True
                    break
            if val_valid:
                break
        if not val_valid:
            print(f'  - Ticket {i}: {val} not valid')
            part1 += val
            ticket_valid = False
            break
    if ticket_valid:
        valid_tickets.append(ticket)

print(f'\nPart 1: {part1}\n')

mappings = {}
print(f'There are now {len(valid_tickets)} left out of {len(tickets)}')
print(f'Finding field mappings')
for name, rngs in fields.items():
    print(f'  - Checking field {name}')
    for i in range(len(tickets[0])):
        field_ok = True
        print(f'    - Checking col {i}')
        for j in range(len(valid_tickets)):
            print(f'      - Checking ticket {j}')
            ticket = valid_tickets[j]
            val = ticket[i]
            val_ok = False
            for rng in rngs:
                if val in range(rng[0], rng[1] + 1):
                    print(f'      - Ticket {j} col {i} val {val} is good')
                    val_ok = True
                    break
            if not val_ok:
                print(f'      - Ticket {j} col {i} val {val} does not fit')
                field_ok = False
                break
        if not field_ok:
            print(f'    - Field {name} cannot be col {i}')
        else:
            print(f'    - Field {name} can be col {i}')
            valid_cols = mappings.setdefault(name, [])
            valid_cols.append(i)

print(f'\nMappings: {mappings}')
print('Finalizing mappings')
final_map = {}
while mappings:
    one_map = dict(filter(lambda item: len(item[1]) == 1, mappings.items()))
    print(f'  - Fields with one mapping: {one_map}')
    for one_name, one_cols in one_map.items():
        mappings.pop(one_name)
        print(f'  - Final col for {one_name} is {one_cols[0]}')
        final_map[one_name] = one_cols[0]
        for name, cols in mappings.items():
            if name != one_name and one_cols[0] in cols:
                cols.remove(one_cols[0])

print(f'Finding values for fields starting with "departure"')
part2 = 1
for name, col in final_map.items():
    if name.startswith('departure'):
        print(f'  - {name} in col {col} is {tickets[0][col]}')
        part2 *= tickets[0][col]
print(f'\nPart 2: {part2}')
