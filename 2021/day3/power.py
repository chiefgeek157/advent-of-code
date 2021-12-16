#filename = "test.txt"
filename = "input.txt"

gamma = 0
epsilon = 0
bits = None
values = []
with open(filename, "r") as f:
    for line in f:
        binary = line.strip()
        if bits == None:
            bits = len(binary)
            print(f"bits {bits}")
        value = int(binary, 2)
        print(f"binary {binary} int {value:4}")
        values.append(value)

for i in range(0, bits):
    mask = 1 << i
    print(f"mask {mask:0{bits}b}")
    counts = [0, 0]
    for value in values:
        bit = (value & mask) >> i
        print(f"value {value:0{bits}b} bit {bit}")
        counts[bit] += 1
    print(f'counts {counts}')
    if counts[0] > counts[1]:
        epsilon += mask
    elif counts[1] > counts[0]:
        gamma += mask
    else:
        print("ERROR: counts are the same, which is not defined")
        exit(1)
    
print(f"gamma {gamma:0{bits}b} epsilon {epsilon:0{bits}b}")
print(f"answer {gamma * epsilon}")


