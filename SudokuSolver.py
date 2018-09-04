import SudokuBoard
import os
from View import SudokuView
from tkinter import Tk, Frame, RIGHT, Scrollbar, X, Y, Text, BOTH, WORD, Label, TOP, LEFT, font
from tkinter.font import Font

# data = input('enter 81 numbers between 1 and 9 corresponding to the rows of a Sudoku puzzle. For blanks, use 0')

# # easy
# data_3 = [3, 0, 0, 6, 0, 0, 0, 9, 0,
#         0, 4, 5, 0, 8, 0, 0, 1, 2,
#         0, 0, 0, 0, 0, 1, 0, 7, 0,
#         9, 0, 2, 4, 0, 7, 0, 8, 0,
#         0, 0, 0, 0, 0, 0, 0, 0, 0,
#         0, 0, 1, 0, 9, 2, 0, 0, 0,
#         0, 9, 3, 5, 0, 0, 6, 2, 0,
#         0, 7, 0, 0, 0, 0, 8, 0, 0,
#         0, 5, 8, 0, 0, 0, 0, 0, 1]
#
#
# # hard
# data_2 = [9, 0, 0, 3, 0, 0, 5, 8, 0,
#         0, 8, 0, 0, 0, 0, 3, 7, 0,
#         0, 0, 0, 0, 0, 7, 4, 0, 2,
#         1, 0, 0, 9, 7, 0, 0, 0, 0,
#         0, 0, 0, 4, 0, 8, 0, 0, 0,
#         0, 0, 0, 0, 3, 2, 0, 0, 6,
#         5, 0, 4, 2, 0, 0, 0, 0, 0,
#         0, 7, 6, 0, 0, 0, 0, 9, 0,
#         0, 1, 9, 0, 0, 3, 0, 0, 4]
#
# # # # evil
data_1 = [1, 0, 0, 0, 9, 0, 3, 0, 0,
          0, 6, 0, 7, 0, 0, 0, 0, 8,
          0, 0, 4, 0, 0, 5, 0, 0, 0,
          3, 0, 0, 0, 6, 0, 1, 0, 0,
          0, 7, 0, 8, 0, 0, 0, 0, 0,
          0, 0, 5, 0, 0, 0, 0, 9, 0,
          2, 0, 0, 0, 1, 0, 0, 6, 0,
          0, 8, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 9, 4, 0, 0, 0, 0, 0]

sudoku = SudokuBoard.SudokuBoard([7, 0, 6, 8, 2, 5, 0, 9, 4, 5, 9, 4, 3, 1, 7, 6, 2, 8, 2, 0, 0, 6, 4, 9, 5, 0, 7, 0, 4, 5, 2, 3, 0, 7, 6, 0, 6, 7, 0, 9, 5, 0, 0, 4, 2, 0, 2, 1, 7, 6, 4, 8, 5, 0, 4, 5, 7, 1, 9, 3, 2, 8, 6, 0, 6, 9, 5, 0, 2, 4, 0, 0, 1, 0, 2, 4, 0, 6, 9, 0, 5])
sudoku.set_poss_values({(0, 0): [], (0, 1): [1, 3], (0, 2): [], (0, 3): [], (0, 4): [], (0, 5): [], (0, 6): [1, 3], (0, 7): [], (0, 8): [], (1, 0): [], (1, 1): [], (1, 2): [], (1, 3): [], (1, 4): [], (1, 5): [], (1, 6): [], (1, 7): [], (1, 8): [], (2, 0): [], (2, 1): [1, 3, 8], (2, 2): [3, 8], (2, 3): [], (2, 4): [], (2, 5): [], (2, 6): [], (2, 7): [1, 3], (2, 8): [], (3, 0): [8, 9], (3, 1): [], (3, 2): [], (3, 3): [], (3, 4): [], (3, 5): [1, 8], (3, 6): [], (3, 7): [], (3, 8): [1, 9], (4, 0): [], (4, 1): [], (4, 2): [3, 8], (4, 3): [], (4, 4): [], (4, 5): [1, 8], (4, 6): [1, 3], (4, 7): [], (4, 8): [], (5, 0): [3, 9], (5, 1): [], (5, 2): [], (5, 3): [], (5, 4): [], (5, 5): [], (5, 6): [], (5, 7): [], (5, 8): [3, 9], (6, 0): [], (6, 1): [], (6, 2): [], (6, 3): [], (6, 4): [], (6, 5): [], (6, 6): [], (6, 7): [], (6, 8): [], (7, 0): [3, 8], (7, 1): [], (7, 2): [], (7, 3): [], (7, 4): [7, 8], (7, 5): [], (7, 6): [], (7, 7): [1, 7], (7, 8): [1, 3], (8, 0): [], (8, 1): [3, 8], (8, 2): [], (8, 3): [], (8, 4): [7, 8], (8, 5): [], (8, 6): [], (8, 7): [3, 7], (8, 8): []})
# sudoku.solve()
#
# print(sudoku)
# print(sudoku.board)
# print(sudoku.possible_values)
#
# exit()

# sudoku = SudokuBoard.SudokuBoard(file_path='TestCases/blockcolrow5.sdk')
# sudoku.solve()
# print(sudoku)

# for root, dirs, filenames in os.walk('TestCases'):
#     for f in filenames:
#         sudoku = SudokuBoard.SudokuBoard(file_path='TestCases/' + f, printout=True)
#         sudoku.solve()

root = Tk()
console_frame = Frame(master=root)
vertical_scrollbar = Scrollbar(console_frame)
text = Text(console_frame, height=2, wrap=WORD)
label = Label(console_frame, text="Console: ", anchor="w")
sudoku_view = SudokuView(root, sudoku, text)
console_frame.pack(side=RIGHT, fill=BOTH, expand=1)
label.pack(side=TOP, fill=X)
vertical_scrollbar.pack(side=RIGHT, fill=Y)
text.pack(side=RIGHT, fill=BOTH, expand=1)

root.mainloop()
