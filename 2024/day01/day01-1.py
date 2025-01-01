# read_and_compare.py

# filename = 'test1.txt'
filename = 'input.txt'

def read_file(file_path):
    column1 = []
    column2 = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.split()
            column1.append(int(values[0]))
            column2.append(int(values[1]))
    return column1, column2

def sort_and_compare(column1, column2):
    column1.sort()
    column2.sort()
    differences = [abs(a - b) for a, b in zip(column1, column2)]
    return sum(differences)

def main():
    column1, column2 = read_file(filename)
    total_difference = sort_and_compare(column1, column2)
    print(f'Total sum of absolute differences: {total_difference}')

if __name__ == "__main__":
    main()
