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
            if len(self.board[x][y]) == 1:
                self.board[x][y] = self.board[x][y].pop()
            else:
                self.board[x][y].remove(value)


    def set_board(self, board):
        self.board = board

    def get_sudoku_object(self):
        return SudokuBoard([self.board[x][y] if type(self.board[x][y]) is int else 0 for x, y in product(SudokuBoard.INDEX_RANGE, SudokuBoard.INDEX_RANGE)])

    def check_for_blank_cells(self):
        return [(x, y) for x, y in product(SudokuBoard.INDEX_RANGE, SudokuBoard.INDEX_RANGE) if self.board[x][y] == [] or self.board[x][y] == 0]

    def check_for_poss_to_eliminate_easily(self):
        user_input_map = {(x, y): self.board[x][y] for x, y in product(SudokuBoard.INDEX_RANGE, SudokuBoard.INDEX_RANGE)}
        offending_coord_pairs = []
        for index in SudokuBoard.INDEX_RANGE:
            sub_area_solved_numbers = [
                {coord: val for coord, val in user_input_map.items() if coord[0] == index and type(val) is int},
                {coord: val for coord, val in user_input_map.items() if coord[1] == index and type(val) is int},
                {coord: val for coord, val in user_input_map.items() if SudokuBoard.sector_lookup(coord[0], coord[1]) == index and type(val) is int}]
            sub_area_poss = [
                {coord: val for coord, val in user_input_map.items() if coord[0] == index and type(val) is list},
                {coord: val for coord, val in user_input_map.items() if coord[1] == index and type(val) is list},
                {coord: val for coord, val in user_input_map.items() if SudokuBoard.sector_lookup(coord[0], coord[1]) == index and type(val) is list}]
            for sub_area_index in range(len(sub_area_solved_numbers)):
                for coord_solved, value in sub_area_solved_numbers[sub_area_index].items():
                    for coord_poss, sublist in sub_area_poss[sub_area_index].items():
                        if value in sublist:
                            offending_coord_pairs.append(coord_poss)
                            offending_coord_pairs.append(coord_solved)
                            offending_coord_pairs.append(value)
                            return offending_coord_pairs

    def check_for_simple_contradiction(self):
        user_input_map = {(x, y): self.board[x][y] if type(self.board[x][y]) is int else 0 for x, y in product(SudokuBoard.INDEX_RANGE, SudokuBoard.INDEX_RANGE)}
        counts = {number: 0 for number in SudokuBoard.VALUE_RANGE}
        offending_coord_pairs = []
        for index in SudokuBoard.INDEX_RANGE:
            sub_area_solved_numbers = [{coord: val for coord, val in user_input_map.items() if coord[0] == index and type(val) is int and val != 0},
                                       {coord: val for coord, val in user_input_map.items() if coord[1] == index and type(val) is int and val != 0},
                                       {coord: val for coord, val in user_input_map.items() if SudokuBoard.sector_lookup(coord[0], coord[1]) == index and type(val) is int and val != 0}]
            for sub_area in sub_area_solved_numbers:
                for value in SudokuBoard.VALUE_RANGE:
                    for coord, number in sub_area.items():
                        if number == value:
                            counts[number] += 1
                            offending_coord_pairs.append(coord)
                            if counts[number] > 1:
                                if len(offending_coord_pairs) == 2:
                                    print(offending_coord_pairs)
                                    return offending_coord_pairs
                    offending_coord_pairs.clear()
                counts = {number: 0 for number in SudokuBoard.VALUE_RANGE}





