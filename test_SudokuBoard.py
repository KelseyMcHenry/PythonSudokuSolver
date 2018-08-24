import unittest
from random import randint
from SudokuBoard import SudokuBoard
from itertools import product

# TODO - write better, more comprehensive, tests


class SudokuBoardTestCase(unittest.TestCase):
    """tests for SudokuBoard.py"""

    def setUp(self):
        self.blank_board = SudokuBoard()
        self.random_test_data = [randint(1, 9) for _ in range(81)]
        self.random_board = SudokuBoard(self.random_test_data)
        self.random_i, self.random_j, self.random_s = randint(0, 8), randint(0, 8), randint(0, 8)
        self.random_value = randint(1, 9)

    def test_init_empty(self):
        correct = [[0 for _ in range(9)] for _ in range(9)]
        self.assertEqual(self.blank_board.board, correct)

    def test_init_non_empty(self):
        correct = [[self.random_test_data[(9*j)+i] for i in range(9)] for j in range(9)]
        self.assertEqual(self.random_board.board, correct)

    def test_str(self):
        correct = """[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0]

[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]
"""
        self.assertEqual(str(self.blank_board), correct)

    def test_eq(self):
        self.assertEqual(self.random_board == self.random_board, True)

    def test_set(self):
        self.blank_board.set(self.random_i, self.random_j, self.random_value)
        self.assertEqual(self.blank_board.board[self.random_i][self.random_j], self.random_value)

    def test_get(self):
        self.blank_board.set(self.random_i, self.random_j, self.random_value)
        self.assertEqual(self.blank_board.get(self.random_i, self.random_j), self.random_value)

    def test_row(self):
        self.assertEqual(self.random_board.row(self.random_i), self.random_board.board[self.random_i])

    def test_column(self):
        correct = [row[self.random_j] for row in self.random_board.board]
        self.assertEqual(self.random_board.column(self.random_j), correct)

    def test_sector_lookup(self):
        expected = {(0, 0): 0, (0, 1): 0, (0, 2): 0,
                    (0, 3): 1, (0, 4): 1, (0, 5): 1,
                    (0, 6): 2, (0, 7): 2, (0, 8): 2,
                    (1, 0): 0, (1, 1): 0, (1, 2): 0,
                    (1, 3): 1, (1, 4): 1, (1, 5): 1,
                    (1, 6): 2, (1, 7): 2, (1, 8): 2,
                    (2, 0): 0, (2, 1): 0, (2, 2): 0,
                    (2, 3): 1, (2, 4): 1, (2, 5): 1,
                    (2, 6): 2, (2, 7): 2, (2, 8): 2,
                    (3, 0): 3, (3, 1): 3, (3, 2): 3,
                    (3, 3): 4, (3, 4): 4, (3, 5): 4,
                    (3, 6): 5, (3, 7): 5, (3, 8): 5,
                    (4, 0): 3, (4, 1): 3, (4, 2): 3,
                    (4, 3): 4, (4, 4): 4, (4, 5): 4,
                    (4, 6): 5, (4, 7): 5, (4, 8): 5,
                    (5, 0): 3, (5, 1): 3, (5, 2): 3,
                    (5, 3): 4, (5, 4): 4, (5, 5): 4,
                    (5, 6): 5, (5, 7): 5, (5, 8): 5,
                    (6, 0): 6, (6, 1): 6, (6, 2): 6,
                    (6, 3): 7, (6, 4): 7, (6, 5): 7,
                    (6, 6): 8, (6, 7): 8, (6, 8): 8,
                    (7, 0): 6, (7, 1): 6, (7, 2): 6,
                    (7, 3): 7, (7, 4): 7, (7, 5): 7,
                    (7, 6): 8, (7, 7): 8, (7, 8): 8,
                    (8, 0): 6, (8, 1): 6, (8, 2): 6,
                    (8, 3): 7, (8, 4): 7, (8, 5): 7,
                    (8, 6): 8, (8, 7): 8, (8, 8): 8}
        actual = {(i, j): SudokuBoard.sector_lookup(i, j) for i in range(9) for j in range(9)}
        self.assertEqual(expected, actual)

    def test_sector(self):
        correct = [self.random_board.board[i][j] for i, j in product(range(9), range(9)) if self.random_board.sector_lookup(i, j) == self.random_s]
        self.assertEqual(self.random_board.sector(self.random_s), correct)

    def test_get_possibilities(self):
        self.assertEqual(self.random_board.get_possibilities(self.random_i, self.random_j), self.random_board.possible_values[(self.random_i, self.random_j)])

    def test_get_row_possibilities(self):
        pass

unittest.main()
