import SudokuBoard



# data = input('enter 81 numbers between 1 and 9 corresponding to the rows of a Sudoku puzzle. For blanks, use 0')

data = [3, 0, 0, 6, 0, 0, 0, 9, 0,
        0, 4, 5, 0, 8, 0, 0, 1, 2,
        0, 0, 0, 0, 0, 1, 0, 7, 0,
        9, 0, 2, 4, 0, 7, 0, 8, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 0, 9, 2, 0, 0, 0,
        0, 9, 3, 5, 0, 0, 6, 2, 0,
        0, 7, 0, 0, 0, 0, 8, 0, 0,
        0, 5, 8, 0, 0, 0, 0, 0, 1]

sudoku = SudokuBoard.SudokuBoard(values=data)

sudoku.solve()
print(sudoku.board)

