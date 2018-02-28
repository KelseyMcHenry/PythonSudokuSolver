from itertools import product
import time


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
            for coordinate, possibilities in self.possible_values.items():
                if len(possibilities) == 1:
                    self.set(coordinate[0], coordinate[1], possibilities[0])
                    print(self.board)

        # unique possibility in row, column, sector
        # check for pairs, triples, etc with same values in possibilities. eliminate from other possibilities.
        
