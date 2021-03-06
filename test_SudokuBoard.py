import glob
import os
import unittest
from copy import deepcopy
from random import randint
from SudokuBoard import SudokuBoard
from itertools import product
from Move import Move
from Move import NUMBER_SOLVE, REMOVE_POSS


# TODO - write better, more comprehensive, tests
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
        self.assertNotEqual(self.test_sole_candidates_board.possible_values,
                            {(x, y): [] for x in range(9) for y in range(9)})
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
        correct = [[self.random_test_data[(9 * j) + i] for i in range(9)] for j in range(9)]
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
        correct = [self.random_board.board[i][j] for i, j in product(range(9), range(9)) if
                   self.random_board.sector_lookup(i, j) == self.random_s]
        self.assertEqual(self.random_board.sector(self.random_s), correct)
        self.assertEqual(self.test_board_1.sector(0), [1, 0, 0, 0, 6, 0, 0, 0, 4])
        self.assertEqual(self.test_board_2.sector(0), [9, 0, 0, 0, 8, 0, 0, 0, 0])
        self.assertEqual(self.test_board_3.sector(0), [3, 0, 0, 0, 4, 5, 0, 0, 0])

    def test_get_possibilities(self):
        self.assertEqual(self.random_board.get_possibilities(self.random_i, self.random_j),
                         self.random_board.possible_values[(self.random_i, self.random_j)])
        self.assertEqual(self.test_board_1.get_possibilities(0, 0), self.test_data_1_poss[(0, 0)])
        self.assertEqual(self.test_board_2.get_possibilities(0, 0), self.test_data_2_poss[(0, 0)])
        self.assertEqual(self.test_board_3.get_possibilities(0, 0), self.test_data_3_poss[(0, 0)])

    def test_get_row_possibilities(self):
        self.assertEqual(self.random_board.get_row_possibilities(self.random_i),
                         {(self.random_i, x): self.random_board.possible_values[(self.random_i, x)] for x in range(9)})
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
        dict_1 = {(0, 0): [1, 2, 3], (0, 1): [6, 7, 8]}
        dict_2 = {(0, 0): [2, 3, 4], (0, 1): [6, 7, 8]}
        dict_3 = {(0, 0): [5, 6, 7], (0, 1): [6, 7, 8]}
        # unique to first list
        self.assertEqual(SudokuBoard.unique_to_only_one(1, dict_1, dict_2, dict_3), 0)
        # unique to second list
        self.assertEqual(SudokuBoard.unique_to_only_one(4, dict_1, dict_2, dict_3), 1)
        # unique to third list
        self.assertEqual(SudokuBoard.unique_to_only_one(5, dict_1, dict_2, dict_3), 2)
        # not in any list
        self.assertEqual(SudokuBoard.unique_to_only_one(9, dict_1, dict_2, dict_3), -1)
        # not unique
        self.assertEqual(SudokuBoard.unique_to_only_one(7, dict_1, dict_2, dict_3), -1)

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
        actual_moves = self.test_board_1.eliminate_possibilities_from_row(0, 7, [(0, 0), (0, 2), (4, 0), (4, 2)])
        self.assertEqual(self.test_board_1.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 7, 8], (0, 3): [2, 6], (0, 4): [],
                          (0, 5): [2, 4, 6, 8], (0, 6): [], (0, 7): [2, 4, 5], (0, 8): [2, 4, 5, 6]})
        expected_moves = [
            Move(REMOVE_POSS, 7, (0, 7), 'Row 0 had possibility value of ' + str(7) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + str(
                [(0, 0), (0, 2), (4, 0), (4, 2)])),
            Move(REMOVE_POSS, 7, (0, 8), 'Row 0 had possibility value of ' + str(7) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + str(
                [(0, 0), (0, 2), (4, 0), (4, 2)]))]
        self.assertEqual(expected_moves, actual_moves)

        # test board_ 2 > 1 move
        actual_moves = self.test_board_2.eliminate_possibilities_from_row(0, 7, [(0, 0), (0, 1), (4, 0), (4, 1)])
        self.assertEqual(self.test_board_2.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2], (0, 3): [], (0, 4): [1, 2, 4, 6],
                          (0, 5): [1, 4, 6], (0, 6): [], (0, 7): [], (0, 8): [1]})
        expected_moves = [
            Move(REMOVE_POSS, 7, (0, 2), 'Row 0 had possibility value of ' + str(7) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + str(
                [(0, 0), (0, 1), (4, 0), (4, 1)]))]
        self.assertEqual(expected_moves, actual_moves)

        # test board_ 3 > 0 moves
        actual_moves = self.test_board_3.eliminate_possibilities_from_row(0, 9, [(0, 0), (0, 1), (4, 0), (4, 1)])
        self.assertEqual(self.test_board_3.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [1, 2, 8], (0, 2): [7], (0, 3): [], (0, 4): [2, 4, 5, 7],
                          (0, 5): [4, 5], (0, 6): [4, 5], (0, 7): [], (0, 8): [4, 5, 8]})
        self.assertEqual(actual_moves, [])

    def test_eliminate_poss_from_col(self):
        # test_board 1 > 3 moves
        actual_moves = self.test_board_1.eliminate_possibilities_from_column(0, 9, [(0, 0), (0, 8), (4, 0), (4, 8)])
        self.assertEqual(self.test_board_1.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [5], (2, 0): [7, 8], (3, 0): [], (4, 0): [4, 6, 9],
                          (5, 0): [4, 6, 8], (6, 0): [], (7, 0): [4, 5, 6, 7], (8, 0): [5, 6, 7]})
        expected_moves = [
            Move(REMOVE_POSS, 9, (1, 0), 'Column 0 had possibility value of ' + str(9) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + str(
                [(0, 0), (0, 8), (4, 0), (4, 8)])),
            Move(REMOVE_POSS, 9, (2, 0), 'Column 0 had possibility value of ' + str(9) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + str(
                [(0, 0), (0, 8), (4, 0), (4, 8)]))
        ]
        self.assertEqual(expected_moves, actual_moves)

        # test_board 2 > 3 moves
        actual_moves = self.test_board_2.eliminate_possibilities_from_column(0, 8, [(0, 0), (0, 8), (4, 0), (4, 8)])
        self.assertEqual(self.test_board_2.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [2, 4, 6], (2, 0): [3, 6], (3, 0): [], (4, 0): [2, 3, 6, 7],
                          (5, 0): [4, 7], (6, 0): [], (7, 0): [2, 3], (8, 0): [2]})
        expected_moves = [
            Move(REMOVE_POSS, 8, (5, 0), 'Column 0 had possibility value of ' + str(8) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + str(
                [(0, 0), (0, 8), (4, 0), (4, 8)])),
            Move(REMOVE_POSS, 8, (7, 0), 'Column 0 had possibility value of ' + str(8) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + str(
                [(0, 0), (0, 8), (4, 0), (4, 8)])),
            Move(REMOVE_POSS, 8, (8, 0), 'Column 0 had possibility value of ' + str(8) +
                 ' removed because there was ' + 'an x-wing interaction between cells ' + str(
                [(0, 0), (0, 8), (4, 0), (4, 8)]))]
        self.assertEqual(expected_moves, actual_moves)

        # test_board 3 > 0 moves
        actual_moves = self.test_board_3.eliminate_possibilities_from_column(0, 9, [(0, 0), (0, 8), (4, 0), (4, 8)])
        self.assertEqual(self.test_board_3.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [6, 7], (2, 0): [2, 6, 8], (3, 0): [], (4, 0): [4, 5, 6, 7, 8],
                          (5, 0): [4, 5, 6, 7, 8], (6, 0): [1, 4], (7, 0): [1, 2, 4, 6], (8, 0): [2, 4, 6]})
        self.assertEqual([], actual_moves)

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
        # test_board 1 > 3 moves
        actual_moves = self.test_board_1.eliminate_possibilities_from_row_swordfish(0, 2, (1, 2, 8))
        self.assertEqual(self.test_board_1.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 5], (0, 2): [2, 7, 8], (0, 3): [6], (0, 4): [],
                          (0, 5): [4, 6, 8], (0, 6): [], (0, 7): [4, 5, 7], (0, 8): [2, 4, 5, 6, 7]})
        expected_moves = [
            Move(REMOVE_POSS, 2, (0, 3), 'Row 0 ' + str((0, 3)) + ' had possibility value of ' + str(2) +
                 ' removed because there was ' + 'a swordfish interaction between columns ' + str((1, 2, 8))),
            Move(REMOVE_POSS, 2, (0, 5), 'Row 0 ' + str((0, 5)) + ' had possibility value of ' + str(2) +
                 ' removed because there was ' + 'a swordfish interaction between columns ' + str((1, 2, 8))),
            Move(REMOVE_POSS, 2, (0, 7), 'Row 0 ' + str((0, 7)) + ' had possibility value of ' + str(2) +
                 ' removed because there was ' + 'a swordfish interaction between columns ' + str((1, 2, 8)))]
        self.assertEqual(expected_moves, actual_moves)

        # test_board 2 > 1 move
        actual_moves = self.test_board_2.eliminate_possibilities_from_row_swordfish(0, 1, (2, 4, 8))
        self.assertEqual(self.test_board_2.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [2, 4, 6], (0, 2): [1, 2, 7], (0, 3): [], (0, 4): [1, 2, 4, 6],
                          (0, 5): [4, 6], (0, 6): [], (0, 7): [], (0, 8): [1]})
        expected_moves = [
            Move(REMOVE_POSS, 1, (0, 5), 'Row 0 ' + str((0, 5)) + ' had possibility value of ' + str(1) +
                 ' removed because there was ' + 'a swordfish interaction between columns ' + str((2, 4, 8)))]
        self.assertEqual(expected_moves, actual_moves)

        # test_board 3 > 2 moves
        actual_moves = self.test_board_3.eliminate_possibilities_from_row_swordfish(0, 2, (0, 2, 3))
        self.assertEqual(self.test_board_3.get_row_possibilities(0),
                         {(0, 0): [], (0, 1): [1, 8], (0, 2): [7], (0, 3): [], (0, 4): [4, 5, 7],
                          (0, 5): [4, 5], (0, 6): [4, 5], (0, 7): [], (0, 8): [4, 5, 8]})
        expected_moves = [
            Move(REMOVE_POSS, 2, (0, 1), 'Row 0 ' + str((0, 1)) + ' had possibility value of ' + str(2) +
                 ' removed because there was ' + 'a swordfish interaction between columns ' + str((0, 2, 3))),
            Move(REMOVE_POSS, 2, (0, 4), 'Row 0 ' + str((0, 4)) + ' had possibility value of ' + str(2) +
                 ' removed because there was ' + 'a swordfish interaction between columns ' + str((0, 2, 3)))]
        self.assertEqual(expected_moves, actual_moves)

    def test_eliminate_possibilities_from_col_swordfish(self):
        # test_board 1 > 0 moves
        actual_moves = self.test_board_1.eliminate_possibilities_from_column_swordfish(0, 7, (2, 7, 8))
        self.assertEqual(self.test_board_1.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [5, 9], (2, 0): [7, 8, 9], (3, 0): [], (4, 0): [4, 6, 9],
                          (5, 0): [4, 6, 8], (6, 0): [], (7, 0): [4, 5, 6, 7], (8, 0): [5, 6, 7]})
        self.assertEqual([], actual_moves)

        # test_board > 1 move
        actual_moves = self.test_board_2.eliminate_possibilities_from_column_swordfish(0, 2, (1, 4, 8))
        self.assertEqual(self.test_board_2.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [2, 4, 6], (2, 0): [3, 6], (3, 0): [], (4, 0): [2, 3, 6, 7],
                          (5, 0): [4, 7, 8], (6, 0): [], (7, 0): [3, 8], (8, 0): [2, 8]})
        expected_moves = [
            Move(REMOVE_POSS, 2, (7, 0), 'Column 0 ' + str((7, 0)) + ' had possibility value of ' + str(2) +
                 ' removed because there was ' + 'a swordfish interaction between rows ' + str((1, 4, 8)))]

        self.assertEqual(expected_moves, actual_moves)

        # test_board 3 > 3 moves
        actual_moves = self.test_board_3.eliminate_possibilities_from_column_swordfish(0, 6, (5, 7, 8))
        self.assertEqual(self.test_board_3.get_col_possibilities(0),
                         {(0, 0): [], (1, 0): [7], (2, 0): [2, 8], (3, 0): [], (4, 0): [4, 5, 7, 8],
                          (5, 0): [4, 5, 6, 7, 8], (6, 0): [1, 4], (7, 0): [1, 2, 4, 6], (8, 0): [2, 4, 6]})
        expected_moves = [
            Move(REMOVE_POSS, 6, (1, 0), 'Column 0 ' + str((1, 0)) + ' had possibility value of ' + str(6) +
                 ' removed because there was ' + 'a swordfish interaction between rows ' + str((5, 7, 8))),
            Move(REMOVE_POSS, 6, (2, 0), 'Column 0 ' + str((2, 0)) + ' had possibility value of ' + str(6) +
                 ' removed because there was ' + 'a swordfish interaction between rows ' + str((5, 7, 8))),
            Move(REMOVE_POSS, 6, (4, 0), 'Column 0 ' + str((4, 0)) + ' had possibility value of ' + str(6) +
                 ' removed because there was ' + 'a swordfish interaction between rows ' + str((5, 7, 8)))]
        self.assertEqual(expected_moves, actual_moves)

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
        actual_moves = self.test_sole_candidates_board.sole_candidates()
        expected_moves = [
            Move(NUMBER_SOLVE, 7, (0, 4), 'Cell ' + str((0, 4)) + ' set to ' + str(7) +
                 ' because it was the only possibility remaining for that cell.'),
            Move(NUMBER_SOLVE, 6, (2, 1), 'Cell ' + str((2, 1)) + ' set to ' + str(6) +
                 ' because it was the only possibility remaining for that cell.'),
            Move(NUMBER_SOLVE, 5, (8, 6), 'Cell ' + str((8, 6)) + ' set to ' + str(5) +
                 ' because it was the only possibility remaining for that cell.')]
        test_data_sole_expected = [[9, 3, 0, 6, 7, 0, 2, 4, 0],
                                   [0, 0, 5, 8, 0, 0, 0, 0, 0],
                                   [2, 6, 0, 0, 4, 0, 0, 8, 0],
                                   [0, 1, 0, 0, 0, 0, 0, 0, 0],
                                   [6, 0, 0, 0, 1, 0, 0, 0, 7],
                                   [0, 0, 0, 0, 0, 0, 0, 1, 0],
                                   [0, 9, 0, 0, 5, 0, 0, 0, 4],
                                   [0, 0, 0, 0, 0, 9, 6, 0, 0],
                                   [0, 7, 3, 0, 0, 1, 5, 9, 8]]

        self.assertEqual(expected_moves, actual_moves)
        self.assertEqual(test_data_sole_expected, self.test_sole_candidates_board.board)

        # no effect
        temp_board = deepcopy(self.test_board_1.board)
        actual_moves = self.test_board_1.sole_candidates()
        self.assertEqual([], actual_moves)
        self.assertEqual(temp_board, self.test_board_1.board)

    def test_unique_candidates_generic_row(self):
        unique_row_test_board = SudokuBoard([0, 0, 5, 0, 0, 3, 0, 8, 0, 0, 0, 7, 8, 9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                                             0, 0, 9, 0, 1, 0, 8, 0, 2, 5, 0, 0, 7, 0, 0, 2, 0, 0, 3, 0, 0, 5, 4, 0, 3,
                                             0, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5, 8, 4, 0, 0, 0, 1, 0,
                                             4, 0, 0, 3, 0, 0])

        # hand checked success
        actual_moves = unique_row_test_board.unique_candidates_generic(unique_row_test_board.get_row_possibilities)
        expected_moves = [
            Move(NUMBER_SOLVE, 3, (3, 1), 'Cell (3, 1) set to 3 because the possibility was unique to row 3.'),
            Move(NUMBER_SOLVE, 2, (5, 0), 'Cell (5, 0) set to 2 because the possibility was unique to row 5.'),
            Move(NUMBER_SOLVE, 1, (7, 3), 'Cell (7, 3) set to 1 because the possibility was unique to row 7.')]

        unique_row_test_board_expected = [[0, 0, 5, 0, 0, 3, 0, 8, 0],
                                          [0, 0, 7, 8, 9, 0, 0, 0, 0],
                                          [1, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [9, 3, 1, 0, 8, 0, 2, 5, 0],
                                          [0, 7, 0, 0, 2, 0, 0, 3, 0],
                                          [2, 5, 4, 0, 3, 0, 8, 0, 7],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 1],
                                          [0, 0, 0, 1, 5, 8, 4, 0, 0],
                                          [0, 1, 0, 4, 0, 0, 3, 0, 0]]

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(unique_row_test_board.board, unique_row_test_board_expected)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.unique_candidates_generic(self.blank_board.get_row_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_unique_candidates_generic_column(self):
        unique_column_test_board = SudokuBoard([0, 0, 5, 0, 0, 3, 0, 8, 0, 0, 0, 7, 8, 9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                                                0, 0, 0, 9, 3, 1, 0, 8, 0, 2, 5, 0, 0, 7, 0, 0, 2, 0, 0, 3, 0, 2, 5, 4,
                                                0, 3, 0, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 5, 8, 4, 0, 0,
                                                0, 1, 0, 4, 0, 0, 3, 0, 0])

        # hand checked success
        actual_moves = unique_column_test_board.unique_candidates_generic(
            unique_column_test_board.get_col_possibilities)
        expected_moves = [
            Move(NUMBER_SOLVE, 3, (6, 3), 'Cell (6, 3) set to 3 because the possibility was unique to column 3.'),
            Move(NUMBER_SOLVE, 1, (0, 4), 'Cell (0, 4) set to 1 because the possibility was unique to column 4.'),
            Move(NUMBER_SOLVE, 8, (8, 8), 'Cell (8, 8) set to 8 because the possibility was unique to column 8.')]

        unique_column_test_board_expected = [[0, 0, 5, 0, 1, 3, 0, 8, 0],
                                             [0, 0, 7, 8, 9, 0, 0, 0, 0],
                                             [1, 0, 0, 0, 0, 0, 0, 0, 0],
                                             [9, 3, 1, 0, 8, 0, 2, 5, 0],
                                             [0, 7, 0, 0, 2, 0, 0, 3, 0],
                                             [2, 5, 4, 0, 3, 0, 8, 0, 7],
                                             [0, 0, 0, 3, 0, 0, 0, 0, 1],
                                             [0, 0, 0, 1, 5, 8, 4, 0, 0],
                                             [0, 1, 0, 4, 0, 0, 3, 0, 8]]

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(unique_column_test_board.board, unique_column_test_board_expected)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.unique_candidates_generic(self.blank_board.get_col_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_unique_candidates_generic_sector(self):
        unique_sector_test_board = SudokuBoard([6, 0, 7, 0, 3, 0, 1, 2, 4, 2, 4, 3, 0, 1, 0, 0, 6, 0, 9, 0, 1, 2, 6, 4,
                                                3, 0, 0, 4, 1, 9, 0, 0, 3, 6, 5, 2, 0, 2, 5, 6, 9, 1, 4, 3, 0, 0, 3, 6,
                                                4, 2, 5, 0, 9, 1, 3, 9, 4, 1, 0, 2, 5, 0, 6, 1, 6, 8, 0, 5, 0, 2, 4, 3,
                                                5, 7, 2, 3, 4, 6, 0, 1, 0])

        # hand checked success
        actual_moves = unique_sector_test_board.unique_candidates_generic(
            unique_sector_test_board.get_sector_possibilities)
        expected_moves = [
            Move(NUMBER_SOLVE, 8, (6, 4), 'Cell (6, 4) set to 8 because the possibility was unique to sector 7.'),
            Move(NUMBER_SOLVE, 7, (6, 7), 'Cell (6, 7) set to 7 because the possibility was unique to sector 8.')]

        unique_sector_test_board_expected = [[6, 0, 7, 0, 3, 0, 1, 2, 4],
                                             [2, 4, 3, 0, 1, 0, 0, 6, 0],
                                             [9, 0, 1, 2, 6, 4, 3, 0, 0],
                                             [4, 1, 9, 0, 0, 3, 6, 5, 2],
                                             [0, 2, 5, 6, 9, 1, 4, 3, 0],
                                             [0, 3, 6, 4, 2, 5, 0, 9, 1],
                                             [3, 9, 4, 1, 8, 2, 5, 7, 6],
                                             [1, 6, 8, 0, 5, 0, 2, 4, 3],
                                             [5, 7, 2, 3, 4, 6, 0, 1, 0]]

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(unique_sector_test_board.board, unique_sector_test_board_expected)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.unique_candidates_generic(self.blank_board.get_sector_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_unique_candidates(self):
        # TEST ROW WILL BE EXECUTED
        unique_row_test_board = SudokuBoard([0, 0, 5, 0, 0, 3, 0, 8, 0, 0, 0, 7, 8, 9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
                                             0, 0, 9, 0, 1, 0, 8, 0, 2, 5, 0, 0, 7, 0, 0, 2, 0, 0, 3, 0, 0, 5, 4, 0, 3,
                                             0, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5, 8, 4, 0, 0, 0, 1, 0,
                                             4, 0, 0, 3, 0, 0])

        # hand checked success
        actual_moves = unique_row_test_board.unique_candidate()
        expected_moves = [
            Move(NUMBER_SOLVE, 3, (3, 1), 'Cell (3, 1) set to 3 because the possibility was unique to row 3.'),
            Move(NUMBER_SOLVE, 2, (5, 0), 'Cell (5, 0) set to 2 because the possibility was unique to row 5.'),
            Move(NUMBER_SOLVE, 1, (7, 3), 'Cell (7, 3) set to 1 because the possibility was unique to row 7.')]

        unique_row_test_board_expected = [[0, 0, 5, 0, 0, 3, 0, 8, 0],
                                          [0, 0, 7, 8, 9, 0, 0, 0, 0],
                                          [1, 0, 0, 0, 0, 0, 0, 0, 0],
                                          [9, 3, 1, 0, 8, 0, 2, 5, 0],
                                          [0, 7, 0, 0, 2, 0, 0, 3, 0],
                                          [2, 5, 4, 0, 3, 0, 8, 0, 7],
                                          [0, 0, 0, 0, 0, 0, 0, 0, 1],
                                          [0, 0, 0, 1, 5, 8, 4, 0, 0],
                                          [0, 1, 0, 4, 0, 0, 3, 0, 0]]

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(unique_row_test_board.board, unique_row_test_board_expected)

        # TEST COLUMN WILL BE EXECUTED
        unique_column_test_board = SudokuBoard([0, 0, 5, 0, 0, 3, 0, 8, 0, 0, 0, 7, 8, 9, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                                                0, 0, 0, 9, 3, 1, 0, 8, 0, 2, 5, 0, 0, 7, 0, 0, 2, 0, 0, 3, 0, 2, 5, 4,
                                                0, 3, 0, 8, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 5, 8, 4, 0, 0,
                                                0, 1, 0, 4, 0, 0, 3, 0, 0])

        # hand checked success
        actual_moves = unique_column_test_board.unique_candidate()
        expected_moves = [
            Move(NUMBER_SOLVE, 3, (6, 3), 'Cell (6, 3) set to 3 because the possibility was unique to column 3.'),
            Move(NUMBER_SOLVE, 1, (0, 4), 'Cell (0, 4) set to 1 because the possibility was unique to column 4.'),
            Move(NUMBER_SOLVE, 8, (8, 8), 'Cell (8, 8) set to 8 because the possibility was unique to column 8.')]

        unique_column_test_board_expected = [[0, 0, 5, 0, 1, 3, 0, 8, 0],
                                             [0, 0, 7, 8, 9, 0, 0, 0, 0],
                                             [1, 0, 0, 0, 0, 0, 0, 0, 0],
                                             [9, 3, 1, 0, 8, 0, 2, 5, 0],
                                             [0, 7, 0, 0, 2, 0, 0, 3, 0],
                                             [2, 5, 4, 0, 3, 0, 8, 0, 7],
                                             [0, 0, 0, 3, 0, 0, 0, 0, 1],
                                             [0, 0, 0, 1, 5, 8, 4, 0, 0],
                                             [0, 1, 0, 4, 0, 0, 3, 0, 8]]

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(unique_column_test_board.board, unique_column_test_board_expected)

        # TEST SECTOR WILL BE EXECUTED
        unique_sector_test_board = SudokuBoard([6, 0, 7, 0, 3, 0, 1, 2, 4, 2, 4, 3, 0, 1, 0, 0, 6, 0, 9, 0, 1, 2, 6, 4,
                                                3, 0, 0, 4, 1, 9, 0, 0, 3, 6, 5, 2, 0, 2, 5, 6, 9, 1, 4, 3, 0, 0, 3, 6,
                                                4, 2, 5, 0, 9, 1, 3, 9, 4, 1, 0, 2, 5, 0, 6, 1, 6, 8, 0, 5, 0, 2, 4, 3,
                                                5, 7, 2, 3, 4, 6, 0, 1, 0])

        # hand checked success
        actual_moves = unique_sector_test_board.unique_candidate()
        expected_moves = [
            Move(NUMBER_SOLVE, 8, (6, 4), 'Cell (6, 4) set to 8 because the possibility was unique to sector 7.'),
            Move(NUMBER_SOLVE, 7, (6, 7), 'Cell (6, 7) set to 7 because the possibility was unique to sector 8.')]

        unique_sector_test_board_expected = [[6, 0, 7, 0, 3, 0, 1, 2, 4],
                                             [2, 4, 3, 0, 1, 0, 0, 6, 0],
                                             [9, 0, 1, 2, 6, 4, 3, 0, 0],
                                             [4, 1, 9, 0, 0, 3, 6, 5, 2],
                                             [0, 2, 5, 6, 9, 1, 4, 3, 0],
                                             [0, 3, 6, 4, 2, 5, 0, 9, 1],
                                             [3, 9, 4, 1, 8, 2, 5, 7, 6],
                                             [1, 6, 8, 0, 5, 0, 2, 4, 3],
                                             [5, 7, 2, 3, 4, 6, 0, 1, 0]]

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(unique_sector_test_board.board, unique_sector_test_board_expected)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.unique_candidate()
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_sector_line_interaction_generic_row(self):
        sector_row_interaction = SudokuBoard([0, 9, 0, 6, 7, 0, 0, 0, 5, 7, 5, 1, 0, 0, 9, 0, 8, 6, 0, 3, 6, 5, 8, 0, 0,
                                              0, 0, 9, 6, 7, 8, 0, 0, 1, 0, 0, 0, 8, 4, 0, 6, 0, 9, 3, 7, 0, 0, 3, 9, 0,
                                              7, 0, 6, 8, 0, 0, 0, 0, 9, 2, 6, 0, 0, 3, 0, 0, 0, 0, 6, 8, 0, 1, 6, 0, 0,
                                              0, 0, 8, 0, 2, 0])

        actual_moves = sector_row_interaction.sector_line_interaction_generic(
            sector_row_interaction.row_indices_in_sector,
            sector_row_interaction.get_sector_subrow_possibilities)

        expected_moves = [
            Move(REMOVE_POSS, 2, (1, 6),
                 'Cell (1, 6) had possibility value of 2 removed because sector 1 must contain it via a row interaction.')
        ]

        sector_row_interaction_expected_board = [[0, 9, 0, 6, 7, 0, 0, 0, 5],
                                                 [7, 5, 1, 0, 0, 9, 0, 8, 6],
                                                 [0, 3, 6, 5, 8, 0, 0, 0, 0],
                                                 [9, 6, 7, 8, 0, 0, 1, 0, 0],
                                                 [0, 8, 4, 0, 6, 0, 9, 3, 7],
                                                 [0, 0, 3, 9, 0, 7, 0, 6, 8],
                                                 [0, 0, 0, 0, 9, 2, 6, 0, 0],
                                                 [3, 0, 0, 0, 0, 6, 8, 0, 1],
                                                 [6, 0, 0, 0, 0, 8, 0, 2, 0]]

        sector_row_interaction_expected_poss = {(0, 0): [2, 4, 8], (0, 1): [], (0, 2): [2, 8], (0, 3): [], (0, 4): [],
                                                (0, 5): [1, 3, 4], (0, 6): [2, 3, 4], (0, 7): [1, 4], (0, 8): [],
                                                (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [2, 3, 4],
                                                (1, 4): [2, 3, 4], (1, 5): [], (1, 6): [3, 4], (1, 7): [], (1, 8): [],
                                                (2, 0): [2, 4], (2, 1): [], (2, 2): [], (2, 3): [], (2, 4): [],
                                                (2, 5): [1, 4], (2, 6): [2, 4, 7], (2, 7): [1, 4, 7, 9],
                                                (2, 8): [2, 4, 9], (3, 0): [], (3, 1): [], (3, 2): [], (3, 3): [],
                                                (3, 4): [2, 3, 4, 5], (3, 5): [3, 4, 5], (3, 6): [], (3, 7): [4, 5],
                                                (3, 8): [2, 4], (4, 0): [1, 2, 5], (4, 1): [], (4, 2): [],
                                                (4, 3): [1, 2], (4, 4): [], (4, 5): [1, 5], (4, 6): [], (4, 7): [],
                                                (4, 8): [], (5, 0): [1, 2, 5], (5, 1): [1, 2], (5, 2): [], (5, 3): [],
                                                (5, 4): [1, 2, 4, 5], (5, 5): [], (5, 6): [2, 4, 5], (5, 7): [],
                                                (5, 8): [], (6, 0): [1, 4, 5, 8], (6, 1): [1, 4, 7], (6, 2): [5, 8],
                                                (6, 3): [1, 3, 4, 7], (6, 4): [], (6, 5): [], (6, 6): [],
                                                (6, 7): [4, 5, 7], (6, 8): [3, 4], (7, 0): [], (7, 1): [2, 4, 7],
                                                (7, 2): [2, 5, 9], (7, 3): [4, 7], (7, 4): [4, 5], (7, 5): [],
                                                (7, 6): [], (7, 7): [4, 5, 7, 9], (7, 8): [], (8, 0): [],
                                                (8, 1): [1, 4, 7], (8, 2): [5, 9], (8, 3): [1, 3, 4, 7],
                                                (8, 4): [1, 3, 4, 5], (8, 5): [], (8, 6): [3, 4, 5, 7], (8, 7): [],
                                                (8, 8): [3, 4, 9]}

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(sector_row_interaction.board, sector_row_interaction_expected_board)
        self.assertEqual(sector_row_interaction.possible_values, sector_row_interaction_expected_poss)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.sector_line_interaction_generic(
            self.blank_board.row_indices_in_sector,
            self.blank_board.get_sector_subrow_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_sector_line_interaction_generic_column(self):
        sector_col_interaction = SudokuBoard([0, 9, 0, 6, 7, 0, 0, 0, 5, 7, 5, 1, 0, 0, 9, 0, 8, 6, 0, 3, 6, 5, 8, 0, 0,
                                              0, 0, 9, 6, 7, 8, 0, 0, 1, 0, 0, 0, 8, 4, 0, 6, 0, 9, 3, 7, 0, 0, 3, 9, 0,
                                              7, 0, 6, 8, 0, 0, 0, 0, 9, 2, 6, 0, 0, 3, 0, 0, 0, 0, 6, 8, 0, 1, 6, 0, 0,
                                              0, 0, 8, 0, 2, 0])

        actual_moves = sector_col_interaction.sector_line_interaction_generic(
            sector_col_interaction.col_indices_in_sector,
            sector_col_interaction.get_sector_subcolumn_possibilities)

        expected_moves = [
            Move(REMOVE_POSS, 4, (6, 0),
                 'Cell (6, 0) had possibility value of 4 removed because sector 0 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 1, (4, 5),
                 'Cell (4, 5) had possibility value of 1 removed because sector 1 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 3, (8, 6),
                 'Cell (8, 6) had possibility value of 3 removed because sector 2 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 5, (6, 0),
                 'Cell (6, 0) had possibility value of 5 removed because sector 3 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 5, (3, 4),
                 'Cell (3, 4) had possibility value of 5 removed because sector 7 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 5, (5, 4),
                 'Cell (5, 4) had possibility value of 5 removed because sector 7 must contain it via a column interaction.'),
        ]

        sector_col_interaction_expected_board = [[0, 9, 0, 6, 7, 0, 0, 0, 5], [7, 5, 1, 0, 0, 9, 0, 8, 6],
                                                 [0, 3, 6, 5, 8, 0, 0, 0, 0], [9, 6, 7, 8, 0, 0, 1, 0, 0],
                                                 [0, 8, 4, 0, 6, 0, 9, 3, 7], [0, 0, 3, 9, 0, 7, 0, 6, 8],
                                                 [0, 0, 0, 0, 9, 2, 6, 0, 0], [3, 0, 0, 0, 0, 6, 8, 0, 1],
                                                 [6, 0, 0, 0, 0, 8, 0, 2, 0]]

        sector_col_interaction_expected_poss = {(0, 0): [2, 4, 8], (0, 1): [], (0, 2): [2, 8], (0, 3): [], (0, 4): [],
                                                (0, 5): [1, 3, 4], (0, 6): [2, 3, 4], (0, 7): [1, 4], (0, 8): [],
                                                (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [2, 3, 4],
                                                (1, 4): [2, 3, 4], (1, 5): [], (1, 6): [2, 3, 4], (1, 7): [],
                                                (1, 8): [],
                                                (2, 0): [2, 4], (2, 1): [], (2, 2): [], (2, 3): [], (2, 4): [],
                                                (2, 5): [1, 4], (2, 6): [2, 4, 7], (2, 7): [1, 4, 7, 9],
                                                (2, 8): [2, 4, 9], (3, 0): [], (3, 1): [], (3, 2): [], (3, 3): [],
                                                (3, 4): [2, 3, 4], (3, 5): [3, 4, 5], (3, 6): [], (3, 7): [4, 5],
                                                (3, 8): [2, 4], (4, 0): [1, 2, 5], (4, 1): [], (4, 2): [],
                                                (4, 3): [1, 2], (4, 4): [], (4, 5): [5], (4, 6): [], (4, 7): [],
                                                (4, 8): [], (5, 0): [1, 2, 5], (5, 1): [1, 2], (5, 2): [], (5, 3): [],
                                                (5, 4): [1, 2, 4], (5, 5): [], (5, 6): [2, 4, 5], (5, 7): [],
                                                (5, 8): [], (6, 0): [1, 8], (6, 1): [1, 4, 7], (6, 2): [5, 8],
                                                (6, 3): [1, 3, 4, 7], (6, 4): [], (6, 5): [], (6, 6): [],
                                                (6, 7): [4, 5, 7], (6, 8): [3, 4], (7, 0): [], (7, 1): [2, 4, 7],
                                                (7, 2): [2, 5, 9], (7, 3): [4, 7], (7, 4): [4, 5], (7, 5): [],
                                                (7, 6): [], (7, 7): [4, 5, 7, 9], (7, 8): [], (8, 0): [],
                                                (8, 1): [1, 4, 7], (8, 2): [5, 9], (8, 3): [1, 3, 4, 7],
                                                (8, 4): [1, 3, 4, 5], (8, 5): [], (8, 6): [4, 5, 7], (8, 7): [],
                                                (8, 8): [3, 4, 9]}

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(sector_col_interaction.board, sector_col_interaction_expected_board)
        self.assertEqual(sector_col_interaction.possible_values, sector_col_interaction_expected_poss)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.sector_line_interaction_generic(
            self.blank_board.row_indices_in_sector,
            self.blank_board.get_sector_subrow_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_sector_line_interaction(self):
        sector_row_interaction = SudokuBoard([0, 9, 0, 6, 7, 0, 0, 0, 5, 7, 5, 1, 0, 0, 9, 0, 8, 6, 0, 3, 6, 5, 8, 0, 0,
                                              0, 0, 9, 6, 7, 8, 0, 0, 1, 0, 0, 0, 8, 4, 0, 6, 0, 9, 3, 7, 0, 0, 3, 9, 0,
                                              7, 0, 6, 8, 0, 0, 0, 0, 9, 2, 6, 0, 0, 3, 0, 0, 0, 0, 6, 8, 0, 1, 6, 0, 0,
                                              0, 0, 8, 0, 2, 0])

        actual_moves = sector_row_interaction.sector_line_interaction()

        expected_moves = [
            Move(REMOVE_POSS, 2, (1, 6),
                 'Cell (1, 6) had possibility value of 2 removed because sector 1 must contain it via a row interaction.')
        ]

        sector_row_interaction_expected_board = [[0, 9, 0, 6, 7, 0, 0, 0, 5],
                                                 [7, 5, 1, 0, 0, 9, 0, 8, 6],
                                                 [0, 3, 6, 5, 8, 0, 0, 0, 0],
                                                 [9, 6, 7, 8, 0, 0, 1, 0, 0],
                                                 [0, 8, 4, 0, 6, 0, 9, 3, 7],
                                                 [0, 0, 3, 9, 0, 7, 0, 6, 8],
                                                 [0, 0, 0, 0, 9, 2, 6, 0, 0],
                                                 [3, 0, 0, 0, 0, 6, 8, 0, 1],
                                                 [6, 0, 0, 0, 0, 8, 0, 2, 0]]

        sector_row_interaction_expected_poss = {(0, 0): [2, 4, 8], (0, 1): [], (0, 2): [2, 8], (0, 3): [], (0, 4): [],
                                                (0, 5): [1, 3, 4], (0, 6): [2, 3, 4], (0, 7): [1, 4], (0, 8): [],
                                                (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [2, 3, 4],
                                                (1, 4): [2, 3, 4], (1, 5): [], (1, 6): [3, 4], (1, 7): [], (1, 8): [],
                                                (2, 0): [2, 4], (2, 1): [], (2, 2): [], (2, 3): [], (2, 4): [],
                                                (2, 5): [1, 4], (2, 6): [2, 4, 7], (2, 7): [1, 4, 7, 9],
                                                (2, 8): [2, 4, 9], (3, 0): [], (3, 1): [], (3, 2): [], (3, 3): [],
                                                (3, 4): [2, 3, 4, 5], (3, 5): [3, 4, 5], (3, 6): [], (3, 7): [4, 5],
                                                (3, 8): [2, 4], (4, 0): [1, 2, 5], (4, 1): [], (4, 2): [],
                                                (4, 3): [1, 2], (4, 4): [], (4, 5): [1, 5], (4, 6): [], (4, 7): [],
                                                (4, 8): [], (5, 0): [1, 2, 5], (5, 1): [1, 2], (5, 2): [], (5, 3): [],
                                                (5, 4): [1, 2, 4, 5], (5, 5): [], (5, 6): [2, 4, 5], (5, 7): [],
                                                (5, 8): [], (6, 0): [1, 4, 5, 8], (6, 1): [1, 4, 7], (6, 2): [5, 8],
                                                (6, 3): [1, 3, 4, 7], (6, 4): [], (6, 5): [], (6, 6): [],
                                                (6, 7): [4, 5, 7], (6, 8): [3, 4], (7, 0): [], (7, 1): [2, 4, 7],
                                                (7, 2): [2, 5, 9], (7, 3): [4, 7], (7, 4): [4, 5], (7, 5): [],
                                                (7, 6): [], (7, 7): [4, 5, 7, 9], (7, 8): [], (8, 0): [],
                                                (8, 1): [1, 4, 7], (8, 2): [5, 9], (8, 3): [1, 3, 4, 7],
                                                (8, 4): [1, 3, 4, 5], (8, 5): [], (8, 6): [3, 4, 5, 7], (8, 7): [],
                                                (8, 8): [3, 4, 9]}

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(sector_row_interaction.board, sector_row_interaction_expected_board)
        self.assertEqual(sector_row_interaction.possible_values, sector_row_interaction_expected_poss)

        sector_col_interaction = sector_row_interaction

        actual_moves = sector_col_interaction.sector_line_interaction()

        expected_moves = [
            Move(REMOVE_POSS, 4, (6, 0),
                 'Cell (6, 0) had possibility value of 4 removed because sector 0 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 1, (4, 5),
                 'Cell (4, 5) had possibility value of 1 removed because sector 1 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 3, (8, 6),
                 'Cell (8, 6) had possibility value of 3 removed because sector 2 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 5, (6, 0),
                 'Cell (6, 0) had possibility value of 5 removed because sector 3 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 5, (3, 4),
                 'Cell (3, 4) had possibility value of 5 removed because sector 7 must contain it via a column interaction.'),
            Move(REMOVE_POSS, 5, (5, 4),
                 'Cell (5, 4) had possibility value of 5 removed because sector 7 must contain it via a column interaction.'),
        ]

        sector_col_interaction_expected_board = [[0, 9, 0, 6, 7, 0, 0, 0, 5], [7, 5, 1, 0, 0, 9, 0, 8, 6],
                                                 [0, 3, 6, 5, 8, 0, 0, 0, 0], [9, 6, 7, 8, 0, 0, 1, 0, 0],
                                                 [0, 8, 4, 0, 6, 0, 9, 3, 7], [0, 0, 3, 9, 0, 7, 0, 6, 8],
                                                 [0, 0, 0, 0, 9, 2, 6, 0, 0], [3, 0, 0, 0, 0, 6, 8, 0, 1],
                                                 [6, 0, 0, 0, 0, 8, 0, 2, 0]]

        sector_col_interaction_expected_poss = {(0, 0): [2, 4, 8], (0, 1): [], (0, 2): [2, 8], (0, 3): [], (0, 4): [],
                                                (0, 5): [1, 3, 4], (0, 6): [2, 3, 4], (0, 7): [1, 4], (0, 8): [],
                                                (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [2, 3, 4],
                                                (1, 4): [2, 3, 4], (1, 5): [], (1, 6): [3, 4], (1, 7): [], (1, 8): [],
                                                (2, 0): [2, 4], (2, 1): [], (2, 2): [], (2, 3): [], (2, 4): [],
                                                (2, 5): [1, 4], (2, 6): [2, 4, 7], (2, 7): [1, 4, 7, 9],
                                                (2, 8): [2, 4, 9], (3, 0): [], (3, 1): [], (3, 2): [], (3, 3): [],
                                                (3, 4): [2, 3, 4], (3, 5): [3, 4, 5], (3, 6): [], (3, 7): [4, 5],
                                                (3, 8): [2, 4], (4, 0): [1, 2, 5], (4, 1): [], (4, 2): [],
                                                (4, 3): [1, 2], (4, 4): [], (4, 5): [5], (4, 6): [], (4, 7): [],
                                                (4, 8): [], (5, 0): [1, 2, 5], (5, 1): [1, 2], (5, 2): [], (5, 3): [],
                                                (5, 4): [1, 2, 4], (5, 5): [], (5, 6): [2, 4, 5], (5, 7): [],
                                                (5, 8): [], (6, 0): [1, 8], (6, 1): [1, 4, 7], (6, 2): [5, 8],
                                                (6, 3): [1, 3, 4, 7], (6, 4): [], (6, 5): [], (6, 6): [],
                                                (6, 7): [4, 5, 7], (6, 8): [3, 4], (7, 0): [], (7, 1): [2, 4, 7],
                                                (7, 2): [2, 5, 9], (7, 3): [4, 7], (7, 4): [4, 5], (7, 5): [],
                                                (7, 6): [], (7, 7): [4, 5, 7, 9], (7, 8): [], (8, 0): [],
                                                (8, 1): [1, 4, 7], (8, 2): [5, 9], (8, 3): [1, 3, 4, 7],
                                                (8, 4): [1, 3, 4, 5], (8, 5): [], (8, 6): [4, 5, 7], (8, 7): [],
                                                (8, 8): [3, 4, 9]}

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(sector_col_interaction.board, sector_col_interaction_expected_board)
        self.assertEqual(sector_col_interaction.possible_values, sector_col_interaction_expected_poss)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.sector_line_interaction()
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_pointing_tuple_generic_row(self):
        pointing_tuple_row = SudokuBoard(
            [0, 3, 0, 7, 8, 1, 0, 5, 0, 7, 0, 0, 2, 3, 9, 6, 8, 0, 0, 0, 0, 6, 5, 4, 0, 7, 3, 5, 0, 0, 0, 0, 7, 3, 9, 8,
             3, 1, 7, 9, 2, 8, 5, 4, 6, 4, 8, 9, 3, 6, 5, 7, 1, 2, 0, 0, 0, 0, 0, 2, 0, 3, 0, 1, 0, 0, 0, 0, 3, 0, 6, 0,
             0, 0, 3, 0, 0, 6, 4, 2, 7])

        actual_moves = pointing_tuple_row.pointing_tuple_generic(pointing_tuple_row.get_row_possibilities,
                                                                 pointing_tuple_row.get_sector_subrow_possibilities,
                                                                 pointing_tuple_row.row_indices_in_sector)

        expected_moves = [
            Move(REMOVE_POSS, 1, (6, 3),
                 'row 0 ((6, 3)) had possibility value of 1 removed due to a pointing tuple in sector 8'),
            Move(REMOVE_POSS, 1, (6, 4),
                 'row 0 ((6, 4)) had possibility value of 1 removed due to a pointing tuple in sector 8')
        ]

        pointing_tuple_row_board = [[0, 3, 0, 7, 8, 1, 0, 5, 0],
                                    [7, 0, 0, 2, 3, 9, 6, 8, 0],
                                    [0, 0, 0, 6, 5, 4, 0, 7, 3],
                                    [5, 0, 0, 0, 0, 7, 3, 9, 8],
                                    [3, 1, 7, 9, 2, 8, 5, 4, 6],
                                    [4, 8, 9, 3, 6, 5, 7, 1, 2],
                                    [0, 0, 0, 0, 0, 2, 0, 3, 0],
                                    [1, 0, 0, 0, 0, 3, 0, 6, 0],
                                    [0, 0, 3, 0, 0, 6, 4, 2, 7]]

        pointing_tuple_row_poss = {(0, 0): [2, 6, 9], (0, 1): [], (0, 2): [2, 4, 6], (0, 3): [], (0, 4): [], (0, 5): [],
                                   (0, 6): [2, 9], (0, 7): [], (0, 8): [4, 9], (1, 0): [], (1, 1): [4, 5],
                                   (1, 2): [1, 4, 5], (1, 3): [], (1, 4): [], (1, 5): [], (1, 6): [], (1, 7): [],
                                   (1, 8): [1, 4], (2, 0): [2, 8, 9], (2, 1): [2, 9], (2, 2): [1, 2, 8], (2, 3): [],
                                   (2, 4): [], (2, 5): [], (2, 6): [1, 2, 9], (2, 7): [], (2, 8): [], (3, 0): [],
                                   (3, 1): [2, 6], (3, 2): [2, 6], (3, 3): [1, 4], (3, 4): [1, 4], (3, 5): [],
                                   (3, 6): [], (3, 7): [], (3, 8): [], (4, 0): [], (4, 1): [], (4, 2): [], (4, 3): [],
                                   (4, 4): [], (4, 5): [], (4, 6): [], (4, 7): [], (4, 8): [], (5, 0): [], (5, 1): [],
                                   (5, 2): [], (5, 3): [], (5, 4): [], (5, 5): [], (5, 6): [], (5, 7): [], (5, 8): [],
                                   (6, 0): [6, 8, 9], (6, 1): [4, 5, 6, 7, 9], (6, 2): [4, 5, 6, 8], (6, 3): [4, 5, 8],
                                   (6, 4): [4, 7, 9], (6, 5): [], (6, 6): [1, 8, 9], (6, 7): [], (6, 8): [1, 5, 9],
                                   (7, 0): [], (7, 1): [2, 4, 5, 7, 9], (7, 2): [2, 4, 5, 8], (7, 3): [4, 5, 8],
                                   (7, 4): [4, 7, 9], (7, 5): [], (7, 6): [8, 9], (7, 7): [], (7, 8): [5, 9],
                                   (8, 0): [8, 9], (8, 1): [5, 9], (8, 2): [], (8, 3): [1, 5, 8], (8, 4): [1, 9],
                                   (8, 5): [], (8, 6): [], (8, 7): [], (8, 8): []}

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(pointing_tuple_row_board, pointing_tuple_row.board)
        self.assertEqual(pointing_tuple_row_poss, pointing_tuple_row.possible_values)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.pointing_tuple_generic(self.blank_board.get_row_possibilities,
                                                               self.blank_board.get_sector_subrow_possibilities,
                                                               self.blank_board.row_indices_in_sector)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_pointing_tuple_generic_column(self):
        pointing_tuple_col = SudokuBoard(
            [0, 9, 0, 0, 0, 7, 0, 5, 0, 0, 5, 0, 8, 0, 0, 0, 0, 0, 1, 4, 0, 0, 5, 0, 2, 0, 0,
             7, 0, 4, 0, 9, 0, 0, 0, 0, 3, 8, 1, 7, 0, 0, 5, 9, 6, 5, 0, 9, 0, 8, 0, 7, 0, 4,
             0, 7, 5, 0, 3, 8, 0, 4, 1, 0, 1, 0, 0, 0, 6, 0, 7, 0, 0, 3, 0, 1, 7, 0, 0, 8, 0]
        )

        actual_moves = pointing_tuple_col.pointing_tuple_generic(pointing_tuple_col.get_col_possibilities,
                                                                 pointing_tuple_col.get_sector_subcolumn_possibilities,
                                                                 pointing_tuple_col.col_indices_in_sector)

        expected_moves = [
            Move(REMOVE_POSS, 1, (1, 5),
                 'column 2 ((1, 5)) had possibility value of 1 removed due to a pointing tuple in sector 4'),
            Move(REMOVE_POSS, 6, (0, 3),
                 'column 0 ((0, 3)) had possibility value of 6 removed due to a pointing tuple in sector 4'),
            Move(REMOVE_POSS, 6, (2, 3),
                 'column 0 ((2, 3)) had possibility value of 6 removed due to a pointing tuple in sector 4'),
            Move(REMOVE_POSS, 2, (3, 8),
                 'column 2 ((3, 8)) had possibility value of 2 removed due to a pointing tuple in sector 8'),
            Move(REMOVE_POSS, 6, (0, 6),
                 'column 0 ((0, 6)) had possibility value of 6 removed due to a pointing tuple in sector 8'),
            Move(REMOVE_POSS, 6, (1, 6),
                 'column 0 ((1, 6)) had possibility value of 6 removed due to a pointing tuple in sector 8')
        ]

        pointing_tuple_col_board = [[0, 9, 0, 0, 0, 7, 0, 5, 0], [0, 5, 0, 8, 0, 0, 0, 0, 0],
                                    [1, 4, 0, 0, 5, 0, 2, 0, 0], [7, 0, 4, 0, 9, 0, 0, 0, 0],
                                    [3, 8, 1, 7, 0, 0, 5, 9, 6], [5, 0, 9, 0, 8, 0, 7, 0, 4],
                                    [0, 7, 5, 0, 3, 8, 0, 4, 1], [0, 1, 0, 0, 0, 6, 0, 7, 0],
                                    [0, 3, 0, 1, 7, 0, 0, 8, 0]]

        pointing_tuple_col_poss = {(0, 0): [2, 6, 8], (0, 1): [], (0, 2): [2, 3, 6, 8], (0, 3): [2, 3, 4],
                                   (0, 4): [1, 2, 4, 6], (0, 5): [], (0, 6): [1, 3, 4, 8], (0, 7): [], (0, 8): [3, 8],
                                   (1, 0): [2, 6], (1, 1): [], (1, 2): [2, 3, 6, 7], (1, 3): [], (1, 4): [1, 2, 4, 6],
                                   (1, 5): [2, 3, 4, 9], (1, 6): [1, 3, 4, 9], (1, 7): [1, 3, 6], (1, 8): [3, 7, 9],
                                   (2, 0): [], (2, 1): [], (2, 2): [3, 6, 7, 8], (2, 3): [3, 9], (2, 4): [],
                                   (2, 5): [3, 9], (2, 6): [], (2, 7): [3, 6], (2, 8): [3, 7, 8, 9], (3, 0): [],
                                   (3, 1): [2, 6], (3, 2): [], (3, 3): [2, 3, 5, 6], (3, 4): [], (3, 5): [1, 2, 3, 5],
                                   (3, 6): [1, 3, 8], (3, 7): [1, 2, 3], (3, 8): [3, 8], (4, 0): [], (4, 1): [],
                                   (4, 2): [], (4, 3): [], (4, 4): [2, 4], (4, 5): [2, 4], (4, 6): [], (4, 7): [],
                                   (4, 8): [], (5, 0): [], (5, 1): [2, 6], (5, 2): [], (5, 3): [2, 3, 6], (5, 4): [],
                                   (5, 5): [1, 2, 3], (5, 6): [], (5, 7): [1, 2, 3], (5, 8): [], (6, 0): [2, 6, 9],
                                   (6, 1): [], (6, 2): [], (6, 3): [2, 9], (6, 4): [], (6, 5): [], (6, 6): [6, 9],
                                   (6, 7): [], (6, 8): [], (7, 0): [2, 4, 8, 9], (7, 1): [], (7, 2): [2, 8],
                                   (7, 3): [2, 4, 5, 9], (7, 4): [2, 4], (7, 5): [], (7, 6): [3, 9], (7, 7): [],
                                   (7, 8): [2, 3, 5, 9], (8, 0): [2, 4, 6, 9], (8, 1): [], (8, 2): [2, 6], (8, 3): [],
                                   (8, 4): [], (8, 5): [2, 4, 5, 9], (8, 6): [6, 9], (8, 7): [], (8, 8): [2, 5, 9]}

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(pointing_tuple_col_board, pointing_tuple_col.board)
        self.assertEqual(pointing_tuple_col_poss, pointing_tuple_col.possible_values)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.pointing_tuple_generic(self.blank_board.get_col_possibilities,
                                                               self.blank_board.get_sector_subcolumn_possibilities,
                                                               self.blank_board.col_indices_in_sector)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_pointing_tuple(self):
        pass

    def test_sector_sector_interaction(self):
        sector_sector_interaction = SudokuBoard(
            [0, 0, 0, 0, 0, 3, 9, 4, 8, 3, 0, 9, 0, 0, 8, 5, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 2, 5, 0, 0, 9, 0, 0, 0, 0, 0,
             0, 0, 7, 0, 1, 0, 6, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1, 6, 9, 2, 0, 0, 0, 1, 0, 0, 4, 3, 8, 7, 0, 1, 2, 0, 9,
             1, 7, 5, 3, 0, 0, 0, 0, 0])

        actual_moves = sector_sector_interaction.sector_sector_interaction()
        expected_moves = [
            Move(REMOVE_POSS, 3, (3, 6),
                 'Cell (3, 6) had possibility value of 3 removed because of a sector - sector interaction between 3 and 4.'),
            Move(REMOVE_POSS, 3, (3, 7),
                 'Cell (3, 7) had possibility value of 3 removed because of a sector - sector interaction between 3 and 4.'),
            Move(REMOVE_POSS, 3, (3, 8),
                 'Cell (3, 8) had possibility value of 3 removed because of a sector - sector interaction between 3 and 4.'),
            Move(REMOVE_POSS, 3, (5, 6),
                 'Cell (5, 6) had possibility value of 3 removed because of a sector - sector interaction between 3 and 4.'),
            Move(REMOVE_POSS, 3, (5, 7),
                 'Cell (5, 7) had possibility value of 3 removed because of a sector - sector interaction between 3 and 4.'),
            Move(REMOVE_POSS, 3, (2, 7),
                 'Cell (2, 7) had possibility value of 3 removed because of a sector - sector interaction between 5 and 8.')
        ]

        sector_sector_interaction_expected_board = [[0, 0, 0, 0, 0, 3, 9, 4, 8], [3, 0, 9, 0, 0, 8, 5, 0, 0],
                                                    [0, 0, 4, 0, 0, 0, 0, 0, 2], [5, 0, 0, 9, 0, 0, 0, 0, 0],
                                                    [0, 0, 7, 0, 1, 0, 6, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 1],
                                                    [6, 9, 2, 0, 0, 0, 1, 0, 0], [4, 3, 8, 7, 0, 1, 2, 0, 9],
                                                    [1, 7, 5, 3, 0, 0, 0, 0, 0]]

        sector_sector_interaction_expected_poss = {(0, 0): [2, 7], (0, 1): [1, 2, 5, 6], (0, 2): [1, 6],
                                                   (0, 3): [1, 2, 5, 6], (0, 4): [2, 5, 6, 7], (0, 5): [], (0, 6): [],
                                                   (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [1, 2, 6], (1, 2): [],
                                                   (1, 3): [1, 2, 4, 6], (1, 4): [2, 4, 6, 7], (1, 5): [], (1, 6): [],
                                                   (1, 7): [1, 6, 7], (1, 8): [6, 7], (2, 0): [7, 8],
                                                   (2, 1): [1, 5, 6, 8], (2, 2): [], (2, 3): [1, 5, 6],
                                                   (2, 4): [5, 6, 7, 9], (2, 5): [5, 6, 9], (2, 6): [3, 7],
                                                   (2, 7): [1, 6, 7], (2, 8): [], (3, 0): [], (3, 1): [1, 2, 4, 6, 8],
                                                   (3, 2): [1, 3, 6], (3, 3): [], (3, 4): [2, 3, 4, 6, 8],
                                                   (3, 5): [2, 4, 6], (3, 6): [4, 7, 8], (3, 7): [2, 7, 8],
                                                   (3, 8): [4, 7], (4, 0): [2, 8, 9], (4, 1): [2, 4, 8], (4, 2): [],
                                                   (4, 3): [2, 4, 5, 8], (4, 4): [], (4, 5): [2, 4, 5], (4, 6): [],
                                                   (4, 7): [2, 3, 5, 8, 9], (4, 8): [3, 4, 5], (5, 0): [2, 8, 9],
                                                   (5, 1): [2, 4, 6, 8], (5, 2): [3, 6], (5, 3): [2, 4, 5, 6, 8],
                                                   (5, 4): [2, 3, 4, 5, 6, 8], (5, 5): [], (5, 6): [4, 8],
                                                   (5, 7): [2, 5, 8, 9], (5, 8): [], (6, 0): [], (6, 1): [], (6, 2): [],
                                                   (6, 3): [4, 5, 8], (6, 4): [4, 5, 8], (6, 5): [4, 5], (6, 6): [],
                                                   (6, 7): [3, 5, 7, 8], (6, 8): [3, 4, 5, 7], (7, 0): [], (7, 1): [],
                                                   (7, 2): [], (7, 3): [], (7, 4): [5, 6], (7, 5): [], (7, 6): [],
                                                   (7, 7): [5, 6], (7, 8): [], (8, 0): [], (8, 1): [], (8, 2): [],
                                                   (8, 3): [], (8, 4): [2, 4, 6, 8, 9], (8, 5): [2, 4, 6, 9],
                                                   (8, 6): [4, 8], (8, 7): [6, 8], (8, 8): [4, 6]}

        self.assertEqual(actual_moves, expected_moves)
        self.assertEqual(sector_sector_interaction.board, sector_sector_interaction_expected_board)
        self.assertEqual(sector_sector_interaction.possible_values, sector_sector_interaction_expected_poss)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.sector_sector_interaction()
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_naked_subset_row(self):
        naked_subset_row = SudokuBoard(
            [3, 2, 0, 9, 0, 1, 4, 0, 0, 9, 0, 0, 4, 0, 2, 0, 0, 3, 0, 0, 6, 3, 7, 8, 2, 0, 9,
             8, 0, 1, 2, 0, 5, 0, 0, 0, 7, 0, 0, 1, 8, 6, 0, 0, 0, 0, 0, 0, 7, 0, 9, 1, 0, 8,
             1, 0, 0, 6, 9, 3, 5, 0, 0, 2, 0, 0, 8, 1, 4, 0, 0, 7, 6, 0, 4, 5, 2, 7, 0, 3, 1]
        )

        actual_moves = naked_subset_row.naked_subset_generic(naked_subset_row.get_row_possibilities)

        expected_moves = [
            Move(REMOVE_POSS, 5, (0, 2),
                 'Cell (0, 2) had possibility value of 5 removed because there was a naked subset at ((0, 4), (0, 8)) of size 2 in row 0'),
            Move(REMOVE_POSS, 5, (0, 7),
                 'Cell (0, 7) had possibility value of 5 removed because there was a naked subset at ((0, 4), (0, 8)) of size 2 in row 0'),
            Move(REMOVE_POSS, 6, (0, 7),
                 'Cell (0, 7) had possibility value of 6 removed because there was a naked subset at ((0, 4), (0, 8)) of size 2 in row 0'),
            Move(REMOVE_POSS, 8, (6, 7),
                 'Cell (6, 7) had possibility value of 8 removed because there was a naked subset at ((6, 1), (6, 2)) of size 2 in row 6'),
            Move(REMOVE_POSS, 9, (7, 1),
                 'Cell (7, 1) had possibility value of 9 removed because there was a naked subset at ((7, 6), (7, 7)) of size 2 in row 7'),
            Move(REMOVE_POSS, 9, (7, 2),
                 'Cell (7, 2) had possibility value of 9 removed because there was a naked subset at ((7, 6), (7, 7)) of size 2 in row 7')
        ]

        naked_subset_row_expected_board = [[3, 2, 0, 9, 0, 1, 4, 0, 0], [9, 0, 0, 4, 0, 2, 0, 0, 3],
                                           [0, 0, 6, 3, 7, 8, 2, 0, 9], [8, 0, 1, 2, 0, 5, 0, 0, 0],
                                           [7, 0, 0, 1, 8, 6, 0, 0, 0], [0, 0, 0, 7, 0, 9, 1, 0, 8],
                                           [1, 0, 0, 6, 9, 3, 5, 0, 0], [2, 0, 0, 8, 1, 4, 0, 0, 7],
                                           [6, 0, 4, 5, 2, 7, 0, 3, 1]]

        naked_subset_row_expected_poss = {(0, 0): [], (0, 1): [], (0, 2): [7, 8], (0, 3): [], (0, 4): [5, 6],
                                          (0, 5): [], (0, 6): [], (0, 7): [7, 8], (0, 8): [5, 6], (1, 0): [],
                                          (1, 1): [1, 5, 7, 8], (1, 2): [5, 7, 8], (1, 3): [], (1, 4): [5, 6],
                                          (1, 5): [], (1, 6): [6, 7, 8], (1, 7): [1, 5, 6, 7, 8], (1, 8): [],
                                          (2, 0): [4, 5], (2, 1): [1, 4, 5], (2, 2): [], (2, 3): [], (2, 4): [],
                                          (2, 5): [], (2, 6): [], (2, 7): [1, 5], (2, 8): [], (3, 0): [],
                                          (3, 1): [3, 4, 6, 9], (3, 2): [], (3, 3): [], (3, 4): [3, 4], (3, 5): [],
                                          (3, 6): [3, 6, 7, 9], (3, 7): [4, 6, 7, 9], (3, 8): [4, 6], (4, 0): [],
                                          (4, 1): [3, 4, 5, 9], (4, 2): [2, 3, 5, 9], (4, 3): [], (4, 4): [],
                                          (4, 5): [], (4, 6): [3, 9], (4, 7): [2, 4, 5, 9], (4, 8): [2, 4, 5],
                                          (5, 0): [4, 5], (5, 1): [3, 4, 5, 6], (5, 2): [2, 3, 5], (5, 3): [],
                                          (5, 4): [3, 4], (5, 5): [], (5, 6): [], (5, 7): [2, 4, 5, 6], (5, 8): [],
                                          (6, 0): [], (6, 1): [7, 8], (6, 2): [7, 8], (6, 3): [], (6, 4): [],
                                          (6, 5): [], (6, 6): [], (6, 7): [2, 4], (6, 8): [2, 4], (7, 0): [],
                                          (7, 1): [3, 5], (7, 2): [3, 5], (7, 3): [], (7, 4): [], (7, 5): [],
                                          (7, 6): [6, 9], (7, 7): [6, 9], (7, 8): [], (8, 0): [], (8, 1): [8, 9],
                                          (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [], (8, 6): [8, 9], (8, 7): [],
                                          (8, 8): []}

        self.assertEqual(naked_subset_row.board, naked_subset_row_expected_board)
        self.assertEqual(naked_subset_row.possible_values, naked_subset_row_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.naked_subset_generic(self.blank_board.get_row_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_naked_subset_col(self):
        naked_subset_column = SudokuBoard(
            [8, 6, 0, 1, 0, 4, 0, 5, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2, 0, 0, 0, 0, 0, 1, 7,
             4, 3, 0, 9, 0, 7, 0, 8, 5, 0, 0, 0, 0, 4, 0, 7, 9, 0, 7, 9, 0, 8, 0, 5, 0, 6, 4,
             6, 4, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 4, 0, 3, 0, 7, 6])

        actual_moves = naked_subset_column.naked_subset_generic(naked_subset_column.get_col_possibilities)

        expected_moves = [
            Move(REMOVE_POSS, 2, (1, 6),
                 'Cell (1, 6) had possibility value of 2 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6'),
            Move(REMOVE_POSS, 3, (1, 6),
                 'Cell (1, 6) had possibility value of 3 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6'),
            Move(REMOVE_POSS, 3, (2, 6),
                 'Cell (2, 6) had possibility value of 3 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6'),
            Move(REMOVE_POSS, 3, (6, 6),
                 'Cell (6, 6) had possibility value of 3 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6'),
            Move(REMOVE_POSS, 3, (7, 6),
                 'Cell (7, 6) had possibility value of 3 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6')
        ]

        naked_subset_column_expected_board = [[8, 6, 0, 1, 0, 4, 0, 5, 9], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                              [9, 2, 0, 0, 0, 0, 0, 1, 7], [4, 3, 0, 9, 0, 7, 0, 8, 5],
                                              [0, 0, 0, 0, 4, 0, 7, 9, 0], [7, 9, 0, 8, 0, 5, 0, 6, 4],
                                              [6, 4, 0, 0, 0, 0, 0, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                              [2, 1, 0, 4, 0, 3, 0, 7, 6]]

        naked_subset_column_expected_poss = {(0, 0): [], (0, 1): [], (0, 2): [3, 7], (0, 3): [], (0, 4): [2, 3, 7],
                                             (0, 5): [], (0, 6): [2, 3], (0, 7): [], (0, 8): [], (1, 0): [1, 3, 5],
                                             (1, 1): [5, 7], (1, 2): [1, 3, 4, 5, 7], (1, 3): [2, 3, 5, 6, 7],
                                             (1, 4): [2, 3, 5, 6, 7, 8, 9], (1, 5): [2, 6, 8, 9], (1, 6): [4, 6, 8],
                                             (1, 7): [3, 4], (1, 8): [2, 3, 8], (2, 0): [], (2, 1): [],
                                             (2, 2): [3, 4, 5], (2, 3): [3, 5, 6], (2, 4): [3, 5, 6, 8], (2, 5): [6, 8],
                                             (2, 6): [4, 6, 8], (2, 7): [], (2, 8): [], (3, 0): [], (3, 1): [],
                                             (3, 2): [1, 2, 6], (3, 3): [], (3, 4): [1, 2, 6], (3, 5): [],
                                             (3, 6): [1, 2], (3, 7): [], (3, 8): [], (4, 0): [1, 5], (4, 1): [5, 8],
                                             (4, 2): [1, 2, 5, 6, 8], (4, 3): [2, 3, 6], (4, 4): [], (4, 5): [1, 2, 6],
                                             (4, 6): [], (4, 7): [], (4, 8): [2, 3], (5, 0): [], (5, 1): [],
                                             (5, 2): [1, 2], (5, 3): [], (5, 4): [1, 2, 3], (5, 5): [],
                                             (5, 6): [1, 2, 3], (5, 7): [], (5, 8): [], (6, 0): [], (6, 1): [],
                                             (6, 2): [3, 5, 7, 8, 9], (6, 3): [5, 7], (6, 4): [5, 7, 8, 9],
                                             (6, 5): [8, 9], (6, 6): [5, 8, 9], (6, 7): [], (6, 8): [], (7, 0): [3, 5],
                                             (7, 1): [5, 7, 8], (7, 2): [3, 5, 7, 8, 9], (7, 3): [2, 5, 6, 7],
                                             (7, 4): [1, 2, 5, 6, 7, 8, 9], (7, 5): [1, 2, 6, 8, 9],
                                             (7, 6): [4, 5, 8, 9], (7, 7): [3, 4], (7, 8): [3, 8], (8, 0): [],
                                             (8, 1): [], (8, 2): [5, 8, 9], (8, 3): [], (8, 4): [5, 8, 9], (8, 5): [],
                                             (8, 6): [5, 8, 9], (8, 7): [], (8, 8): []}

        self.assertEqual(naked_subset_column.board, naked_subset_column_expected_board)
        self.assertEqual(naked_subset_column.possible_values, naked_subset_column_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.naked_subset_generic(self.blank_board.get_col_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_naked_subset_sector(self):
        naked_subset_sector = SudokuBoard(
            [0, 0, 8, 2, 1, 7, 0, 0, 0, 2, 3, 0, 5, 6, 9, 0, 0, 8, 5, 0, 0, 4, 3, 8, 0, 2, 0,
             0, 0, 5, 0, 2, 0, 0, 8, 0, 3, 0, 0, 8, 4, 5, 0, 0, 6, 0, 8, 0, 0, 9, 0, 5, 0, 0,
             0, 4, 0, 6, 0, 1, 0, 0, 9, 0, 0, 0, 3, 0, 2, 0, 1, 4, 0, 0, 0, 9, 8, 4, 7, 0, 0])

        actual_moves = naked_subset_sector.naked_subset_generic(naked_subset_sector.get_sector_possibilities)

        expected_moves = [
            Move(REMOVE_POSS, 4, (0, 6),
                 'Cell (0, 6) had possibility value of 4 removed because there was a naked subset at ((1, 6), (1, 7), (2, 8)) of size 3 in sector 2'),
            Move(REMOVE_POSS, 4, (0, 7),
                 'Cell (0, 7) had possibility value of 4 removed because there was a naked subset at ((1, 6), (1, 7), (2, 8)) of size 3 in sector 2'),
            Move(REMOVE_POSS, 1, (2, 6),
                 'Cell (2, 6) had possibility value of 1 removed because there was a naked subset at ((1, 6), (1, 7), (2, 8)) of size 3 in sector 2')
        ]

        naked_subset_sector_expected_board = [[0, 0, 8, 2, 1, 7, 0, 0, 0], [2, 3, 0, 5, 6, 9, 0, 0, 8],
                                              [5, 0, 0, 4, 3, 8, 0, 2, 0], [0, 0, 5, 0, 2, 0, 0, 8, 0],
                                              [3, 0, 0, 8, 4, 5, 0, 0, 6], [0, 8, 0, 0, 9, 0, 5, 0, 0],
                                              [0, 4, 0, 6, 0, 1, 0, 0, 9], [0, 0, 0, 3, 0, 2, 0, 1, 4],
                                              [0, 0, 0, 9, 8, 4, 7, 0, 0]]

        naked_subset_sector_expected_poss = {(0, 0): [4, 6, 9], (0, 1): [6, 9], (0, 2): [], (0, 3): [], (0, 4): [],
                                             (0, 5): [], (0, 6): [3, 6, 9], (0, 7): [3, 5, 6, 9], (0, 8): [3, 5],
                                             (1, 0): [], (1, 1): [], (1, 2): [1, 4, 7], (1, 3): [], (1, 4): [],
                                             (1, 5): [],
                                             (1, 6): [1, 4], (1, 7): [4, 7], (1, 8): [], (2, 0): [],
                                             (2, 1): [1, 6, 7, 9],
                                             (2, 2): [1, 6, 7, 9], (2, 3): [], (2, 4): [], (2, 5): [], (2, 6): [6, 9],
                                             (2, 7): [], (2, 8): [1, 7], (3, 0): [1, 4, 6, 7, 9], (3, 1): [1, 6, 7, 9],
                                             (3, 2): [], (3, 3): [1, 7], (3, 4): [], (3, 5): [3, 6],
                                             (3, 6): [1, 3, 4, 9],
                                             (3, 7): [], (3, 8): [1, 3, 7], (4, 0): [], (4, 1): [1, 2, 7, 9],
                                             (4, 2): [1, 2, 7, 9], (4, 3): [], (4, 4): [], (4, 5): [],
                                             (4, 6): [1, 2, 9],
                                             (4, 7): [7, 9], (4, 8): [], (5, 0): [1, 4, 6, 7], (5, 1): [],
                                             (5, 2): [1, 2, 4, 6, 7], (5, 3): [1, 7], (5, 4): [], (5, 5): [3, 6],
                                             (5, 6): [], (5, 7): [3, 4, 7], (5, 8): [1, 2, 3, 7], (6, 0): [7, 8],
                                             (6, 1): [], (6, 2): [2, 3, 7], (6, 3): [], (6, 4): [5, 7], (6, 5): [],
                                             (6, 6): [2, 3, 8], (6, 7): [3, 5], (6, 8): [], (7, 0): [6, 7, 8, 9],
                                             (7, 1): [5, 6, 7, 9], (7, 2): [6, 7, 9], (7, 3): [], (7, 4): [5, 7],
                                             (7, 5): [], (7, 6): [6, 8], (7, 7): [], (7, 8): [], (8, 0): [1, 6],
                                             (8, 1): [1, 2, 5, 6], (8, 2): [1, 2, 3, 6], (8, 3): [], (8, 4): [],
                                             (8, 5): [], (8, 6): [], (8, 7): [3, 5, 6], (8, 8): [2, 3, 5]}

        self.assertEqual(naked_subset_sector.board, naked_subset_sector_expected_board)
        self.assertEqual(naked_subset_sector.possible_values, naked_subset_sector_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.naked_subset_generic(self.blank_board.get_sector_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_naked_subset(self):
        naked_subset_row = SudokuBoard(
            [3, 2, 0, 9, 0, 1, 4, 0, 0, 9, 0, 0, 4, 0, 2, 0, 0, 3, 0, 0, 6, 3, 7, 8, 2, 0, 9,
             8, 0, 1, 2, 0, 5, 0, 0, 0, 7, 0, 0, 1, 8, 6, 0, 0, 0, 0, 0, 0, 7, 0, 9, 1, 0, 8,
             1, 0, 0, 6, 9, 3, 5, 0, 0, 2, 0, 0, 8, 1, 4, 0, 0, 7, 6, 0, 4, 5, 2, 7, 0, 3, 1]
        )

        actual_moves = naked_subset_row.naked_subset()

        expected_moves = [
            Move(REMOVE_POSS, 5, (0, 2),
                 'Cell (0, 2) had possibility value of 5 removed because there was a naked subset at ((0, 4), (0, 8)) of size 2 in row 0'),
            Move(REMOVE_POSS, 5, (0, 7),
                 'Cell (0, 7) had possibility value of 5 removed because there was a naked subset at ((0, 4), (0, 8)) of size 2 in row 0'),
            Move(REMOVE_POSS, 6, (0, 7),
                 'Cell (0, 7) had possibility value of 6 removed because there was a naked subset at ((0, 4), (0, 8)) of size 2 in row 0'),
            Move(REMOVE_POSS, 8, (6, 7),
                 'Cell (6, 7) had possibility value of 8 removed because there was a naked subset at ((6, 1), (6, 2)) of size 2 in row 6'),
            Move(REMOVE_POSS, 9, (7, 1),
                 'Cell (7, 1) had possibility value of 9 removed because there was a naked subset at ((7, 6), (7, 7)) of size 2 in row 7'),
            Move(REMOVE_POSS, 9, (7, 2),
                 'Cell (7, 2) had possibility value of 9 removed because there was a naked subset at ((7, 6), (7, 7)) of size 2 in row 7')
        ]

        naked_subset_row_expected_board = [[3, 2, 0, 9, 0, 1, 4, 0, 0], [9, 0, 0, 4, 0, 2, 0, 0, 3],
                                           [0, 0, 6, 3, 7, 8, 2, 0, 9], [8, 0, 1, 2, 0, 5, 0, 0, 0],
                                           [7, 0, 0, 1, 8, 6, 0, 0, 0], [0, 0, 0, 7, 0, 9, 1, 0, 8],
                                           [1, 0, 0, 6, 9, 3, 5, 0, 0], [2, 0, 0, 8, 1, 4, 0, 0, 7],
                                           [6, 0, 4, 5, 2, 7, 0, 3, 1]]

        naked_subset_row_expected_poss = {(0, 0): [], (0, 1): [], (0, 2): [7, 8], (0, 3): [], (0, 4): [5, 6],
                                          (0, 5): [], (0, 6): [], (0, 7): [7, 8], (0, 8): [5, 6], (1, 0): [],
                                          (1, 1): [1, 5, 7, 8], (1, 2): [5, 7, 8], (1, 3): [], (1, 4): [5, 6],
                                          (1, 5): [], (1, 6): [6, 7, 8], (1, 7): [1, 5, 6, 7, 8], (1, 8): [],
                                          (2, 0): [4, 5], (2, 1): [1, 4, 5], (2, 2): [], (2, 3): [], (2, 4): [],
                                          (2, 5): [], (2, 6): [], (2, 7): [1, 5], (2, 8): [], (3, 0): [],
                                          (3, 1): [3, 4, 6, 9], (3, 2): [], (3, 3): [], (3, 4): [3, 4], (3, 5): [],
                                          (3, 6): [3, 6, 7, 9], (3, 7): [4, 6, 7, 9], (3, 8): [4, 6], (4, 0): [],
                                          (4, 1): [3, 4, 5, 9], (4, 2): [2, 3, 5, 9], (4, 3): [], (4, 4): [],
                                          (4, 5): [], (4, 6): [3, 9], (4, 7): [2, 4, 5, 9], (4, 8): [2, 4, 5],
                                          (5, 0): [4, 5], (5, 1): [3, 4, 5, 6], (5, 2): [2, 3, 5], (5, 3): [],
                                          (5, 4): [3, 4], (5, 5): [], (5, 6): [], (5, 7): [2, 4, 5, 6], (5, 8): [],
                                          (6, 0): [], (6, 1): [7, 8], (6, 2): [7, 8], (6, 3): [], (6, 4): [],
                                          (6, 5): [], (6, 6): [], (6, 7): [2, 4], (6, 8): [2, 4], (7, 0): [],
                                          (7, 1): [3, 5], (7, 2): [3, 5], (7, 3): [], (7, 4): [], (7, 5): [],
                                          (7, 6): [6, 9], (7, 7): [6, 9], (7, 8): [], (8, 0): [], (8, 1): [8, 9],
                                          (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [], (8, 6): [8, 9], (8, 7): [],
                                          (8, 8): []}

        self.assertEqual(naked_subset_row.board, naked_subset_row_expected_board)
        self.assertEqual(naked_subset_row.possible_values, naked_subset_row_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        naked_subset_column = SudokuBoard(
            [8, 6, 0, 1, 0, 4, 0, 5, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2, 0, 0, 0, 0, 0, 1, 7,
             4, 3, 0, 9, 0, 7, 0, 8, 5, 0, 0, 0, 0, 4, 0, 7, 9, 0, 7, 9, 0, 8, 0, 5, 0, 6, 4,
             6, 4, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 4, 0, 3, 0, 7, 6])

        actual_moves = naked_subset_column.naked_subset()

        expected_moves = [
            Move(REMOVE_POSS, 2, (1, 6),
                 'Cell (1, 6) had possibility value of 2 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6'),
            Move(REMOVE_POSS, 3, (1, 6),
                 'Cell (1, 6) had possibility value of 3 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6'),
            Move(REMOVE_POSS, 3, (2, 6),
                 'Cell (2, 6) had possibility value of 3 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6'),
            Move(REMOVE_POSS, 3, (6, 6),
                 'Cell (6, 6) had possibility value of 3 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6'),
            Move(REMOVE_POSS, 3, (7, 6),
                 'Cell (7, 6) had possibility value of 3 removed because there was a naked subset at ((0, 6), (3, 6), (5, 6)) of size 3 in column 6')
        ]

        naked_subset_column_expected_board = [[8, 6, 0, 1, 0, 4, 0, 5, 9], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                              [9, 2, 0, 0, 0, 0, 0, 1, 7], [4, 3, 0, 9, 0, 7, 0, 8, 5],
                                              [0, 0, 0, 0, 4, 0, 7, 9, 0], [7, 9, 0, 8, 0, 5, 0, 6, 4],
                                              [6, 4, 0, 0, 0, 0, 0, 2, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                              [2, 1, 0, 4, 0, 3, 0, 7, 6]]

        naked_subset_column_expected_poss = {(0, 0): [], (0, 1): [], (0, 2): [3, 7], (0, 3): [], (0, 4): [2, 3, 7],
                                             (0, 5): [], (0, 6): [2, 3], (0, 7): [], (0, 8): [], (1, 0): [1, 3, 5],
                                             (1, 1): [5, 7], (1, 2): [1, 3, 4, 5, 7], (1, 3): [2, 3, 5, 6, 7],
                                             (1, 4): [2, 3, 5, 6, 7, 8, 9], (1, 5): [2, 6, 8, 9], (1, 6): [4, 6, 8],
                                             (1, 7): [3, 4], (1, 8): [2, 3, 8], (2, 0): [], (2, 1): [],
                                             (2, 2): [3, 4, 5], (2, 3): [3, 5, 6], (2, 4): [3, 5, 6, 8], (2, 5): [6, 8],
                                             (2, 6): [4, 6, 8], (2, 7): [], (2, 8): [], (3, 0): [], (3, 1): [],
                                             (3, 2): [1, 2, 6], (3, 3): [], (3, 4): [1, 2, 6], (3, 5): [],
                                             (3, 6): [1, 2], (3, 7): [], (3, 8): [], (4, 0): [1, 5], (4, 1): [5, 8],
                                             (4, 2): [1, 2, 5, 6, 8], (4, 3): [2, 3, 6], (4, 4): [], (4, 5): [1, 2, 6],
                                             (4, 6): [], (4, 7): [], (4, 8): [2, 3], (5, 0): [], (5, 1): [],
                                             (5, 2): [1, 2], (5, 3): [], (5, 4): [1, 2, 3], (5, 5): [],
                                             (5, 6): [1, 2, 3], (5, 7): [], (5, 8): [], (6, 0): [], (6, 1): [],
                                             (6, 2): [3, 5, 7, 8, 9], (6, 3): [5, 7], (6, 4): [5, 7, 8, 9],
                                             (6, 5): [8, 9], (6, 6): [5, 8, 9], (6, 7): [], (6, 8): [], (7, 0): [3, 5],
                                             (7, 1): [5, 7, 8], (7, 2): [3, 5, 7, 8, 9], (7, 3): [2, 5, 6, 7],
                                             (7, 4): [1, 2, 5, 6, 7, 8, 9], (7, 5): [1, 2, 6, 8, 9],
                                             (7, 6): [4, 5, 8, 9], (7, 7): [3, 4], (7, 8): [3, 8], (8, 0): [],
                                             (8, 1): [], (8, 2): [5, 8, 9], (8, 3): [], (8, 4): [5, 8, 9], (8, 5): [],
                                             (8, 6): [5, 8, 9], (8, 7): [], (8, 8): []}

        self.assertEqual(naked_subset_column.board, naked_subset_column_expected_board)
        self.assertEqual(naked_subset_column.possible_values, naked_subset_column_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        naked_subset_sector = SudokuBoard(
            [0, 0, 8, 2, 1, 7, 0, 0, 0, 2, 3, 0, 5, 6, 9, 0, 0, 8, 5, 0, 0, 4, 3, 8, 0, 2, 0,
             0, 0, 5, 0, 2, 0, 0, 8, 0, 3, 0, 0, 8, 4, 5, 0, 0, 6, 0, 8, 0, 0, 9, 0, 5, 0, 0,
             0, 4, 0, 6, 0, 1, 0, 0, 9, 0, 0, 0, 3, 0, 2, 0, 1, 4, 0, 0, 0, 9, 8, 4, 7, 0, 0])

        actual_moves = naked_subset_sector.naked_subset()

        expected_moves = [
            Move(REMOVE_POSS, 4, (0, 6),
                 'Cell (0, 6) had possibility value of 4 removed because there was a naked subset at ((1, 6), (1, 7), (2, 8)) of size 3 in sector 2'),
            Move(REMOVE_POSS, 4, (0, 7),
                 'Cell (0, 7) had possibility value of 4 removed because there was a naked subset at ((1, 6), (1, 7), (2, 8)) of size 3 in sector 2'),
            Move(REMOVE_POSS, 1, (2, 6),
                 'Cell (2, 6) had possibility value of 1 removed because there was a naked subset at ((1, 6), (1, 7), (2, 8)) of size 3 in sector 2')
        ]

        naked_subset_sector_expected_board = [[0, 0, 8, 2, 1, 7, 0, 0, 0], [2, 3, 0, 5, 6, 9, 0, 0, 8],
                                              [5, 0, 0, 4, 3, 8, 0, 2, 0], [0, 0, 5, 0, 2, 0, 0, 8, 0],
                                              [3, 0, 0, 8, 4, 5, 0, 0, 6], [0, 8, 0, 0, 9, 0, 5, 0, 0],
                                              [0, 4, 0, 6, 0, 1, 0, 0, 9], [0, 0, 0, 3, 0, 2, 0, 1, 4],
                                              [0, 0, 0, 9, 8, 4, 7, 0, 0]]

        naked_subset_sector_expected_poss = {(0, 0): [4, 6, 9], (0, 1): [6, 9], (0, 2): [], (0, 3): [], (0, 4): [],
                                             (0, 5): [], (0, 6): [3, 6, 9], (0, 7): [3, 5, 6, 9], (0, 8): [3, 5],
                                             (1, 0): [], (1, 1): [], (1, 2): [1, 4, 7], (1, 3): [], (1, 4): [],
                                             (1, 5): [],
                                             (1, 6): [1, 4], (1, 7): [4, 7], (1, 8): [], (2, 0): [],
                                             (2, 1): [1, 6, 7, 9],
                                             (2, 2): [1, 6, 7, 9], (2, 3): [], (2, 4): [], (2, 5): [], (2, 6): [6, 9],
                                             (2, 7): [], (2, 8): [1, 7], (3, 0): [1, 4, 6, 7, 9], (3, 1): [1, 6, 7, 9],
                                             (3, 2): [], (3, 3): [1, 7], (3, 4): [], (3, 5): [3, 6],
                                             (3, 6): [1, 3, 4, 9],
                                             (3, 7): [], (3, 8): [1, 3, 7], (4, 0): [], (4, 1): [1, 2, 7, 9],
                                             (4, 2): [1, 2, 7, 9], (4, 3): [], (4, 4): [], (4, 5): [],
                                             (4, 6): [1, 2, 9],
                                             (4, 7): [7, 9], (4, 8): [], (5, 0): [1, 4, 6, 7], (5, 1): [],
                                             (5, 2): [1, 2, 4, 6, 7], (5, 3): [1, 7], (5, 4): [], (5, 5): [3, 6],
                                             (5, 6): [], (5, 7): [3, 4, 7], (5, 8): [1, 2, 3, 7], (6, 0): [7, 8],
                                             (6, 1): [], (6, 2): [2, 3, 7], (6, 3): [], (6, 4): [5, 7], (6, 5): [],
                                             (6, 6): [2, 3, 8], (6, 7): [3, 5], (6, 8): [], (7, 0): [6, 7, 8, 9],
                                             (7, 1): [5, 6, 7, 9], (7, 2): [6, 7, 9], (7, 3): [], (7, 4): [5, 7],
                                             (7, 5): [], (7, 6): [6, 8], (7, 7): [], (7, 8): [], (8, 0): [1, 6],
                                             (8, 1): [1, 2, 5, 6], (8, 2): [1, 2, 3, 6], (8, 3): [], (8, 4): [],
                                             (8, 5): [], (8, 6): [], (8, 7): [3, 5, 6], (8, 8): [2, 3, 5]}

        self.assertEqual(naked_subset_sector.board, naked_subset_sector_expected_board)
        self.assertEqual(naked_subset_sector.possible_values, naked_subset_sector_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.naked_subset()
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_hidden_subset_row(self):
        hidden_subset_row = SudokuBoard(
            [5, 0, 2, 6, 0, 0, 7, 4, 9, 0, 0, 0, 9, 0, 0, 6, 1, 2, 0, 0, 6, 0, 2, 0, 3, 8, 5,
             0, 0, 4, 0, 9, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 2, 7, 0, 9, 3, 0,
             8, 3, 7, 0, 6, 2, 0, 9, 1, 2, 6, 1, 0, 0, 9, 0, 0, 0, 4, 5, 9, 7, 1, 8, 2, 6, 3])

        actual_moves = hidden_subset_row.hidden_subset_generic(hidden_subset_row.get_row_possibilities)

        expected_moves = [
            Move(REMOVE_POSS, 1, (4, 0),
                 'Cell (4, 0) had possibility value of 1 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 1, (4, 1),
                 'Cell (4, 1) had possibility value of 1 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 8, (4, 1),
                 'Cell (4, 1) had possibility value of 8 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 5, (4, 7),
                 'Cell (4, 7) had possibility value of 5 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 4, (4, 8),
                 'Cell (4, 8) had possibility value of 4 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 8, (4, 8),
                 'Cell (4, 8) had possibility value of 8 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))')
        ]

        hidden_subset_row_expected_board = [[5, 0, 2, 6, 0, 0, 7, 4, 9], [0, 0, 0, 9, 0, 0, 6, 1, 2],
                                            [0, 0, 6, 0, 2, 0, 3, 8, 5], [0, 0, 4, 0, 9, 6, 1, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 2, 7, 0, 9, 3, 0],
                                            [8, 3, 7, 0, 6, 2, 0, 9, 1], [2, 6, 1, 0, 0, 9, 0, 0, 0],
                                            [4, 5, 9, 7, 1, 8, 2, 6, 3]]

        hidden_subset_row_expected_poss = {(0, 0): [], (0, 1): [1, 8], (0, 2): [], (0, 3): [], (0, 4): [3, 8],
                                           (0, 5): [1, 3], (0, 6): [], (0, 7): [], (0, 8): [], (1, 0): [3, 7],
                                           (1, 1): [4, 7, 8], (1, 2): [3, 8], (1, 3): [], (1, 4): [3, 4, 5, 8],
                                           (1, 5): [3, 4, 5, 7], (1, 6): [], (1, 7): [], (1, 8): [], (2, 0): [1, 7, 9],
                                           (2, 1): [1, 4, 7, 9], (2, 2): [], (2, 3): [1, 4], (2, 4): [],
                                           (2, 5): [1, 4, 7], (2, 6): [], (2, 7): [], (2, 8): [], (3, 0): [3, 7],
                                           (3, 1): [2, 7, 8], (3, 2): [], (3, 3): [3, 5, 8], (3, 4): [], (3, 5): [],
                                           (3, 6): [], (3, 7): [2, 5, 7], (3, 8): [7, 8], (4, 0): [3, 6, 7, 9],
                                           (4, 1): [2, 7, 9], (4, 2): [3, 8], (4, 3): [1, 3, 4, 5, 8],
                                           (4, 4): [3, 4, 5, 8], (4, 5): [1, 3, 4, 5], (4, 6): [4, 5, 8],
                                           (4, 7): [2, 7], (4, 8): [6, 7], (5, 0): [1, 6], (5, 1): [1, 8], (5, 2): [],
                                           (5, 3): [], (5, 4): [], (5, 5): [1, 4], (5, 6): [], (5, 7): [],
                                           (5, 8): [4, 6, 8], (6, 0): [], (6, 1): [], (6, 2): [], (6, 3): [4, 5],
                                           (6, 4): [], (6, 5): [], (6, 6): [4, 5], (6, 7): [], (6, 8): [], (7, 0): [],
                                           (7, 1): [], (7, 2): [], (7, 3): [3, 4, 5], (7, 4): [3, 4, 5], (7, 5): [],
                                           (7, 6): [4, 5, 8], (7, 7): [5, 7], (7, 8): [4, 7, 8], (8, 0): [], (8, 1): [],
                                           (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [], (8, 6): [], (8, 7): [],
                                           (8, 8): []}

        self.assertEqual(hidden_subset_row.board, hidden_subset_row_expected_board)
        self.assertEqual(hidden_subset_row.possible_values, hidden_subset_row_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.hidden_subset_generic(self.blank_board.get_row_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_hidden_subset_col(self):
        hidden_subset_col = SudokuBoard(
            [0, 4, 9, 1, 3, 2, 0, 0, 0, 0, 8, 1, 4, 7, 9, 0, 0, 0, 3, 2, 7, 6, 8, 5, 9, 1, 4,
             0, 9, 6, 0, 5, 1, 8, 0, 0, 0, 7, 5, 0, 2, 8, 0, 0, 0, 0, 3, 8, 0, 4, 6, 0, 0, 5,
             8, 5, 3, 2, 6, 7, 0, 0, 0, 7, 1, 2, 8, 9, 4, 5, 6, 3, 9, 6, 4, 5, 1, 3, 0, 0, 0]
        )

        actual_moves = hidden_subset_col.hidden_subset_generic(hidden_subset_col.get_col_possibilities)

        expected_moves = [
            Move(REMOVE_POSS, 6, (4, 8),
                 'Cell (4, 8) had possibility value of 6 removed because there was a hidden subset of size 2 (1, 9) in column 8 at cells ((4, 8), (6, 8))')
        ]

        hidden_subset_col_expected_board = [[0, 4, 9, 1, 3, 2, 0, 0, 0], [0, 8, 1, 4, 7, 9, 0, 0, 0],
                                            [3, 2, 7, 6, 8, 5, 9, 1, 4], [0, 9, 6, 0, 5, 1, 8, 0, 0],
                                            [0, 7, 5, 0, 2, 8, 0, 0, 0], [0, 3, 8, 0, 4, 6, 0, 0, 5],
                                            [8, 5, 3, 2, 6, 7, 0, 0, 0], [7, 1, 2, 8, 9, 4, 5, 6, 3],
                                            [9, 6, 4, 5, 1, 3, 0, 0, 0]]

        hidden_subset_col_expected_poss = {(0, 0): [5, 6], (0, 1): [], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [],
                                           (0, 6): [6, 7], (0, 7): [5, 7, 8], (0, 8): [6, 7, 8], (1, 0): [5, 6],
                                           (1, 1): [], (1, 2): [], (1, 3): [], (1, 4): [], (1, 5): [],
                                           (1, 6): [2, 3, 6], (1, 7): [2, 3, 5], (1, 8): [2, 6], (2, 0): [], (2, 1): [],
                                           (2, 2): [], (2, 3): [], (2, 4): [], (2, 5): [], (2, 6): [], (2, 7): [],
                                           (2, 8): [], (3, 0): [2, 4], (3, 1): [], (3, 2): [], (3, 3): [3, 7],
                                           (3, 4): [], (3, 5): [], (3, 6): [], (3, 7): [2, 3, 4, 7], (3, 8): [2, 7],
                                           (4, 0): [1, 4], (4, 1): [], (4, 2): [], (4, 3): [3, 9], (4, 4): [],
                                           (4, 5): [], (4, 6): [1, 3, 4, 6], (4, 7): [3, 4, 9], (4, 8): [1, 9],
                                           (5, 0): [1, 2], (5, 1): [], (5, 2): [], (5, 3): [7, 9], (5, 4): [],
                                           (5, 5): [], (5, 6): [1, 2, 7], (5, 7): [2, 7, 9], (5, 8): [], (6, 0): [],
                                           (6, 1): [], (6, 2): [], (6, 3): [], (6, 4): [], (6, 5): [], (6, 6): [1, 4],
                                           (6, 7): [4, 9], (6, 8): [1, 9], (7, 0): [], (7, 1): [], (7, 2): [],
                                           (7, 3): [], (7, 4): [], (7, 5): [], (7, 6): [], (7, 7): [], (7, 8): [],
                                           (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [],
                                           (8, 6): [2, 7], (8, 7): [2, 7, 8], (8, 8): [2, 7, 8]}

        self.assertEqual(hidden_subset_col.board, hidden_subset_col_expected_board)
        self.assertEqual(hidden_subset_col.possible_values, hidden_subset_col_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.hidden_subset_generic(self.blank_board.get_col_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_hidden_subset_sector(self):
        hidden_subset_sector = SudokuBoard(
            [8, 1, 6, 5, 7, 3, 2, 9, 4, 3, 9, 2, 0, 0, 0, 0, 0, 0, 4, 5, 7, 2, 0, 9, 0, 0, 6,
             9, 4, 1, 0, 0, 0, 5, 6, 8, 7, 8, 5, 4, 9, 6, 1, 2, 3, 6, 2, 3, 8, 0, 0, 0, 4, 0,
             2, 7, 9, 0, 0, 0, 0, 0, 1, 1, 3, 8, 0, 0, 0, 0, 7, 0, 5, 6, 4, 0, 0, 0, 0, 8, 2]
        )

        hidden_subset_sector.set_poss_values(
            {(0, 0): [], (0, 1): [], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [], (0, 6): [], (0, 7): [], (0, 8): [],
             (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [1, 6], (1, 4): [1, 4, 6, 8], (1, 5): [1, 4, 8],
             (1, 6): [7, 8], (1, 7): [1, 5], (1, 8): [5, 7], (2, 0): [], (2, 1): [], (2, 2): [], (2, 3): [],
             (2, 4): [1, 8], (2, 5): [], (2, 6): [3, 8], (2, 7): [1, 3], (2, 8): [], (3, 0): [], (3, 1): [], (3, 2): [],
             (3, 3): [3, 7], (3, 4): [2, 3], (3, 5): [2, 7], (3, 6): [], (3, 7): [], (3, 8): [], (4, 0): [], (4, 1): [],
             (4, 2): [], (4, 3): [], (4, 4): [], (4, 5): [], (4, 6): [], (4, 7): [], (4, 8): [], (5, 0): [], (5, 1): [],
             (5, 2): [], (5, 3): [], (5, 4): [1, 5], (5, 5): [1, 5], (5, 6): [7, 9], (5, 7): [], (5, 8): [7, 9],
             (6, 0): [], (6, 1): [], (6, 2): [], (6, 3): [3, 6], (6, 4): [3, 4, 5, 6, 8], (6, 5): [4, 5, 8],
             (6, 6): [4, 6], (6, 7): [3, 5], (6, 8): [], (7, 0): [], (7, 1): [], (7, 2): [], (7, 3): [6, 9],
             (7, 4): [2, 4, 5, 6], (7, 5): [2, 4, 5], (7, 6): [4, 6], (7, 7): [], (7, 8): [5, 9], (8, 0): [],
             (8, 1): [], (8, 2): [], (8, 3): [1, 3, 7, 9], (8, 4): [1, 3], (8, 5): [1, 7], (8, 6): [3, 9], (8, 7): [],
             (8, 8): []})

        actual_moves = hidden_subset_sector.hidden_subset_generic(hidden_subset_sector.get_sector_possibilities)

        expected_moves = [
            Move(REMOVE_POSS, 3, (6, 4),
                 'Cell (6, 4) had possibility value of 3 removed because there was a hidden subset of size 4 (2, 4, 5, 8) in sector 7 at cells ((6, 4), (6, 5), (7, 4), (7, 5))'),
            Move(REMOVE_POSS, 6, (6, 4),
                 'Cell (6, 4) had possibility value of 6 removed because there was a hidden subset of size 4 (2, 4, 5, 8) in sector 7 at cells ((6, 4), (6, 5), (7, 4), (7, 5))'),
            Move(REMOVE_POSS, 6, (7, 4),
                 'Cell (7, 4) had possibility value of 6 removed because there was a hidden subset of size 4 (2, 4, 5, 8) in sector 7 at cells ((6, 4), (6, 5), (7, 4), (7, 5))')
        ]

        hidden_subset_sector_expected_board = [[8, 1, 6, 5, 7, 3, 2, 9, 4], [3, 9, 2, 0, 0, 0, 0, 0, 0],
                                               [4, 5, 7, 2, 0, 9, 0, 0, 6], [9, 4, 1, 0, 0, 0, 5, 6, 8],
                                               [7, 8, 5, 4, 9, 6, 1, 2, 3], [6, 2, 3, 8, 0, 0, 0, 4, 0],
                                               [2, 7, 9, 0, 0, 0, 0, 0, 1], [1, 3, 8, 0, 0, 0, 0, 7, 0],
                                               [5, 6, 4, 0, 0, 0, 0, 8, 2]]

        hidden_subset_sector_expected_poss = {(0, 0): [], (0, 1): [], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [],
                                              (0, 6): [], (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [], (1, 2): [],
                                              (1, 3): [1, 6], (1, 4): [1, 4, 6, 8], (1, 5): [1, 4, 8], (1, 6): [7, 8],
                                              (1, 7): [1, 5], (1, 8): [5, 7], (2, 0): [], (2, 1): [], (2, 2): [],
                                              (2, 3): [], (2, 4): [1, 8], (2, 5): [], (2, 6): [3, 8], (2, 7): [1, 3],
                                              (2, 8): [], (3, 0): [], (3, 1): [], (3, 2): [], (3, 3): [3, 7],
                                              (3, 4): [2, 3], (3, 5): [2, 7], (3, 6): [], (3, 7): [], (3, 8): [],
                                              (4, 0): [], (4, 1): [], (4, 2): [], (4, 3): [], (4, 4): [], (4, 5): [],
                                              (4, 6): [], (4, 7): [], (4, 8): [], (5, 0): [], (5, 1): [], (5, 2): [],
                                              (5, 3): [], (5, 4): [1, 5], (5, 5): [1, 5], (5, 6): [7, 9], (5, 7): [],
                                              (5, 8): [7, 9], (6, 0): [], (6, 1): [], (6, 2): [], (6, 3): [3, 6],
                                              (6, 4): [4, 5, 8], (6, 5): [4, 5, 8], (6, 6): [4, 6], (6, 7): [3, 5],
                                              (6, 8): [], (7, 0): [], (7, 1): [], (7, 2): [], (7, 3): [6, 9],
                                              (7, 4): [2, 4, 5], (7, 5): [2, 4, 5], (7, 6): [4, 6], (7, 7): [],
                                              (7, 8): [5, 9], (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [1, 3, 7, 9],
                                              (8, 4): [1, 3], (8, 5): [1, 7], (8, 6): [3, 9], (8, 7): [], (8, 8): []}

        self.assertEqual(hidden_subset_sector.board, hidden_subset_sector_expected_board)
        self.assertEqual(hidden_subset_sector.possible_values, hidden_subset_sector_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.hidden_subset_generic(self.blank_board.get_sector_possibilities)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_hidden_subset(self):
        hidden_subset_row = SudokuBoard(
            [5, 0, 2, 6, 0, 0, 7, 4, 9, 0, 0, 0, 9, 0, 0, 6, 1, 2, 0, 0, 6, 0, 2, 0, 3, 8, 5,
             0, 0, 4, 0, 9, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 2, 7, 0, 9, 3, 0,
             8, 3, 7, 0, 6, 2, 0, 9, 1, 2, 6, 1, 0, 0, 9, 0, 0, 0, 4, 5, 9, 7, 1, 8, 2, 6, 3])

        actual_moves = hidden_subset_row.hidden_subset()

        expected_moves = [
            Move(REMOVE_POSS, 1, (4, 0),
                 'Cell (4, 0) had possibility value of 1 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 1, (4, 1),
                 'Cell (4, 1) had possibility value of 1 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 8, (4, 1),
                 'Cell (4, 1) had possibility value of 8 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 5, (4, 7),
                 'Cell (4, 7) had possibility value of 5 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 4, (4, 8),
                 'Cell (4, 8) had possibility value of 4 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))'),
            Move(REMOVE_POSS, 8, (4, 8),
                 'Cell (4, 8) had possibility value of 8 removed because there was a hidden subset of size 4 (2, 6, 7, 9) in row 4 at cells ((4, 0), (4, 1), (4, 7), (4, 8))')
        ]

        hidden_subset_row_expected_board = [[5, 0, 2, 6, 0, 0, 7, 4, 9], [0, 0, 0, 9, 0, 0, 6, 1, 2],
                                            [0, 0, 6, 0, 2, 0, 3, 8, 5], [0, 0, 4, 0, 9, 6, 1, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 2, 7, 0, 9, 3, 0],
                                            [8, 3, 7, 0, 6, 2, 0, 9, 1], [2, 6, 1, 0, 0, 9, 0, 0, 0],
                                            [4, 5, 9, 7, 1, 8, 2, 6, 3]]

        hidden_subset_row_expected_poss = {(0, 0): [], (0, 1): [1, 8], (0, 2): [], (0, 3): [], (0, 4): [3, 8],
                                           (0, 5): [1, 3], (0, 6): [], (0, 7): [], (0, 8): [], (1, 0): [3, 7],
                                           (1, 1): [4, 7, 8], (1, 2): [3, 8], (1, 3): [], (1, 4): [3, 4, 5, 8],
                                           (1, 5): [3, 4, 5, 7], (1, 6): [], (1, 7): [], (1, 8): [], (2, 0): [1, 7, 9],
                                           (2, 1): [1, 4, 7, 9], (2, 2): [], (2, 3): [1, 4], (2, 4): [],
                                           (2, 5): [1, 4, 7], (2, 6): [], (2, 7): [], (2, 8): [], (3, 0): [3, 7],
                                           (3, 1): [2, 7, 8], (3, 2): [], (3, 3): [3, 5, 8], (3, 4): [], (3, 5): [],
                                           (3, 6): [], (3, 7): [2, 5, 7], (3, 8): [7, 8], (4, 0): [3, 6, 7, 9],
                                           (4, 1): [2, 7, 9], (4, 2): [3, 8], (4, 3): [1, 3, 4, 5, 8],
                                           (4, 4): [3, 4, 5, 8], (4, 5): [1, 3, 4, 5], (4, 6): [4, 5, 8],
                                           (4, 7): [2, 7], (4, 8): [6, 7], (5, 0): [1, 6], (5, 1): [1, 8], (5, 2): [],
                                           (5, 3): [], (5, 4): [], (5, 5): [1, 4], (5, 6): [], (5, 7): [],
                                           (5, 8): [4, 6, 8], (6, 0): [], (6, 1): [], (6, 2): [], (6, 3): [4, 5],
                                           (6, 4): [], (6, 5): [], (6, 6): [4, 5], (6, 7): [], (6, 8): [], (7, 0): [],
                                           (7, 1): [], (7, 2): [], (7, 3): [3, 4, 5], (7, 4): [3, 4, 5], (7, 5): [],
                                           (7, 6): [4, 5, 8], (7, 7): [5, 7], (7, 8): [4, 7, 8], (8, 0): [], (8, 1): [],
                                           (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [], (8, 6): [], (8, 7): [],
                                           (8, 8): []}

        self.assertEqual(hidden_subset_row.board, hidden_subset_row_expected_board)
        self.assertEqual(hidden_subset_row.possible_values, hidden_subset_row_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        hidden_subset_col = SudokuBoard(
            [0, 4, 9, 1, 3, 2, 0, 0, 0, 0, 8, 1, 4, 7, 9, 0, 0, 0, 3, 2, 7, 6, 8, 5, 9, 1, 4,
             0, 9, 6, 0, 5, 1, 8, 0, 0, 0, 7, 5, 0, 2, 8, 0, 0, 0, 0, 3, 8, 0, 4, 6, 0, 0, 5,
             8, 5, 3, 2, 6, 7, 0, 0, 0, 7, 1, 2, 8, 9, 4, 5, 6, 3, 9, 6, 4, 5, 1, 3, 0, 0, 0]
        )

        actual_moves = hidden_subset_col.hidden_subset()

        expected_moves = [
            Move(REMOVE_POSS, 6, (4, 8),
                 'Cell (4, 8) had possibility value of 6 removed because there was a hidden subset of size 2 (1, 9) in column 8 at cells ((4, 8), (6, 8))')
        ]

        hidden_subset_col_expected_board = [[0, 4, 9, 1, 3, 2, 0, 0, 0], [0, 8, 1, 4, 7, 9, 0, 0, 0],
                                            [3, 2, 7, 6, 8, 5, 9, 1, 4], [0, 9, 6, 0, 5, 1, 8, 0, 0],
                                            [0, 7, 5, 0, 2, 8, 0, 0, 0], [0, 3, 8, 0, 4, 6, 0, 0, 5],
                                            [8, 5, 3, 2, 6, 7, 0, 0, 0], [7, 1, 2, 8, 9, 4, 5, 6, 3],
                                            [9, 6, 4, 5, 1, 3, 0, 0, 0]]

        hidden_subset_col_expected_poss = {(0, 0): [5, 6], (0, 1): [], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [],
                                           (0, 6): [6, 7], (0, 7): [5, 7, 8], (0, 8): [6, 7, 8], (1, 0): [5, 6],
                                           (1, 1): [], (1, 2): [], (1, 3): [], (1, 4): [], (1, 5): [],
                                           (1, 6): [2, 3, 6], (1, 7): [2, 3, 5], (1, 8): [2, 6], (2, 0): [], (2, 1): [],
                                           (2, 2): [], (2, 3): [], (2, 4): [], (2, 5): [], (2, 6): [], (2, 7): [],
                                           (2, 8): [], (3, 0): [2, 4], (3, 1): [], (3, 2): [], (3, 3): [3, 7],
                                           (3, 4): [], (3, 5): [], (3, 6): [], (3, 7): [2, 3, 4, 7], (3, 8): [2, 7],
                                           (4, 0): [1, 4], (4, 1): [], (4, 2): [], (4, 3): [3, 9], (4, 4): [],
                                           (4, 5): [], (4, 6): [1, 3, 4, 6], (4, 7): [3, 4, 9], (4, 8): [1, 9],
                                           (5, 0): [1, 2], (5, 1): [], (5, 2): [], (5, 3): [7, 9], (5, 4): [],
                                           (5, 5): [], (5, 6): [1, 2, 7], (5, 7): [2, 7, 9], (5, 8): [], (6, 0): [],
                                           (6, 1): [], (6, 2): [], (6, 3): [], (6, 4): [], (6, 5): [], (6, 6): [1, 4],
                                           (6, 7): [4, 9], (6, 8): [1, 9], (7, 0): [], (7, 1): [], (7, 2): [],
                                           (7, 3): [], (7, 4): [], (7, 5): [], (7, 6): [], (7, 7): [], (7, 8): [],
                                           (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [],
                                           (8, 6): [2, 7], (8, 7): [2, 7, 8], (8, 8): [2, 7, 8]}

        self.assertEqual(hidden_subset_col.board, hidden_subset_col_expected_board)
        self.assertEqual(hidden_subset_col.possible_values, hidden_subset_col_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        hidden_subset_sector = SudokuBoard(
            [8, 1, 6, 5, 7, 3, 2, 9, 4, 3, 9, 2, 0, 0, 0, 0, 0, 0, 4, 5, 7, 2, 0, 9, 0, 0, 6,
             9, 4, 1, 0, 0, 0, 5, 6, 8, 7, 8, 5, 4, 9, 6, 1, 2, 3, 6, 2, 3, 8, 0, 0, 0, 4, 0,
             2, 7, 9, 0, 0, 0, 0, 0, 1, 1, 3, 8, 0, 0, 0, 0, 7, 0, 5, 6, 4, 0, 0, 0, 0, 8, 2]
        )

        hidden_subset_sector.set_poss_values(
            {(0, 0): [], (0, 1): [], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [], (0, 6): [], (0, 7): [], (0, 8): [],
             (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [1, 6], (1, 4): [1, 4, 6, 8], (1, 5): [1, 4, 8],
             (1, 6): [7, 8], (1, 7): [1, 5], (1, 8): [5, 7], (2, 0): [], (2, 1): [], (2, 2): [], (2, 3): [],
             (2, 4): [1, 8], (2, 5): [], (2, 6): [3, 8], (2, 7): [1, 3], (2, 8): [], (3, 0): [], (3, 1): [], (3, 2): [],
             (3, 3): [3, 7], (3, 4): [2, 3], (3, 5): [2, 7], (3, 6): [], (3, 7): [], (3, 8): [], (4, 0): [], (4, 1): [],
             (4, 2): [], (4, 3): [], (4, 4): [], (4, 5): [], (4, 6): [], (4, 7): [], (4, 8): [], (5, 0): [], (5, 1): [],
             (5, 2): [], (5, 3): [], (5, 4): [1, 5], (5, 5): [1, 5], (5, 6): [7, 9], (5, 7): [], (5, 8): [7, 9],
             (6, 0): [], (6, 1): [], (6, 2): [], (6, 3): [3, 6], (6, 4): [3, 4, 5, 6, 8], (6, 5): [4, 5, 8],
             (6, 6): [4, 6], (6, 7): [3, 5], (6, 8): [], (7, 0): [], (7, 1): [], (7, 2): [], (7, 3): [6, 9],
             (7, 4): [2, 4, 5, 6], (7, 5): [2, 4, 5], (7, 6): [4, 6], (7, 7): [], (7, 8): [5, 9], (8, 0): [],
             (8, 1): [], (8, 2): [], (8, 3): [1, 3, 7, 9], (8, 4): [1, 3], (8, 5): [1, 7], (8, 6): [3, 9], (8, 7): [],
             (8, 8): []})

        actual_moves = hidden_subset_sector.hidden_subset()

        expected_moves = [
            Move(REMOVE_POSS, 3, (6, 4),
                 'Cell (6, 4) had possibility value of 3 removed because there was a hidden subset of size 4 (2, 4, 5, 8) in sector 7 at cells ((6, 4), (6, 5), (7, 4), (7, 5))'),
            Move(REMOVE_POSS, 6, (6, 4),
                 'Cell (6, 4) had possibility value of 6 removed because there was a hidden subset of size 4 (2, 4, 5, 8) in sector 7 at cells ((6, 4), (6, 5), (7, 4), (7, 5))'),
            Move(REMOVE_POSS, 6, (7, 4),
                 'Cell (7, 4) had possibility value of 6 removed because there was a hidden subset of size 4 (2, 4, 5, 8) in sector 7 at cells ((6, 4), (6, 5), (7, 4), (7, 5))')
        ]

        hidden_subset_sector_expected_board = [[8, 1, 6, 5, 7, 3, 2, 9, 4], [3, 9, 2, 0, 0, 0, 0, 0, 0],
                                               [4, 5, 7, 2, 0, 9, 0, 0, 6], [9, 4, 1, 0, 0, 0, 5, 6, 8],
                                               [7, 8, 5, 4, 9, 6, 1, 2, 3], [6, 2, 3, 8, 0, 0, 0, 4, 0],
                                               [2, 7, 9, 0, 0, 0, 0, 0, 1], [1, 3, 8, 0, 0, 0, 0, 7, 0],
                                               [5, 6, 4, 0, 0, 0, 0, 8, 2]]

        hidden_subset_sector_expected_poss = {(0, 0): [], (0, 1): [], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [],
                                              (0, 6): [], (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [], (1, 2): [],
                                              (1, 3): [1, 6], (1, 4): [1, 4, 6, 8], (1, 5): [1, 4, 8], (1, 6): [7, 8],
                                              (1, 7): [1, 5], (1, 8): [5, 7], (2, 0): [], (2, 1): [], (2, 2): [],
                                              (2, 3): [], (2, 4): [1, 8], (2, 5): [], (2, 6): [3, 8], (2, 7): [1, 3],
                                              (2, 8): [], (3, 0): [], (3, 1): [], (3, 2): [], (3, 3): [3, 7],
                                              (3, 4): [2, 3], (3, 5): [2, 7], (3, 6): [], (3, 7): [], (3, 8): [],
                                              (4, 0): [], (4, 1): [], (4, 2): [], (4, 3): [], (4, 4): [], (4, 5): [],
                                              (4, 6): [], (4, 7): [], (4, 8): [], (5, 0): [], (5, 1): [], (5, 2): [],
                                              (5, 3): [], (5, 4): [1, 5], (5, 5): [1, 5], (5, 6): [7, 9], (5, 7): [],
                                              (5, 8): [7, 9], (6, 0): [], (6, 1): [], (6, 2): [], (6, 3): [3, 6],
                                              (6, 4): [4, 5, 8], (6, 5): [4, 5, 8], (6, 6): [4, 6], (6, 7): [3, 5],
                                              (6, 8): [], (7, 0): [], (7, 1): [], (7, 2): [], (7, 3): [6, 9],
                                              (7, 4): [2, 4, 5], (7, 5): [2, 4, 5], (7, 6): [4, 6], (7, 7): [],
                                              (7, 8): [5, 9], (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [1, 3, 7, 9],
                                              (8, 4): [1, 3], (8, 5): [1, 7], (8, 6): [3, 9], (8, 7): [], (8, 8): []}

        self.assertEqual(hidden_subset_sector.board, hidden_subset_sector_expected_board)
        self.assertEqual(hidden_subset_sector.possible_values, hidden_subset_sector_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.hidden_subset()
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_x_wing(self):
        x_wing = SudokuBoard(
            [7, 0, 6, 2, 3, 9, 0, 1, 4, 1, 0, 2, 6, 0, 4, 7, 0, 3, 0, 4, 3, 0, 7, 1, 0, 2, 0,
             0, 2, 0, 3, 6, 7, 1, 4, 9, 6, 3, 9, 1, 4, 5, 0, 7, 0, 4, 1, 7, 9, 2, 8, 3, 6, 5,
             0, 7, 1, 4, 9, 3, 0, 8, 0, 3, 0, 4, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 4, 3, 7]
        )

        x_wing.set_poss_values(
            {(0, 0): [], (0, 1): [5, 8], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [], (0, 6): [5, 8], (0, 7): [],
             (0, 8): [], (1, 0): [], (1, 1): [5, 8, 9], (1, 2): [], (1, 3): [], (1, 4): [5, 8], (1, 5): [], (1, 6): [],
             (1, 7): [5, 9], (1, 8): [], (2, 0): [5, 8, 9], (2, 1): [], (2, 2): [], (2, 3): [5, 8], (2, 4): [],
             (2, 5): [], (2, 6): [5, 6, 8, 9], (2, 7): [], (2, 8): [6, 8], (3, 0): [5, 8], (3, 1): [], (3, 2): [5, 8],
             (3, 3): [], (3, 4): [], (3, 5): [], (3, 6): [], (3, 7): [], (3, 8): [], (4, 0): [], (4, 1): [], (4, 2): [],
             (4, 3): [], (4, 4): [], (4, 5): [], (4, 6): [2, 8], (4, 7): [], (4, 8): [2, 8], (5, 0): [], (5, 1): [],
             (5, 2): [], (5, 3): [], (5, 4): [], (5, 5): [], (5, 6): [], (5, 7): [], (5, 8): [], (6, 0): [2, 5],
             (6, 1): [], (6, 2): [], (6, 3): [], (6, 4): [], (6, 5): [], (6, 6): [2, 5, 6], (6, 7): [], (6, 8): [2, 6],
             (7, 0): [], (7, 1): [5, 6, 8], (7, 2): [], (7, 3): [], (7, 4): [5, 8], (7, 5): [2, 6], (7, 6): [2, 5, 9],
             (7, 7): [5, 9], (7, 8): [], (8, 0): [2, 9], (8, 1): [6, 9], (8, 2): [5, 8], (8, 3): [5, 8], (8, 4): [],
             (8, 5): [2, 6], (8, 6): [], (8, 7): [], (8, 8): []})

        actual_moves = x_wing.x_wing()

        expected_moves = [
            Move(REMOVE_POSS, 5, (1, 1),
                 'Row 1 had possibility value of 5 removed because there was an x-wing interaction between cells [(1, 4), (1, 7), (7, 4), (7, 7)]'),
            Move(REMOVE_POSS, 5, (7, 1),
                 'Row 7 had possibility value of 5 removed because there was an x-wing interaction between cells [(1, 4), (1, 7), (7, 4), (7, 7)]'),
            Move(REMOVE_POSS, 5, (7, 6),
                 'Row 7 had possibility value of 5 removed because there was an x-wing interaction between cells [(1, 4), (1, 7), (7, 4), (7, 7)]'),
            Move(REMOVE_POSS, 8, (0, 1),
                 'Column 1 had possibility value of 8 removed because there was an x-wing interaction between cells [(7, 1), (7, 4), (1, 1), (1, 4)]')
        ]

        x_wing_expected_board = [[7, 0, 6, 2, 3, 9, 0, 1, 4], [1, 0, 2, 6, 0, 4, 7, 0, 3], [0, 4, 3, 0, 7, 1, 0, 2, 0],
                                 [0, 2, 0, 3, 6, 7, 1, 4, 9], [6, 3, 9, 1, 4, 5, 0, 7, 0], [4, 1, 7, 9, 2, 8, 3, 6, 5],
                                 [0, 7, 1, 4, 9, 3, 0, 8, 0], [3, 0, 4, 7, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 4, 3, 7]]

        x_wing_expected_poss = {(0, 0): [], (0, 1): [5], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [], (0, 6): [5, 8],
                                (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [8, 9], (1, 2): [], (1, 3): [],
                                (1, 4): [5, 8], (1, 5): [], (1, 6): [], (1, 7): [5, 9], (1, 8): [], (2, 0): [5, 8, 9],
                                (2, 1): [], (2, 2): [], (2, 3): [5, 8], (2, 4): [], (2, 5): [], (2, 6): [5, 6, 8, 9],
                                (2, 7): [], (2, 8): [6, 8], (3, 0): [5, 8], (3, 1): [], (3, 2): [5, 8], (3, 3): [],
                                (3, 4): [], (3, 5): [], (3, 6): [], (3, 7): [], (3, 8): [], (4, 0): [], (4, 1): [],
                                (4, 2): [], (4, 3): [], (4, 4): [], (4, 5): [], (4, 6): [2, 8], (4, 7): [],
                                (4, 8): [2, 8], (5, 0): [], (5, 1): [], (5, 2): [], (5, 3): [], (5, 4): [], (5, 5): [],
                                (5, 6): [], (5, 7): [], (5, 8): [], (6, 0): [2, 5], (6, 1): [], (6, 2): [], (6, 3): [],
                                (6, 4): [], (6, 5): [], (6, 6): [2, 5, 6], (6, 7): [], (6, 8): [2, 6], (7, 0): [],
                                (7, 1): [6, 8], (7, 2): [], (7, 3): [], (7, 4): [5, 8], (7, 5): [2, 6], (7, 6): [2, 9],
                                (7, 7): [5, 9], (7, 8): [], (8, 0): [2, 9], (8, 1): [6, 9], (8, 2): [5, 8],
                                (8, 3): [5, 8], (8, 4): [], (8, 5): [2, 6], (8, 6): [], (8, 7): [], (8, 8): []}

        self.assertEqual(x_wing.board, x_wing_expected_board)
        self.assertEqual(x_wing.possible_values, x_wing_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.x_wing()
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_swordfish_row(self):
        swordfish_row = SudokuBoard(
            [0, 0, 8, 0, 9, 0, 1, 4, 5, 5, 3, 1, 6, 4, 0, 0, 0, 0, 4, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
             0, 5, 3, 0, 1, 0, 6, 0, 4, 0, 0, 0, 4, 0, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 4, 2, 0,
             8, 7, 9, 2, 6, 4, 3, 5, 1])

        swordfish_row.set_poss_values(
            {(0, 0): [2, 6, 7], (0, 1): [2, 6], (0, 2): [], (0, 3): [3, 7], (0, 4): [], (0, 5): [2, 3], (0, 6): [],
             (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [], (1, 4): [], (1, 5): [2, 8],
             (1, 6): [2, 7, 8, 9], (1, 7): [7, 8, 9], (1, 8): [2, 8, 9], (2, 0): [], (2, 1): [], (2, 2): [2, 7],
             (2, 3): [1, 5, 7, 8], (2, 4): [2, 5, 7, 8], (2, 5): [1, 2, 8], (2, 6): [2, 8], (2, 7): [3, 6],
             (2, 8): [3, 6], (3, 0): [1, 2, 6, 7, 9], (3, 1): [1, 2, 4, 6, 8], (3, 2): [4, 6], (3, 3): [3, 7, 8, 9],
             (3, 4): [2, 3, 7, 8], (3, 5): [], (3, 6): [2, 7, 8, 9], (3, 7): [1, 3, 7, 8, 9], (3, 8): [2, 3, 8, 9],
             (4, 0): [2, 7, 9], (4, 1): [], (4, 2): [], (4, 3): [7, 8, 9], (4, 4): [], (4, 5): [2, 8, 9], (4, 6): [],
             (4, 7): [7, 8, 9], (4, 8): [], (5, 0): [1, 2, 7, 9], (5, 1): [1, 2, 8], (5, 2): [2, 7], (5, 3): [],
             (5, 4): [2, 3, 7, 8], (5, 5): [], (5, 6): [], (5, 7): [1, 3, 7, 8, 9], (5, 8): [2, 3, 8, 9],
             (6, 0): [1, 2, 3, 6], (6, 1): [1, 2, 4, 6], (6, 2): [4, 5, 6], (6, 3): [1, 3, 5, 8, 9], (6, 4): [3, 5, 8],
             (6, 5): [1, 3, 8, 9], (6, 6): [8, 9], (6, 7): [6, 8, 9], (6, 8): [], (7, 0): [1, 3, 6], (7, 1): [1, 6],
             (7, 2): [5, 6], (7, 3): [1, 3, 5, 8, 9], (7, 4): [3, 5, 8], (7, 5): [], (7, 6): [], (7, 7): [],
             (7, 8): [6, 8, 9], (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [], (8, 6): [],
             (8, 7): [], (8, 8): []}
        )

        actual_moves = swordfish_row.swordfish_generic(swordfish_row.get_row_possibilities,
                                                       swordfish_row.eliminate_possibilities_from_column_swordfish)

        expected_moves = [
            Move(REMOVE_POSS, 2, (3, 0),
                 'Column 0 (3, 0) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (5, 0),
                 'Column 0 (5, 0) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (3, 1),
                 'Column 1 (3, 1) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (5, 1),
                 'Column 1 (5, 1) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (1, 5),
                 'Column 5 (1, 5) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (2, 5),
                 'Column 5 (2, 5) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)')
        ]

        swordfish_row_expected_board = [[0, 0, 8, 0, 9, 0, 1, 4, 5], [5, 3, 1, 6, 4, 0, 0, 0, 0],
                                        [4, 9, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0],
                                        [0, 5, 3, 0, 1, 0, 6, 0, 4], [0, 0, 0, 4, 0, 6, 5, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 7, 4, 2, 0],
                                        [8, 7, 9, 2, 6, 4, 3, 5, 1]]

        swordfish_row_expected_poss = {(0, 0): [2, 6, 7], (0, 1): [2, 6], (0, 2): [], (0, 3): [3, 7], (0, 4): [],
                                       (0, 5): [2, 3], (0, 6): [], (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [],
                                       (1, 2): [], (1, 3): [], (1, 4): [], (1, 5): [8], (1, 6): [2, 7, 8, 9],
                                       (1, 7): [7, 8, 9], (1, 8): [2, 8, 9], (2, 0): [], (2, 1): [], (2, 2): [2, 7],
                                       (2, 3): [1, 5, 7, 8], (2, 4): [2, 5, 7, 8], (2, 5): [1, 8], (2, 6): [2, 8],
                                       (2, 7): [3, 6], (2, 8): [3, 6], (3, 0): [1, 6, 7, 9], (3, 1): [1, 4, 6, 8],
                                       (3, 2): [4, 6], (3, 3): [3, 7, 8, 9], (3, 4): [2, 3, 7, 8], (3, 5): [],
                                       (3, 6): [2, 7, 8, 9], (3, 7): [1, 3, 7, 8, 9], (3, 8): [2, 3, 8, 9],
                                       (4, 0): [2, 7, 9], (4, 1): [], (4, 2): [], (4, 3): [7, 8, 9], (4, 4): [],
                                       (4, 5): [2, 8, 9], (4, 6): [], (4, 7): [7, 8, 9], (4, 8): [], (5, 0): [1, 7, 9],
                                       (5, 1): [1, 8], (5, 2): [2, 7], (5, 3): [], (5, 4): [2, 3, 7, 8], (5, 5): [],
                                       (5, 6): [], (5, 7): [1, 3, 7, 8, 9], (5, 8): [2, 3, 8, 9], (6, 0): [1, 2, 3, 6],
                                       (6, 1): [1, 2, 4, 6], (6, 2): [4, 5, 6], (6, 3): [1, 3, 5, 8, 9],
                                       (6, 4): [3, 5, 8], (6, 5): [1, 3, 8, 9], (6, 6): [8, 9], (6, 7): [6, 8, 9],
                                       (6, 8): [], (7, 0): [1, 3, 6], (7, 1): [1, 6], (7, 2): [5, 6],
                                       (7, 3): [1, 3, 5, 8, 9], (7, 4): [3, 5, 8], (7, 5): [], (7, 6): [], (7, 7): [],
                                       (7, 8): [6, 8, 9], (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [], (8, 4): [],
                                       (8, 5): [], (8, 6): [], (8, 7): [], (8, 8): []}

        self.assertEqual(swordfish_row.board, swordfish_row_expected_board)
        self.assertEqual(swordfish_row.possible_values, swordfish_row_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.swordfish_generic(swordfish_row.get_row_possibilities,
                                                          swordfish_row.eliminate_possibilities_from_column_swordfish)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_swordfish_col(self):
        swordfish_column = SudokuBoard(
            [0, 0, 0, 4, 7, 9, 6, 2, 0, 0, 0, 4, 0, 0, 0, 3, 9, 5, 9, 2, 6, 0, 0, 0, 0, 0, 0,
             0, 3, 1, 0, 0, 0, 0, 6, 9, 0, 0, 0, 9, 3, 6, 0, 0, 0, 0, 0, 9, 0, 0, 0, 2, 8, 3,
             0, 5, 0, 8, 9, 4, 7, 1, 6, 4, 0, 8, 0, 0, 0, 9, 5, 2, 0, 9, 7, 0, 5, 2, 0, 3, 0]
        )

        swordfish_column.set_poss_values(
            {(0, 0): [3, 5], (0, 1): [1, 8], (0, 2): [3, 5], (0, 3): [], (0, 4): [], (0, 5): [], (0, 6): [], (0, 7): [],
             (0, 8): [1, 8], (1, 0): [1, 7, 8], (1, 1): [1, 7, 8], (1, 2): [], (1, 3): [2, 6], (1, 4): [2, 6],
             (1, 5): [1, 8], (1, 6): [], (1, 7): [], (1, 8): [], (2, 0): [], (2, 1): [], (2, 2): [], (2, 3): [3, 5],
             (2, 4): [1, 8], (2, 5): [3, 5], (2, 6): [1, 4, 8], (2, 7): [4, 7], (2, 8): [1, 4, 7, 8], (3, 0): [5, 7],
             (3, 1): [], (3, 2): [], (3, 3): [2, 5, 7], (3, 4): [2, 4, 8], (3, 5): [5, 7, 8], (3, 6): [4, 5],
             (3, 7): [], (3, 8): [], (4, 0): [2, 5, 8], (4, 1): [4, 8], (4, 2): [2, 5], (4, 3): [], (4, 4): [],
             (4, 5): [], (4, 6): [1, 4, 5], (4, 7): [4, 7], (4, 8): [1, 4, 7], (5, 0): [5, 6, 7], (5, 1): [4, 6, 7],
             (5, 2): [], (5, 3): [1, 5, 7], (5, 4): [1, 4], (5, 5): [1, 5, 7], (5, 6): [], (5, 7): [], (5, 8): [],
             (6, 0): [2, 3], (6, 1): [], (6, 2): [2, 3], (6, 3): [], (6, 4): [], (6, 5): [], (6, 6): [], (6, 7): [],
             (6, 8): [], (7, 0): [], (7, 1): [1, 6], (7, 2): [], (7, 3): [3, 7], (7, 4): [1, 6], (7, 5): [3, 7],
             (7, 6): [], (7, 7): [], (7, 8): [], (8, 0): [1, 6], (8, 1): [], (8, 2): [], (8, 3): [1, 6], (8, 4): [],
             (8, 5): [], (8, 6): [4, 8], (8, 7): [], (8, 8): [4, 8]}

        )

        actual_moves = swordfish_column.swordfish_generic(swordfish_column.get_col_possibilities,
                                                          swordfish_column.eliminate_possibilities_from_row_swordfish)

        expected_moves = [
            Move(REMOVE_POSS, 1, (1, 1),
                 'Row 1 (1, 1) had possibility value of 1 removed because there was a swordfish interaction between columns (0, 3, 5)'),
            Move(REMOVE_POSS, 1, (5, 4),
                 'Row 5 (5, 4) had possibility value of 1 removed because there was a swordfish interaction between columns (0, 3, 5)')
        ]

        swordfish_row_expected_board = [[0, 0, 0, 4, 7, 9, 6, 2, 0], [0, 0, 4, 0, 0, 0, 3, 9, 5],
                                        [9, 2, 6, 0, 0, 0, 0, 0, 0], [0, 3, 1, 0, 0, 0, 0, 6, 9],
                                        [0, 0, 0, 9, 3, 6, 0, 0, 0], [0, 0, 9, 0, 0, 0, 2, 8, 3],
                                        [0, 5, 0, 8, 9, 4, 7, 1, 6], [4, 0, 8, 0, 0, 0, 9, 5, 2],
                                        [0, 9, 7, 0, 5, 2, 0, 3, 0]]

        swordfish_row_expected_poss = {(0, 0): [3, 5], (0, 1): [1, 8], (0, 2): [3, 5], (0, 3): [], (0, 4): [],
                                       (0, 5): [], (0, 6): [], (0, 7): [], (0, 8): [1, 8], (1, 0): [1, 7, 8],
                                       (1, 1): [7, 8], (1, 2): [], (1, 3): [2, 6], (1, 4): [2, 6], (1, 5): [1, 8],
                                       (1, 6): [], (1, 7): [], (1, 8): [], (2, 0): [], (2, 1): [], (2, 2): [],
                                       (2, 3): [3, 5], (2, 4): [1, 8], (2, 5): [3, 5], (2, 6): [1, 4, 8],
                                       (2, 7): [4, 7], (2, 8): [1, 4, 7, 8], (3, 0): [5, 7], (3, 1): [], (3, 2): [],
                                       (3, 3): [2, 5, 7], (3, 4): [2, 4, 8], (3, 5): [5, 7, 8], (3, 6): [4, 5],
                                       (3, 7): [], (3, 8): [], (4, 0): [2, 5, 8], (4, 1): [4, 8], (4, 2): [2, 5],
                                       (4, 3): [], (4, 4): [], (4, 5): [], (4, 6): [1, 4, 5], (4, 7): [4, 7],
                                       (4, 8): [1, 4, 7], (5, 0): [5, 6, 7], (5, 1): [4, 6, 7], (5, 2): [],
                                       (5, 3): [1, 5, 7], (5, 4): [4], (5, 5): [1, 5, 7], (5, 6): [], (5, 7): [],
                                       (5, 8): [], (6, 0): [2, 3], (6, 1): [], (6, 2): [2, 3], (6, 3): [], (6, 4): [],
                                       (6, 5): [], (6, 6): [], (6, 7): [], (6, 8): [], (7, 0): [], (7, 1): [1, 6],
                                       (7, 2): [], (7, 3): [3, 7], (7, 4): [1, 6], (7, 5): [3, 7], (7, 6): [],
                                       (7, 7): [], (7, 8): [], (8, 0): [1, 6], (8, 1): [], (8, 2): [], (8, 3): [1, 6],
                                       (8, 4): [], (8, 5): [], (8, 6): [4, 8], (8, 7): [], (8, 8): [4, 8]}

        self.assertEqual(swordfish_column.board, swordfish_row_expected_board)
        self.assertEqual(swordfish_column.possible_values, swordfish_row_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.swordfish_generic(swordfish_column.get_row_possibilities,
                                                          swordfish_column.eliminate_possibilities_from_column_swordfish)
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_swordfish(self):
        swordfish_row = SudokuBoard(
            [0, 0, 8, 0, 9, 0, 1, 4, 5, 5, 3, 1, 6, 4, 0, 0, 0, 0, 4, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
             0, 5, 3, 0, 1, 0, 6, 0, 4, 0, 0, 0, 4, 0, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 4, 2, 0,
             8, 7, 9, 2, 6, 4, 3, 5, 1])

        swordfish_row.set_poss_values(
            {(0, 0): [2, 6, 7], (0, 1): [2, 6], (0, 2): [], (0, 3): [3, 7], (0, 4): [], (0, 5): [2, 3], (0, 6): [],
             (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [], (1, 4): [], (1, 5): [2, 8],
             (1, 6): [2, 7, 8, 9], (1, 7): [7, 8, 9], (1, 8): [2, 8, 9], (2, 0): [], (2, 1): [], (2, 2): [2, 7],
             (2, 3): [1, 5, 7, 8], (2, 4): [2, 5, 7, 8], (2, 5): [1, 2, 8], (2, 6): [2, 8], (2, 7): [3, 6],
             (2, 8): [3, 6], (3, 0): [1, 2, 6, 7, 9], (3, 1): [1, 2, 4, 6, 8], (3, 2): [4, 6], (3, 3): [3, 7, 8, 9],
             (3, 4): [2, 3, 7, 8], (3, 5): [], (3, 6): [2, 7, 8, 9], (3, 7): [1, 3, 7, 8, 9], (3, 8): [2, 3, 8, 9],
             (4, 0): [2, 7, 9], (4, 1): [], (4, 2): [], (4, 3): [7, 8, 9], (4, 4): [], (4, 5): [2, 8, 9], (4, 6): [],
             (4, 7): [7, 8, 9], (4, 8): [], (5, 0): [1, 2, 7, 9], (5, 1): [1, 2, 8], (5, 2): [2, 7], (5, 3): [],
             (5, 4): [2, 3, 7, 8], (5, 5): [], (5, 6): [], (5, 7): [1, 3, 7, 8, 9], (5, 8): [2, 3, 8, 9],
             (6, 0): [1, 2, 3, 6], (6, 1): [1, 2, 4, 6], (6, 2): [4, 5, 6], (6, 3): [1, 3, 5, 8, 9], (6, 4): [3, 5, 8],
             (6, 5): [1, 3, 8, 9], (6, 6): [8, 9], (6, 7): [6, 8, 9], (6, 8): [], (7, 0): [1, 3, 6], (7, 1): [1, 6],
             (7, 2): [5, 6], (7, 3): [1, 3, 5, 8, 9], (7, 4): [3, 5, 8], (7, 5): [], (7, 6): [], (7, 7): [],
             (7, 8): [6, 8, 9], (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [], (8, 4): [], (8, 5): [], (8, 6): [],
             (8, 7): [], (8, 8): []}
        )

        actual_moves = swordfish_row.swordfish()

        expected_moves = [
            Move(REMOVE_POSS, 2, (3, 0),
                 'Column 0 (3, 0) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (5, 0),
                 'Column 0 (5, 0) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (3, 1),
                 'Column 1 (3, 1) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (5, 1),
                 'Column 1 (5, 1) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (1, 5),
                 'Column 5 (1, 5) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)'),
            Move(REMOVE_POSS, 2, (2, 5),
                 'Column 5 (2, 5) had possibility value of 2 removed because there was a swordfish interaction between rows (0, 4, 6)')
        ]

        swordfish_row_expected_board = [[0, 0, 8, 0, 9, 0, 1, 4, 5], [5, 3, 1, 6, 4, 0, 0, 0, 0],
                                        [4, 9, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0, 0],
                                        [0, 5, 3, 0, 1, 0, 6, 0, 4], [0, 0, 0, 4, 0, 6, 5, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 7, 4, 2, 0],
                                        [8, 7, 9, 2, 6, 4, 3, 5, 1]]

        swordfish_row_expected_poss = {(0, 0): [2, 6, 7], (0, 1): [2, 6], (0, 2): [], (0, 3): [3, 7], (0, 4): [],
                                       (0, 5): [2, 3], (0, 6): [], (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [],
                                       (1, 2): [], (1, 3): [], (1, 4): [], (1, 5): [8], (1, 6): [2, 7, 8, 9],
                                       (1, 7): [7, 8, 9], (1, 8): [2, 8, 9], (2, 0): [], (2, 1): [], (2, 2): [2, 7],
                                       (2, 3): [1, 5, 7, 8], (2, 4): [2, 5, 7, 8], (2, 5): [1, 8], (2, 6): [2, 8],
                                       (2, 7): [3, 6], (2, 8): [3, 6], (3, 0): [1, 6, 7, 9], (3, 1): [1, 4, 6, 8],
                                       (3, 2): [4, 6], (3, 3): [3, 7, 8, 9], (3, 4): [2, 3, 7, 8], (3, 5): [],
                                       (3, 6): [2, 7, 8, 9], (3, 7): [1, 3, 7, 8, 9], (3, 8): [2, 3, 8, 9],
                                       (4, 0): [2, 7, 9], (4, 1): [], (4, 2): [], (4, 3): [7, 8, 9], (4, 4): [],
                                       (4, 5): [2, 8, 9], (4, 6): [], (4, 7): [7, 8, 9], (4, 8): [], (5, 0): [1, 7, 9],
                                       (5, 1): [1, 8], (5, 2): [2, 7], (5, 3): [], (5, 4): [2, 3, 7, 8], (5, 5): [],
                                       (5, 6): [], (5, 7): [1, 3, 7, 8, 9], (5, 8): [2, 3, 8, 9], (6, 0): [1, 2, 3, 6],
                                       (6, 1): [1, 2, 4, 6], (6, 2): [4, 5, 6], (6, 3): [1, 3, 5, 8, 9],
                                       (6, 4): [3, 5, 8], (6, 5): [1, 3, 8, 9], (6, 6): [8, 9], (6, 7): [6, 8, 9],
                                       (6, 8): [], (7, 0): [1, 3, 6], (7, 1): [1, 6], (7, 2): [5, 6],
                                       (7, 3): [1, 3, 5, 8, 9], (7, 4): [3, 5, 8], (7, 5): [], (7, 6): [], (7, 7): [],
                                       (7, 8): [6, 8, 9], (8, 0): [], (8, 1): [], (8, 2): [], (8, 3): [], (8, 4): [],
                                       (8, 5): [], (8, 6): [], (8, 7): [], (8, 8): []}

        self.assertEqual(swordfish_row.board, swordfish_row_expected_board)
        self.assertEqual(swordfish_row.possible_values, swordfish_row_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        swordfish_column = SudokuBoard(
            [0, 0, 0, 4, 7, 9, 6, 2, 0, 0, 0, 4, 0, 0, 0, 3, 9, 5, 9, 2, 6, 0, 0, 0, 0, 0, 0,
             0, 3, 1, 0, 0, 0, 0, 6, 9, 0, 0, 0, 9, 3, 6, 0, 0, 0, 0, 0, 9, 0, 0, 0, 2, 8, 3,
             0, 5, 0, 8, 9, 4, 7, 1, 6, 4, 0, 8, 0, 0, 0, 9, 5, 2, 0, 9, 7, 0, 5, 2, 0, 3, 0]
        )

        swordfish_column.set_poss_values(
            {(0, 0): [3, 5], (0, 1): [1, 8], (0, 2): [3, 5], (0, 3): [], (0, 4): [], (0, 5): [], (0, 6): [], (0, 7): [],
             (0, 8): [1, 8], (1, 0): [1, 7, 8], (1, 1): [1, 7, 8], (1, 2): [], (1, 3): [2, 6], (1, 4): [2, 6],
             (1, 5): [1, 8], (1, 6): [], (1, 7): [], (1, 8): [], (2, 0): [], (2, 1): [], (2, 2): [], (2, 3): [3, 5],
             (2, 4): [1, 8], (2, 5): [3, 5], (2, 6): [1, 4, 8], (2, 7): [4, 7], (2, 8): [1, 4, 7, 8], (3, 0): [5, 7],
             (3, 1): [], (3, 2): [], (3, 3): [2, 5, 7], (3, 4): [2, 4, 8], (3, 5): [5, 7, 8], (3, 6): [4, 5],
             (3, 7): [], (3, 8): [], (4, 0): [2, 5, 8], (4, 1): [4, 8], (4, 2): [2, 5], (4, 3): [], (4, 4): [],
             (4, 5): [], (4, 6): [1, 4, 5], (4, 7): [4, 7], (4, 8): [1, 4, 7], (5, 0): [5, 6, 7], (5, 1): [4, 6, 7],
             (5, 2): [], (5, 3): [1, 5, 7], (5, 4): [1, 4], (5, 5): [1, 5, 7], (5, 6): [], (5, 7): [], (5, 8): [],
             (6, 0): [2, 3], (6, 1): [], (6, 2): [2, 3], (6, 3): [], (6, 4): [], (6, 5): [], (6, 6): [], (6, 7): [],
             (6, 8): [], (7, 0): [], (7, 1): [1, 6], (7, 2): [], (7, 3): [3, 7], (7, 4): [1, 6], (7, 5): [3, 7],
             (7, 6): [], (7, 7): [], (7, 8): [], (8, 0): [1, 6], (8, 1): [], (8, 2): [], (8, 3): [1, 6], (8, 4): [],
             (8, 5): [], (8, 6): [4, 8], (8, 7): [], (8, 8): [4, 8]}

        )

        actual_moves = swordfish_column.swordfish()

        expected_moves = [
            Move(REMOVE_POSS, 1, (1, 1),
                 'Row 1 (1, 1) had possibility value of 1 removed because there was a swordfish interaction between columns (0, 3, 5)'),
            Move(REMOVE_POSS, 1, (5, 4),
                 'Row 5 (5, 4) had possibility value of 1 removed because there was a swordfish interaction between columns (0, 3, 5)')
        ]

        swordfish_row_expected_board = [[0, 0, 0, 4, 7, 9, 6, 2, 0], [0, 0, 4, 0, 0, 0, 3, 9, 5],
                                        [9, 2, 6, 0, 0, 0, 0, 0, 0], [0, 3, 1, 0, 0, 0, 0, 6, 9],
                                        [0, 0, 0, 9, 3, 6, 0, 0, 0], [0, 0, 9, 0, 0, 0, 2, 8, 3],
                                        [0, 5, 0, 8, 9, 4, 7, 1, 6], [4, 0, 8, 0, 0, 0, 9, 5, 2],
                                        [0, 9, 7, 0, 5, 2, 0, 3, 0]]

        swordfish_row_expected_poss = {(0, 0): [3, 5], (0, 1): [1, 8], (0, 2): [3, 5], (0, 3): [], (0, 4): [],
                                       (0, 5): [], (0, 6): [], (0, 7): [], (0, 8): [1, 8], (1, 0): [1, 7, 8],
                                       (1, 1): [7, 8], (1, 2): [], (1, 3): [2, 6], (1, 4): [2, 6], (1, 5): [1, 8],
                                       (1, 6): [], (1, 7): [], (1, 8): [], (2, 0): [], (2, 1): [], (2, 2): [],
                                       (2, 3): [3, 5], (2, 4): [1, 8], (2, 5): [3, 5], (2, 6): [1, 4, 8],
                                       (2, 7): [4, 7], (2, 8): [1, 4, 7, 8], (3, 0): [5, 7], (3, 1): [], (3, 2): [],
                                       (3, 3): [2, 5, 7], (3, 4): [2, 4, 8], (3, 5): [5, 7, 8], (3, 6): [4, 5],
                                       (3, 7): [], (3, 8): [], (4, 0): [2, 5, 8], (4, 1): [4, 8], (4, 2): [2, 5],
                                       (4, 3): [], (4, 4): [], (4, 5): [], (4, 6): [1, 4, 5], (4, 7): [4, 7],
                                       (4, 8): [1, 4, 7], (5, 0): [5, 6, 7], (5, 1): [4, 6, 7], (5, 2): [],
                                       (5, 3): [1, 5, 7], (5, 4): [4], (5, 5): [1, 5, 7], (5, 6): [], (5, 7): [],
                                       (5, 8): [], (6, 0): [2, 3], (6, 1): [], (6, 2): [2, 3], (6, 3): [], (6, 4): [],
                                       (6, 5): [], (6, 6): [], (6, 7): [], (6, 8): [], (7, 0): [], (7, 1): [1, 6],
                                       (7, 2): [], (7, 3): [3, 7], (7, 4): [1, 6], (7, 5): [3, 7], (7, 6): [],
                                       (7, 7): [], (7, 8): [], (8, 0): [1, 6], (8, 1): [], (8, 2): [], (8, 3): [1, 6],
                                       (8, 4): [], (8, 5): [], (8, 6): [4, 8], (8, 7): [], (8, 8): [4, 8]}

        self.assertEqual(swordfish_column.board, swordfish_row_expected_board)
        self.assertEqual(swordfish_column.possible_values, swordfish_row_expected_poss)
        self.assertEqual(actual_moves, expected_moves)

        # trivial 0 move result
        blank_board_copy = deepcopy(self.blank_board.board)
        blank_board_poss_copy = deepcopy(self.blank_board.possible_values)

        actual_moves = self.blank_board.swordfish()
        self.assertEqual(actual_moves, [])
        self.assertEqual(self.blank_board.board, blank_board_copy)
        self.assertEqual(self.blank_board.possible_values, blank_board_poss_copy)

    def test_force_chain(self):
        force_chain = SudokuBoard(
            [5, 1, 2, 6, 3, 7, 4, 8, 9, 3, 6, 0, 8, 0, 0, 7, 2, 5, 7, 0, 8, 2, 0, 0, 1, 6, 3, 9, 5, 1, 3, 8, 4, 2, 7, 6,
             4, 2, 7, 5, 9, 6, 8, 3, 1, 8, 3, 6, 1, 7, 2, 9, 5, 4, 2, 7, 0, 9, 0, 0, 6, 4, 8, 1, 0, 0, 7, 6, 0, 5, 9, 2,
             6, 0, 0, 4, 2, 0, 3, 1, 7])

        actual_moves = force_chain.force_chain()
        expected_moves = [
            Move(REMOVE_POSS, 4, (1, 2),
                 '(1, 2) had possibility value of 4 removed due to trial and error. Invalid cell value of 5 cannot be set at (6, 4)')
        ]

        force_chain_expected_board = [[5, 1, 2, 6, 3, 7, 4, 8, 9], [3, 6, 9, 8, 4, 1, 7, 2, 5],
                                      [7, 4, 8, 2, 5, 9, 1, 6, 3], [9, 5, 1, 3, 8, 4, 2, 7, 6],
                                      [4, 2, 7, 5, 9, 6, 8, 3, 1], [8, 3, 6, 1, 7, 2, 9, 5, 4],
                                      [2, 7, 3, 9, 1, 5, 6, 4, 8], [1, 8, 4, 7, 6, 3, 5, 9, 2],
                                      [6, 9, 5, 4, 2, 8, 3, 1, 7]]

        self.assertEqual(actual_moves, expected_moves)
        self.assertTrue(force_chain.board, force_chain_expected_board)

    def test_solve(self):
        # pass
        for root, dirs, filenames in os.walk('TestCases'):
            for f in filenames:
                with self.subTest(file=f):
                    sudoku = SudokuBoard(file_path='TestCases/' + f, printout=False)
                    sudoku.solve()
                    self.assertTrue(sudoku.is_solved())
                    del sudoku
