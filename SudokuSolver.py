import SudokuBoard
import os

# data = input('enter 81 numbers between 1 and 9 corresponding to the rows of a Sudoku puzzle. For blanks, use 0')

# easy
# data = [3, 0, 0, 6, 0, 0, 0, 9, 0,
#         0, 4, 5, 0, 8, 0, 0, 1, 2,
#         0, 0, 0, 0, 0, 1, 0, 7, 0,
#         9, 0, 2, 4, 0, 7, 0, 8, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 1, 0, 9, 2, 0, 0, 0,
#         0, 9, 3, 5, 0, 0, 6, 2, 0,
#         0, 7, 0, 0, 0, 0, 8, 0, 0,
#         0, 5, 8, 0, 0, 0, 0, 0, 1]


# hard
# data = [9, 0, 0, 3, 0, 0, 5, 8, 0,
#         0, 8, 0, 0, 0, 0, 3, 7, 0,
#         0, 0, 0, 0, 0, 7, 4, 0, 2,
#         1, 0, 0, 9, 7, 0, 0, 0, 0,
#         0, 0, 0, 4, 0, 8, 0, 0, 0,
#         0, 0, 0, 0, 3, 2, 0, 0, 6,
#         5, 0, 4, 2, 0, 0, 0, 0, 0,
#         0, 7, 6, 0, 0, 0, 0, 9, 0,
#         0, 1, 9, 0, 0, 3, 0, 0, 4]

# # evil
# data = [0, 9, 1, 0, 3, 0, 0, 0, 0,
#         0, 0, 0, 0, 9, 0, 0, 0, 8,
#         7, 3, 0, 0, 0, 0, 0, 5, 0,
#         3, 0, 0, 0, 0, 4, 1, 0, 0,
#         0, 2, 8, 0, 0, 0, 5, 4, 0,
#         0, 0, 7, 2, 0, 0, 0, 0, 3,
#         0, 7, 0, 0, 0, 0, 0, 9, 5,
#         2, 0, 0, 0, 6, 0, 0, 0, 0,
#         0, 0, 0, 0, 1, 0, 4, 7, 0]
#
# sudoku = SudokuBoard.SudokuBoard(values=data)
#
# sudoku.solve()

# sudoku = SudokuBoard.SudokuBoard(file_path='TestCases/blockcolrow5.sdk')
# sudoku.solve()
# print(sudoku)

for root, dirs, filenames in os.walk('TestCases'):
    for f in filenames:
        sudoku = SudokuBoard.SudokuBoard(file_path='TestCases/' + f, printout=False)
        sudoku.solve()


