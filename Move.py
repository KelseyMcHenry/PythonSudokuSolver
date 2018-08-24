REMOVE_POSS = 'remove possibility'
NUMBER_SOLVE = 'number solve'


class Move:
    def __init__(self, operation, number, pos, reason):
        self.operation = operation
        self.move_pos = pos
        self.number = number
        self.reason = reason
