import copy as cp

# filename = '2021/day23/test1.txt'
filename = '2021/day23/test2.txt'
# filename = '2021/day22/input.txt'

class Piece():

    PIECES = []

    __TYPE_NAMES = 'ABCD'
    __MOVE_COSTS = [1, 10, 100, 1000]

    # Type is 0-3
    def __init__(self, type_char, id):
        self.type = Piece.__TYPE_NAMES.index(type_char)
        self.id = id
        self.move_cost = Piece.__MOVE_COSTS[self.type]

    def __str__(self):
        return f'{Piece.__TYPE_NAMES[self.type]}{self.id}'

Piece.PIECES.append(Piece('A', 1))
Piece.PIECES.append(Piece('A', 2))
Piece.PIECES.append(Piece('B', 1))
Piece.PIECES.append(Piece('B', 2))
Piece.PIECES.append(Piece('C', 1))
Piece.PIECES.append(Piece('C', 2))
Piece.PIECES.append(Piece('D', 1))
Piece.PIECES.append(Piece('D', 2))

class Board():
    # Board positions
    #
    # 00 01 .. 02 .. 03 .. 04 .. 05 06
    #       07    08    09    10
    #       11    12    13    14

    __POSITIONS = range(0,14)

    # Home positions by piece type
    __HOME_POS = [[7, 11], [8, 12], [9, 13], [10, 14]]

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

    __PATHS = {
        ( 0,  7): ([ 1,  7], 3),
        ( 0, 11): ([ 1,  7, 11], 4),
        ( 0,  8): ([ 1,  2,  8], 5),
        ( 0, 12): ([ 1,  2,  8, 12], 6),
        ( 0,  7): ([ 1,  7], 3),
        ( 0, 11): ([ 1,  7, 11], 4),
        ( 0,  7): ([ 1,  7], 3),
        ( 0, 11): ([ 1,  7, 11], 4),
    }

    def __init__(self):
        pass

    def dist_to_goal(self, piece, pos):
        # print(f'dist_to_goal({piece},{pos}): {Board.__HOME_DISTS[piece.type][pos] * piece.move_cost}')
        return Board.__HOME_DISTS[piece.type][pos] * piece.move_cost

    def adjacent_pos(self, pos):
        return cp.copy(self.__ADJS[pos])

    def in_home_pos(self, piece, pos):
        return pos in Board.__HOME_POS[piece.type]

    # Find all possible next states and the incremental cost for that state
    def find_next_states(self, state):
        next_states = []
        for pos in Board.__POSITIONS:
            piece = state[pos]
            if piece is not None:
                # This position is occupied
                for adj, mult in Board.__ADJS[pos]:
                    if state[adj] is None and self.is_allowed(piece, pos, adj):
                        # This adjacent position is not occupied and the move
                        # is allowed
                        new_state = cp.deepcopy(state)
                        del new_state[pos]
                        new_state.cost = None
                        new_state[adj] = piece
                        incr_cost = mult * piece.move_cost
                        next_states.append((new_state, incr_cost))
        return next_states

    def is_allowed(self, piece, start, dest):
        # Pieces can only move from the hallway into homes that
        # match their correct type
        if start >= 7:
            return True
        elif dest < 7:
            return False
        elif piece.type == 0 and dest not in [7, 11] or \
                piece.type == 1 and dest not in [8, 12] or \
                piece.type == 2 and dest not in [9, 13] or \
                piece.type == 3 and dest not in [10, 14]:
            return False
        else:
            return True

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
        state_pos = pos
        for c in line.strip():
            # print(f'Reading char {c} as pos {pos}')
            if c != '#':
                if c == '.':
                    if pos not in [2, 3, 4, 5]: state_pos += 1
                else:
                    id = 1
                    if c in pieces_read:
                        id = 2
                    else:
                        id = 1
                        pieces_read.append(c)
                    piece = Piece(c, id)
                    # print(f'Setting pos {pos} to piece {piece}')
                    state[state_pos] = piece
                    state_pos += 1
                pos += 1
        return state_pos

    def __init__(self, board, cost = None):
        self.predecessor = None
        self.cost = cost
        self.__board = board
        # Dict of {pos, piece}
        self.__state = dict()
        self.__dist = None
        self.__hash = None

    def unset(self, pos):
        self.__state.pop(pos)
        self.__dist = None
        self.__hash = None

    def dist_to_goal(self):
        if self.__dist is None:
            self.__dist = 0
            for pos, piece in self.__state.items(): self.__dist += self.__board.dist_to_goal(piece, pos)
        return self.__dist

    def total_cost(self):
        return self.cost + self.dist_to_goal()

    def update(self, incr_cost, predecessor):
        new_cost = predecessor.cost + incr_cost
        if self.cost is None or new_cost < self.cost:
            self.cost = new_cost
            self.predecessor = predecessor
            return True
        return False

    def is_final(self):
        for pos, piece in self.__state.items():
            if not self.__board.in_home_pos(piece, pos): return False
        return True

    def cost_chain(self):
        chain = f'{self.cost}'
        if self.predecessor is not None:
            chain = f'{self.predecessor.cost_chain()}.{chain}'
        return chain

    def __getitem__(self, pos):
        return self.__state.get(pos)

    def __setitem__(self, pos, piece):
        self.__state[pos] = piece
        self.__dist = None
        self.__hash = None

    def __delitem__(self, pos):
        del self.__state[pos]
        self.__dist = None
        self.__hash = None

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        return hash(self) == hash(other)

    def __hash__(self):
        if self.__hash is None:
            self.__hash = ''
            for pos in sorted(self.__state.keys()): self.__hash += f'{pos:2}{self.__state[pos]}'
            # print(f'{self.__hash}')
        return hash(self.__hash)

    def __str__(self):
        s = f'{self.__symbol(0)} {self.__symbol(1)}    '
        s += f'{self.__symbol(2)}    {self.__symbol(3)}    '
        s += f'{self.__symbol(4)}    {self.__symbol(5)} {self.__symbol(6)}\n'
        s += f'      {self.__symbol(7)}    {self.__symbol(8)}'
        s += f'    {self.__symbol(9)}    {self.__symbol(10)}\n'
        s += f'      {self.__symbol(11)}    {self.__symbol(12)}'
        s += f'    {self.__symbol(13)}    {self.__symbol(14)}'
        return s

    def __symbol(self, pos):
        if pos in self.__state: return f'{self.__state[pos]}'
        return '..'
