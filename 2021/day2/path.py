with open("commands.txt", "r") as f:
    position = [0, 0]
    for line in f:
        fields = line.strip().split()
        command = fields[0]
        dist = int(fields[1])
        if command == "forward":
            position[0] += dist
        elif command == "up":
            position[1] -= dist
        elif command == "down":
            position[1] += dist
        else:
            print("Unexpected command {0}".format(command))
            exit(1)

        print("{0}".format(position))

    print("answer {0}".format(position[0] * position[1]))


