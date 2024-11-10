# filename = '2023/day12/input.txt'
filename = '2023/day12/test1.txt'

def parse_data(segs: list[int], data: str) -> int:
    count = 0
    if len(data) > 0:
        c = data[0]
        count = parse_data(segs, data[1:])
    return count

def main() -> int:
    total = 0
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            fields = line.strip().split()
            data = fields[0]
            segs = fields[1].split(',')
            total += parse_data(segs, data)
            line = f.readline()
    return total

if __name__ == '__main__':
    print(f'Answer: {main()}')
