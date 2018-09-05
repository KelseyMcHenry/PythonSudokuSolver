import time
from itertools import product, permutations
from itertools import chain
from itertools import combinations
from datetime import datetime
from copy import deepcopy
from Move import Move, REMOVE_POSS, NUMBER_SOLVE


# TODO: add reasons for when possibilities are updated
# TODO: add reasons instead of simply returning a success or not.
# TODO: PEP3
# TODO: switch over to using formatted strings
# TODO: split file into board model and solving functions
# TODO: instead of calling .board, make a function to return the board / same for poss
# TODO : redo docs

class SudokuBoard:
    """A data structure designed to hold sudoku data"""

    # -------------------------------------- Constant initialization -----------------------------------------------

    INDEX_RANGE = range(9)
    VALUE_RANGE = range(1, 10)
    call_stack_depth = 0

    # -------------------------------------- Python Reserved Functions  --------------------------------------------

    def __init__(self, values=[0] * 81, file_path='', printout=True):
        """
        Initializes the board values and initializes the cell possible values. Default is empty board
        :param values: list of values 81 values long, with 0 representing an empty space.
        Values are listed left to right, top to bottom.
        :param file_path: path to a .sdk file, format details located at http://www.sadmansoftware.com/sudoku/faq19.php
        :param printout: boolean value indicating whether or not to print the process to the console.
        """

        # array where solved values are stored
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        # map where possibilities for cells are stored
        self.possible_values = {(i, j): [] for i, j in product(range(9), range(9))}
        # 'cache' variable for x-wing method, which iterates over a complex set which is expensive to reproduce
        self.coordinates_to_check = []
        # English plaintext reasons output file
        timestamp = datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H%M%S')
        reasons_filename = 'reasons_' + timestamp
        if file_path:
            reasons_filename += '_' + file_path[10: -4]
        reasons_filename += '.txt'
        self.file = open(reasons_filename, 'w')
        self.print_status = printout
        self.file_path_name = file_path

        new_values = []
        if file_path != '':
            sudoku_file = open(file_path, 'r')
            for line in sudoku_file:
                for character in line:
                    if character == '.':
                        new_values.append(0)
                    elif character == '\n':
                        pass
                    else:
                        new_values.append(int(character))
            sudoku_file.close()

        # if this if statement is not here, random unit tests fail as the "values" default seems to get overwritten...
        if not new_values:
            new_values.extend(values)

        for i, value in enumerate(new_values):
            self.board[i // 9][i % 9] = value

        for coordinate, possibilities in self.possible_values.items():
            for n in self.VALUE_RANGE:
                if (self.board[coordinate[0]][coordinate[1]] == 0 and
                        (n not in self.board[coordinate[0]]) and
                        (n not in [self.board[i][coordinate[1]] for i in self.INDEX_RANGE]) and
                        (n not in [self.board[i][j] for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE)
                                   if self.sector_lookup(i, j) == self.sector_lookup(coordinate[0], coordinate[1])])):
                    self.possible_values[coordinate].append(n)

        # print(self.board)
        # print(self.possible_values)

    def __del__(self):
        self.file.close()

    def __str__(self):
        """
        Allows string conversion to appropriately format the Sudoku
        :return: formatted string version of the puzzle
        """
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
        """
        Allows 2 SudokuBoard opjects to be compared to each other for equality
        :param other: other board being compared against.
        :return:
        """
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

        # TODO: add global moves queue
        # TODO : have set add to moves when it updates possibilities
        self.board[i][j] = value
        self.possible_values[(i, j)] = []
        for x, y in product(self.INDEX_RANGE, self.INDEX_RANGE):
            if x == i or y == j or self.sector_lookup(x, y) == self.sector_lookup(i, j):
                if value in self.possible_values[(x, y)]:
                    self.possible_values[(x, y)].remove(value)
            if self.board[x][y] == 0 and len(self.get_possibilities(x, y)) == 0:
                raise ValueError('Invalid cell value of ' + str(value) + ' cannot be set at ' + str((x, y)))

    def set_poss_values(self, possibilities):
        """
        Sets the possibilities of a SudokuBoard manually
        :param possibilities: dictionary of all possible values the cells could contain at time of execution
                              Keys: Tuples (i, j) for each cell
                              Values: Lists containing all possible values cell i,j could contain at time of execution
        :return:
        """
        self.possible_values = deepcopy(possibilities)

    # ------------------------------------------- Solving Functions -------------------------------------------------
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    # http://www.sadmansoftware.com/sudoku/solvingtechniques.php

    def sole_candidates(self):
        """
        Solves the values of all cells that only have one possibility
        :return: a boolean indicating if any values were successfully solved
        """

        queue = {}

        successes = []
        for coordinate, possibilities in self.possible_values.items():
            if len(possibilities) == 1:
                value = possibilities[0]
                queue[coordinate] = value

        for coordinate, value in queue.items():
            try:
                self.set(coordinate[0], coordinate[1], value)
                reason = 'Cell ' + str(coordinate) + ' set to ' + str(
                    value) + ' because it was the only possibility remaining for that cell.'
                self.print_reason_to_file(reason)
                successes.append(Move(NUMBER_SOLVE, value, coordinate, reason))
            except ValueError as e:
                raise e

        return successes

    def unique_candidates_generic(self, poss_func):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its row, column, or sector as
        indicated by poss_func
        :param poss_func: a function which gives either row, col, or sector possibilities.
        :return: a boolean indicating if any values were successfully solved
        """

        successes = []
        for index in self.INDEX_RANGE:
            # accumulate all of the possibilities for all cells in col j
            area_total_poss = list(chain.from_iterable(poss_func(index).values()))
            # find all unique values in prior list
            unique_values_in_area = [n for n in area_total_poss if area_total_poss.count(n) == 1]

            for value in unique_values_in_area:
                for key, poss_list in poss_func(index).items():
                    if value in poss_list:
                        self.set(key[0], key[1], value)
                        if poss_func.__name__ == 'get_row_possibilities':
                            subarea_type = 'row'
                        elif poss_func.__name__ == 'get_col_possibilities':
                            subarea_type = 'column'
                        elif poss_func.__name__ == 'get_sector_possibilities':
                            subarea_type = 'sector'
                        reason = 'Cell ' + str(key) + ' set to ' + str(value) + ' because the possibility was unique to ' + subarea_type + ' ' + str(index) + '.'
                        successes.append(Move(NUMBER_SOLVE, value, key, reason))
                        self.print_reason_to_file(reason)

        return successes

    def unique_candidate(self):
        """
        Solves the values of all cells where one of the cell's possibilities is unique to its row, column, or sector.
        Note that this function will try row then col then sector, stopping if any are successful.
        :return: a boolean indicating if any values were successfully solved
        """

        # Takes advantage of Python's OR operator short circuiting to cut down on number of functions run
        return self.unique_candidates_generic(self.get_row_possibilities) or \
            self.unique_candidates_generic(self.get_col_possibilities) or \
            self.unique_candidates_generic(self.get_sector_possibilities)

    # --------------------------------- Possibility Eliminating Functions -----------------------------------------
    # https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php
    # http://www.sadmansoftware.com/sudoku/solvingtechniques.php

    def sector_line_interaction_generic(self, subarea_indices_func, subarea_poss_func):
        """
        Eliminates possibilities within a row outside of a sector if a possibility is unique to row within said sector
        :return: a boolean indicating if any possibilities were successfully eliminated
        """

        # determine the function needed to grab the whole line based on the functions provided...
        get_line_possibilities = None
        if 'row' in subarea_indices_func.__name__:
            subarea_type = 'row'
            get_line_possibilities = self.get_row_possibilities
        elif 'col' in subarea_indices_func.__name__:
            subarea_type = 'column'
            get_line_possibilities = self.get_col_possibilities

        successes = []
        # for each sector in the puzzle...
        for sector in self.INDEX_RANGE:
            # find out what row/column indices are contained within the sector...
            #   ie sector 2 has row indices (0, 1, 2) or col indices (6, 7, 8)
            area_indices_in_sector = subarea_indices_func(sector)

            # grab the possibility lists from the intersection of the row indices above and the sector above...
            list_1 = subarea_poss_func(sector, area_indices_in_sector[0])
            list_2 = subarea_poss_func(sector, area_indices_in_sector[1])
            list_3 = subarea_poss_func(sector, area_indices_in_sector[2])

            # for every number value...
            for n in self.VALUE_RANGE:
                # check to see if that value is unique to only one of the 'intersection subset' lists
                unique_index = self.unique_to_only_one(n, list_1, list_2, list_3)
                # if it is unique to only one...
                if unique_index > -1:
                    # then grab the whole line
                    line_possibilities = get_line_possibilities(area_indices_in_sector[unique_index])
                    for coord, poss in line_possibilities.items():
                        if self.sector_lookup(coord[0], coord[1]) != sector and n in self.possible_values[coord]:
                            self.possible_values[coord].remove(n)
                            reason = 'Cell ' + str(coord) + ' had possibility value of ' + str(n) + ' removed because sector ' + str(sector) + ' must ' + 'contain it via a ' + subarea_type + ' interaction.'
                            self.print_reason_to_file(reason)
                            successes.append(Move(REMOVE_POSS, n, coord, reason))

        return successes

    def sector_line_interaction(self):
        """
        Eliminates possibilities within a row outside of a sector if a possibility is unique to row or column within
        said sector
        Note that this function will try row then col, stopping if any are successful.
        :return: a boolean indicating if any values were successfully solved
        """
        # Takes advantage of Python's OR operator short circuiting to cut down on number of functions run
        return self.sector_line_interaction_generic(self.row_indices_in_sector,
                                                    self.get_sector_subrow_possibilities) or \
            self.sector_line_interaction_generic(self.col_indices_in_sector,
                                                 self.get_sector_subcolumn_possibilities)

    def sector_sector_interaction(self):
        """
        Eliminates possibilities in other cells in a column or row if a number appears as candidates
        for only two cells in two different blocks, but both cells are in the same column or row
        :return: a boolean indicating if any possibilities were successfully eliminated
        """

        successes = []
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
                if sector_1_row_indices != -1 and sector_1_row_indices == sector_2_row_indices:
                    for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE):
                        ij_sector = self.sector_lookup(i, j)
                        if ij_sector != sector_1 and ij_sector != sector_2 and i in sector_1_row_indices:
                            if n in self.possible_values[(i, j)]:
                                self.possible_values[(i, j)].remove(n)
                                reason = 'Cell (' + str(i) + ', ' + str(j) + ') had possibility value of ' + str(n) + ' removed because of a sector - sector interaction ' + 'between ' + str(sector_1) + ' and ' + str(sector_2) + '.'
                                self.print_reason_to_file(reason)
                                successes.append(Move(REMOVE_POSS, n, (i, j), reason))

        for sector_1, sector_2 in sectors_to_check_cols:
            for n in self.INDEX_RANGE:
                # if possibility n is unique to the same 2 columns in sector 1 and sector 2,
                # then remove them from all other cells in that same column outside of sector 1 and sector 2
                sector_1_col_indices = self.unique_to_two_cols(n, sector_1)
                sector_2_col_indices = self.unique_to_two_cols(n, sector_2)
                if sector_1_col_indices != -1 and sector_1_col_indices == sector_2_col_indices:
                    for i, j in product(self.INDEX_RANGE, self.INDEX_RANGE):
                        ij_sector = self.sector_lookup(i, j)
                        if ij_sector != sector_1 and ij_sector != sector_2 and j in sector_1_col_indices:
                            if n in self.possible_values[(i, j)]:
                                self.possible_values[(i, j)].remove(n)
                                reason = 'Cell (' + str(i) + ', ' + str(j) + ') had possibility value of ' + str(n) + ' removed because of a sector - sector interaction ' + 'between ' + str(sector_1) + ' and ' + str(sector_2) + '.'
                                self.print_reason_to_file(reason)
                                successes.append(Move(REMOVE_POSS, n, (i, j), reason))

        return successes

    # https://www.thonky.com/sudoku/pointing-pairs-triples
    # TODO: other functions from thonky?
    def pointing_tuple_generic(self, poss_func, subarea_poss_func, subarea_indices_func):
        if 'row' in poss_func.__name__:
            subarea_type = 'row'
        elif 'col' in poss_func.__name__:
            subarea_type = 'column'

        successes = []

        for sector in self.INDEX_RANGE:
            area_indices_in_sector = subarea_indices_func(sector)
            subarea_1 = area_indices_in_sector[0]
            subarea_2 = area_indices_in_sector[1]
            subarea_3 = area_indices_in_sector[2]
            for value in self.VALUE_RANGE:
                index_to_remove_value_from = self.unique_to_only_one(value, subarea_poss_func(sector, subarea_1), subarea_poss_func(sector, subarea_2), subarea_poss_func(sector, subarea_3))
                if index_to_remove_value_from >= 0:
                    for coord, poss in poss_func(area_indices_in_sector[index_to_remove_value_from]).items():
                        if self.sector_lookup(coord[0], coord[1]) != sector:
                            if value in self.possible_values[coord]:
                                self.possible_values[coord].remove(value)
                                reason = subarea_type + ' ' + str(index_to_remove_value_from) + ' (' + str(coord) + ') had possibility value of ' + str(value) + ' removed due to a pointing tuple in sector ' + str(sector)
                                successes.append(Move(REMOVE_POSS, value, coord, reason))
        if successes:
            for s in successes:
                print(s)

        return successes

    def pointing_tuple(self):
        # Takes advantage of Python's OR operator short circuiting to cut down on number of functions run
        return self.pointing_tuple_generic(self.get_row_possibilities, self.get_sector_subrow_possibilities, self.row_indices_in_sector) or \
               self.pointing_tuple_generic(self.get_col_possibilities, self.get_sector_subcolumn_possibilities, self.col_indices_in_sector)

    def naked_subset_generic(self, poss_func):
        """
        Eliminates possibilities from other cells in a row, column or block if N cells in the same row, column or
        block have only the same N candidates. N ranges from 2 to 5.
        In theory it could go up to 8 but this function stops at 5, because the operation gets more expensive the
        larger the number and combinations that high get increasingly rare.
        :param poss_func: a function which gives either row, col, or sector possibilities.
        :return: a boolean indicating if any possibilities were successfully eliminated
        """

        subarea_type = ''
        if 'row' in poss_func.__name__:
            subarea_type = 'row'
        elif 'col' in poss_func.__name__:
            subarea_type = 'column'
        elif 'sector' in poss_func.__name__:
            subarea_type = 'sector'

        successes = []
        # for all subset sizes from 2 ... 5
        for subset_size in range(2, 6):
            # for all row/col/sectors depending on poss_func
            for index in self.INDEX_RANGE:
                poss_dict = poss_func(index)
                # remove all cells from data structure that are already solved
                new_poss_dict = {coord: values for coord, values in poss_dict.items() if values}

                # find all combinations of size (subset_size) of the cells which have possibility lists;
                # specifically the coord values. ie if (0, 0), (0, 1), and (0, 2) are the only cells returned
                # by poss_func which are not solved, cell_sets_to_try should contain:
                #   [[(0, 0), (0, 1)], [(0, 0), (0, 2)], [(0, 1), (0, 2)]]
                cell_sets_to_try = combinations(new_poss_dict, subset_size)
                for cell_set in cell_sets_to_try:
                    # list out all of the poss located at these coords ...
                    list_of_all_poss_in_cell_set = [new_poss_dict[coord] for coord in cell_set]
                    # flatten this list of lists into a single list containing every possibility
                    flattened_list_of_all_poss_in_cell_set = [item for sublist in list_of_all_poss_in_cell_set for item in sublist]
                    # remove duplicates from this flattened list
                    values_to_check_for = set(flattened_list_of_all_poss_in_cell_set)
                    # if these possibilities are of the correct size, you have a match and can eliminate
                    # the possibilities from the other cells returned in poss_func
                    if len(values_to_check_for) == subset_size:
                        for coord, poss in new_poss_dict.items():
                            if coord not in cell_set:
                                for value in values_to_check_for:
                                    if value in self.possible_values[coord]:
                                        self.possible_values[coord].remove(value)
                                        reason = 'Cell ' + str(coord) + ' had possibility value of ' + str(value) + ' removed because there was a naked subset at ' + str(cell_set) + ' of size ' + str(subset_size) + ' in ' + subarea_type + ' ' + str(index)
                                        self.print_reason_to_file(reason)
                                        successes.append(Move(REMOVE_POSS, value, coord, reason))
            if successes:
                break

        return successes

    def naked_subset(self):
        """
        Performs naked_subset_subarea for row, col, and sector.
        Note that this function will try row then col then sector, stopping if any are successful.
        :return: a boolean indicating if any possibilities were successfully eliminated
        """

        # Takes advantage of Python's OR operator short circuiting to cut down on number of functions run
        return self.naked_subset_generic(self.get_row_possibilities) or \
            self.naked_subset_generic(self.get_col_possibilities) or \
            self.naked_subset_generic(self.get_sector_possibilities)

    def hidden_subset_generic(self, poss_func):
        """
        Eliminates all other possibilities from N cells in the same row, col, or block if those N cells contain N
        candidates between them that don't appear elsewhere in the same row, column or block. N ranges from 2 to 5.
        In theory it could go up to 8 but this function stops at 5, because the operation gets more expensive the
        larger the number and combinations that high get increasingly rare.
        :param poss_func: a function which gives either row, col, or sector possibilities.
        :return: a boolean indicating if any possibilities were successfully eliminated
        """

        subarea_type = ''
        if 'row' in poss_func.__name__:
            subarea_type = 'row'
        elif 'col' in poss_func.__name__:
            subarea_type = 'column'
        elif 'sector' in poss_func.__name__:
            subarea_type = 'sector'

        successes = []
        # for all subset sizes from 2 ... 5
        for subset_size in range(2, 6):
            # for all row/col/sectors depending on poss_func
            for index in self.INDEX_RANGE:
                poss_dict = poss_func(index)
                # remove all cells from data structure that are already solved
                new_poss_dict = {coord: values for coord, values in poss_dict.items() if values}

                # find all combinations of size (subset_size) of the cells which have possibility lists;
                # specifically the coord values. ie if (0, 0), (0, 1), and (0, 2) are the only cells returned
                # by poss_func which are not solved, cell_sets_to_try should contain:
                #   [[(0, 0), (0, 1)], [(0, 0), (0, 2)], [(0, 1), (0, 2)]]
                cell_sets_to_try = combinations(new_poss_dict, subset_size)
                for cell_set in cell_sets_to_try:
                    # list out all of the poss located at these coords ...
                    list_of_all_poss_in_cell_set = [new_poss_dict[coord] for coord in cell_set]
                    # flatten this list of lists into a single list containing every possibility
                    flattened_list_of_all_poss_in_cell_set = [item for sublist in list_of_all_poss_in_cell_set for item
                                                              in sublist]
                    # remove duplicates from this flattened list
                    values_to_check_for = set(flattened_list_of_all_poss_in_cell_set)
                    # generate pairs, triplets, etc of all the different combinations of values you are looking for
                    for value_grouping in combinations(values_to_check_for, subset_size):
                        # if all of the values in value grouping are exclusive to this cell set...
                        all_values_are_exclusive = True
                        for value in value_grouping:
                            for coord, poss in new_poss_dict.items():
                                if value in poss and coord not in cell_set:
                                    all_values_are_exclusive = False
                                    break
                            if not all_values_are_exclusive:
                                break
                        if all_values_are_exclusive:
                            # then you can remove any other values from the cell set that aren't in the value set
                            for coord, poss in poss_dict.items():
                                for value in poss:
                                    if value not in value_grouping and coord in cell_set:
                                        self.possible_values[coord].remove(value)
                                        reason = 'Cell ' + str(coord) + ' had possibility value of ' + str(
                                            value) + ' removed because there was a hidden subset of size ' + str(subset_size) + ' ' + str(
                                            value_grouping) + ' in ' + subarea_type + ' ' + str(index) + ' at cells ' + str(
                                            cell_set)
                                        self.print_reason_to_file(reason)
                                        successes.append(Move(REMOVE_POSS, value, coord, reason))

        return successes

    def hidden_subset(self):
        """
        Performs hidden_subset_subarea for row, col, and sector.
        Note that this function will try row then col then sector, stopping if any are successful.
        :return: a boolean indicating if any possibilities were successfully eliminated
        """

        # Takes advantage of Python's OR operator short circuiting to cut down on number of functions run
        return self.hidden_subset_generic(self.get_row_possibilities) or \
            self.hidden_subset_generic(self.get_col_possibilities) or \
            self.hidden_subset_generic(self.get_sector_possibilities)

    def x_wing(self):
        """
        Picks sets of 4 cells, where the cells form the corners of a rectangle and eliminates any possibilities shared
        between all 4 from the remaining cells in the 4 corners' sectors.
        :return: a boolean indicating if any possibilities were successfully eliminated
        """

        successes = []
        # if coordinates_to_check is not initialized...
        if len(self.coordinates_to_check) == 0:
            # for all combinations of 4 coordinate pairs where the 4 coordinates are on matching corners ...
            # and all 4 corners are in different sectors ...
            # TODO : Optimization target
            self.coordinates_to_check = [(a, b, c, d, e, f, g, h) for a, b, c, d, e, f, g, h in
                                         product(self.INDEX_RANGE, repeat=8)
                                         if (a == c and e == g and b == f and d == h) and len(
                    {self.sector_lookup(a, b), self.sector_lookup(c, d),
                     self.sector_lookup(e, f), self.sector_lookup(g, h)}) == 4]

        for a, b, c, d, e, f, g, h in self.coordinates_to_check:
            poss_1 = [i for i in self.get_possibilities(a, b) if i != 0]
            poss_2 = [i for i in self.get_possibilities(c, d) if i != 0]
            poss_3 = [i for i in self.get_possibilities(e, f) if i != 0]
            poss_4 = [i for i in self.get_possibilities(g, h) if i != 0]
            intersection = list(set(poss_1) & set(poss_2) & set(poss_3) & set(poss_4))
            if len(intersection) > 0:
                value_to_eliminate = intersection.pop()
                # check that the value only shows up in rows/columns possibilities twice
                # remove the value from the columns/rows
                row_1_poss = [value for poss_list in self.get_row_possibilities(a).values() for value in poss_list]
                row_2_poss = [value for poss_list in self.get_row_possibilities(e).values() for value in poss_list]

                col_1_poss = [value for poss_list in self.get_col_possibilities(b).values() for value in poss_list]
                col_2_poss = [value for poss_list in self.get_col_possibilities(d).values() for value in poss_list]
                if row_1_poss.count(value_to_eliminate) == 2 and row_2_poss.count(value_to_eliminate) == 2:
                    # eliminate value from columns b, d
                    moves1 = self.eliminate_possibilities_from_column(b, value_to_eliminate, [(a, b), (c, d), (e, f), (g, h)])
                    moves2 = self.eliminate_possibilities_from_column(d, value_to_eliminate, [(a, b), (c, d), (e, f), (g, h)])
                    reason = 'Columns ' + str(b) + ' and ' + str(d) + ' had possibility value of ' + str(value_to_eliminate) + ' removed because there was ' + 'an x-wing interaction between cells ' + str([(a, b), (c, d), (e, f), (g, h)])
                    self.print_reason_to_file(reason)
                    successes.extend(moves1)
                    successes.extend(moves2)
                elif col_1_poss.count(value_to_eliminate) == 2 and col_2_poss.count(value_to_eliminate) == 2:
                    # eliminate value from rows a, e
                    moves1 = self.eliminate_possibilities_from_row(a, value_to_eliminate, [(a, b), (c, d), (e, f), (g, h)])
                    moves2 = self.eliminate_possibilities_from_row(e, value_to_eliminate, [(a, b), (c, d), (e, f), (g, h)])
                    reason = 'Rows ' + str(a) + ' and ' + str(e) + ' had possibility value of ' + str(value_to_eliminate) + ' removed because there was ' + 'an x-wing interaction between cells ' + str([(a, b), (c, d), (e, f), (g, h)])
                    self.print_reason_to_file(reason)
                    successes.extend(moves1)
                    successes.extend(moves2)

        return successes

    def swordfish_generic(self, poss_func, poss_eliminator_func):
        if poss_func.__name__ == 'get_row_possibilities':
            subarea_type = 'row'
            opposite_subarea = 'column'
        elif poss_func.__name__ == 'get_col_possibilities':
            subarea_type = 'column'
            opposite_subarea = 'row'
        else:
            raise Exception

        successes = []
        index_triplets = [(a, b, c) for a, b, c in product(self.INDEX_RANGE, repeat=3) if a != b and b != c and a != c]
        # grab 3 rows
        for triplet in index_triplets:
            # grab the set of possibilities for each row/col
            sets_of_poss = (poss_func(triplet[0]), poss_func(triplet[1]), poss_func(triplet[2]))
            # for a given value
            for value in self.VALUE_RANGE:
                # check to see if all 3 rows/columns contain that value exactly twice
                if all(list(chain.from_iterable(subarea_poss.values())).count(value) >= 2 for subarea_poss in sets_of_poss) and all(list(chain.from_iterable(subarea_poss.values())).count(value) <= 3 for subarea_poss in sets_of_poss) or all(list(chain.from_iterable(subarea_poss.values())).count(value) == 2 for subarea_poss in sets_of_poss):
                    opposite_subarea_indices = []
                    for subarea_poss in sets_of_poss:
                        for coord, poss in subarea_poss.items():
                            if value in poss:
                                if subarea_type == 'row':
                                    opposite_subarea_indices.append(coord[1])
                                else:
                                    opposite_subarea_indices.append(coord[0])
                    if len(set(opposite_subarea_indices)) == 3:
                        # if so, remove value from all 3 columns/rows
                        for index in set(opposite_subarea_indices):
                            moves = poss_eliminator_func(index, value, triplet)
                            reason = subarea_type.title() + str(index) + ' had possibility value of ' + str(value) + ' removed because there was ' + 'a swordfish interaction between ' + opposite_subarea + 's ' + str(triplet)
                            self.print_reason_to_file(reason)
                            successes.extend(moves)

        return successes

    def swordfish(self):
        return self.swordfish_generic(self.get_row_possibilities,  self.eliminate_possibilities_from_column_swordfish) or \
               self.swordfish_generic(self.get_col_possibilities,  self.eliminate_possibilities_from_row_swordfish)

    def force_chain(self):
        """
        Takes the first available unsolved cell performs a recursive "guess-n-check" in an attempt to remove
        possibilities. For each value it tries it solves a copy of the puzzle either to completion or
        until a contradiction is met. Upon finding a contradiction it goes back to the original and removes that value.
        Upon completing the puzzle, it copies the completed results back to the current puzzle.

        NOTE: This method is the "nuclear option" and should be avoided until you have solved the puzzle as far as you
        can or else it could run until the heat death of the universe.... or just exceed the recursion limit.

        :return: a boolean indicating if any possibilities were successfully eliminated
        """

        before_board = deepcopy(self.board)
        before_poss = deepcopy(self.possible_values)

        successes = []
        values = []
        for row in self.board:
            values.extend(row)

        # for every cell...
        for coord, poss in self.possible_values.items():
            # if that cell has any possibilities in it...
            if len(poss) > 1:
                # create a copy of the board in its current state...
                attempt_board = SudokuBoard(values=values, printout=False)
                attempt_board.set_poss_values(deepcopy(self.possible_values))
                # go through all the possible values for the cell ...
                value_to_try = poss[0]
                try:
                    # in the 'alternate universe' copy, try to set that value
                    attempt_board.set(coord[0], coord[1], value_to_try)
                    print("Forcing chain on " + str(coord) + " with value " + str(value_to_try) + '....')
                    try:
                        # attempt to solve the 'alternate universe' puzzle under the assumption that it is correct.
                        temp_successes = attempt_board.solve()
                        if temp_successes:
                            successes.extend(temp_successes)
                    except ValueError as e:
                        if self.call_stack_depth == 1:
                            if value_to_try in self.possible_values[coord]:
                                self.possible_values[coord].remove(value_to_try)
                                reason = str(coord) + ' had possibility value of ' + str(value_to_try) + ' removed due to trial and error. ' + str(e)
                                self.print_reason_to_file(reason)
                                successes.append(Move(REMOVE_POSS, value_to_try, coord, reason))
                                return successes
                        else:
                            print('Returning from depth: ' + str(self.call_stack_depth))
                            self.call_stack_depth -= 1
                            return []
                except ValueError as e:
                    # if setting the value on your 'alternate universe' puzzle ran into problems,
                    # you have reached a contradiction. NOTE: you should not hit this when the call stack depth = 1
                    # otherwise your solver is broken!

                    if self.call_stack_depth == 1:
                        if value_to_try in self.possible_values[coord]:
                            self.possible_values[coord].remove(value_to_try)
                            reason = str(coord) + ' had possibility value of ' + str(value_to_try) + ' removed due to trial and error. ' + str(e)
                            self.print_reason_to_file(reason)
                            successes.append(Move(REMOVE_POSS, value_to_try, coord, reason))
                    else:
                        print('Returning from depth: ' + str(self.call_stack_depth))
                        return []

        return successes

    # ------------------------------------------- Helper Functions -------------------------------------------------

    @staticmethod
    def unique_to_only_one(n, poss_dict_1, poss_dict_2, poss_dict_3):
        # TODO : update doc
        """
        Returns the index of the list passed in if value n is unique to said list (among the 3 lists entered)
        :param n: value to be checked for uniqueness
        :param poss_dict_1: first list
        :param poss_dict_2: second list
        :param poss_dict_3: third list
        :return: index of list which uniquely contains n, -1 if none contain n or if n is in multiple lists
        """
        list_1_poss = []
        for coord, poss in poss_dict_1.items():
            list_1_poss.extend(poss)

        list_2_poss = []
        for coord, poss in poss_dict_2.items():
            list_2_poss.extend(poss)

        list_3_poss = []
        for coord, poss in poss_dict_3.items():
            list_3_poss.extend(poss)

        if (n in list_1_poss) and (n not in list_2_poss) and (n not in list_3_poss):
            return 0
        elif (n not in list_1_poss) and (n in list_2_poss) and (n not in list_3_poss):
            return 1
        elif (n not in list_1_poss) and (n not in list_2_poss) and (n in list_3_poss):
            return 2
        else:
            return -1

    def unique_to_two_rows(self, value, sector):
        """
        Determines if a value n is unique to 2 and only 2 rows within a sector
        :param value: value to check for
        :param sector: sector index to search in
        :return: a tuple of all row indices that contain value. These row indices are guaranteed to be in the sector
        specified by the parameter
        """
        row_indices_in_sector = self.row_indices_in_sector(sector)
        list_1 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[0])
        list_2 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[1])
        list_3 = self.get_sector_subrow_possibilities(sector, row_indices_in_sector[2])

        return_val = []
        for index, sublist in list_1.items():
            if value in sublist:
                return_val.append(row_indices_in_sector[0])
                break
        for index, sublist in list_2.items():
            if value in sublist:
                return_val.append(row_indices_in_sector[1])
                break
        for index, sublist in list_3.items():
            if value in sublist:
                return_val.append(row_indices_in_sector[2])
                break
        return_val = tuple(sorted(return_val))

        if len(return_val) != 2:
            return -1
        else:
            return return_val

    def unique_to_two_cols(self, value, sector):
        """
        Determines if a value n is unique to 2 and only 2 columns within a sector
        :param value: value to check for
        :param sector: sector index to search in
        :return: a tuple of all column indices that contain value. These column indices are guaranteed to be in the
        sector specified by the parameter
        """
        col_indices_in_sector = self.col_indices_in_sector(sector)
        list_1 = self.get_sector_subcolumn_possibilities(sector, col_indices_in_sector[0])
        list_2 = self.get_sector_subcolumn_possibilities(sector, col_indices_in_sector[1])
        list_3 = self.get_sector_subcolumn_possibilities(sector, col_indices_in_sector[2])

        return_val = []
        for index, sublist in list_1.items():
            if value in sublist:
                return_val.append(col_indices_in_sector[0])
                break
        for index, sublist in list_2.items():
            if value in sublist:
                return_val.append(col_indices_in_sector[1])
                break
        for index, sublist in list_3.items():
            if value in sublist:
                return_val.append(col_indices_in_sector[2])
                break

        return_val = tuple(sorted(return_val))

        if len(return_val) != 2:
            return -1
        else:
            return return_val

    def is_solved(self):
        """
        :return: a boolean indicating if the sudoku is solved
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
        """
        returns a list containing all row indices contained in sector
        :param sector: sector index
        :return: list of row indices in sector
        """
        return [i for i in self.INDEX_RANGE if i // 3 == sector // 3]

    def col_indices_in_sector(self, sector):
        """
        returns a list containing all col indices contained in sector
        :param sector: sector index
        :return: list of col indices in sector
        """
        return [j for j in self.INDEX_RANGE if j in range(((sector % 3) * 3), ((sector % 3) * 3) + 3)]

    def eliminate_possibilities_from_row(self, row, value, quad):
        """
        Removes the value from all possibility lists in row
        :param row: row index
        :param value: value to eliminate from row
        """
        moves = []

        possibilities = self.get_row_possibilities(row)
        for coord, values in possibilities.items():
            if value in self.possible_values[coord] and coord not in quad:
                self.possible_values[coord].remove(value)
                reason = 'Row ' + str(row) + ' had possibility value of ' + str(
                    value) + ' removed because there was ' + 'an x-wing interaction between cells ' + str(quad)
                moves.append(Move(REMOVE_POSS, value, coord, reason))

        return moves

    def eliminate_possibilities_from_column(self, col, value, quad):
        """
        Removes the value from all possibility lists in column
        :param col: column index
        :param value: value to eliminate from row
        """
        moves = []

        possibilities = self.get_col_possibilities(col)
        for coord, values in possibilities.items():
            if value in self.possible_values[coord] and coord not in quad:
                self.possible_values[coord].remove(value)
                reason = 'Column ' + str(col) + ' had possibility value of ' + str(value) + ' removed because there was ' + 'an x-wing interaction between cells ' + str(quad)
                moves.append(Move(REMOVE_POSS, value, coord, reason))

        return moves

    def eliminate_possibilities_from_sector(self, sector, value):
        """
        Removes the value from all possibility lists in sector
        :param sector: sector index
        :param value: value to eliminate from sector
        """
        for coord, possibilities in self.possible_values.items():
            if self.sector_lookup(coord[0], coord[1]) == sector and value in possibilities:
                self.possible_values[coord].remove(value)

    def eliminate_possibilities_from_row_swordfish(self, row, value, exclusion_triplet):
        """
        Removes the value from all possibility lists in row
        :param row: row index
        :param value: value to eliminate from row
        :param exclusion_triplet: triplet of indices which possibilities will remain untouched.
        """
        moves = []

        possibilities = self.get_row_possibilities(row)
        for coord, values in possibilities.items():
            if value in values and coord[1] not in exclusion_triplet:
                self.possible_values[coord].remove(value)
                reason = 'Row ' + str(row) + ' ' + str(coord) + ' had possibility value of ' + str(value) + ' removed because there was a swordfish interaction between columns ' + str(exclusion_triplet)
                moves.append(Move(REMOVE_POSS, value, coord, reason))

        return moves

    def eliminate_possibilities_from_column_swordfish(self, col, value, exclusion_triplet):
        """
        Removes the value from all possibility lists in column
        :param col: column index
        :param value: value to eliminate from row
        :param exclusion_triplet: triplet of indices which possibilities will remain untouched.
        """
        moves = []

        possibilities = self.get_col_possibilities(col)
        for coord, values in possibilities.items():
            if value in values and coord[0] not in exclusion_triplet:
                self.possible_values[coord].remove(value)
                reason = 'Column ' + str(col) + ' ' + str(coord) + ' had possibility value of ' + str(value) + ' removed because there was a swordfish interaction between rows ' + str(exclusion_triplet)
                moves.append(Move(REMOVE_POSS, value, coord, reason))

        return moves

    # ---------------------------------------------- Utility ---------------------------------------------------------

    def print_reason_to_file(self, s):
        """
        Prints s to a file called "reasons.txt", prints s to the console, prints the sudoku puzzle to console
        :param s: string to be printed to the reasons file, intended to be human readable step by step explanation of
        how the puzzle was solved.
        """
        if self.print_status:
            self.file.write(s + '\n')

    def solve(self):
        """
        Solves the sudoku puzzle
        """
        self.call_stack_depth += 1
        moves = []
        start_time = datetime.now()
        print(self)
        # TODO XWING
        method_progression = [self.sole_candidates, self.unique_candidate, self.sector_line_interaction,
                              self.naked_subset, self.hidden_subset, self.sector_sector_interaction,
                              self.swordfish, self.force_chain]

        most_complex_function_index = 0
        index = 0
        while index < len(method_progression):
            print(method_progression[index].__name__)
            try:
                successes = method_progression[index]()
                if successes:
                    print(self)
            except ValueError as e:
                raise e
            moves.extend(successes)
            if self.is_solved():
                end_time = datetime.now()
                diff = divmod((end_time - start_time).total_seconds(), 60)
                if self.file_path_name:
                    print('Completed ' + self.file_path_name + ' in ' + str(diff[0]) + ' minutes and ' + str(diff[1])
                          + ' seconds, with the most complex function used being '
                          + str(method_progression[most_complex_function_index].__name__) + '.')
                return moves
            else:
                if not successes:
                    index += 1
                    if index > most_complex_function_index:
                        most_complex_function_index = index
                else:
                    index = 0

        end_time = datetime.now()
        diff = divmod((end_time - start_time).total_seconds(), 60)
        if self.file_path_name:
            print('Unable to complete ' + self.file_path_name + ' in ' + str(diff[0]) + ' minutes and ' + str(
                diff[1]) + ' seconds.')
            print(self)

        return moves
