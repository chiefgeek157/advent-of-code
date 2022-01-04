import functools

# def evaluate(board_size, item):
#     print(f'Evaluating item {item}')
#     space = ((item.spaces[item.player] + item.roll - 1) % board_size) + 1
#     score = item.scores[item.player] + space
#     return space, score

    # winner = None
    # spaces = [pos0[0], pos0[1]]
    # scores = [0, 0]
    # p = 0
    # rounds = 0
    # for r in reversed(range(len(rolls))):
    #     spaces[p] = (spaces[p] + rolls[r]) % board_size
    #     scores[p] += spaces[p]
    #     if scores[p] >= winning_score:
    #         winner = p
    #         break
    #     p = (p + 1) % 2
    #     rounds += 1
    # print(f'winner of {rolls} is {winner} after {rounds} rounds')
    # # input('Enter')
    # return winner, rounds

# def increment_rolls(rolls):
#     i = len(rolls) - 1
#     while True:
#         rolls[i] += 1
#         if rolls[i] > 3:
#             rolls[i] = 1
#             if i == 0:
#                 rolls.insert(0, 1)
#                 break
#             else:
#                 i -= 1
#         else:
#             break

# class WorkItem():

#     def __init__(self, player, spaces, scores, rolls, roll):
#         self.player = player
#         self.spaces = spaces
#         self.scores = scores
#         self.roll = roll
#         self.rolls = rolls + str(roll)

#     def __str__(self):
#         return f'player {self.player} spaces {self.spaces} scores {self.scores} rolls {self.rolls}'

@functools.cache
def play_round(my_pos, my_score, other_pos, other_score):
    if my_score >= winning_score:
        return 1, 0
    elif other_score >= winning_score:
        return 0, 1

    my_wins = 0
    other_wins = 0
    for roll in roll_counts.keys():
        new_pos = ((my_pos + roll - 1) % board_size) + 1
        new_score = my_score + new_pos

        ow, mw = play_round(other_pos, other_score, new_pos, new_score)

        my_wins += mw * roll_counts[roll]
        other_wins += ow * roll_counts[roll]

    return my_wins, other_wins

roll_counts = {}
for i in range(3):
    for j in range(3):
        for k in range(3):
            total = i + j + k + 3
            if total not in roll_counts: roll_counts[total] = 0
            roll_counts[total] += 1

print(f'roll counts {roll_counts}')

p1_pos0 = 8
p2_pos0 = 6
board_size = 10
winning_score = 21

p1_wins, p2_wins = play_round(p1_pos0, 0, p2_pos0, 0)

print(f'Answer: p1 wins {p1_wins} p2 wins {p2_wins}')