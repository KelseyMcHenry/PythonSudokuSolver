from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, LEFT
from tkinter.font import Font
from UserSudokuModel import UserBoard

# http://newcoder.io/gui/part-3/
# http://wiki.tcl.tk/37701

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

MAJOR_LINE_COLOR = "blue"
MINOR_LINE_COLOR = "gray"

ORIGINAL_NUMBER = "black"
ENTERED_NUMBER = "sea green"

CURSOR_COLOR = "red"

# TODO: async pass the original puzzle to the solver, when it returns set a flag.
    # TODO: disable solve and hint buttons until it returns
# TODO: add an option to 'handhold' and not allow them to add incorrect possibilities
# TODO: docstrings
# TODO: button styling
# TODO: make console read only


class SudokuView(Frame):

    def __init__(self, parent, game, text):
        self.game_model = game
        self.user_board = UserBoard(game)
        self.parent = parent
        self.console = text
        Frame.__init__(self, parent)

        self.row, self.col = 0, 0
        self.parent.title("Sudoku Solver")
        self.pack(fill=BOTH, side=LEFT)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        clear_button = Button(self, text="Clear Answers", command=self.clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        hint_button = Button(self, text="Hint", command=self.hint)
        hint_button.pack(fill=BOTH, side=BOTTOM)

        solve_button = Button(self, text="Solve", command=self.solve)
        solve_button.pack(fill=BOTH, side=BOTTOM)

        new_puzzle_button = Button(self, text="New Puzzle", command=self.new_puzzle)
        new_puzzle_button.pack(fill=BOTH, side=BOTTOM)

        self.draw_grid()
        self.draw_puzzle()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)
        self.canvas.bind("<FocusOut>", self.clear_cursor)

    def draw_grid(self):
        for i in range(10):
            color = MAJOR_LINE_COLOR if i % 3 == 0 else MINOR_LINE_COLOR

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.user_board.get(i, j)
                if answer != 0:
                    original = self.game_model.get(i, j)
                    color = ORIGINAL_NUMBER if answer == original else ENTERED_NUMBER
                    if type(answer) is list:
                        font = Font(family="Segoe UI", size=9)
                        for number in answer:
                            x = MARGIN + j * SIDE + 14 * ((number - 1) % 3) + 10
                            y = MARGIN + i * SIDE + 14 * ((number - 1) // 3) + 10
                            self.canvas.create_text(x, y, text=number, tags="numbers", fill=color, font=font)
                    elif type(answer) is int:
                        x = MARGIN + j * SIDE + SIDE / 2
                        y = MARGIN + i * SIDE + SIDE / 2
                        font = Font(family="Segoe UI", size=12)
                        self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color, font=font)

    def cell_clicked(self, event):
        # if self.user_board.is_solved():
        #     return
        x, y = event.x, event.y
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            else:
                self.row, self.col = row, col

        self.draw_cursor()

    def draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline=CURSOR_COLOR, tags="cursor")

    def key_pressed(self, event):
        # if self.user_board.is_solved():
        #     return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            val = int(event.char)
            cell = self.user_board.get(self.row, self.col)
            if type(cell) == int and cell == self.game_model.get(self.row, self.col) and cell != 0:
                return
            if type(cell) == int:
                if val == cell:
                    self.user_board.set(self.row, self.col, 0)
                elif cell == 0:
                    self.user_board.set(self.row, self.col, val)
                else:
                    self.user_board.add_possibility(self.row, self.col, val)
            elif type(cell) == list:
                if val in cell:
                    self.user_board.remove_possibility(self.row, self.col, val)
                else:
                    self.user_board.add_possibility(self.row, self.col, val)

            # self.col, self.row = -1, -1
            self.draw_puzzle()
            self.draw_cursor()
            # if self.user_board.check_win():
            #     self.draw_victory()

    def draw_victory(self):
        # TODO: Don't particularly like this, look into changing it
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(x, y, text="You win!", tags="winner", fill="white", font=("Arial", 32))

    def clear_answers(self):
        for i in range(9):
            for j in range(9):
                answer = self.user_board.get(i, j)
                original = self.game_model.get(i, j)
                if answer != original:
                    self.user_board.set(i, j, 0)
        self.draw_puzzle()

    def hint(self):
        # TODO
        # check and see if any cells are incorrect, possibilities or solutions; if so highlight them and say so.
        #   possibly attempt to explain why it is wrong?

        # grab the next move, see if the user has already figured it, if so, move on to the next move.
        #   dole out position, then operation, then number with a reason.

        # put a note in the console
        pass

    def solve(self):
        # TODO solve the whole thing and dump the reasons to the console
        pass

    def new_puzzle(self):
        # TODO
        # pull a puzzle from online
        pass

    def write_to_console(self, text):
        self.console.insert('end', text + '\n')

    def clear_cursor(self, event):
        self.row, self.col = -1, -1
        self.draw_cursor()
