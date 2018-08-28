REMOVE_POSS = 'remove possibility'
NUMBER_SOLVE = 'number solve'


class Move:
    def __init__(self, operation, number, pos, reason):
        self.operation = operation
        self.move_pos = pos
        self.number = number
        self.reason = reason

    def __eq__(self, other):
        return other.operation == self.operation and \
               other.move_pos == self.move_pos and \
               other.number == self.number and \
               other.reason == self.reason
