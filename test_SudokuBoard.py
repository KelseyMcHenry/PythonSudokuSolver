import unittest
from random import randint
from SudokuBoard import SudokuBoard
from itertools import product

# TODO - write better, more comprehensive, tests

class SudokuBoardTestCase(unittest.TestCase):
    """tests for SudokuBoard.py"""

    def setUp(self):
        """Creates a test board we will work with"""
        test_data = [randint(1, 9) for _ in range(81)]
        self.test_board = SudokuBoard(test_data)

    def test_init_empty(self):
        board = SudokuBoard()
        correct = [[0 for _ in range(9)] for _ in range(9)]
        self.assertEqual(board.board, correct)

    def test_init_non_empty(self):
        test_data = [randint(1, 9) for _ in range(81)]
        board = SudokuBoard(test_data)
        correct = [[test_data[(9*j)+i] for i in range(9)] for j in range(9)]
        self.assertEqual(board.board, correct)

    def test_get(self):
        i, j = randint(0, 8), randint(0, 8)
        self.assertEqual(self.test_board.get(i, j), self.test_board.board[i][j])

    def test_row(self):
        i = randint(0, 8)
        self.assertEqual(self.test_board.row(i), self.test_board.board[i])

    def test_column(self):
        j = randint(0, 8)
        correct = [row[j] for row in self.test_board.board]
        self.assertEqual(self.test_board.column(j), correct)

    def test_sector(self):
        s = randint(0, 8)
        correct = [self.test_board.board[i][j] for i, j in product(range(9), range(9)) if self.sector_lookup(i, j) == s]
        self.assertEqual(self.test_board.sector(s), correct)


unittest.main()
