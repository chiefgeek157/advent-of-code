
def play_game(input: list[int], limit: int) -> int:
    numbers = {}
    turn = 1
    while turn <= limit:
        # print(f'=== Turn {turn} ===')
        if turn - 1 < len(input):
            number = input[turn - 1]
        else:
            last_turns = numbers[last_number]
            if last_turns[0] is None:
                # print(f'  - Last number {last_number} was spoken for the first time')
                number = 0
            else:
                # print(f'  - Last number is {last_number} and turns are {last_turns[-2:]}')
                number = last_turns[1] - last_turns[0]
        # print(f'  - Visiting number {number}')
        turns = numbers.setdefault(number, [None, None])
        turns[0] = turns[1]
        turns[1] = turn
        turn += 1
        last_number = number
    return number

results = [436, 1, 10, 27, 78, 438, 1836]
inputs = [[0,3,6], [1,3,2], [2,1,3], [1,2,3], [2,3,1], [3,2,1], [3,1,2]]
for i in range(len(results)):
    result = play_game(inputs[i], 2020)
    print(f'play_game({inputs[i]}): {result} = {results[i]} -> {result == results[i]}')

part1 = play_game([2,0,6,12,1,3], 2020)
print(f'\nPart 1: {part1}\n')

# results = [175594, 2578, 3544142, 261214, 6895259, 18, 362]
# for i in range(len(results)):
#     result = play_game(inputs[i], 30000000)
#     print(f'play_game({inputs[i]}): {result} = {results[i]} -> {result == results[i]}')

part2 = play_game([2,0,6,12,1,3], 30000000)
print(f'\nPart 2: {part2}\n')
