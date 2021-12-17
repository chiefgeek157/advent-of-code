with open("sonar.txt", "r") as f:
    depth_count = 0
    increase_count = 0
    decrease_count = 0
    same_count = 0
    prev_depth = None
    for line in f:
        depth = int(line.rstrip())
        depth_count += 1
        increased = "same"
        if prev_depth != None:
            if depth > prev_depth:
                increase_count += 1
                increased = "increased"
            elif depth < prev_depth:
                decrease_count += 1
                increased = "decreased"
            else:
                same_count += 1
        else:
            increased = "first reading"
        print("{0}: {1} {2} total increases {3}".format(depth_count, depth, increased, increase_count))
        prev_depth = depth
    print("Number of downward changes {0}".format(increase_count))            
    print("Number of upward   changes {0}".format(decrease_count))            
    print("Number of same     changes {0}".format(same_count))       
    print("total {0}".format(increase_count+decrease_count+same_count+1))     


