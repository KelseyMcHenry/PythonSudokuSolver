import glob
import os
import unittest
from random import randint
from SudokuBoard import SudokuBoard
from itertools import product
from Move import Move
from Move import NUMBER_SOLVE, REMOVE_POSS

# TODO - write better, more comprehensive, tests
# TODO - generate sdk files with solutions to compare
# TODO - convert all "strings" to 'strings'
# TODO - make sure pass / fail covered as well as all outcomes
# TODO - make sure Moves are returned correctly.


class SudokuBoardTestCase(unittest.TestCase):
    """tests for SudokuBoard.py"""

    # 'evil' difficulty
    test_data_1 = [1, 0, 0, 0, 9, 0, 3, 0, 0,
                   0, 6, 0, 7, 0, 0, 0, 0, 8,
                   0, 0, 4, 0, 0, 5, 0, 0, 0,
                   3, 0, 0, 0, 6, 0, 1, 0, 0,
                   0, 7, 0, 8, 0, 0, 0, 0, 0,
                   0, 0, 5, 0, 0, 0, 0, 9, 0,
                   2, 0, 0, 0, 1, 0, 0, 6, 0,
                   0, 8, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 9, 4, 0, 0, 0, 0, 0]

    test_data_1_poss = {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 7, 8], (0, 3): [2, 6], (0, 4): [], (0, 5): [2, 4, 6, 8],
                        (0, 6): [], (0, 7): [2, 4, 5, 7], (0, 8): [2, 4, 5, 6, 7], (1, 0): [5, 9], (1, 1): [],
                        (1, 2): [2, 3], (1, 3): [], (1, 4): [2, 3, 4], (1, 5): [1, 2, 3, 4], (1, 6): [2, 4, 5, 9],
                        (1, 7): [1, 2, 4, 5], (1, 8): [], (2, 0): [7, 8, 9], (2, 1): [2, 3, 9], (2, 2): [],
                        (2, 3): [1, 2, 3, 6], (2, 4): [2, 3, 8], (2, 5): [], (2, 6): [2, 6, 7, 9], (2, 7): [1, 2, 7],
                        (2, 8): [1, 2, 6, 7, 9], (3, 0): [], (3, 1): [2, 4, 9], (3, 2): [2, 8], (3, 3): [2, 5, 9],
                        (3, 4): [], (3, 5): [2, 4, 7, 9], (3, 6): [], (3, 7): [2, 4, 5, 7, 8], (3, 8): [2, 4, 5, 7],
                        (4, 0): [4, 6, 9], (4, 1): [], (4, 2): [1, 2, 6], (4, 3): [], (4, 4): [2, 3, 4, 5],
                        (4, 5): [1, 2, 3, 4, 9], (4, 6): [2, 4, 5, 6], (4, 7): [2, 3, 4, 5], (4, 8): [2, 3, 4, 5, 6],
                        (5, 0): [4, 6, 8], (5, 1): [1, 2, 4], (5, 2): [], (5, 3): [1, 2, 3], (5, 4): [2, 3, 4, 7],
                        (5, 5): [1, 2, 3, 4, 7], (5, 6): [2, 4, 6, 7, 8], (5, 7): [], (5, 8): [2, 3, 4, 6, 7],
                        (6, 0): [], (6, 1): [3, 4, 5], (6, 2): [3, 7], (6, 3): [3, 5, 9], (6, 4): [],
                        (6, 5): [3, 7, 8, 9], (6, 6): [4, 5, 7, 8, 9], (6, 7): [], (6, 8): [3, 4, 5, 7, 9],
                        (7, 0): [4, 5, 6, 7], (7, 1): [], (7, 2): [1, 3, 6, 7], (7, 3): [2, 3, 5, 6, 9],
                        (7, 4): [2, 3, 5, 7], (7, 5): [2, 3, 6, 7, 9], (7, 6): [2, 4, 5, 7, 9],
                        (7, 7): [1, 2, 3, 4, 5, 7], (7, 8): [1, 2, 3, 4, 5, 7, 9], (8, 0): [5, 6, 7], (8, 1): [1, 3, 5],
                        (8, 2): [], (8, 3): [], (8, 4): [2, 3, 5, 7, 8], (8, 5): [2, 3, 6, 7, 8], (8, 6): [2, 5, 7, 8],
                        (8, 7): [1, 2, 3, 5, 7, 8], (8, 8): [1, 2, 3, 5, 7]}

    test_data_1_soln = [1, 5, 8, 6, 9, 4, 3, 2, 7,
                        9, 6, 3, 7, 2, 1, 5, 4, 8,
                        7, 2, 4, 3, 8, 5, 6, 1, 9,
                        3, 9, 2, 5, 6, 7, 1, 8, 4,
                        6, 7, 1, 8, 4, 9, 2, 5, 3,
                        8, 4, 5, 1, 3, 2, 7, 9, 6,
                        2, 3, 7, 9, 1, 8, 4, 6, 5,
                        4, 8, 6, 2, 5, 3, 9, 7, 1,
                        5, 1, 9, 4, 7, 6, 8, 3, 2]

    # 'hard' difficulty
    test_data_2 = [9, 0, 0, 3, 0, 0, 5, 8, 0,
                   0, 8, 0, 0, 0, 0, 3, 7, 0,
                   0, 0, 0, 0, 0, 7, 4, 0, 2,
                   1, 0, 0, 9, 7, 0, 0, 0, 0,
                   0, 0, 0, 4, 0, 8, 0, 0, 0,
                   0, 0, 0, 0, 3, 2, 0, 0, 6,
                   5, 0, 4, 2, 0, 0, 0, 0, 0,
                   0, 7, 6, 0, 0, 0, 0, 9, 0,
                   0, 1, 9, 0, 0, 3, 0, 0, 4]

    test_data_2_poss = {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2, 7], (0, 3): [], (0, 4): [1, 2, 4, 6],
                        (0, 5): [1, 4, 6], (0, 6): [], (0, 7): [], (0, 8): [1], (1, 0): [2, 4, 6], (1, 1): [],
                        (1, 2): [1, 2, 5], (1, 3): [1, 5, 6], (1, 4): [1, 2, 4, 5, 6, 9], (1, 5): [1, 4, 5, 6, 9],
                        (1, 6): [], (1, 7): [], (1, 8): [1, 9], (2, 0): [3, 6], (2, 1): [3, 5, 6], (2, 2): [1, 3, 5],
                        (2, 3): [1, 5, 6, 8], (2, 4): [1, 5, 6, 8, 9], (2, 5): [], (2, 6): [], (2, 7): [1, 6],
                        (2, 8): [], (3, 0): [], (3, 1): [2, 3, 4, 5, 6], (3, 2): [2, 3, 5, 8], (3, 3): [], (3, 4): [],
                        (3, 5): [5, 6], (3, 6): [2, 8], (3, 7): [2, 3, 4, 5], (3, 8): [3, 5, 8], (4, 0): [2, 3, 6, 7],
                        (4, 1): [2, 3, 5, 6, 9], (4, 2): [2, 3, 5, 7], (4, 3): [], (4, 4): [1, 5, 6], (4, 5): [],
                        (4, 6): [1, 2, 7, 9], (4, 7): [1, 2, 3, 5], (4, 8): [1, 3, 5, 7, 9], (5, 0): [4, 7, 8],
                        (5, 1): [4, 5, 9], (5, 2): [5, 7, 8], (5, 3): [1, 5], (5, 4): [], (5, 5): [],
                        (5, 6): [1, 7, 8, 9], (5, 7): [1, 4, 5], (5, 8): [], (6, 0): [], (6, 1): [3], (6, 2): [],
                        (6, 3): [], (6, 4): [1, 6, 8, 9], (6, 5): [1, 6, 9], (6, 6): [1, 6, 7, 8], (6, 7): [1, 3, 6],
                        (6, 8): [1, 3, 7, 8], (7, 0): [2, 3, 8], (7, 1): [], (7, 2): [], (7, 3): [1, 5, 8],
                        (7, 4): [1, 4, 5, 8], (7, 5): [1, 4, 5], (7, 6): [1, 2, 8], (7, 7): [], (7, 8): [1, 3, 5, 8],
                        (8, 0): [2, 8], (8, 1): [], (8, 2): [], (8, 3): [5, 6, 7, 8], (8, 4): [5, 6, 8], (8, 5): [],
                        (8, 6): [2, 6, 7, 8], (8, 7): [2, 5, 6], (8, 8): []}

    test_data_2_soln = [9, 6, 7, 3, 2, 4, 5, 8, 1,
                        4, 8, 2, 6, 5, 1, 3, 7, 9,
                        3, 5, 1, 8, 9, 7, 4, 6, 2,
                        1, 4, 3, 9, 7, 6, 8, 2, 5,
                        6, 2, 5, 4, 1, 8, 9, 3, 7,
                        7, 9, 8, 5, 3, 2, 1, 4, 6,
                        5, 3, 4, 2, 6, 9, 7, 1, 8,
                        8, 7, 6, 1, 4, 5, 2, 9, 3,
                        2, 1, 9, 7, 8, 3, 6, 5, 4]

    # 'easy' difficulty
    test_data_3 = [3, 0, 0, 6, 0, 0, 0, 9, 0,
                   0, 4, 5, 0, 8, 0, 0, 1, 2,
                   0, 0, 0, 0, 0, 1, 0, 7, 0,
                   9, 0, 2, 4, 0, 7, 0, 8, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 1, 0, 9, 2, 0, 0, 0,
                   0, 9, 3, 5, 0, 0, 6, 2, 0,
                   0, 7, 0, 0, 0, 0, 8, 0, 0,
                   0, 5, 8, 0, 0, 0, 0, 0, 1]

    test_data_3_poss = {(0, 0): [], (0, 1): [1, 2, 8], (0, 2): [7], (0, 3): [], (0, 4): [2, 4, 5, 7], (0, 5): [4, 5],
                        (0, 6): [4, 5], (0, 7): [], (0, 8): [4, 5, 8], (1, 0): [6, 7], (1, 1): [], (1, 2): [],
                        (1, 3): [3, 7, 9], (1, 4): [], (1, 5): [3, 9], (1, 6): [3], (1, 7): [], (1, 8): [],
                        (2, 0): [2, 6, 8], (2, 1): [2, 6, 8], (2, 2): [6, 9], (2, 3): [2, 3, 9], (2, 4): [2, 3, 4, 5],
                        (2, 5): [], (2, 6): [3, 4, 5], (2, 7): [], (2, 8): [3, 4, 5, 6, 8], (3, 0): [], (3, 1): [3, 6],
                        (3, 2): [], (3, 3): [], (3, 4): [1, 3, 5, 6], (3, 5): [], (3, 6): [1, 3, 5], (3, 7): [],
                        (3, 8): [3, 5, 6], (4, 0): [4, 5, 6, 7, 8], (4, 1): [3, 6, 8], (4, 2): [4, 6, 7],
                        (4, 3): [1, 3, 8], (4, 4): [1, 3, 5, 6], (4, 5): [3, 5, 6, 8], (4, 6): [1, 2, 3, 4, 5, 7, 9],
                        (4, 7): [3, 4, 5, 6], (4, 8): [3, 4, 5, 6, 7, 9], (5, 0): [4, 5, 6, 7, 8], (5, 1): [3, 6, 8],
                        (5, 2): [], (5, 3): [3, 8], (5, 4): [], (5, 5): [], (5, 6): [3, 4, 5, 7], (5, 7): [3, 4, 5, 6],
                        (5, 8): [3, 4, 5, 6, 7], (6, 0): [1, 4], (6, 1): [], (6, 2): [], (6, 3): [], (6, 4): [1, 4, 7],
                        (6, 5): [4, 8], (6, 6): [], (6, 7): [], (6, 8): [4, 7], (7, 0): [1, 2, 4, 6], (7, 1): [],
                        (7, 2): [4, 6], (7, 3): [1, 2, 3, 9], (7, 4): [1, 2, 3, 4, 6], (7, 5): [3, 4, 6, 9], (7, 6): [],
                        (7, 7): [3, 4, 5], (7, 8): [3, 4, 5, 9], (8, 0): [2, 4, 6], (8, 1): [], (8, 2): [],
                        (8, 3): [2, 3, 7, 9], (8, 4): [2, 3, 4, 6, 7], (8, 5): [3, 4, 6, 9], (8, 6): [3, 4, 7, 9],
                        (8, 7): [3, 4], (8, 8): []}

    test_data_3_soln = [3, 1, 7, 6, 2, 4, 5, 9, 8,
                        6, 4, 5, 7, 8, 9, 3, 1, 2,
                        8, 2, 9, 3, 5, 1, 4, 7, 6,
                        9, 3, 2, 4, 6, 7, 1, 8, 5,
                        7, 8, 4, 1, 3, 5, 2, 6, 9,
                        5, 6, 1, 8, 9, 2, 7, 4, 3,
                        1, 9, 3, 5, 4, 8, 6, 2, 7,
                        2, 7, 6, 9, 1, 3, 8, 5, 4,
                        4, 5, 8, 2, 7, 6, 9, 3, 1]

    test_data_sole_candidates = [9, 3, 0, 6, 0, 0, 2, 4, 0,
                                 0, 0, 5, 8, 0, 0, 0, 0, 0,
                                 2, 0, 0, 0, 4, 0, 0, 8, 0,
                                 0, 1, 0, 0, 0, 0, 0, 0, 0,
                                 6, 0, 0, 0, 1, 0, 0, 0, 7,
                                 0, 0, 0, 0, 0, 0, 0, 1, 0,
                                 0, 9, 0, 0, 5, 0, 0, 0, 4,
                                 0, 0, 0, 0, 0, 9, 6, 0, 0,
                                 0, 7, 3, 0, 0, 1, 0, 9, 8]

    test_data_sole_candidates_poss = {(0, 0): [], (0, 1): [], (0, 2): [1, 7, 8], (0, 3): [], (0, 4): [7],
                                      (0, 5): [5, 7], (0, 6): [], (0, 7): [], (0, 8): [1, 5], (1, 0): [1, 4, 7],
                                      (1, 1): [4, 6], (1, 2): [], (1, 3): [], (1, 4): [2, 3, 7, 9], (1, 5): [2, 3, 7],
                                      (1, 6): [1, 3, 7, 9], (1, 7): [3, 6, 7], (1, 8): [1, 3, 6, 9], (2, 0): [],
                                      (2, 1): [6], (2, 2): [1, 6, 7], (2, 3): [1, 3, 5, 7, 9], (2, 4): [],
                                      (2, 5): [3, 5, 7], (2, 6): [1, 3, 5, 7, 9], (2, 7): [], (2, 8): [1, 3, 5, 6, 9],
                                      (3, 0): [3, 4, 5, 7, 8], (3, 1): [], (3, 2): [2, 4, 7, 8, 9],
                                      (3, 3): [2, 3, 4, 5, 7, 9], (3, 4): [2, 3, 6, 7, 8, 9],
                                      (3, 5): [2, 3, 4, 5, 6, 7, 8], (3, 6): [3, 4, 5, 8, 9],
                                      (3, 7): [2, 3, 5, 6], (3, 8): [2, 3, 5, 6, 9], (4, 0): [], (4, 1): [2, 4, 5, 8],
                                      (4, 2): [2, 4, 8, 9], (4, 3): [2, 3, 4, 5, 9], (4, 4): [],
                                      (4, 5): [2, 3, 4, 5, 8], (4, 6): [3, 4, 5, 8, 9], (4, 7): [2, 3, 5],
                                      (4, 8): [], (5, 0): [3, 4, 5, 7, 8], (5, 1): [2, 4, 5, 8],
                                      (5, 2): [2, 4, 7, 8, 9], (5, 3): [2, 3, 4, 5, 7, 9],
                                      (5, 4): [2, 3, 6, 7, 8, 9], (5, 5): [2, 3, 4, 5, 6, 7, 8],
                                      (5, 6): [3, 4, 5, 8, 9], (5, 7): [], (5, 8): [2, 3, 5, 6, 9],
                                      (6, 0): [1, 8], (6, 1): [], (6, 2): [1, 2, 6, 8], (6, 3): [2, 3, 7],
                                      (6, 4): [], (6, 5): [2, 3, 6, 7, 8], (6, 6): [1, 3, 7], (6, 7): [2, 3, 7],
                                      (6, 8): [], (7, 0): [1, 4, 5, 8], (7, 1): [2, 4, 5, 8], (7, 2): [1, 2, 4, 8],
                                      (7, 3): [2, 3, 4, 7], (7, 4): [2, 3, 7, 8], (7, 5): [], (7, 6): [],
                                      (7, 7): [2, 3, 5, 7], (7, 8): [1, 2, 3, 5], (8, 0): [4, 5], (8, 1): [],
                                      (8, 2): [], (8, 3): [2, 4], (8, 4): [2, 6], (8, 5): [], (8, 6): [5], (8, 7): [],
                                      (8, 8): []}

    test_data_sole_candidates_soln = [9, 3, 8, 6, 7, 5, 2, 4, 1,
                                      1, 4, 5, 8, 9, 2, 7, 3, 6,
                                      2, 6, 7, 1, 4, 3, 9, 8, 5,
                                      7, 1, 9, 5, 3, 8, 4, 6, 2,
                                      6, 8, 2, 9, 1, 4, 3, 5, 7,
                                      3, 5, 4, 7, 2, 6, 8, 1, 9,
                                      8, 9, 6, 3, 5, 7, 1, 2, 4,
                                      5, 2, 1, 4, 8, 9, 6, 7, 3,
                                      4, 7, 3, 2, 6, 1, 5, 9, 8]

    def setUp(self):
        self.blank_board = SudokuBoard()
        # NOTE: the random datasets do not follow Sudoku rules, they are only intended for data access testing
        self.random_test_data = [randint(1, 9) for _ in range(81)]
        self.random_board = SudokuBoard(self.random_test_data)
        self.random_i, self.random_j, self.random_s = randint(0, 8), randint(0, 8), randint(0, 8)
        self.random_value = randint(1, 9)
        # test boards 1, 2, 3 are all solvable sudokus
        self.test_board_1 = SudokuBoard(self.test_data_1)
        self.test_board_2 = SudokuBoard(self.test_data_2)
        self.test_board_3 = SudokuBoard(self.test_data_3)
        self.test_sole_candidates_board = SudokuBoard(self.test_data_sole_candidates)
        self.assertNotEqual(self.test_sole_candidates_board.possible_values, {(x, y): [] for x in range(9) for y in range(9)})
        self.assertNotEqual(self.test_board_1.possible_values, {(x, y): [] for x in range(9) for y in range(9)})
        self.assertNotEqual(self.test_board_2.possible_values, {(x, y): [] for x in range(9) for y in range(9)})
        self.assertNotEqual(self.test_board_3.possible_values, {(x, y): [] for x in range(9) for y in range(9)})

    def tearDown(self):
        # delete all of the boards that were created to force them to release their files
        del self.blank_board
        del self.random_board
        del self.test_board_1
        del self.test_board_2
        del self.test_board_3
        del self.test_sole_candidates_board
        # remove the file this generated
        for filename in glob.glob('reasons_*.txt'):
            os.remove(filename)

    def test_init_empty(self):
        correct = [[0 for _ in range(9)] for _ in range(9)]
        self.assertEqual(self.blank_board.board, correct)

    def test_init_non_empty(self):
        correct = [[self.random_test_data[(9*j)+i] for i in range(9)] for j in range(9)]
        self.assertEqual(self.random_board.board, correct)

    def test_init_from_sdk_file(self):
        self.sole_candidates = SudokuBoard(file_path='TestCases\\nakedsingle1.sdk')
        self.assertEqual(self.sole_candidates, self.test_sole_candidates_board)
        del self.sole_candidates

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
        self.assertTrue(self.random_board == self.random_board)
        self.assertTrue(self.test_board_1 == self.test_board_1)
        self.assertTrue(self.test_board_2 == self.test_board_2)
        self.assertTrue(self.test_board_3 == self.test_board_3)
        self.assertFalse(self.test_board_1 == self.test_board_2)
        self.assertFalse(self.test_board_2 == self.test_board_3)
        self.assertFalse(self.test_board_3 == self.test_board_1)

    def test_set(self):
        self.blank_board.set(self.random_i, self.random_j, self.random_value)
        self.assertEqual(self.blank_board.board[self.random_i][self.random_j], self.random_value)

    def test_get(self):
        self.blank_board.set(self.random_i, self.random_j, self.random_value)
        self.assertEqual(self.blank_board.get(self.random_i, self.random_j), self.random_value)
        self.assertEqual(self.test_board_1.get(0, 0), 1)
        self.assertEqual(self.test_board_2.get(0, 0), 9)
        self.assertEqual(self.test_board_3.get(0, 0), 3)

    def test_row(self):
        self.assertEqual(self.random_board.row(self.random_i), self.random_board.board[self.random_i])
        self.assertEqual(self.test_board_1.row(0), [1, 0, 0, 0, 9, 0, 3, 0, 0])
        self.assertEqual(self.test_board_2.row(0), [9, 0, 0, 3, 0, 0, 5, 8, 0])
        self.assertEqual(self.test_board_3.row(0), [3, 0, 0, 6, 0, 0, 0, 9, 0])

    def test_column(self):
        correct = [row[self.random_j] for row in self.random_board.board]
        self.assertEqual(self.random_board.column(self.random_j), correct)
        self.assertEqual(self.test_board_1.column(0), [1, 0, 0, 3, 0, 0, 2, 0, 0])
        self.assertEqual(self.test_board_2.column(0), [9, 0, 0, 1, 0, 0, 5, 0, 0])
        self.assertEqual(self.test_board_3.column(0), [3, 0, 0, 9, 0, 0, 0, 0, 0])

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
        self.assertEqual(self.test_board_1.sector(0), [1, 0, 0, 0, 6, 0, 0, 0, 4])
        self.assertEqual(self.test_board_2.sector(0), [9, 0, 0, 0, 8, 0, 0, 0, 0])
        self.assertEqual(self.test_board_3.sector(0), [3, 0, 0, 0, 4, 5, 0, 0, 0])

    def test_get_possibilities(self):
        self.assertEqual(self.random_board.get_possibilities(self.random_i, self.random_j), self.random_board.possible_values[(self.random_i, self.random_j)])
        self.assertEqual(self.test_board_1.get_possibilities(0, 0), self.test_data_1_poss[(0, 0)])
        self.assertEqual(self.test_board_2.get_possibilities(0, 0), self.test_data_2_poss[(0, 0)])
        self.assertEqual(self.test_board_3.get_possibilities(0, 0), self.test_data_3_poss[(0, 0)])

    def test_get_row_possibilities(self):
        self.assertEqual(self.random_board.get_row_possibilities(self.random_i),
                         {(self.random_i, x):self.random_board.possible_values[(self.random_i, x)] for x in range(9)})
        self.assertEqual(self.test_board_1.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 7, 8], (0, 3): [2, 6], (0, 4): [],
                          (0, 5): [2, 4, 6, 8], (0, 6): [], (0, 7): [2, 4, 5, 7], (0, 8): [2, 4, 5, 6, 7]})
        self.assertEqual(self.test_board_2.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2, 7], (0, 3): [], (0, 4): [1, 2, 4, 6],
                          (0, 5): [1, 4, 6], (0, 6): [], (0, 7): [], (0, 8): [1]})
        self.assertEqual(self.test_board_3.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [1, 2, 8], (0, 2): [7], (0, 3): [], (0, 4): [2, 4, 5, 7],
                          (0, 5): [4, 5], (0, 6): [4, 5], (0, 7): [], (0, 8): [4, 5, 8]})

    def test_get_col_possibilities(self):
        self.assertEqual(self.random_board.get_col_possibilities(self.random_j),
                         {(x, self.random_j): self.random_board.possible_values[(x, self.random_j)] for x in range(9)})
        self.assertEqual(self.test_board_1.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [5, 9], (2, 0): [7, 8, 9], (3, 0): [], (4, 0): [4, 6, 9],
                          (5, 0): [4, 6, 8], (6, 0): [], (7, 0): [4, 5, 6, 7], (8, 0): [5, 6, 7]})
        self.assertEqual(self.test_board_2.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [2, 4, 6], (2, 0): [3, 6], (3, 0): [], (4, 0): [2, 3, 6, 7],
                          (5, 0): [4, 7, 8], (6, 0): [], (7, 0): [2, 3, 8], (8, 0): [2, 8]})
        self.assertEqual(self.test_board_3.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [6, 7], (2, 0): [2, 6, 8], (3, 0): [], (4, 0): [4, 5, 6, 7, 8],
                          (5, 0): [4, 5, 6, 7, 8], (6, 0): [1, 4], (7, 0): [1, 2, 4, 6], (8, 0): [2, 4, 6]})

    def test_get_sector_possibilities(self):
        self.assertEqual(self.random_board.get_sector_possibilities(self.random_j),
                         {(x, y): self.random_board.possible_values[(x, y)] for x in range(9) for y in range(9)
                          if self.random_board.sector_lookup(x, y) == self.random_j})
        self.assertEqual(self.test_board_1.get_sector_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 7, 8], (1, 0): [5, 9], (1, 1): [],
                          (1, 2): [2, 3], (2, 0): [7, 8, 9], (2, 1): [2, 3, 9], (2, 2): []})
        self.assertEqual(self.test_board_2.get_sector_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2, 7], (1, 0): [2, 4, 6], (1, 1): [],
                          (1, 2): [1, 2, 5], (2, 0): [3, 6], (2, 1): [3, 5, 6], (2, 2): [1, 3, 5]})
        self.assertEqual(self.test_board_3.get_sector_possibilities(0),
                         {(0, 0): [], (0, 1): [1, 2, 8], (0, 2): [7], (1, 0): [6, 7], (1, 1): [],
                          (1, 2): [], (2, 0): [2, 6, 8], (2, 1): [2, 6, 8], (2, 2): [6, 9]})

    def test_get_sector_subrow_possibilities(self):
        self.assertEqual(self.random_board.get_sector_subrow_possibilities(
            SudokuBoard.sector_lookup(self.random_i, self.random_j), self.random_i),
            {(self.random_i, x): self.random_board.possible_values[(self.random_i, x)] for x in range(9)
             if self.random_board.sector_lookup(self.random_i, x) ==
             SudokuBoard.sector_lookup(self.random_i, self.random_j)})
        self.assertEqual(self.test_board_1.get_sector_subrow_possibilities(0, 0),
                         {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 7, 8]})
        self.assertEqual(self.test_board_2.get_sector_subrow_possibilities(0, 0),
                         {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2, 7]})
        self.assertEqual(self.test_board_3.get_sector_subrow_possibilities(0, 0),
                         {(0, 0): [], (0, 1): [1, 2, 8], (0, 2): [7]})

    def test_get_sector_subcolumn_possibilities(self):
        self.assertEqual(self.random_board.get_sector_subcolumn_possibilities(
            SudokuBoard.sector_lookup(self.random_i, self.random_j), self.random_j),
            {(x, self.random_j): self.random_board.possible_values[(x, self.random_j)] for x in range(9)
             if self.random_board.sector_lookup(x, self.random_j) ==
             SudokuBoard.sector_lookup(self.random_i, self.random_j)})
        self.assertEqual(self.test_board_1.get_sector_subcolumn_possibilities(0, 0),
                         {(0, 0): [], (1, 0): [5, 9], (2, 0): [7, 8, 9]})
        self.assertEqual(self.test_board_2.get_sector_subcolumn_possibilities(0, 0),
                         {(0, 0): [], (1, 0): [2, 4, 6], (2, 0): [3, 6]})
        self.assertEqual(self.test_board_3.get_sector_subcolumn_possibilities(0, 0),
                         {(0, 0): [], (1, 0): [6, 7], (2, 0): [2, 6, 8]})

    def test_set_correctly_updates_possibilites(self):
        self.test_board_1.set(8, 8, 2)
        self.assertNotIn(2, self.test_board_1.get_row_possibilities(8))
        self.assertNotIn(2, self.test_board_1.get_col_possibilities(8))
        self.assertNotIn(2, self.test_board_1.get_sector_possibilities(SudokuBoard.sector_lookup(8, 8)))

        self.test_board_2.set(0, 8, 1)
        self.assertNotIn(1, self.test_board_2.get_row_possibilities(0))
        self.assertNotIn(1, self.test_board_2.get_col_possibilities(8))
        self.assertNotIn(1, self.test_board_2.get_sector_possibilities(SudokuBoard.sector_lookup(0, 8)))

        self.test_board_3.set(0, 8, 8)
        self.assertNotIn(8, self.test_board_3.get_row_possibilities(0))
        self.assertNotIn(8, self.test_board_3.get_col_possibilities(8))
        self.assertNotIn(8, self.test_board_3.get_sector_possibilities(SudokuBoard.sector_lookup(0, 8)))

    def test_set_poss_values(self):
        # TODO : ensure that the poss updates are returned correctly
        self.test_board_1.set_poss_values(self.test_board_2.possible_values)
        self.test_board_3.set_poss_values(self.test_board_2.possible_values)
        self.assertEqual(self.test_board_1.possible_values, self.test_board_3.possible_values)

    def test_unique_to_only_one(self):
        list_1 = [1, 2, 3]
        list_2 = [2, 3, 4]
        list_3 = [5, 6, 7]
        # unique to first list
        self.assertEqual(SudokuBoard.unique_to_only_one(1, list_1, list_2, list_3), 0)
        # unique to second list
        self.assertEqual(SudokuBoard.unique_to_only_one(4, list_1, list_2, list_3), 1)
        # unique to third list
        self.assertEqual(SudokuBoard.unique_to_only_one(7, list_1, list_2, list_3), 2)
        # not in any list
        self.assertEqual(SudokuBoard.unique_to_only_one(9, list_1, list_2, list_3), -1)
        # not unique
        self.assertEqual(SudokuBoard.unique_to_only_one(2, list_1, list_2, list_3), -1)

    def test_unique_to_two_rows(self):
        # different combination of return values
        self.assertEqual(self.test_board_3.unique_to_two_rows(6, 0), (1, 2))
        self.assertEqual(self.test_board_3.unique_to_two_rows(7, 0), (0, 1))
        self.assertEqual(self.test_board_3.unique_to_two_rows(8, 0), (0, 2))
        # non existent
        self.assertEqual(self.test_board_3.unique_to_two_rows(5, 0), -1)
        # exists in only one row
        self.assertEqual(self.test_board_3.unique_to_two_rows(1, 0), -1)
        # exists in all 3 rows
        self.assertEqual(self.test_board_1.unique_to_two_rows(2, 0), -1)

    def test_unique_to_two_cols(self):
        # different combination of return values
        self.assertEqual(self.test_board_3.unique_to_two_cols(7, 0), (0, 2))
        self.assertEqual(self.test_board_3.unique_to_two_cols(2, 0), (0, 1))
        self.assertEqual(self.test_board_1.unique_to_two_cols(2, 0), (1, 2))
        # non existent
        self.assertEqual(self.test_board_3.unique_to_two_cols(5, 0), -1)
        # exists in only one column
        self.assertEqual(self.test_board_3.unique_to_two_cols(1, 0), -1)
        # exists in all 3 columns
        self.assertEqual(self.test_board_3.unique_to_two_cols(6, 0), -1)

    def test_is_solved(self):
        self.assertFalse(self.blank_board.is_solved())
        self.assertFalse(self.test_board_1.is_solved())
        self.assertFalse(self.test_board_2.is_solved())
        self.assertFalse(self.test_board_3.is_solved())
        self.assertFalse(self.test_sole_candidates_board.is_solved())
        self.assertTrue(SudokuBoard(self.test_data_1_soln).is_solved())
        self.assertTrue(SudokuBoard(self.test_data_2_soln).is_solved())
        self.assertTrue(SudokuBoard(self.test_data_3_soln).is_solved())
        self.assertTrue(SudokuBoard(self.test_data_sole_candidates_soln).is_solved())

    def test_row_indices_in_sector(self):
        self.assertEqual(self.blank_board.row_indices_in_sector(0), [0, 1, 2])
        self.assertEqual(self.blank_board.row_indices_in_sector(1), [0, 1, 2])
        self.assertEqual(self.blank_board.row_indices_in_sector(2), [0, 1, 2])
        self.assertEqual(self.blank_board.row_indices_in_sector(3), [3, 4, 5])
        self.assertEqual(self.blank_board.row_indices_in_sector(4), [3, 4, 5])
        self.assertEqual(self.blank_board.row_indices_in_sector(5), [3, 4, 5])
        self.assertEqual(self.blank_board.row_indices_in_sector(6), [6, 7, 8])
        self.assertEqual(self.blank_board.row_indices_in_sector(7), [6, 7, 8])
        self.assertEqual(self.blank_board.row_indices_in_sector(8), [6, 7, 8])

    def test_col_indices_in_sector(self):
        self.assertEqual(self.blank_board.col_indices_in_sector(0), [0, 1, 2])
        self.assertEqual(self.blank_board.col_indices_in_sector(1), [3, 4, 5])
        self.assertEqual(self.blank_board.col_indices_in_sector(2), [6, 7, 8])
        self.assertEqual(self.blank_board.col_indices_in_sector(3), [0, 1, 2])
        self.assertEqual(self.blank_board.col_indices_in_sector(4), [3, 4, 5])
        self.assertEqual(self.blank_board.col_indices_in_sector(5), [6, 7, 8])
        self.assertEqual(self.blank_board.col_indices_in_sector(6), [0, 1, 2])
        self.assertEqual(self.blank_board.col_indices_in_sector(7), [3, 4, 5])
        self.assertEqual(self.blank_board.col_indices_in_sector(8), [6, 7, 8])

    def test_eliminate_poss_from_row(self):
        # test board_ 1 > 3 move
        actual_moves = self.test_board_1.eliminate_possibilities_from_row(0, 7, "test_val")
        self.assertEqual(self.test_board_1.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 8], (0, 3): [2, 6], (0, 4): [],
                          (0, 5): [2, 4, 6, 8], (0, 6): [], (0, 7): [2, 4, 5], (0, 8): [2, 4, 5, 6]})
        expected_moves = [
            Move(REMOVE_POSS, 7, (0, 2), str((0, 2)) + ' had possibility value of ' + str(7) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + "test_val"),
            Move(REMOVE_POSS, 7, (0, 7), str((0, 7)) + ' had possibility value of ' + str(7) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + "test_val"),
            Move(REMOVE_POSS, 7, (0, 8), str((0, 8)) + ' had possibility value of ' + str(7) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + "test_val")]
        self.assertEqual(expected_moves, actual_moves)

        # test board_ 2 > 1 move
        actual_moves = self.test_board_2.eliminate_possibilities_from_row(0, 7, "test_val")
        self.assertEqual(self.test_board_2.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2], (0, 3): [], (0, 4): [1, 2, 4, 6],
                          (0, 5): [1, 4, 6], (0, 6): [], (0, 7): [], (0, 8): [1]})
        expected_moves = [
            Move(REMOVE_POSS, 7, (0, 2), str((0, 2)) + ' had possibility value of ' + str(7) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + "test_val")]
        self.assertEqual(expected_moves, actual_moves)

        # test board_ 3 > 0 moves
        actual_moves = self.test_board_3.eliminate_possibilities_from_row(0, 9, "test_val")
        self.assertEqual(self.test_board_3.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [1, 2, 8], (0, 2): [7], (0, 3): [], (0, 4): [2, 4, 5, 7],
                          (0, 5): [4, 5], (0, 6): [4, 5], (0, 7): [], (0, 8): [4, 5, 8]})
        self.assertEqual(actual_moves, [])

    def test_eliminate_poss_from_col(self):
        self.test_board_1.eliminate_possibilities_from_column(0, 9, "test_val")
        self.assertEqual(self.test_board_1.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [5], (2, 0): [7, 8], (3, 0): [], (4, 0): [4, 6],
                          (5, 0): [4, 6, 8], (6, 0): [], (7, 0): [4, 5, 6, 7], (8, 0): [5, 6, 7]})
        self.test_board_2.eliminate_possibilities_from_column(0, 8, "test_val")
        self.assertEqual(self.test_board_2.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [2, 4, 6], (2, 0): [3, 6], (3, 0): [], (4, 0): [2, 3, 6, 7],
                          (5, 0): [4, 7], (6, 0): [], (7, 0): [2, 3], (8, 0): [2]})
        self.test_board_3.eliminate_possibilities_from_column(0, 9, "test_val")
        self.assertEqual(self.test_board_3.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [6, 7], (2, 0): [2, 6, 8], (3, 0): [], (4, 0): [4, 5, 6, 7, 8],
                          (5, 0): [4, 5, 6, 7, 8], (6, 0): [1, 4], (7, 0): [1, 2, 4, 6], (8, 0): [2, 4, 6]})

    def test_eliminate_poss_from_sector(self):
        self.test_board_1.eliminate_possibilities_from_sector(0, 9)
        self.assertEqual(self.test_board_1.get_sector_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 7, 8], (1, 0): [5], (1, 1): [],
                          (1, 2): [2, 3], (2, 0): [7, 8], (2, 1): [2, 3], (2, 2): []})
        self.test_board_2.eliminate_possibilities_from_sector(0, 8)
        self.assertEqual(self.test_board_2.get_sector_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2, 7], (1, 0): [2, 4, 6], (1, 1): [],
                          (1, 2): [1, 2, 5], (2, 0): [3, 6], (2, 1): [3, 5, 6], (2, 2): [1, 3, 5]})
        self.test_board_3.eliminate_possibilities_from_sector(0, 2)
        self.assertEqual(self.test_board_3.get_sector_possibilities(0),
                         {(0, 0): [], (0, 1): [1, 8], (0, 2): [7], (1, 0): [6, 7], (1, 1): [],
                          (1, 2): [], (2, 0): [6, 8], (2, 1): [6, 8], (2, 2): [6, 9]})

    def test_eliminate_possibilities_from_row_swordfish(self):
        self.test_board_1.eliminate_possibilities_from_row_swordfish(0, 2, (1, 2, 8))
        self.assertEqual(self.test_board_1.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 7, 8], (0, 3): [6], (0, 4): [],
                          (0, 5): [4, 6, 8], (0, 6): [], (0, 7): [4, 5, 7], (0, 8): [2, 4, 5, 6, 7]})
        self.test_board_2.eliminate_possibilities_from_row_swordfish(0, 1, (2, 4, 8))
        self.assertEqual(self.test_board_2.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2, 7], (0, 3): [], (0, 4): [1, 2, 4, 6],
                          (0, 5): [4, 6], (0, 6): [], (0, 7): [], (0, 8): [1]})
        self.test_board_3.eliminate_possibilities_from_row_swordfish(0, 2, (0, 2, 3))
        self.assertEqual(self.test_board_3.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [1, 8], (0, 2): [7], (0, 3): [], (0, 4): [4, 5, 7],
                          (0, 5): [4, 5], (0, 6): [4, 5], (0, 7): [], (0, 8): [4, 5, 8]})

    def test_eliminate_possibilities_from_col_swordfish(self):
        self.test_board_1.eliminate_possibilities_from_column_swordfish(0, 7, (2, 7, 8))
        self.assertEqual(self.test_board_1.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [5, 9], (2, 0): [7, 8, 9], (3, 0): [], (4, 0): [4, 6, 9],
                          (5, 0): [4, 6, 8], (6, 0): [], (7, 0): [4, 5, 6, 7], (8, 0): [5, 6, 7]})
        self.test_board_2.eliminate_possibilities_from_column_swordfish(0, 2, (1, 4, 8))
        self.assertEqual(self.test_board_2.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [2, 4, 6], (2, 0): [3, 6], (3, 0): [], (4, 0): [2, 3, 6, 7],
                          (5, 0): [4, 7, 8], (6, 0): [], (7, 0): [3, 8], (8, 0): [2, 8]})
        self.test_board_3.eliminate_possibilities_from_column_swordfish(0, 6, (5, 7, 8))
        self.assertEqual(self.test_board_3.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [7], (2, 0): [2, 8], (3, 0): [], (4, 0): [4, 5, 7, 8],
                          (5, 0): [4, 5, 6, 7, 8], (6, 0): [1, 4], (7, 0): [1, 2, 4, 6], (8, 0): [2, 4, 6]})

    def test_print_reason_to_file(self):
        test_string = 'test test test'
        self.blank_board.print_reason_to_file(test_string)
        # force blank board to free the file
        self.blank_board.__del__()
        with open(self.blank_board.file.name, 'r') as written_to_file:
            self.assertIsNotNone(written_to_file)
            value = written_to_file.readlines()
            self.assertEqual(value[-1], test_string + '\n')
            written_to_file.close()

    def test_sole_candidates(self):
        # TODO add all naked single test cases
        # TODO : ensure that moves are returned correctly
        self.test_sole_candidates_board.sole_candidates()
        self.assertEqual(self.test_sole_candidates_board.get(0, 4), 7)
        self.assertEqual(self.test_sole_candidates_board.get(2, 1), 6)
        self.assertEqual(self.test_sole_candidates_board.get(8, 6), 5)

    # /////////////////// TODO //////////////////////
    # ******************** test pass and fail *****************

    def test_unique_candidates_generic_row(self):
        pass

    def test_unique_candidates_generic_column(self):
        pass

    def test_unique_candidates_generic_sector(self):
        pass

    def test_unique_candidates(self):
        # make sure to bypass / not bypass short circuiting
        pass

    def test_sector_line_interaction_generic_row(self):
        pass

    def test_sector_line_interaction_generic_column(self):
        pass

    def test_sector_line_interaction(self):
        # make sure to bypass / not bypass short circuiting
        pass

    def test_sector_sector_interaction(self):
        pass

    def test_naked_subset_row(self):
        pass

    def test_naked_subset_col(self):
        pass

    def test_naked_subset_sector(self):
        pass

    def test_naked_subset(self):
        # make sure to bypass / not bypass short circuiting
        pass

    def test_hidden_subset_row(self):
        pass

    def test_hidden_subset_col(self):
        pass

    def test_hidden_subset_sector(self):
        pass

    def test_hidden_subset(self):
        # make sure to bypass / not bypass short circuiting
        pass

    def test_x_wing(self):
        pass

    def test_swordfish_row(self):
        pass

    def test_swordfish_col(self):
        pass

    def test_swordfish(self):
        # make sure to bypass / not bypass short circuiting
        pass

    def test_force_chain(self):
        pass

    def test_solve(self):
        # test valid and invalid
        pass


