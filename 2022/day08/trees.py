filename = '2022/day08/input.txt'
# filename = '2022/day08/test1.txt'
part2 = False

grid = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        grid.append(line.strip())
        line = f.readline()

w = len(grid[0])
h = len(grid)
total = 2 * ( w + h ) - 4
print(f'Total starts at {total}')
for r in range(1, h - 1):
    for c in range(1, w - 1):
        tree = grid[r][c]
        # print(f'Checking tree [{r}][{c}]: {tree}')
        visible = True
        for rr in range(r):
            # print(f'Comparing to tree [{rr}][{c}]: {grid[rr][c]}')
            if grid[rr][c] >= tree:
                # print(f'Not visible up')
                visible = False
                break
        if not visible:
            visible = True
            for rr in range(r + 1, h):
                # print(f'Comparing to tree [{rr}][{c}]: {grid[rr][c]}')
                if grid[rr][c] >= tree:
                    # print(f'Not visible down')
                    visible = False
                    break
        if not visible:
            visible = True
            for cc in range(c):
                # print(f'Comparing to tree [{r}][{cc}]: {grid[r][cc]}')
                if grid[r][cc] >= tree:
                    # print(f'Not visible left')
                    visible = False
                    break
        if not visible:
            visible = True
            for cc in range(c + 1, w):
                # print(f'Comparing to tree [{r}][{cc}]: {grid[r][cc]}')
                if grid[r][cc] >= tree:
                    # print(f'Not visible right')
                    visible = False
                    break
        if visible:
            # print(f'Visible')
            total += 1

print(f'Part 1: {total}')

max_score = 0
for r in range(1, h - 1):
    for c in range(1, w - 1):
        tree = grid[r][c]
        # print(f'Checking tree [{r}][{c}]: {tree}')
        # print(f'Looking up')
        d_up = 0
        for rr in reversed(range(r)):
            # print(f'Comparing to tree [{rr}][{c}]: {grid[rr][c]}')
            d_up += 1
            if grid[rr][c] >= tree:
                break
        # print(f'Looking down')
        d_down = 0
        for rr in range(r + 1, h):
            # print(f'Comparing to tree [{rr}][{c}]: {grid[rr][c]}')
            d_down += 1
            if grid[rr][c] >= tree:
                break
        # print(f'Looking left')
        d_left = 0
        for cc in reversed(range(c)):
            # print(f'Comparing to tree [{r}][{cc}]: {grid[r][cc]}')
            d_left += 1
            if grid[r][cc] >= tree:
                break
        # print(f'Looking right')
        d_right = 0
        for cc in range(c + 1, w):
            # print(f'Comparing to tree [{r}][{cc}]: {grid[r][cc]}')
            d_right += 1
            if grid[r][cc] >= tree:
                break

        total = d_up * d_down * d_left * d_right
        # print(f'{d_up} * {d_down} * {d_left} * {d_right} = {total}')
        if total > max_score:
            print(f'New max score at [{r}][{c}]: {total}')
            max_score = total

print(f'Part 2: {max_score}')