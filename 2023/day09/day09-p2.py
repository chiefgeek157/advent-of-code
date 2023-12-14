filename = '2023/day09/input.txt'
# filename = '2023/day09/test1.txt'

def main() -> int:
    sum_next = 0
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            vals = list(int(x) for x in line.strip().split())

            rows = [vals]
            row = rows[0]
            print(f'Start: {row}')
            while any([x != 0 for x in row]):
                next_row = []
                rows.append(next_row)
                for i in range(len(row) - 1):
                    next_row.append(row[i + 1] - row[i])
                print(f'  Next row: {next_row}')
                row = next_row
            for i in reversed(range(len(rows) - 1)):
                rows[i] = [rows[i][0] - rows[i + 1][0]] + rows[i]
                print(f'  Rows[{i}] now {rows[i]}')
            print(f'  Adding {rows[0][0]}')
            sum_next += rows[0][0]

            line = f.readline()

    return sum_next

if __name__ == '__main__':
    print(f'Answer: {main()}')
