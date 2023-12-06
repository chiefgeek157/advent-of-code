filename = '2023/day03/input.txt'
# filename = '2023/day03/test1.txt'

def is_symbol(c: str) -> bool:
    return not c.isdigit() and c != '.'

# Open the file and read each line one at a time
with open(filename) as f:
    # Map of interesting coordinates
    # Keys are tuples of (row, col)
    # Values are a map with interesting values
    coords = {}

    row = 0
    line = f.readline().strip()
    while line:
        print(f'Line {row}: {line}')
        for col in range(len(line)):
            char = line[col]
            prev_item = coords[(row, col-1)] if col > 0 else None
            coord = (row, col)
            item = {}
            coords[coord] = item

            if char.isdigit():
                print(f'   Found digit {char} at {coord}')
                item['type'] = 'digit'
                item['char'] = char
                if prev_item is not None:
                    if prev_item['type'] == 'digit':
                        print(f'      This digit is not the head of a number')
                        item['head'] = prev_item['head']
                        item['head']['value'] = item['head']['value'] * 10 + int(char)
                    elif prev_item['type'] == 'symbol':
                        print(f'      Previous item is a symbol, this number is valid')
                        item['head'] = item
                        item['value'] = int(char)
                        item['valid'] = True
                    else:
                        print(f'      This digit is the head of a number')
                        item['head'] = item
                        item['value'] = int(char)
                        item['valid'] = False
                else:
                    print(f'      This digit is the head of a number')
                    item['head'] = item
                    item['value'] = int(char)
                    item['valid'] = False

                if not item['head']['valid']:
                    for prev_col in range(col-1, col+2):
                        print(f'      Checking previous row {row-1}, column {prev_col}')
                        other_item = coords.get((row-1, prev_col), None)
                        if other_item is not None and other_item['type'] == 'symbol':
                            print(f'         Found symbol {other_item["char"]} at {row-1}, {prev_col}')
                            item['head']['valid'] = True
                            break
            elif line[col] == '.':
                item['type'] = 'empty'
            else:
                print(f'   Found symbol {char} at {coord}')
                item['type'] = 'symbol'
                item['char'] = char
                if prev_item is not None:
                    if prev_item['type'] == 'digit':
                        print(f'      Previous item is a digit')
                        prev_item['head']['valid'] = True

                for prev_col in range(col-1, col+2):
                    print(f'      Checking previous row {row-1}, column {prev_col}')
                    other_item = coords.get((row-1, prev_col), None)
                    if other_item is not None and other_item['type'] == 'digit':
                        print(f'         Found digit {other_item["char"]} at {row-1}, {prev_col}')
                        other_item['head']['valid'] = True

        line = f.readline().strip()
        row += 1

    sum_valid = 0
    for coord, item in coords.items():
        if item['type'] == 'digit' and item['head'] == item and item['valid']:
            print(f'Valid item[{coord}]: {item["value"]}')
            sum_valid += item['value']

    print(f'Sum of valid items: {sum_valid}')
