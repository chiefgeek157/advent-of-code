# --- Day 3: Squares With Three Sides ---
# Now that you can think clearly, you move deeper into the labyrinth of
# hallways and office furniture that makes up this part of Easter Bunny HQ.
# This must be a graphic design department; the walls are covered in
# specifications for triangles.

# Or are they?

# The design document gives the side lengths of each triangle it describes,
# but... 5 10 25? Some of these aren't triangles. You can't help but mark the
# impossible ones.

# In a valid triangle, the sum of any two sides must be larger than the
# remaining side. For example, the "triangle" given above is impossible,
# because 5 + 10 is not larger than 25.

# In your puzzle input, how many of the listed triangles are possible?

# --- Part Two ---
# Now that you've helpfully marked up their design documents, it occurs to you
# that triangles are specified in groups of three vertically. Each set of three
# numbers in a column specifies a triangle. Rows are unrelated.

# For example, given the following specification, numbers with the same
# hundreds digit would be part of the same triangle:

# 101 301 501
# 102 302 502
# 103 303 503
# 201 401 601
# 202 402 602
# 203 403 603
# In your puzzle input, and instead reading by columns, how many of the listed
# triangles are possible?

input = 'input.txt'

def main():

    # --- Part One --

    with open(input) as f:
        # Read a line a split into three integers
        # The map function applies int to each element of the split line
        triangles = [list(map(int, line.split())) for line in f]

    # Count the number of valid triangles
    count = 0
    for triangle in triangles:
        # Sort the sides of the triangle
        triangle.sort()

        # Check if the sum of the two smaller sides is greater than the largest
        if triangle[0] + triangle[1] > triangle[2]:
            count += 1

    print('Part One:', count)

    # --- Part Two ---

    with open(input) as f:
        count = 0
        triangles = []
        # Read a line a split into three integers
        # The map function applies int to each element of the split line
        for line in f:
            triangles.append(list(map(int, line.split())))

            # If we have three triangles, check if they are valid
            if len(triangles) == 3:
                for i in range(3):
                    triangle = [triangles[0][i], triangles[1][i], triangles[2][i]]
                    triangle.sort()

                    # Check if the sum of the two smaller sides is greater than the largest
                    if triangle[0] + triangle[1] > triangle[2]:
                        count += 1

                # Clear the list
                triangles = []

    print('Part Two:', count)

if __name__ == '__main__':
    main()
