from copy import deepcopy


class UserBoard:
    def __init__(self, board):
        self.board = deepcopy(board.board)

    def get(self, x, y):
        return self.board[x][y]

    def set(self, x, y, value):
        self.board[x][y] = value

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

