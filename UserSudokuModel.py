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
            if not (x_index == x and y_index == y) and \
                    (x_index == x or y_index == y or SudokuBoard.sector_lookup(x_index, y_index) == SudokuBoard.sector_lookup(x, y)) and \
                    type(self.board[x_index][y_index]) is list and \
                    value in self.board[x_index][y_index]:
                moves.append(Move(REMOVE_POSS, value, (x_index, y_index), f'The value {value} was eliminated from the possibilities at {x_index, y_index} because we determined {x, y} to be {value}'))

        return moves

    def add_possibility(self, x, y, value):
        if value == 0:
            return
        if type(self.board[x][y]) is int:
            self.board[x][y] = [self.board[x][y], value]
        else:
            self.board[x][y].append(value)

    def remove_possibility(self, x, y, value):
        if type(self.board[x][y]) is list:
            self.board[x][y].remove(value)
            if len(self.board[x][y]) == 1:
                self.board[x][y] = self.board[x][y].pop()

    def set_board(self, board):
        self.board = board

    def get_sudoku_object(self):
        return SudokuBoard(chain.from_iterable(self.board))

    def check_for_simple_contradiction(self):
        user_input_map = {(x, y): self.board[x][y] if type(self.board[x][y]) is int else 0 for x, y in product(SudokuBoard.INDEX_RANGE, SudokuBoard.INDEX_RANGE)}
        for index in SudokuBoard.INDEX_RANGE:
            user_input_map_row = {coord: val for coord, val in user_input_map.items() if coord[1] == index}
            user_input_map_column = {coord: val for coord, val in user_input_map.items() if coord[0] == index}
            user_input_map_sector = {coord: val for coord, val in user_input_map.items() if SudokuBoard.sector_lookup(coord[0], coord[1]) == index}
            
            row_value_counts = {val: list(user_input_map_row.values()).count(val) for val in user_input_map_row.values() if val != 0}
            column_value_counts = {val: list(user_input_map_column.values()).count(val) for val in user_input_map_column.values() if val != 0}
            sector_value_counts = {val: list(user_input_map_sector.values()).count(val) for val in user_input_map_sector.values() if val != 0}
            
            row_duplicates = {val: count for val, count in row_value_counts.items() if count > 1}
            column_duplicates = {val: count for val, count in column_value_counts.items() if count > 1}
            sector_duplicates = {val: count for val, count in sector_value_counts.items() if count > 1}

            offending_row_coords = {coord: val for coord, val in user_input_map_row.items() if val in row_duplicates.keys()}
            offending_column_coords = {coord: val for coord, val in user_input_map_column.items() if val in column_duplicates.keys()}
            offending_sector_coords = {coord: val for coord, val in user_input_map_sector.items() if val in sector_duplicates.keys()}

            if offending_row_coords:
                return offending_row_coords.keys()
            elif offending_column_coords:
                return offending_column_coords.keys()
            elif offending_sector_coords:
                return offending_sector_coords.keys()
        return []



