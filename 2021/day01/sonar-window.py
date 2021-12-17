with open("sonar.txt", "r") as f:
    increases = 0
    curr_sum = 0
    prev_sum = None
    window_width = 0
    index = 0
    depths = [0, 0, 0]
    for line in f:
        depth = int(line.rstrip())
        depths[index % 3] = depth
        if index >= 2:
            curr_sum = sum(depths)
            if prev_sum != None:
                if curr_sum > prev_sum:
                    increases += 1
            prev_sum = curr_sum
        print("index {0} depth {1} curr_sum {2} prev_sum {3} increases {4}".format(
                index, depth, curr_sum, prev_sum, increases
            ))
        index += 1
    print("Number of downward changes {0}".format(increases))            


