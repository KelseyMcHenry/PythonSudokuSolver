from SudokuBoard import SudokuBoard
import os
from View import SudokuView
from tkinter import Tk, Frame, RIGHT, Scrollbar, X, Y, Text, BOTH, WORD, Label, TOP, LEFT, font
from tkinter.font import Font

if __name__ == '__main__':
    sudoku = SudokuBoard(file_path=r'TestCases/blockcolrow4.sdk')
    sudoku_view = SudokuView(sudoku)



