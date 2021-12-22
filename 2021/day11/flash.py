import colorama
from colorama import Fore
from colorama import Back
from colorama import Style

#filename = "test.txt"
filename = "input.txt"

size = 10

def print_grid(grid):
    for x in range(size):
        for y in range(size):
            char = f"{grid[x][y]}"
            if grid[x][y] == 0:
                print(f"{Fore.BLUE}{Style.BRIGHT}", end="")
            elif grid[x][y] > 9:
                char = "#"
            else:
                print(f"{Style.DIM}", end="")
            print(f"{char}{Style.RESET_ALL}", end="")
        print()


def generation(grid):
    # Increment grid by 1
    for x in range(size):
        for y in range(size):
            grid[x][y] += 1
    # print("Incremented grid")
    # print_grid(grid)

    # Find seed flashers (> 9)
    flashers = set()
    for x in range(size):
        for y in range(size):
            if grid[x][y] > 9:
                flashers.add((x, y))
                grid[x][y] = 0
    # print("Seeded grid")
    # print_grid(grid)
    

    flashed = set()
    while len(flashers) > 0:
        # print(f"Flashers {flashers}")
        flasher = flashers.pop()
        flashed.add(flasher)
        neighbors = get_neighbors(grid, flasher)
        for neighbor in neighbors:
            # print(f"Flashed {flashed}")
            # print(f"Neighbor {neighbor}")
            if neighbor not in flashed and neighbor not in flashers:
                grid[neighbor[0]][neighbor[1]] += 1
                # print("Incremented neighbor")
                # print_grid(grid)
                if grid[neighbor[0]][neighbor[1]] > 9:
                    # print("Neighbor flashing")
                    flashers.add(neighbor)
                    # print(f"Flashers {flashers}")
            # else:
            #     print("Neighbor flasher or flashed")

        # print_grid(grid)
        # input("Press enter to continue...")

    for flasher in flashed:
        grid[flasher[0]][flasher[1]] = 0
    return len(flashed)

def get_neighbors(grid, node):
    x = node[0]
    y = node[1]
    neighbors = set()
    if x > 0:
        neighbors.add((x - 1, y))
        if y > 0:
            neighbors.add((x - 1, y - 1))
        if y < len(grid[x]) - 1:
            neighbors.add((x - 1, y + 1))
    if x < len(grid) - 1:
        neighbors.add((x + 1, y))
        if y > 0:
            neighbors.add((x + 1, y - 1))
        if y < len(grid[x]) - 1:
            neighbors.add((x + 1, y + 1))
    if y > 0:
        neighbors.add((x, y - 1))
    if y < len(grid[x]) - 1:
        neighbors.add((x, y + 1))
    return neighbors

grid = []
with open(filename, "r") as f:
    line = f.readline()
    while line:
        row = []
        for char in line.strip():
            row.append(int(char))
        grid.append(row)
        line = f.readline()

print_grid(grid)

total_flashes = 0
for i in range(1000):
    flashes = generation(grid)
    if flashes == (size * size):
        print(f"ALL FLASH at {i + 1}")
        break
    total_flashes += flashes
    print(f"Gen {i:3} Flashes {flashes:3} total {total_flashes:6}")
    print_grid(grid)
    # input("Press enter to continue...")

print(f"Answer: {total_flashes}")