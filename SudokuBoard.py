from itertools import product
from itertools import chain


class SudokuBoard:
    """A data structure designed to hold sudoku data"""

    board = [[0 for _ in range(9)] for _ in range(9)]
    possible_values = {}
    for i, j in product(range(9), range(9)):
        possible_values[(i, j)] = []

    def __init__(self, values=[0]*81):
        for i, value in enumerate(values):
            self.board[i // 9][i % 9] = value
        for coordinate, possibilities in self.possible_values.items():
            for n in range(1, 10):
                if (self.board[coordinate[0]][coordinate[1]] == 0 and (n not in self.board[coordinate[0]]) and (n not in [self.board[i][coordinate[1]] for i in range(9)]) and (n not in [self.board[i][j] for i, j in product(range(9), range(9)) if SudokuBoard.sector_lookup(i, j) == SudokuBoard.sector_lookup(coordinate[0], coordinate[1])])):
                    self.possible_values[coordinate].append(n)

    def get(self, i, j):
        return self.board[i][j]

    def row(self, i):
        return self.board[i]

    def column(self, j):
        return [self.board[i][j] for i in range(9)]

    def get_possibilities(self, i, j):
        return self.possible_values[(i, j)]

    def get_row_possibilities(self, i):
        return {(i, j): self.possible_values[(i, j)] for j in range(9)}

    def get_col_possibilities(self, j):
        return {(i, j): self.possible_values[(i, j)] for i in range(9)}

    def get_sector_possibilities(self, s):
        return {(i, j): self.possible_values[(i, j)] for i, j in product(range(9), range(9)) if self.sector_lookup(i, j) == s}

    @staticmethod
    def sector_lookup(i, j):
        return ((i // 3) * 3) + (j // 3)

    def sector(self, sector):
        return [self.board[i][j] for i, j in product(range(9), range(9)) if SudokuBoard.sector_lookup(i, j) == sector]

    def set(self, i, j, value):
        self.board[i][j] = value
        for x, y in product(range(9), range(9)):
            self.possible_values[(x, y)] = []
        for coordinate, possibilities in self.possible_values.items():
            for n in range(1, 10):
                if (self.board[coordinate[0]][coordinate[1]] == 0 and (n not in self.row(coordinate[0])) and (n not in self.column(coordinate[1])) and (n not in self.sector(SudokuBoard.sector_lookup(coordinate[0], coordinate[1])))):
                    self.possible_values[coordinate].append(n)

    def is_solved(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def solve(self):
        while not self.is_solved():
            # does cell x contain only a single value? if so set it
            for coordinate, possibilities in self.possible_values.items():
                if len(possibilities) == 1:
                    self.set(coordinate[0], coordinate[1], possibilities[0])
                    print(self.board)

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



        # check for pairs, triples, etc with same values in possibilities. eliminate from other possibilities.
        
