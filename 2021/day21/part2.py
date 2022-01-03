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

p1_pos0 = 4
p2_pos0 = 8
p1_wins = 0
p2_wins = 0
board_size = 10
winning_score = 2

roll_counts = {}
for i in range(3):
    for j in range(3):
        for k in range(3):
            total = i + j + k + 3
            if total not in roll_counts: roll_counts[total] = 0
            roll_counts[total] += 1

print(f'roll counts {roll_counts}')

# state[(player, p1_pos, ps_pos, p1_score, p2_score)] = count of ways to get to this state
states = {}
for player in range(2):
    for p1_pos in range(10):
        for p2_pos in range(10):
            for p1_score in range(21):
                for p2_score in range(21):
                    # initial count is zero
                    states[(player, p1_pos, p2_pos, p1_score, p2_score)] = 0

# Work items are a tuple (player_turn, p1_pos, p2_pos, p1_score, p2_score)
work = []
work.append((0, p1_pos0, p2_pos0, 0, 0))
while work:
    item = work.pop(0)
    (player, p1_pos, p2_pos, p1_score, p2_score) = item
    count = states[item]
    for roll in roll_counts.keys():
        incr = count + roll_counts[roll]
        if player == 0:
            p1_new_pos = ((p1_pos + roll - 1) % board_size) + 1
            p1_new_score = min(winning_score, p1_score + p1_new_pos)
            if p1_new_score < winning_score:
                new_item = (1, p1_new_pos, p2_pos, p1_new_score, p2_score)
                states[new_item] += incr
                work.append(new_item)
            else:
                p1_wins += incr
        else:
            p2_new_pos = ((p2_pos + roll - 1) % board_size) + 1
            p2_new_score = min(winning_score, p2_score + p2_new_pos)
            if p1_new_score < winning_score:
                new_item = (1, p1_new_pos, p2_pos, p1_new_score, p2_score)
                states[p1_pos][p2_new_pos][p1_score][p2_new_score] += incr
                work.append((1, p1_pos, p2_new_pos, p1_score, p2_new_score))
            else:
                p2_wins += incr

print(f'Answer: p1 wins {p1_wins} p2 wins {p2_wins}')