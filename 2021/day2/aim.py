#filename = "test.txt"
filename = "input.txt"

with open(filename, "r") as f:
    position = [0, 0]
    aim = 0
    for line in f:
        fields = line.strip().split()
        command = fields[0]
        value = int(fields[1])
        if command == "forward":
            position[0] += value
            position[1] += aim * value
        elif command == "up":
            aim -= value
        elif command == "down":
            aim += value
        else:
            print("Unexpected command {0}".format(command))
            exit(1)

        print("command {0} value {1}: pos {2} aim {3}".format(command, value, position, aim))

    print("answer {0}".format(position[0] * position[1]))


