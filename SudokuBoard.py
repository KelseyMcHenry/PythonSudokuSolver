from itertools import product
from itertools import chain


class SudokuBoard:
    """A data structure designed to hold sudoku data"""

    # -------------------------------------- Variable initialization -----------------------------------------------

    board = [[0 for _ in range(9)] for _ in range(9)]
    possible_values = {(i, j): [] for i, j in product(range(9), range(9))}

    # --------------------------------------------- Constructor  ---------------------------------------------------

    def __init__(self, values=[0]*81):
        """Initializes the board values and initializes the cell possibile values. Default is empty board"""
        for i, value in enumerate(values):
            self.board[i // 9][i % 9] = value
        for coordinate, possibilities in self.possible_values.items():
            for n in range(1, 10):
                if (self.board[coordinate[0]][coordinate[1]] == 0 and
                        (n not in self.board[coordinate[0]]) and
                        (n not in [self.board[i][coordinate[1]] for i in range(9)]) and
                        (n not in [self.board[i][j] for i, j in product(range(9), range(9))
                                   if self.sector_lookup(i, j) == self.sector_lookup(coordinate[0], coordinate[1])])):
                    self.possible_values[coordinate].append(n)

    # ------------------------------------------- Getters / Setters -------------------------------------------------

    def get(self, i, j):
        """
        Returns the value contained in cell (i , j), 0 if empty
        :param i: x coordinate. starts at 0, which is located far left
        :param j: y coordinate. starts at 0, which is located at the top
        :return: value contained in cell (i , j), 0 if empty
        """
        return self.board[i][j]

    def row(self, i):
        """
        Returns a list of values contained in row i, empty cells are indicated by a 0
        :param i: row index. starts at 0, which is located at the top
        :return: list of values contained in row i, empty cells are indicated by a 0
        """
        return self.board[i]

    def column(self, j):
        """
        Returns a list of values contained in column j, empty cells are indicated by a 0
        :param j: column index. starts at 0, which is located at the far left
        :return: list of values contained in column j, empty cells are indicated by a 0
        """
        return [self.board[i][j] for i in range(9)]

    @staticmethod
    def sector_lookup(i, j):
        """Returns sector index of a cell based on its i,j coordinates
        :param i: x coordinate. starts at 0, which is located far left
        :param j: y coordinate. starts at 0, which is located at the top
        :return: sector index of cell i,j. Sector indeces start at 0 and go left to right, top to bottom.
        """
        return ((i // 3) * 3) + (j // 3)

    def sector(self, sector):
        """
        :param sector: index of the sector, found using sector_lookup(i, j)
        :return list of values contained in sector, empty cells are indicated by a 0
        """
        return [self.board[i][j] for i, j in product(range(9), range(9)) if SudokuBoard.sector_lookup(i, j) == sector]

    def get_possibilities(self, i, j):
        """
        Returns a list of all possible values cell i,j could contain at time of execution
        :param i: x coordinate. starts at 0, which is located far left
        :param j: y coordinate. starts at 0, which is located at the top
        :return: list of all possible values cell i,j could contain at time of execution
        """
        return self.possible_values[(i, j)]

    def get_row_possibilities(self, i):
        """
        Returns a dictionary of all possible values the cells in row i could contain at time of execution
        :param i: row index. starts at 0, which is located at the top
        :return dictionary of all possible values the cells in row i could contain at time of execution
                 Keys: Tuples (i, j) for each cell
                 Values: Lists containing all possible values cell i,j could contain at time of execution
        """
        return {(i, j): self.possible_values[(i, j)] for j in range(9)}

    def get_col_possibilities(self, j):
        """
        Returns a dictionary of all possible values the cells in column j could contain at time of execution
        :param j: column index. starts at 0, which is located at the far left
        :return dictionary of all possible values the cells in column j could contain at time of execution
                 Keys: Tuples (i, j) for each cell
                 Values: Lists containing all possible values cell i,j could contain at time of execution
        """
        return {(i, j): self.possible_values[(i, j)] for i in range(9)}

    def get_sector_possibilities(self, sector):
        """
        Returns a dictionary of all possible values the cells in sector could contain at time of execution
        :param sector: index of the sector, found using sector_lookup(i, j)
        :return dictionary of all possible values the cells in sector s could contain at time of execution
                Keys: Tuples (i, j) for each cell
                Values: Lists containing all possible values cell i,j could contain at time of execution
        """
        return {(i, j): self.possible_values[(i, j)] for i, j in product(range(9), range(9)) if self.sector_lookup(i, j) == sector}

    def set(self, i, j, value):
        """
        Sets the value at i,j and updates the possibilities dictionary
        :param i: x coordinate. starts at 0, which is located far left
        :param j: y coordinate. starts at 0, which is located at the top
        :param value: value to set
        """
        self.board[i][j] = value
        for x, y in product(range(9), range(9)):
            self.possible_values[(x, y)] = []
        for coordinate, possibilities in self.possible_values.items():
            for n in range(1, 10):
                if (self.board[coordinate[0]][coordinate[1]] == 0 and
                        (n not in self.row(coordinate[0])) and
                        (n not in self.column(coordinate[1])) and
                        (n not in self.sector(self.sector_lookup(coordinate[0], coordinate[1])))):
                    self.possible_values[coordinate].append(n)

    # -------------------------------------- Solving Helper Functions -----------------------------------------------
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php

    def is_solved(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def sole_candidates(self):
        # does cell x contain only a single value? if so set it
        for coordinate, possibilities in self.possible_values.items():
            if len(possibilities) == 1:
                self.set(coordinate[0], coordinate[1], possibilities[0])

    def unique_candidate_rows(self):
        # does row i contain a unique value? if so set it
        for i in range(9):
            # accumulate all of the possibilities for all cells in row i
            row_i_total_poss = list(chain.from_iterable(self.get_row_possibilities(i).values()))
            # find all unique values in prior list
            unique_values_in_row_i = [n for n in row_i_total_poss if row_i_total_poss.count(n) == 1]

            for value in unique_values_in_row_i:
                for key, poss_list in self.get_row_possibilities(i).items():
                    if value in poss_list:
                        self.set(key[0], key[1], value)

    def unique_candidate_columns(self):
        # does column j contain a unique value? if so set it
        for j in range(9):
            # accumulate all of the possibilities for all cells in col j
            col_j_total_poss = list(chain.from_iterable(self.get_col_possibilities(j).values()))
            # find all unique values in prior list
            unique_values_in_col_j = [n for n in col_j_total_poss if col_j_total_poss.count(n) == 1]

            for value in unique_values_in_col_j:
                for key, poss_list in self.get_col_possibilities(j).items():
                    if value in poss_list:
                        self.set(key[0], key[1], value)

    def unique_candidate_sectors(self):
        # does sector s contain a unique value? if so set it
        for s in range(9):
            # accumulate all of the possibilities for all cells in sector s
            sector_s_total_poss = list(chain.from_iterable(self.get_sector_possibilities(s).values()))
            # find all unique values in prior list
            unique_values_in_sector_s = [n for n in sector_s_total_poss if sector_s_total_poss.count(n) == 1]

            for value in unique_values_in_sector_s:
                for key, poss_list in self.get_sector_possibilities(s).items():
                    if value in poss_list:
                        self.set(key[0], key[1], value)

    # TODO
    """"
    - https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    - block and column / row interaction
    - block / block interaction
    - naked subset
    - hidden subset
    - "X - Wing"
    - "Swordfish"
    - Forcing Chain
    """

    def solve(self):
        while not self.is_solved():
            self.sole_candidates()
            self.unique_candidate_columns()
            self.unique_candidate_rows()
            self.unique_candidate_sectors()










