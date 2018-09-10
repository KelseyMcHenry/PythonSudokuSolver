from copy import deepcopy
from itertools import chain, product
from SudokuBoard import SudokuBoard
from Move import Move, REMOVE_POSS

class UserBoard:
    def __init__(self, board, poss_dict=None):
        self.board = deepcopy(board.board)
        if poss_dict:
            for coord, poss_list in poss_dict.items():
                if self.board[coord[0]][coord[1]] == 0:
                    self.board[coord[0]][coord[1]] = list()
                    self.board[coord[0]][coord[1]].extend(poss_list)

    def get(self, x, y):
        return self.board[x][y]

    def set(self, x, y, value):
        self.board[x][y] = value

    def code_set(self, x, y, value):
        moves = []
        self.board[x][y] = value
        indices = product(SudokuBoard.INDEX_RANGE, SudokuBoard.INDEX_RANGE)
        for x_index, y_index in indices:
            if x_index == x or y_index == y or SudokuBoard.sector_lookup(x_index, y_index) == SudokuBoard.sector_lookup(x, y) and type(self.board[x][y]) is list:
                moves.append(Move(REMOVE_POSS, (x_index, y_index), value, f'The value {value} was eliminated from the possibilities at {x_index, y_index} because we determined {x, y} to be {value}'))

        return moves

    def add_possibility(self, x, y, value):
        if value == 0:
            return
        if type(self.board[x][y]) is int:
            self.board[x][y] = [self.board[x][y], value]
        else:
            self.board[x][y].append(value)

    def remove_possibility(self, x, y, value):
        self.board[x][y].remove(value)
        if len(self.board[x][y]) == 1:
            self.board[x][y] = self.board[x][y].pop()

    def set_board(self, board):
        self.board = board

