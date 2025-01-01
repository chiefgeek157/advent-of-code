# similarity_score.py

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

def calculate_similarity_score(column1, column2):
    similarity_score = 0
    for value in column1:
        count = column2.count(value)
        similarity = count * value
        similarity_score += similarity
    return similarity_score

def main():
    column1, column2 = read_file(filename)
    score = calculate_similarity_score(column1, column2)
    print(f'Similarity score: {score}')

if __name__ == "__main__":
    main()