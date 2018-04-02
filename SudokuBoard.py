from itertools import product
from itertools import chain
from random import randint
from datetime import datetime
from copy import deepcopy

class SudokuBoard:
    """A data structure designed to hold sudoku data"""

    INDEX_RANGE = range(9)
    VALUE_RANGE = range(1, 10)

    # TODO make functions take functions as parameters (ie col, row, sector) to avoid repeating code
    # TODO document
    # TODO error checking

    # -------------------------------------- Variable initialization -----------------------------------------------



    # --------------------------------------------- Constructor  ---------------------------------------------------

    def __init__(self, values=[0]*81, file_path='', printout=True):
        """
        Initializes the board values and initializes the cell possible values. Default is empty board
        http://www.sadmansoftware.com/sudoku/faq19.php
        """

        # array where solved values are stored
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        # map where possibilities for cells are stored
        self.possible_values = {(i, j): [] for i, j in product(range(9), range(9))}
        # 'cache' variable for x-wing method, which iterates over a complex set which is expensive to reproduce on every run
        self.coordinates_to_check = []
        # English plaintext reasons output file
        self.file = open('reasons.txt', 'w')
        self.print_status = printout
        self.file_path_name = file_path

        if file_path != '':
            values.clear()
            sudoku_file = open(file_path, 'r')
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
            for n in self.VALUE_RANGE:
                if (self.board[coordinate[0]][coordinate[1]] == 0 and
                        (n not in self.board[coordinate[0]]) and
                        (n not in [self.board[i][coordinate[1]] for i in self.INDEX_RANGE]) and
                        (n not in [self.board[i][j] for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE)
                                   if self.sector_lookup(i, j) == self.sector_lookup(coordinate[0], coordinate[1])])):
                    self.possible_values[coordinate].append(n)

    def __str__(self):
        print_value = ""
        # construct the string of the board
        for row in self.board:
            print_value += str(row) + '\n'
        print_value += '\n'
        # construct the possibilities, printed in left justified columns
        max_len = 0
        for index, poss_list in self.possible_values.items():
            if len(poss_list) > max_len:
                max_len = len(poss_list)
        for index, poss_list in self.possible_values.items():
            if len(poss_list) > 0:
                print_value += str(poss_list) + (' ' * ((3 * (max_len - 1) + 3) - (3 * (len(poss_list) - 1) + 3)))
            else:
                print_value += str(poss_list) + (' ' * ((3 * (max_len - 1) + 3) - 2))

            if index[1] == 8:
                print_value += '\n'
            else:
                print_value += ', '

        return print_value

    def __eq__(self, other):
        for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE):
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
        return [self.board[i][j] for i in self.INDEX_RANGE]

    def sector(self, sector):
        """
        :param sector: index of the sector, found using sector_lookup(i, j)
        :return list of values contained in sector, empty cells are indicated by a 0
        """
        return [self.board[i][j] for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE)
                if SudokuBoard.sector_lookup(i, j) == sector]

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
        return {(i, j): self.possible_values[(i, j)] for j in self.INDEX_RANGE}

    def get_col_possibilities(self, j):
        """
        Returns a dictionary of all possible values the cells in column j could contain at time of execution
        :param j: column index. starts at 0, which is located at the far left
        :return dictionary of all possible values the cells in column j could contain at time of execution
                 Keys: Tuples (i, j) for each cell
                 Values: Lists containing all possible values cell i,j could contain at time of execution
        """
        return {(i, j): self.possible_values[(i, j)] for i in self.INDEX_RANGE}

    def get_sector_possibilities(self, sector):
        """
        Returns a dictionary of all possible values the cells in sector could contain at time of execution
        :param sector: index of the sector, found using sector_lookup(i, j)
        :return dictionary of all possible values the cells in sector s could contain at time of execution
                Keys: Tuples (i, j) for each cell
                Values: Lists containing all possible values cell i,j could contain at time of execution
        """
        return {(i, j): self.possible_values[(i, j)] for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE)
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

        # check which validates if i is truly in sector
        assert i // 3 == sector // 3
        sector_poss = self.get_sector_possibilities(sector)
        return {(row, col): sector_poss[(row, col)] for row, col in product(self.INDEX_RANGE, self.INDEX_RANGE)
                if row == i and self.sector_lookup(row, col) == sector}

    def get_sector_subcolumn_possibilities(self, sector, j):
        """
        Returns a subset of the possibilities equal to the intersection of sector and row i
        :param sector: index of the sector, found using sector_lookup(i, j)
        :param j: col index. starts at 0, which is located at the left
        :return: dictionary of all possible values the cells in sector s AND row i could contain at time of execution
                 Keys: Tuples (i, j) for each cell
                 Values: Lists containing all possible values cell i,j could contain at time of execution
        """

        # check which validates if j is truly within sector
        assert ((j % 3) // 3) == ((sector % 3) // 3)
        sector_poss = self.get_sector_possibilities(sector)
        return {(row, col): sector_poss[(row, col)] for row, col in product(self.INDEX_RANGE, self.INDEX_RANGE)
                if col == j and self.sector_lookup(row, col) == sector}

    def set(self, i, j, value):
        """
        Sets the value at i,j and updates the possibilities dictionary
        :param i: x coordinate. starts at 0, which is located far left
        :param j: y coordinate. starts at 0, which is located at the top
        :param value: value to set
        """
        self.board[i][j] = value
        self.possible_values[(i, j)] = []
        for x, y in product(self.INDEX_RANGE, self.INDEX_RANGE):
            if x == i or y == j or self.sector_lookup(x, y) == self.sector_lookup(i, j):
                if value in self.possible_values[(x, y)]:
                    self.possible_values[(x, y)].remove(value)
            if self.board[x][y] == 0 and len(self.get_possibilities(x, y)) == 0:
                raise ValueError('Invalid cell set at ' + str((x, y)))

    def set_poss_values(self, possibilities):
        self.possible_values = deepcopy(possibilities)

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

    def unique_candidates(self, poss_func):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its row, column, or sector as
        indicated by poss_func
        """
        success = 0
        for index in self.INDEX_RANGE:
            # accumulate all of the possibilities for all cells in col j
            area_total_poss = list(chain.from_iterable(poss_func(index).values()))
            # find all unique values in prior list
            unique_values_in_area = [n for n in area_total_poss if area_total_poss.count(n) == 1]

            for value in unique_values_in_area:
                for key, poss_list in poss_func(index).items():
                    if value in poss_list:
                        success = 1
                        self.set(key[0], key[1], value)
                        self.print_reason_to_file('Cell ' + str(key) + ' set to ' + str(value) +
                                                  ' because the possibility was unique to column ' + str(index) + '.')
        return success

    def unique_candidate_rows(self):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its row
        """
        return self.unique_candidates(self.get_row_possibilities)

    def unique_candidate_columns(self):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its column
        """
        return self.unique_candidates(self.get_col_possibilities)

    def unique_candidate_sectors(self):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its sector
        """
        return self.unique_candidates(self.get_sector_possibilities)

    # --------------------------------- Possibility Eliminating Functions -----------------------------------------
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    # http://www.sadmansoftware.com/sudoku/solvingtechniques.php

    def sector_row_interaction(self):
        """
        Eliminates possibilities within a row outside of a sector if a possibility is unique to row within said sector
        """
        success = 0
        for sector in self.INDEX_RANGE:
            row_indices_in_sector = self.row_indices_in_sector(sector)

            list_1 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[0])
            list_2 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[1])
            list_3 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[2])
            for n in self.VALUE_RANGE:
                unique_index = self.unique_to_only_one(n, list_1, list_2, list_3)
                if unique_index >= 0:
                    for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE):
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
        for sector in self.INDEX_RANGE:
            column_indices_in_sector = self.col_indices_in_sector(sector)

            list_1 = self.get_sector_subcolumn_possibilities(sector, column_indices_in_sector[0])
            list_2 = self.get_sector_subcolumn_possibilities(sector, column_indices_in_sector[1])
            list_3 = self.get_sector_subcolumn_possibilities(sector, column_indices_in_sector[2])
            for n in self.VALUE_RANGE:
                unique_index = self.unique_to_only_one(n, list_1, list_2, list_3)
                if unique_index >= 0:
                    for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE):
                        if j == column_indices_in_sector[unique_index] and self.sector_lookup(i, j) != sector:
                            success = 1
                            self.possible_values[(i, j)].remove(n)
                            self.print_reason_to_file('Cell (' + str(i) + ', ' + str(j) + ') had possibility value of '
                                                      + str(n) + ' removed because sector '
                                                      + str(sector) + ' must contain it via a column interaction.')
        return success

    def sector_sector_interaction(self):
        success = 0
        right_adjacent = [(x, x + 1) for x in self.INDEX_RANGE if (x + 1) % 3 != 0 and (x + 1) < 9]
        bottom_adjacent = [(x, x + 3) for x in self.INDEX_RANGE if (x + 3) < 9]
        bottom_two_adjacent = [(x, x + 6) for x in self.INDEX_RANGE if (x + 6) < 9]
        right_two_adjacent = [(x, x + 2) for x in self.INDEX_RANGE if (x // 3) == ((x + 2) // 3) and (x + 2) < 9]
        sectors_to_check_rows = right_adjacent + right_two_adjacent
        sectors_to_check_cols = bottom_adjacent + bottom_two_adjacent

        for sector_1, sector_2 in sectors_to_check_rows:
            for n in self.INDEX_RANGE:
                # if possibility n is unique to the same 2 rows in sector 1 and sector 2,
                # then remove them from all other cells in that same row outside of sector 1 and sector 2
                sector_1_row_indices = self.unique_to_two_rows(n, sector_1)
                sector_2_row_indices = self.unique_to_two_rows(n, sector_2)
                if sector_1_row_indices == sector_2_row_indices and len(sector_1_row_indices) == 2:
                    for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE):
                        ij_sector = self.sector_lookup(i, j)
                        if ij_sector != sector_1 and ij_sector != sector_2 and i in sector_1_row_indices:
                            if n in self.possible_values[(i, j)]:
                                success = 1
                                self.possible_values[(i, j)].remove(n)
                                self.print_reason_to_file('Cell (' + str(i) + ', ' + str(j) + ') had possibility value of '
                                                      + str(n) + ' removed because of a sector - sector interaction '
                                                      + 'between ' + str(sector_1) + ' and ' + str(sector_2) + '.')

        for sector_1, sector_2 in sectors_to_check_cols:
            for n in self.INDEX_RANGE:
                # if possibility n is unique to the same 2 columns in sector 1 and sector 2,
                # then remove them from all other cells in that same column outside of sector 1 and sector 2
                sector_1_col_indices = self.unique_to_two_cols(n, sector_1)
                sector_2_col_indices = self.unique_to_two_cols(n, sector_2)
                if sector_1_col_indices == sector_2_col_indices and len(sector_1_col_indices) == 2:
                    for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE):
                        ij_sector = self.sector_lookup(i, j)
                        if ij_sector != sector_1 and ij_sector != sector_2 and j in sector_1_col_indices:
                            if n in self.possible_values[(i, j)]:
                                success = 1
                                self.possible_values[(i, j)].remove(n)
                                self.print_reason_to_file('Cell (' + str(i) + ', ' + str(j) + ') had possibility value of '
                                                      + str(n) + ' removed because of a sector - sector interaction '
                                                      + 'between ' + str(sector_1) + ' and ' + str(sector_2) + '.')

        return success

    def naked_subset_subarea(self, poss_func):
        success = 0
        # for all subset sizes from 2 ... 5
        for subset_size in range(2, 6):
            # for all row/col/sectors depending on poss_func
            for index in self.INDEX_RANGE:
                # for all possible combinations of 1 ... 9 of size subset_size (without repeats)
                for values in [list(x) for x in product(self.VALUE_RANGE, repeat=subset_size) if len(set(x)) == subset_size]:
                    cells_that_contain_subset = []
                    # if the possibilities in cell in said row/col/sector can ONLY be that subset add it to a list
                    for coordinate, possibilities in poss_func(index).items():
                        if all(i in possibilities for i in values) and len(possibilities) == subset_size:
                            cells_that_contain_subset.append(coordinate)
                            # TODO store items, pop from items, reference that subset of items instead of the if at 383
                    # if only X cells can contain a certain subset of size X, remove the values in said subset from
                    # all other members of the row/col/sector
                    if len(cells_that_contain_subset) == subset_size:
                        for coordinate, possibilities in poss_func(index).items():
                            if coordinate not in cells_that_contain_subset:
                                for value in values:
                                    if value in possibilities:
                                        success = 1
                                        possibilities.remove(value)
                                        self.print_reason_to_file(
                                            'Cell ' + str(coordinate) + ' had possibility value of '
                                            + str(value) + ' removed because there was a naked subset at '
                                            + str(cells_that_contain_subset) + ' of size ' + str(subset_size))

        return success

    def naked_subset(self):
        if not self.naked_subset_subarea(self.get_row_possibilities):
            if not self.naked_subset_subarea(self.get_col_possibilities):
                if not self.naked_subset_subarea(self.get_sector_possibilities):
                    return 0
        return 1

    def hidden_subset_subarea(self, poss_func):
        success = 0
        # for all subset sizes from 2 ... 5
        for subset_size in range(2, 6):
            # for all row/col/sectors depending on poss_func
            for index in self.INDEX_RANGE:
                # for all possible combinations of 1 ... 9 of size subset_size (without repeats)
                for values in [list(x) for x in product(self.VALUE_RANGE, repeat=subset_size) if len(set(x)) == subset_size]:
                    cells_that_contain_members = []
                    for coordinate, possibilities in poss_func(index).items():
                        if any(i in possibilities for i in values):
                            cells_that_contain_members.append(coordinate)
                    total_subarea_possibilities = list(chain.from_iterable(poss_func(index).values()))
                    if all(i in total_subarea_possibilities for i in values):
                        if len(cells_that_contain_members) == subset_size:
                            for coordinate, possibilities in poss_func(index).items():
                                if coordinate in cells_that_contain_members:
                                    for n in self.VALUE_RANGE:
                                        if n in possibilities and n not in values:
                                            success = 1
                                            possibilities.remove(n)
                                            self.print_reason_to_file(
                                                'Cell ' + str(coordinate) + ' had possibility value of '
                                                + str(n) + ' removed because there was a hidden subset at '
                                                + str(cells_that_contain_members) + ' of size ' + str(subset_size)
                                                + ' ' + str(values))

        return success

    def hidden_subset(self):
        if not self.hidden_subset_subarea(self.get_row_possibilities):
            if not self.hidden_subset_subarea(self.get_col_possibilities):
                if not self.hidden_subset_subarea(self.get_sector_possibilities):
                    return 0
        return 1

    def x_wing(self):
        """
        Picks sets of 4 cells, where the cells form the corners of a rectangle and eliminates any possibilities shared
        between all 4 from the remaining cells in the 4 corners' sectors.
        """
        success = 0
        # if coordinates_to_check is not initialized...
        if len(self.coordinates_to_check) == 0:
            # for all combinations of 4 coordinate pairs where the 4 coordinates are on matching corners ...
            # and all 4 corners are in different sectors ...
            self.coordinates_to_check = [(a, b, c, d, e, f, g, h) for a, b, c, d, e, f, g, h in
                                         product(self.INDEX_RANGE, repeat=8)
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

    def swordfish(self):
        success = 0
        index_triplets = [(a, b, c) for a, b, c in product(self.INDEX_RANGE, repeat=3) if a != b and b != c and c != a]
        # index_triplets = [(a, b, c) for a, b, c in product(self.INDEX_RANGE, repeat=3) if a // 3 != b // 3 and b // 3 != c // 3  and c // 3 != a // 3]
        # grab 3 rows
        for row_set in index_triplets:
            row_set_poss = (self.get_row_possibilities(row_set[0]), self.get_row_possibilities(row_set[1]),
                            self.get_row_possibilities(row_set[2]))
            # for a given value
            for value in self.VALUE_RANGE:
                # check to see if all 3 rows contain that value
                if all(value in list(chain.from_iterable(row_poss.values())) for row_poss in row_set_poss):
                    # check to see if within those 3 rows, that value is restricted to the same 3 columns
                    columns = []
                    for row_poss in row_set_poss:
                        for coord, poss in row_poss.items():
                            if value in poss:
                                columns.append(coord[1])
                    if len(set(columns)) == 3:
                        # if so, remove value from all 3 columns
                        for column in columns:
                            for i in self.INDEX_RANGE:
                                if value in self.possible_values[(i, column)] and i not in row_set:
                                    success = 1
                                    self.possible_values[(i, column)].remove(value)
                                    self.print_reason_to_file(
                                        'Column ' + str(column) + ' had possibility value of '
                                        + str(value) + ' removed because there was '
                                        + 'a swordfish interaction between rows ' +
                                        str(row_set))
        for col_set in index_triplets:
            col_set_poss = (self.get_col_possibilities(col_set[0]), self.get_col_possibilities(col_set[1]),
                            self.get_col_possibilities(col_set[2]))
            # for a given value
            for value in self.VALUE_RANGE:
                # check to see if all 3 rows contain that value
                if all(value in list(chain.from_iterable(col_poss.values())) for col_poss in col_set_poss):
                    # check to see if within those 3 rows, that value is restricted to the same 3 columns
                    rows = []
                    for col_poss in col_set_poss:
                        for coord, poss in col_poss.items():
                            if value in poss:
                                rows.append(coord[0])
                    if len(rows) == 3:
                        # if so, remove value from all 3 columns
                        for row in rows:
                            for j in self.INDEX_RANGE:
                                if value in self.possible_values[(row, j)] and j not in col_set:
                                    success = 1
                                    self.possible_values[(row, j)].remove(value)
                                    self.print_reason_to_file(
                                        'Row ' + str(row) + ' had possibility value of '
                                        + str(value) + ' removed because there was '
                                        + 'a swordfish interaction between columns ' +
                                        str(col_set))
        return success

    def force_chain(self):
        success = 0
        values = []
        for row in self.board:
            values.extend(row)
        attempt_board = SudokuBoard(values=values, printout=False)
        attempt_board.set_poss_values(self.possible_values)
        for coord, poss in attempt_board.possible_values.items():
            if len(poss) > 1:
                value_to_try = poss[0]
                try:
                    attempt_board.set(coord[0], coord[1], value_to_try)
                    print("Forcing chain on " + str(coord) + " with value " + str(value_to_try))
                    print(attempt_board)
                    try:
                        attempt_board.solve()
                    except ValueError:
                        if value_to_try in self.possible_values[(coord[0], coord[1])]:
                            success = 1
                            self.possible_values[(coord[0], coord[1])].remove(value_to_try)
                            self.print_reason_to_file(
                                str(coord) + ' had possibility value of '
                                + str(value_to_try) + ' removed due to trial and error')
                            return success
                    else:
                        success = 1
                        self.board = deepcopy(attempt_board.board)
                        return success
                except ValueError:
                    if value_to_try in self.possible_values[(coord[0], coord[1])]:
                        success = 1
                        self.possible_values[(coord[0], coord[1])].remove(value_to_try)
                        self.print_reason_to_file(
                            str(coord) + ' had possibility value of '
                            + str(value_to_try) + ' removed due to trial and error')
                        return success

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

    def unique_to_two_rows(self, n, sector):
        # TODO consider making more similar to unique_to_one
        row_indices_in_sector = self.row_indices_in_sector(sector)
        list_1 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[0])
        list_2 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[1])
        list_3 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[2])

        return_val = []
        for index, sublist in list_1.items():
            if n in sublist:
                return_val.append(row_indices_in_sector[0])
                break
        for index, sublist in list_2.items():
            if n in sublist:
                return_val.append(row_indices_in_sector[1])
                break
        for index, sublist in list_3.items():
            if n in sublist:
                return_val.append(row_indices_in_sector[2])
                break

        return tuple(sorted(return_val))

    def unique_to_two_cols(self, n, sector):
        # TODO consider making more similar to unique_to_one
        col_indices_in_sector = self.col_indices_in_sector(sector)
        list_1 = self.get_sector_subcolumn_possibilities(sector, col_indices_in_sector[0])
        list_2 = self.get_sector_subcolumn_possibilities(sector, col_indices_in_sector[1])
        list_3 = self.get_sector_subcolumn_possibilities(sector, col_indices_in_sector[2])

        return_val = []
        for index, sublist in list_1.items():
            if n in sublist:
                return_val.append(col_indices_in_sector[0])
                break
        for index, sublist in list_2.items():
            if n in sublist:
                return_val.append(col_indices_in_sector[1])
                break
        for index, sublist in list_3.items():
            if n in sublist:
                return_val.append(col_indices_in_sector[2])
                break

        return tuple(sorted(return_val))

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

    def row_indices_in_sector(self, sector):
        return [i for i in self.INDEX_RANGE if i // 3 == sector // 3]

    def col_indices_in_sector(self, sector):
        return [j for j in self.INDEX_RANGE if ((j % 3) // 3) == ((sector % 3) // 3)]

    def eliminate_possibilities_from_row(self, i, value):
        for coord, possibilities in self.possible_values.items():
            if coord[0] == i and value in possibilities:
                possibilities.remove(value)

    def eliminate_possibilities_from_column(self, j, value):
        for coord, possibilities in self.possible_values.items():
            if coord[1] == j and value in possibilities:
                possibilities.remove(value)

    def eliminate_possibilities_from_sector(self, sector, value):
        for coord, possibilities in self.possible_values.items():
                if self.sector_lookup(coord[0], coord[1]) == sector and value in possibilities:
                    possibilities.remove(value)

    # ---------------------------------------------- Utility ---------------------------------------------------------

    def print_reason_to_file(self, s):
        if self.print_status:
            self.file.write(s + '\n')
            print(s)
            print(self)

    # TODO
    """"
    - https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    - Forcing Chain
    - http://www.sadmansoftware.com/sudoku/solvingtechniques.php
    - XY - Wing
    - XYZ - Wing
    """

    def solve(self):
        start_time = datetime.now()
        # print(self)
        method_progression = [self.sole_candidates, self.unique_candidate_columns, self.unique_candidate_rows,
                              self.unique_candidate_sectors, self.naked_subset, self.hidden_subset,
                              self.sector_sector_interaction, self.sector_column_interaction,
                              self.sector_row_interaction, self.x_wing, self.swordfish, self.force_chain]

        index = 0
        while index < len(method_progression):
            success = method_progression[index]()
            if self.is_solved():
                end_time = datetime.now()
                diff = divmod((end_time - start_time).total_seconds(), 60)
                if self.file_path_name:
                    print('Completed ' + self.file_path_name + ' in ' + str(diff[0]) + ' minutes and ' + str(diff[1]) + ' seconds.')
                return
            else:
                if success == 0:
                    index += 1
                else:
                    index = 0

        end_time = datetime.now()
        diff = divmod((end_time - start_time).total_seconds(), 60)
        if self.file_path_name:
            print('Unable to complete ' + self.file_path_name + ' in ' + str(diff[0]) + ' minutes and ' + str(diff[1]) + ' seconds.')
            print(self)


