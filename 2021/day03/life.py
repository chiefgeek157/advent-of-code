#filename = "test.txt"
filename = "input.txt"

def remove_values(list, mask, keep_max ):
    if len(list) == 1:
        print("no change")
        return list
    piles = [[],[]]
    for value in list:
        bit = 0 if (value & mask) == 0 else 1
        print(f"value {value} {value:0{bits}b} pile {bit}")
        piles[bit].append(value)
    print(f"{piles}")

    if len(piles[1]) - len(piles[0]) >= 0:
        if keep_max:
            print("keep pile 1")
            return piles[1]
        else:
            print("keep pile 0")
            return piles[0]
    else:
        if keep_max:
            print("keep pile 0")
            return piles[0]
        else:
            print("keep pile 1")
            return piles[1]

bits = None
o2_values = []
with open(filename, "r") as f:
    for line in f:
        binary = line.strip()
        if bits == None:
            bits = len(binary)
            print(f"bits {bits}")
        value = int(binary, 2)
        print(f"binary {binary} int {value:4}")
        o2_values.append(value)

co2_values = o2_values.copy()

for i in range(bits, 0, -1):
    mask = 1 << (i - 1)
    print(f"mask {mask:0{bits}b}")

    o2_values = remove_values(o2_values, mask, True)
    co2_values = remove_values(co2_values, mask, False)

    if len(o2_values) == 1 and len(co2_values) == 1:
        break
    
print(f"o2 {o2_values[0]:0{bits}b} {o2_values[0]} co1 {co2_values[0]:0{bits}b} {co2_values[0]}")
print(f"answer {o2_values[0] * co2_values[0]}")


