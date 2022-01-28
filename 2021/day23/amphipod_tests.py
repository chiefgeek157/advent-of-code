from binascii import a2b_base64
from amphipod import Piece, State, Board
import unittest
from unittest import TestCase

class PieceTests(TestCase):

    def test_piece(self):
        a1 = Piece('A', 1)
        a2 = Piece('A', 2)
        b1 = Piece('B', 1)
        b2 = Piece('B', 2)
        c1 = Piece('C', 1)
        c2 = Piece('C', 2)
        d1 = Piece('D', 1)
        d2 = Piece('D', 2)
        self.assertEqual(a1.type, 0)
        self.assertEqual(str(a1), 'A1')
        self.assertEqual(a1.move_cost(), 1)
        self.assertEqual(a2.type, 0)
        self.assertEqual(str(a2), 'A2')
        self.assertEqual(a2.move_cost(), 1)
        self.assertEqual(b1.type, 1)
        self.assertEqual(str(b1), 'B1')
        self.assertEqual(b1.move_cost(), 10)
        self.assertEqual(b2.type, 1)
        self.assertEqual(str(b2), 'B2')
        self.assertEqual(b2.move_cost(), 10)
        self.assertEqual(c1.type, 2)
        self.assertEqual(str(c1), 'C1')
        self.assertEqual(c1.move_cost(), 100)
        self.assertEqual(c2.type, 2)
        self.assertEqual(str(c2), 'C2')
        self.assertEqual(c2.move_cost(), 100)
        self.assertEqual(d1.type, 3)
        self.assertEqual(str(d1), 'D1')
        self.assertEqual(d1.move_cost(), 1000)
        self.assertEqual(d2.type, 3)
        self.assertEqual(str(d2), 'D2')
        self.assertEqual(d2.move_cost(), 1000)

class BoardTests(TestCase):

    def test_board(self):
        board = Board()

        a = Piece('A', 1)
        b = Piece('B', 1)
        c = Piece('C', 1)
        d = Piece('D', 1)

        dist = board.dist_to_goal(a, 0)
        self.assertEqual(dist, 3)

        dist = board.dist_to_goal(b, 6)
        self.assertEqual(dist, 70)

        dist = board.dist_to_goal(c, 11)
        self.assertEqual(dist, 700)

        dist = board.dist_to_goal(d, 1)
        self.assertEqual(dist, 8000)

        dist = board.dist_to_goal(a, 7)
        self.assertEqual(dist, 0)

        dist = board.dist_to_goal(d, 14)
        self.assertEqual(dist, 0)

        adjs = board.adjacent_pos(0)
        self.assertEqual(len(adjs), 1)

        adjs = board.adjacent_pos(4)
        self.assertEqual(len(adjs), 4)
        self.assertTupleEqual(adjs[3], (10, 2))

class StateTests(TestCase):

    def test_state_create(self):
        b = Board()
        s = State(b, 0)
        print(f'{s}')

if __name__ == '__main__':
    unittest.main()