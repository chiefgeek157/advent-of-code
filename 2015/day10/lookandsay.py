# INPUT = '1'
INPUT = '1321131112'
# LIMIT = 5
# LIMIT = 40
LIMIT = 50

work = INPUT
rep = 0
while rep < LIMIT:
    # print(f'work: {work}')
    new_work = ''
    run = 0
    prev_digit = None
    for digit in work:
        if prev_digit is None:
            run += 1
        else:
            if digit == prev_digit:
                run += 1
            else:
                new_work += str(run) + prev_digit
                run = 1
        prev_digit = digit
    new_work += str(run) + digit
    work = new_work
    rep += 1

# print(f'work: {work}')
print(f'Ans: {len(work)}')