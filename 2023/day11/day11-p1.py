import aoc.grid as gr

filename = '2023/day11/input.txt'
# filename = '2023/day11/test1.txt'

def main() -> int:
    # Grid is an array of strings
    w = None
    h = None
    empty_rows = set()
    empty_cols = set()
    grid = []
    with open(filename, 'r') as f:
        line = f.readline().strip()
        if w is None:
            w = len(line)
        row = 0
        empty_rows.update(list(range(len(line))))
        empty_cols.update(list(range(len(line))))
        while line:
            for col in range(len(line.strip())):
                if line[col] == '#':
                    grid.append((col, row))
                    empty_cols.discard(col)
                    empty_rows.discard(row)
            line = f.readline()
            row += 1
    h = row

    # gr.print_sparse_grid(w, h, grid)
    print(f'Empty rows: {empty_rows}')
    print(f'Empty cols: {empty_cols}')

    w += len(empty_cols)
    h += len(empty_rows)

    for i in range(len(grid)):
        cell = grid[i]
        col_incr = 0
        row_incr = 0
        for col in empty_cols:
            if cell[0] >= col:
                col_incr += 1
        for row in empty_rows:
            if cell[1] >= row:
                row_incr += 1
        if col_incr > 0 or row_incr > 0:
            # print(f'Shifting {cell} by {(col_incr, row_incr)}')
            grid[i] = (cell[0] + col_incr, cell[1] + row_incr)

    # gr.print_sparse_grid(w, h, grid)

    # Sum all distances
    sum_dist = 0
    for i in range(len(grid)):
        for j in range(i + 1, len(grid)):
            cell1 = grid[i]
            cell2 = grid[j]
            dx = cell2[0] - cell1[0]
            dy = cell2[1] - cell1[1]
            d = abs(dx) + abs(dy)
            # print(f'Dist from {i+1} {cell1} to {j+1} {cell2} is {d}')
            sum_dist += d

    return sum_dist

if __name__ == '__main__':
    print(f'Answer: {main()}')
