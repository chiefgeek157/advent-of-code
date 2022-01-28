import copy as cp

# filename = '2021/day23/test1.txt'
filename = '2021/day23/test2.txt'
# filename = '2021/day22/input.txt'

class Piece():

    __TYPE_NAMES = 'ABCD'
    __MOVE_COSTS = [1, 10, 100, 1000]

    # Type is 0-3
    def __init__(self, type_char, id):
        self.type = Piece.__TYPE_NAMES.index(type_char)
        self.id = id

    def __str__(self):
        return f'{Piece.__TYPE_NAMES[self.type]}{self.id}'

    def move_cost(self):
        return Piece.__MOVE_COSTS[self.type]

class Board():
    # Board positions
    #
    # 00 01 .. 02 .. 03 .. 04 .. 05 06
    #       07    08    09    10
    #       11    12    13    14

    # Distance to the first possible home for each piece type from each position
    __HOME_DISTS = [
        #0  1  2  3  4  5  6  7  8  9  0  1  2  3  4
        [3, 2, 2, 4, 6, 8, 9, 0, 4, 6, 8, 0, 5, 7, 9],
        [5, 4, 2, 2, 4, 6, 7, 4, 0, 4, 6, 5, 0, 5, 7],
        [7, 6, 4, 2, 2, 4, 5, 6, 4, 0, 4, 7, 5, 0, 5],
        [9, 8, 6, 4, 2, 2, 3, 8, 6, 4, 0, 9, 7, 5, 0]
    ]

    # Adjacencies [neighbor, cost multiplier]
    __ADJS = [
        [(1, 1)],                          # 0
        [(0, 1), (2, 2), (7, 2)],          # 1
        [(1, 2), (3, 2), (7, 2), (8, 2)],  # 2
        [(2, 2), (4, 2), (8, 2), (9, 2)],  # 3
        [(3, 2), (5, 2), (9, 2), (10, 2)], # 4
        [(4, 2), (6, 1), (10, 2)],         # 5
        [(5, 1)],                          # 6
        [(1, 2), (2, 2), (11, 1)],         # 7
        [(2, 2), (3, 2), (12, 1)],         # 8
        [(3, 2), (4, 2), (13, 1)],         # 9
        [(4, 2), (5, 2), (14, 1)],         # 10
        [(7, 1)],                          # 11
        [(8, 1)],                          # 12
        [(9, 1)],                          # 13
        [(10, 1)]                          # 14
    ]

    def __init__(self):
        pass

    def dist_to_goal(self, piece, pos):
        return Board.__HOME_DISTS[piece.type][pos] * piece.move_cost()

    def adjacent_pos(self, pos):
        return cp.copy(self.__ADJS[pos])

class State():

    def read(filename, board):
        state = State(board, 0)
        with open(filename, 'r') as f:
            # Discard first line
            f.readline()

            pieces_read = []
            pos = 0
            pos = State.__parse_line(f.readline().strip(), pos, pieces_read, state)
            pos = State.__parse_line(f.readline().strip(), pos, pieces_read, state)
            pos = State.__parse_line(f.readline().strip(), pos, pieces_read, state)
        return state

    def __parse_line(line, pos, pieces_read, state):
        for c in line.strip():
            if c != '#' and c != '.':
                id = 1
                if c in pieces_read:
                    id = 2
                else:
                    id = 1
                    pieces_read.append(c)
                piece = Piece(c, id)
                state.add(piece, pos)
                pos += 1
        return pos

    def __init__(self, board, cost):
        self.predecessor = None
        self.__board = board
        self.__cost = cost
        # Dict of {pos, piece}
        self.__state = dict()
        self.__dist = None
        self.__hash = None

    def set(self, piece, pos):
        self.state[pos] = piece
        self.__hash = None

    def unset(self, pos):
        self.state.pop(pos)
        self.__hash = None

    def dist_to_goal(self):
        if self.__dist is None:
            self.__dist = 0
            for pos in range(19):
                self.__dist += self.__board.dist_to_goal(self.__state[pos], pos)
        return self.__dist

    def cost(self):
        return self.__cost + self.dist_to_goal()

    def update(self, cost, predecessor):
        if cost < self.__cost:
            self.__cost = cost
            self.predecessor = predecessor
            return True
        return False

    def __hash__(self):
        if self.__hash is None:
            self.__hash = ''
            for pos, piece in self.state: self.__hash += f'{pos}{piece}'
        return self.__hash

    def __str__(self):
        s = f'{self.__symbol(0)} {self.__symbol(1)}    '
        s += f'{self.__symbol(2)}    {self.__symbol(3)}    '
        s += f'{self.__symbol(4)}    {self.__symbol(5)} {self.__symbol(6)}\n'
        s += f'      {self.__symbol(7)}    {self.__symbol(8)}'
        s += f'    {self.__symbol(9)}    {self.__symbol(10)}\n'
        s += f'    {self.__symbol(11)}    {self.__symbol(12)}'
        s += f'    {self.__symbol(13)}    {self.__symbol(14)}'
        return s

    def __symbol(self, pos):
        if pos in self.__state: return f'{self.__state[pos]}'
        return '..'
