filename = '2023/day03/input.txt'
# filename = '2023/day03/test1.txt'

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
            prev_coord = (row, col-1)
            prev_item = coords.get(prev_coord, None)
            coord = (row, col)
            item = {}

            if char.isdigit():
                print(f'   Found digit {char} at {coord}')
                coords[coord] = item
                item['type'] = 'digit'
                if prev_item is not None:
                    if prev_item['type'] == 'digit':
                        print(f'      This digit is not the head of a number')
                        item['head'] = prev_item['head']
                        coords[item['head']]['value'] = coords[item['head']]['value'] * 10 + int(char)
                    elif prev_item['type'] == 'gear':
                        print(f'      This digit is the head of a number and next to a gear')
                        item['head'] = coord
                        item['value'] = int(char)
                        prev_item['nums'].add(coord)
                    else:
                        print(f'      This digit is the head of a number')
                        item['head'] = coord
                        item['value'] = int(char)
                else:
                    print(f'      This digit is the head of a number')
                    item['head'] = coord
                    item['value'] = int(char)

                for prev_col in range(col-1, col+2):
                    print(f'      Checking previous row {row-1}, column {prev_col}')
                    other_item = coords.get((row-1, prev_col), None)
                    if other_item is not None and other_item['type'] == 'gear':
                        print(f'         Found gear at {row-1}, {prev_col}')
                        other_item['nums'].add(item['head'])
            elif line[col] == '*':
                print(f'   Found gear at {coord}')
                coords[coord] = item
                item['type'] = 'gear'
                item['nums'] = set()
                if prev_item is not None:
                    if prev_item['type'] == 'digit':
                        print(f'      Previous item is a digit')
                        item['nums'].add(prev_item['head'])

                for prev_col in range(col-1, col+2):
                    print(f'      Checking previous row {row-1}, column {prev_col}')
                    other_coord = (row-1, prev_col)
                    other_item = coords.get(other_coord, None)
                    if other_item is not None and other_item['type'] == 'digit':
                        print(f'         Found number at {other_item["head"]}')
                        item['nums'].add(other_item['head'])

        line = f.readline().strip()
        row += 1

    sum_ratios = 0
    for coord, item in coords.items():
        if item['type'] == 'gear':
            print(f'Checking gear at {coord}: nums = {item["nums"]}', end=' ')
            nums = list(coords[x]['value'] for x in item['nums'])
            if len(nums) == 2:
                print(f'nums = {nums} *** VALID ***')
                ratio = nums[0] * nums[1]
                sum_ratios += ratio
            else:
                print(f'nums = {nums} INVALID')

    print(f'Sum of ratios: {sum_ratios}')
