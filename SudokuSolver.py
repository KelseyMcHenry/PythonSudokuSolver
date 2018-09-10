from SudokuBoard import SudokuBoard
import os
from View import SudokuView
from tkinter import Tk, Frame, RIGHT, Scrollbar, X, Y, Text, BOTH, WORD, Label, TOP, LEFT, font
from tkinter.font import Font


sudoku = SudokuBoard(file_path=r'TestCases/hiddenpair1.sdk')
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
