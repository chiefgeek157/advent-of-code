from amphipod import Piece, State, Board
import unittest
from unittest import TestCase

class PieceTests(TestCase):

    def test_piece(self):
        self.assertEqual(Piece.PIECES[0].type, 0)
        self.assertEqual(str(Piece.PIECES[0]), 'A1')
        self.assertEqual(Piece.PIECES[0].move_cost, 1)
        self.assertEqual(Piece.PIECES[1].type, 0)
        self.assertEqual(str(Piece.PIECES[1]), 'A2')
        self.assertEqual(Piece.PIECES[1].move_cost, 1)
        self.assertEqual(Piece.PIECES[2].type, 1)
        self.assertEqual(str(Piece.PIECES[2]), 'B1')
        self.assertEqual(Piece.PIECES[2].move_cost, 10)
        self.assertEqual(Piece.PIECES[3].type, 1)
        self.assertEqual(str(Piece.PIECES[3]), 'B2')
        self.assertEqual(Piece.PIECES[3].move_cost, 10)
        self.assertEqual(Piece.PIECES[4].type, 2)
        self.assertEqual(str(Piece.PIECES[4]), 'C1')
        self.assertEqual(Piece.PIECES[4].move_cost, 100)
        self.assertEqual(Piece.PIECES[5].type, 2)
        self.assertEqual(str(Piece.PIECES[5]), 'C2')
        self.assertEqual(Piece.PIECES[5].move_cost, 100)
        self.assertEqual(Piece.PIECES[6].type, 3)
        self.assertEqual(str(Piece.PIECES[6]), 'D1')
        self.assertEqual(Piece.PIECES[6].move_cost, 1000)
        self.assertEqual(Piece.PIECES[7].type, 3)
        self.assertEqual(str(Piece.PIECES[7]), 'D2')
        self.assertEqual(Piece.PIECES[7].move_cost, 1000)

class BoardTests(TestCase):

    def test_board(self):
        board = Board()

        a = Piece.PIECES[0]
        b = Piece.PIECES[2]
        c = Piece.PIECES[4]
        d = Piece.PIECES[6]

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

    def test_board_is_allowed(self):
        b = Board()

        self.assertTrue(b.is_allowed(Piece.PIECES[0], 0, 7))
        self.assertTrue(b.is_allowed(Piece.PIECES[0], 1, 7))
        self.assertTrue(b.is_allowed(Piece.PIECES[1], 4, 7))
        self.assertTrue(b.is_allowed(Piece.PIECES[2], 4, 8))
        self.assertTrue(b.is_allowed(Piece.PIECES[4], 6, 9))
        self.assertTrue(b.is_allowed(Piece.PIECES[6], 5, 10))

        self.assertTrue(b.is_allowed(Piece.PIECES[0], 7, 6))
        self.assertTrue(b.is_allowed(Piece.PIECES[0], 11, 7))
        self.assertTrue(b.is_allowed(Piece.PIECES[7], 14, 0))

        self.assertFalse(b.is_allowed(Piece.PIECES[0], 0, 8))
        self.assertFalse(b.is_allowed(Piece.PIECES[0], 0, 14))

class StateTests(TestCase):

    def test_state_create(self):
        b = Board()
        s = State(b, 0)
        s[7] = Piece.PIECES[0]
        s[11] = Piece.PIECES[1]

    def test_state_dist_to_goal(self):
        b = Board()
        s = State(b, 0)

        s[7] = Piece.PIECES[0]
        d = s.dist_to_goal()
        self.assertEqual(d, 0)

        s[1] = Piece.PIECES[1]
        d = s.dist_to_goal()
        self.assertEqual(d, 2)

        s[12] = Piece.PIECES[2]
        d = s.dist_to_goal()
        self.assertEqual(d, 2)

        s[0] = Piece.PIECES[3]
        d = s.dist_to_goal()
        self.assertEqual(d, 52)

        s[9] = Piece.PIECES[4]
        d = s.dist_to_goal()
        self.assertEqual(d, 52)

        s[3] = Piece.PIECES[5]
        d = s.dist_to_goal()
        self.assertEqual(d, 252)

        s[14] = Piece.PIECES[6]
        d = s.dist_to_goal()
        self.assertEqual(d, 252)

        s[6] = Piece.PIECES[7]
        d = s.dist_to_goal()
        self.assertEqual(d, 3252)

    def test_state_cost(self):
        b = Board()
        s = State(b, 1)
        s[7] = Piece.PIECES[0]
        s[1] = Piece.PIECES[1]
        s[12] = Piece.PIECES[2]
        s[0] = Piece.PIECES[3]
        s[9] = Piece.PIECES[4]
        s[2] = Piece.PIECES[5]
        s[14] = Piece.PIECES[6]
        s[6] = Piece.PIECES[7]
        c = s.cost()
        self.assertEqual(c, 3453)

    def test_state_is_final(self):
        b = Board()
        s = State(b, 0)
        s[7] = Piece.PIECES[0]
        s[1] = Piece.PIECES[1]
        s[12] = Piece.PIECES[2]
        s[0] = Piece.PIECES[3]
        s[9] = Piece.PIECES[4]
        s[2] = Piece.PIECES[5]
        s[14] = Piece.PIECES[6]
        s[6] = Piece.PIECES[7]
        self.assertFalse(s.is_final())

        s = State(b, 5)
        s[11] = Piece.PIECES[0]
        s[7] = Piece.PIECES[1]
        s[8] = Piece.PIECES[2]
        s[12] = Piece.PIECES[3]
        s[9] = Piece.PIECES[4]
        s[13] = Piece.PIECES[5]
        s[14] = Piece.PIECES[6]
        s[10] = Piece.PIECES[7]
        self.assertTrue(s.is_final())

    def test_state_read(self):
         b = Board()
         s = State.read('2021/day23/test1.txt', b)
         print(f'State = \n{s}')

if __name__ == '__main__':
    unittest.main()