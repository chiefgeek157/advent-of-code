import game as g

# filename = '2021/day21/test1.txt'
filename = '2021/day21/input.txt'

players = []
with open(filename, 'r') as f:
    line = f.readline()
    while line:
        values = line.strip().split(':')
        num = values[0].split()[1]
        start = int(values[1])
        players.append(g.Player(num, start))
        line = f.readline()

board = g.CircularBoard(10)
roller = g.MultiRoller(3)
die = g.DeterministicDie(100)
scorekeeper = g.SpaceScoreKeeper(1000)
game = g.Game()

winner = game.play(board, die, roller, players, scorekeeper)
loser = players[0] if winner == players[1] else players[1]
print(f'The winner is {winner.num()}')

rolls = die.roll_count()
print(f'Roll count {rolls}')

print(f'Answer: {loser.score() * rolls}')