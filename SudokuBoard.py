from itertools import product


class SudokuBoard:
    """A data structure designed to hold sudoku data"""

    board = [[0 for _ in range(9)] for _ in range(9)]

    def __init__(self, values=[0]*81):
        for i, value in enumerate(values):
            self.board[i // 9][i % 9] = value

    def get(self, i, j):
        return self.board[i][j]

    def row(self, i):
        return self.board[i]

    def column(self, j):
        return [self.board[i][j] for i in range(9)]

    def sector_lookup(self, i, j):
        return (((i+1) % 3) * 3) + ((j + 1) % 3)

    def sector(self, sector):
        return [self.board[i][j] for i, j in product(range(9), range(9)) if (((i+1) % 3) * 3) + ((j + 1) % 3) == sector]

