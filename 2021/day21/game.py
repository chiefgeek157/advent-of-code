class Die():

    def roll(self):
        r = self._do_roll()
        self.__roll_count += 1
        return r

    def roll_count(self):
        return self.__roll_count

    def __init__(self):
        self.__roll_count = 0

class DeterministicDie(Die):

    def __init__(self, sides):
        super().__init__()
        self.__sides = sides
        self.__value = 1

    def _do_roll(self):
        v = self.__value
        self.__value = ((self.__value) % self.__sides) + 1
        return v

    def __str__(self):
        return f'DeterministicDie sides={self.__sides} value={self.__value}'

class DieRoller():

    def roll(self, die):
        return die.roll()

    def __init__(self):
        pass

class MultiRoller(DieRoller):

    def roll(self, die):
        s = 0
        for r in range(self.__times):
            s += die.roll()
        return s

    def __init__(self, times):
        super().__init__()
        self.__times = times

class Player():

    def num(self):
        return self.__num

    def space(self):
        return self.__space

    def move_to(self, space):
        self.__space = space

    def add_score(self, score):
        self.__score += score
        return self.__score

    def score(self):
        return self.__score

    def __init__(self, num, space):
        self.__num = num
        self.__space = space
        self.__score = 0

    def __str__(self):
        return f'Player {self.num()} space {self.space()} score {self.score()}'

class Board():

    def move_player(self, player, spaces):
        player.move_to(player.space() + spaces)

    def __init__(self):
        pass

class CircularBoard():

    def move_player(self, player, spaces):
        space = ((player.space() + spaces - 1) % self.__size) + 1
        player.move_to(space)

    def __init__(self, size):
        super().__init__()
        self.__size = size

class Scorekeeper():

    def add_score(self, player):
        pass

    def is_winner(self, player):
        return player.score() >= self.__winning_score

    def __init__(self, winning_score):
        self.__winning_score = winning_score

class SpaceScoreKeeper(Scorekeeper):

    def add_score(self, player):
        player.add_score(player.space())

    def __init__(self, winning_score):
        super().__init__(winning_score)

class Game():

    def play(self, board, die, roller, players, scorekeeper):
        winner = None
        current = 0
        while winner is None:
            player = players[current]
            print(f'player {player.num()} space {player.space()} score {player.score()}', end='')
            spaces = roller.roll(die)
            print(f' rolls spaces {spaces}', end='')
            board.move_player(player, spaces)
            print(f' moves to space {player.space()}', end='')
            scorekeeper.add_score(player)
            print(f' for new score {player.score()}', end='')
            if scorekeeper.is_winner(player):
                winner = player
            player, current = self.__next_player(players, current)
            print()
        return winner

    def __init__(self):
        pass

    def __next_player(self, players, current_player):
        i = (current_player + 1) % len(players)
        return players[i], i