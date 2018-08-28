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

sudoku = SudokuBoard.SudokuBoard(data_1)

sudoku.solve()

print(sudoku)

exit()

# sudoku.solve()
# print(sudoku)

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
