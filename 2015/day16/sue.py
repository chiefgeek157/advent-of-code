filename = '2015/day16/input.txt'
# filename = '2015/day16/test1.txt'

data = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""

criteria = {}
for line in data.splitlines():
    fields = line.strip().split(':')
    criteria[fields[0]] = int(fields[1])
print(f'criteria: {criteria}')

with open(filename, 'r') as f:
    line = f.readline()
    sue = 1
    while line:
        fields = line.strip()[line.find(':') + 1:].split(',')
        # print(f'fields: {fields}')
        matches = True
        for field in fields:
            props = field.split(':')
            name = props[0].strip()
            value = int(props[1])
            match name:
                case 'cats' | 'trees':
                    matches = (value > criteria[name])
                case 'pomeranians' | 'goldfish':
                    matches = (value < criteria[name])
                case _:
                    matches = (value == criteria[name])
            if not matches:
                break

        if matches:
            print(f'Found match with Sue {sue}: {fields}')
            break

        sue += 1
        line = f.readline()
