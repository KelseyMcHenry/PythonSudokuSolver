class SudokuCell:
    value = 0
    possible_values= []

    def __init__(self, value=0, possibilities=[]):
        self.value = value
        self.possible_values.extend(possibilities)

    def value(self):
        return self.value

    def possibilities(self):
        return self.possible

    def set_value(self, value):
        self.value = value

    # def update_possibilities(self, row, column, sector):
    #     for n in range(9):

