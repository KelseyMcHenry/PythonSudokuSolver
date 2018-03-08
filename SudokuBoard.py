from itertools import product
from itertools import chain


class SudokuBoard:
    """A data structure designed to hold sudoku data"""

    # TODO define range(9)
    # TODO define product(range(9), range(9))
    # TODO use len instead of magic number 9 where possible
    # TODO make functions take functions as parameters (ie col, row, sector) to avoid repeating code
    # TODO create eliminate_possibility_from_row

    # -------------------------------------- Variable initialization -----------------------------------------------

    board = [[0 for _ in range(9)] for _ in range(9)]
    possible_values = {(i, j): [] for i, j in product(range(9), range(9))}
    coordinates_to_check = []
    file = open('reasons.txt', 'w')

    # --------------------------------------------- Constructor  ---------------------------------------------------

    def __init__(self, values=[0]*81, filepath=''):
        """
        Initializes the board values and initializes the cell possible values. Default is empty board
        http://www.sadmansoftware.com/sudoku/faq19.php
        """
        if filepath != '':
            values.clear()
            sudoku_file = open(filepath, 'r')
            for line in sudoku_file:
                for character in line:
                    if character == '.':
                        values.append(0)
                    elif character == '\n':
                        pass
                    else:
                        values.append(int(character))

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

    def __str__(self):
        print_value = ""
        for row in self.board:
            print_value += str(row) + '\n'
        print_value += '\n'
        for index, poss_list in self.possible_values.items():
            print_value += str(index) + ' : ' + str(poss_list) + '\n'
        return print_value

    def __eq__(self, other):
        for i, j in product(range(9), range(9)):
            if other.board[i][j] != self.board[i][j]:
                return False
        if self.possible_values != other.possible_values:
            return False
        return True
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
        return {(i, j): self.possible_values[(i, j)] for i, j in product(range(9), range(9))
                if self.sector_lookup(i, j) == sector}

    def get_sector_subrow_possibilities(self, sector, i):
        """
        Returns a subset of the possibilities equal to the intersection of sector and row i
        :param sector: index of the sector, found using sector_lookup(i, j)
        :param i: row index. starts at 0, which is located at the top
        :return: dictionary of all possible values the cells in sector s AND row i could contain at time of execution
                 Keys: Tuples (i, j) for each cell
                 Values: Lists containing all possible values cell i,j could contain at time of execution
        """
        # TODO error check to make sure i is a valid input
        sector_poss = self.get_sector_possibilities(sector)
        return {(row, col): sector_poss[(row, col)] for row, col in product(range(9), range(9))
                if row == i and self.sector_lookup(row, col) == sector}

    def set(self, i, j, value):
        """
        Sets the value at i,j and updates the possibilities dictionary
        :param i: x coordinate. starts at 0, which is located far left
        :param j: y coordinate. starts at 0, which is located at the top
        :param value: value to set
        """
        self.board[i][j] = value
        self.possible_values[(i, j)] = []
        for x, y in product(range(9), range(9)):
            if x == i or y == j or self.sector_lookup(x, y) == self.sector_lookup(i, j):
                if value in self.possible_values[(x, y)]:
                    self.possible_values[(x, y)].remove(value)
        for x, y in product(range(9), range(9)):
            if self.board[x][y] == 0 and len(self.get_possibilities(x, y)) == 0:
                raise ValueError('Invalid cell set at ' + str((x, y)))

    # ------------------------------------------- Solving Functions -------------------------------------------------
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    # http://www.sadmansoftware.com/sudoku/solvingtechniques.php

    def sole_candidates(self):
        """
        Solves the values of all cells that only have one possibility
        """
        success = 0
        for coordinate, possibilities in self.possible_values.items():
            if len(possibilities) == 1:
                success = 1
                value = possibilities.pop()
                self.set(coordinate[0], coordinate[1], value)
                self.print_reason_to_file('Cell ' + str(coordinate) + ' set to ' + str(value) +
                                          ' because it was the only possibility remaining for that cell.')

        return success

    def unique_candidate_rows(self):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its row
        """
        success = 0
        for i in range(9):
            # accumulate all of the possibilities for all cells in row i
            row_i_total_poss = list(chain.from_iterable(self.get_row_possibilities(i).values()))
            # find all unique values in prior list
            unique_values_in_row_i = [n for n in row_i_total_poss if row_i_total_poss.count(n) == 1]

            for value in unique_values_in_row_i:
                for key, poss_list in self.get_row_possibilities(i).items():
                    if value in poss_list:
                        success = 1
                        self.set(key[0], key[1], value)
                        self.print_reason_to_file('Cell ' + str(key) + ' set to ' + str(value) +
                                                  ' because the possibility was unique to row ' + str(i) + '.')
        return success

    def unique_candidate_columns(self):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its column
        """
        success = 0
        for j in range(9):
            # accumulate all of the possibilities for all cells in col j
            col_j_total_poss = list(chain.from_iterable(self.get_col_possibilities(j).values()))
            # find all unique values in prior list
            unique_values_in_col_j = [n for n in col_j_total_poss if col_j_total_poss.count(n) == 1]

            for value in unique_values_in_col_j:
                for key, poss_list in self.get_col_possibilities(j).items():
                    if value in poss_list:
                        success = 1
                        self.set(key[0], key[1], value)
                        self.print_reason_to_file('Cell ' + str(key) + ' set to ' + str(value) +
                                                  ' because the possibility was unique to column ' + str(j) + '.')
        return success

    def unique_candidate_sectors(self):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its sector
        """
        success = 0
        for s in range(9):
            # accumulate all of the possibilities for all cells in sector s
            sector_s_total_poss = list(chain.from_iterable(self.get_sector_possibilities(s).values()))
            # find all unique values in prior list
            unique_values_in_sector_s = [n for n in sector_s_total_poss if sector_s_total_poss.count(n) == 1]

            for value in unique_values_in_sector_s:
                for key, poss_list in self.get_sector_possibilities(s).items():
                    if value in poss_list:
                        success = 1
                        self.set(key[0], key[1], value)
                        self.print_reason_to_file('Cell ' + str(key) + ' set to ' + str(value) +
                                                  ' because the possibility was unique to sector ' + str(s) + '.')
        return success

    # --------------------------------- Possibility Eliminating Functions -----------------------------------------
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    # http://www.sadmansoftware.com/sudoku/solvingtechniques.php

    def sector_row_interaction(self):
        """
        Eliminates possibilities within a row outside of a sector if a possibility is unique to row within said sector
        """
        success = 0
        for sector in range(9):
            row_indices_in_sector = []
            for i, j in product(range(9), range(9)):
                if self.sector_lookup(i, j) == sector:
                    row_indices_in_sector.append(i)
            row_indices_in_sector = list(set(row_indices_in_sector))

            list_1 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[0])
            list_2 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[1])
            list_3 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[2])
            for n in range(1, 10):
                unique_index = self.unique_to_only_one(n, list_1, list_2, list_3)
                if unique_index >= 0:
                    for i, j in product(range(9), range(9)):
                        if i == row_indices_in_sector[unique_index] and self.sector_lookup(i, j) != sector:
                            success = 1
                            self.possible_values[(i, j)].remove(n)
                            self.print_reason_to_file('Cell (' + str(i) + ', ' + str(j) + ') had possibility value of '
                                                      + str(n) + ' removed because sector '
                                                      + str(sector) + ' must contain it via a row interaction.')
        return success

    def sector_column_interaction(self):
        """
        Eliminates possibilities within a column outside of a sector if a possibility is unique to column within said sector
        """
        success = 0
        for sector in range(9):
            column_indices_in_sector = []
            for i, j in product(range(9), range(9)):
                if self.sector_lookup(i, j) == sector:
                    column_indices_in_sector.append(i)
            column_indices_in_sector = list(set(column_indices_in_sector))

            list_1 = self.get_sector_subrow_possibilities(sector, column_indices_in_sector[0])
            list_2 = self.get_sector_subrow_possibilities(sector, column_indices_in_sector[1])
            list_3 = self.get_sector_subrow_possibilities(sector, column_indices_in_sector[2])
            for n in range(1, 10):
                unique_index = self.unique_to_only_one(n, list_1, list_2, list_3)
                if unique_index >= 0:
                    for i, j in product(range(9), range(9)):
                        if j == column_indices_in_sector[unique_index] and self.sector_lookup(i, j) != sector:
                            success = 1
                            self.possible_values[(i, j)].remove(n)
                            self.print_reason_to_file('Cell (' + str(i) + ', ' + str(j) + ') had possibility value of '
                                                      + str(n) + ' removed because sector '
                                                      + str(sector) + ' must contain it via a column interaction.')
        return success

    def naked_subset(self):
        # TODO - generalize to subsets of 3,4,5,6,7,8
        # TODO - make method iterate over 1, ... ,8
        # TODO - make method take get_row_possibilities and get_column_possibilities as parameters to avoid code dup
        # TODO - naked subset sector
        # subsets of size 2
        success = 0
        for i in range(9):
            # all pairs of values
            for val_1, val_2 in [(x, y) for x, y in product(range(1, 10), range(1, 10)) if x != y]:
                cells_that_contain_pair = []
                for coordinate, possibilities in self.get_row_possibilities(i).items():
                    if (val_1 in possibilities) and (val_2 in possibilities) and len(possibilities) == 2:
                        cells_that_contain_pair.append(coordinate)
                if len(cells_that_contain_pair) == 2:
                    for coordinate, possibilities in self.get_row_possibilities(i).items():
                        if coordinate not in cells_that_contain_pair:
                            if val_1 in possibilities:
                                success = 1
                                possibilities.remove(val_1)
                                self.print_reason_to_file(
                                    'Cell ' + str(coordinate) + ' had possibility value of '
                                    + str(val_1) + ' removed because there was a naked pair subset at '
                                    + str(cells_that_contain_pair))
                            if val_2 in possibilities:
                                success = 1
                                possibilities.remove(val_2)
                                self.print_reason_to_file(
                                    'Cell ' + str(coordinate) + ' had possibility value of '
                                    + str(val_2) + ' removed because there was a naked pair subset at '
                                    + str(cells_that_contain_pair))
        for j in range(9):
            # all pairs of values
            for val_1, val_2 in [(x, y) for x, y in product(range(1, 10), range(1, 10)) if x != y]:
                cells_that_contain_pair = []
                for coordinate, possibilities in self.get_col_possibilities(j).items():
                    if val_1 in possibilities and val_2 in possibilities and len(possibilities) == 2:
                        cells_that_contain_pair.append(coordinate)
                if len(cells_that_contain_pair) == 2:
                    for coordinate, possibilities in self.get_col_possibilities(j).items():
                        if coordinate not in cells_that_contain_pair:
                            if val_1 in possibilities:
                                success = 1
                                possibilities.remove(val_1)
                                self.print_reason_to_file(
                                    'Cell ' + str(coordinate) + ' had possibility value of '
                                    + str(val_1) + ' removed because there was a naked pair subset at '
                                    + str(cells_that_contain_pair))
                            if val_2 in possibilities:
                                success = 1
                                possibilities.remove(val_2)
                                self.print_reason_to_file(
                                    'Cell ' + str(coordinate) + ' had possibility value of '
                                    + str(val_2) + ' removed because there was a naked pair subset at '
                                    + str(cells_that_contain_pair))
        return success

    def x_wing(self):
        """
        Picks sets of 4 cells, where the cells form the corners of a rectangle and eliminates any possibilities shared
        between all 4 from the remaining cells in the 4 corners' sectors.
        """
        success = 0
        # if coordinates_to_check is not initialized...
        if len(self.coordinates_to_check) == 0:
            # for all combinations of 4 coordinate pairs where the 4 coordinates are on matching corners ...
            # and all 4 corners are in different cells ...
            self.coordinates_to_check = [(a, b, c, d, e, f, g, h) for a, b, c, d, e, f, g, h in
                                         product(range(9), repeat=8)
                                         if (b == d and f == h and a == e and c == g) and len(list(
                                            {self.sector_lookup(a, b), self.sector_lookup(c, d),
                                             self.sector_lookup(e, f), self.sector_lookup(g, h)})) == 4]

        for a, b, c, d, e, f, g, h in self.coordinates_to_check:
            poss_1 = [i for i in self.get_possibilities(a, b) if i != 0]
            poss_2 = [i for i in self.get_possibilities(c, d) if i != 0]
            poss_3 = [i for i in self.get_possibilities(e, f) if i != 0]
            poss_4 = [i for i in self.get_possibilities(g, h) if i != 0]
            intersection = self.intersection(poss_1, poss_2, poss_3, poss_4)
            if len(intersection) > 0:
                value_to_eliminate = intersection.pop()
                # check that the value only shows up in rows/columns possibilities twice
                # remove the value from the columns/rows
                row_1_poss = [value for poss_list in self.get_row_possibilities(a) for value in poss_list]
                col_1_poss = [value for poss_list in self.get_col_possibilities(b) for value in poss_list]
                row_2_poss = [value for poss_list in self.get_row_possibilities(c) for value in poss_list]
                col_2_poss = [value for poss_list in self.get_col_possibilities(d) for value in poss_list]
                if row_1_poss.count(value_to_eliminate) == 2 and row_2_poss.count(value_to_eliminate) == 2:
                    # eliminate value from columns b, d
                    success = 1
                    self.eliminate_possibilities_from_column(b, value_to_eliminate)
                    self.eliminate_possibilities_from_column(d, value_to_eliminate)
                    self.print_reason_to_file('Columns ' + str(b) + ' and ' + str(d) + ' had possibility value of '
                                              + str(value_to_eliminate) + ' removed because there was '
                                              + 'an x-wing interaction between cells '
                                              + str([(a, b), (c, d), (e, f), (g, h)]))
                elif col_1_poss.count(value_to_eliminate) == 2 and col_2_poss.count(value_to_eliminate) == 2:
                    # eliminate value from rows a, e
                    success = 1
                    self.eliminate_possibilities_from_row(a, value_to_eliminate)
                    self.eliminate_possibilities_from_row(c, value_to_eliminate)
                    self.print_reason_to_file('Rows ' + str(a) + ' and ' + str(c) + ' had possibility value of '
                                              + str(value_to_eliminate) + ' removed because there was '
                                              + 'an x-wing interaction between cells '
                                              + str([(a, b), (c, d), (e, f), (g, h)]))

        return success

    # ------------------------------------------- Helper Functions -------------------------------------------------

    @staticmethod
    def unique_to_only_one(n, list_1, list_2, list_3):
        """
        Returns the index of the list passed in if value n is unique to said list (among the 3 lists entered)
        :param n: value to be checked for uniqueness
        :param list_1: first list
        :param list_2: second list
        :param list_3: third list
        :return: index of list which uniquely contains n, -1 if none contain n or if n is in multiple lists
        """
        if (n in list_1) and (n not in list_2) and (n not in list_3):
            return 0
        elif (n not in list_1) and (n in list_2) and (n not in list_3):
            return 1
        elif (n not in list_1) and (n not in list_2) and (n in list_3):
            return 2
        else:
            return -1

    @staticmethod
    def intersection(list_1, list_2, list_3, list_4):
        return list(set(list_1) & set(list_2) & set(list_3) & set(list_4))

    def is_solved(self):
        """
        Returns a boolean indicating if the sudoku is solved
        """
        for row in self.board:
            if 0 in row:
                return False
        return True

    @staticmethod
    def sector_lookup(i, j):
        """Returns sector index of a cell based on its i,j coordinates
        :param i: x coordinate. starts at 0, which is located far left
        :param j: y coordinate. starts at 0, which is located at the top
        :return: sector index of cell i,j. Sector indices start at 0 and go left to right, top to bottom.
        """
        return ((i // 3) * 3) + (j // 3)

    def eliminate_possibilities_from_row(self, i, value):
        for coord, possibilities in self.possible_values.items():
            if coord[0] == i:
                possibilities.remove(value)

    def eliminate_possibilities_from_column(self, j, value):
        for coord, possibilities in self.possible_values.items():
            if coord[1] == j:
                possibilities.remove(value)

    # ---------------------------------------------- Utility ---------------------------------------------------------

    def print_reason_to_file(self, s):
        self.file.write(s + '\n')
        print(s)
        print(self)

    # TODO
    """"
    - https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    - block / block interaction
    - naked subset
    - hidden subset
    - "Swordfish"
    - Forcing Chain
    - http://www.sadmansoftware.com/sudoku/solvingtechniques.php
    - XY - Wing
    - XYZ - Wing
    - .sdk file interpreter
    """

    def solve(self):
        print(self)
        method_progression = [self.sole_candidates, self.unique_candidate_columns, self.unique_candidate_rows,
                              self.unique_candidate_sectors, self.naked_subset, self.sector_column_interaction,
                              self.sector_row_interaction, self.x_wing]
        # while not self.is_solved():
        index = 0
        while index < len(method_progression):
            print('index ' + str(index))
            success = method_progression[index]()
            if success == 0:
                index += 1
            else:
                index = 0



