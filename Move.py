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

    def __str__(self):
        return f"Move({self.operation}, {self.number}, {self.move_pos}, '{self.reason}')"
        # return f'OP: {self.operation}, POS: {self.move_pos}, VAL: {self.number}, REASON: {self.reason}'