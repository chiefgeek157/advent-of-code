import json

filename = '2015/day12/input.txt'

def visit(item):
    sum = 0
    if isinstance(item, dict):
        dictsum = 0
        ignore = False
        for value in item.values():
            if isinstance(value, str) and value == 'red':
                print(f'Ignore')
                ignore = True
                break
            dictsum += visit(value)
        if not ignore:
            sum += dictsum
    elif isinstance(item, list):
        for value in item:
            sum += visit(value)
    elif isinstance(item, int):
        sum += item
    return sum

with open(filename, 'r') as f:
    doc = json.load(f)
    sum = visit(doc)
    print(f'Ans: {sum}')
