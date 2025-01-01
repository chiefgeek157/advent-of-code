# analyze_rows.py

# filename = 'test1.txt'
filename = 'input.txt'

def read_file(file_path):
    rows = []
    with open(file_path, 'r') as file:
        for line in file:
            rows.append(list(map(int, line.split())))
    return rows

def analyze_row(row):
    differences = [row[i+1] - row[i] for i in range(len(row) - 1)]
    all_positive = all(1 <= diff <= 3 for diff in differences)
    all_negative = all(-3 <= diff <= -1 for diff in differences)
    return all_positive or all_negative

def count_valid_rows(rows):
    count = 0
    for row in rows:
        if analyze_row(row):
            count += 1
    return count

def main():
    rows = read_file(filename)
    valid_row_count = count_valid_rows(rows)
    print(f'Number of valid rows: {valid_row_count}')

if __name__ == "__main__":
    main()