import unittest
from random import randint
from SudokuBoard import SudokuBoard
from itertools import product

# TODO - write better, more comprehensive, tests


class SudokuBoardTestCase(unittest.TestCase):
    """tests for SudokuBoard.py"""

    def setUp(self):
        pass

    def test_init_empty(self):
        board = SudokuBoard()
        correct = [[0 for _ in range(9)] for _ in range(9)]
        self.assertEqual(board.board, correct)

    def test_init_non_empty(self):
        test_data = [randint(1, 9) for _ in range(81)]
        board = SudokuBoard(test_data)
        correct = [[test_data[(9*j)+i] for i in range(9)] for j in range(9)]
        self.assertEqual(board.board, correct)

    def test_set(self):
        test_board = SudokuBoard()
        i, j = randint(0, 8), randint(0, 8)
        value = randint(1, 9)
        test_board.set(i, j, value)
        self.assertEqual(test_board.board[i][j], value)

    def test_get(self):
        test_board = SudokuBoard()
        i, j = randint(0, 8), randint(0, 8)
        value = randint(1, 9)
        test_board.set(i, j, value)
        self.assertEqual(test_board.get(i, j), value)

    def test_row(self):
        test_data = [randint(1, 9) for _ in range(81)]
        test_board = SudokuBoard(test_data)
        i = randint(0, 8)
        self.assertEqual(test_board.row(i), test_board.board[i])

    def test_column(self):
        test_data = [randint(1, 9) for _ in range(81)]
        test_board = SudokuBoard(test_data)
        j = randint(0, 8)
        correct = [row[j] for row in test_board.board]
        self.assertEqual(test_board.column(j), correct)

    def test_sector(self):
        test_data = [randint(1, 9) for _ in range(81)]
        test_board = SudokuBoard(test_data)
        s = randint(0, 8)
        correct = [test_board.board[i][j] for i, j in product(range(9), range(9)) if test_board.sector_lookup(i, j) == s]
        self.assertEqual(test_board.sector(s), correct)


unittest.main()
