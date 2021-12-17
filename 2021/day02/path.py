#filename = "test.txt"
filename = "input.txt"

with open(filename, "r") as f:
    position = [0, 0]
    for line in f:
        fields = line.strip().split()
        command = fields[0]
        dist = int(fields[1])
        match command:
            case "forward":
                position[0] += dist
            case "up":
                position[1] -= dist
            case "down":
                position[1] += dist
            case _:
                print("Unexpected command {0}".format(command))
                exit(1)

        print("{0}".format(position))

    print("answer {0}".format(position[0] * position[1]))


