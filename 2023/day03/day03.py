# filename = '2023/day03/input.txt'
filename = '2023/day03/text1.txt'

def is_symbol(c: str) -> bool:
    return not c.isdigit() and c != '.'

# Open the file and read each line one at a time
with open(filename) as f:
    prior_line = None
    line = f.readline()
    while line:
        for i in range(len(line)):
            # Check if line[i] is a digit
            if line[i].isdigit():
                # See if the prior character or characters on the prior line
                # are sumbols
                if prior_line is not None:
                    if i > 0:
                        if is_symbol(line[i-1])
                    if prior_line[i] == '|' or prior_line[i] == '-':
                        print(line[i])

