from copy import deepcopy
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, LEFT
from tkinter import Tk, Frame, RIGHT, Scrollbar, X, Y, Text, BOTH, WORD, Label, TOP, LEFT, font
from tkinter.font import Font
from UserSudokuModel import UserBoard
from SudokuBoard import SudokuBoard
from Move import NUMBER_SOLVE, REMOVE_POSS
import time
from multiprocessing.pool import ThreadPool
from threading import Thread
from itertools import chain


# http://newcoder.io/gui/part-3/
# http://wiki.tcl.tk/37701

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board
SECTOR = 3 * SIDE

MAJOR_LINE_COLOR = "steel blue"
MINOR_LINE_COLOR = "gray"

ORIGINAL_NUMBER = "black"
ENTERED_NUMBER = "sea green"

CURSOR_COLOR = "MediumOrchid4"
AI_SOLVING_CURSOR = 'dark slate gray'
AI_POSS_REDUCING_CURSOR = 'orange red'
ERROR_CURSOR_COLOR = 'red'

# TODO: async pass the original puzzle to the solver, when it returns set a flag.
    # TODO: disable solve and hint buttons until it returns
# TODO: add an option to 'handhold' and not allow them to add incorrect possibilities
# TODO: docstrings
# TODO: button styling
# TODO: make console read only
# TODO: make it so clicking a reason highlights the cells ala https://www.sudoku-solutions.com/
# TODO: make reasons their own hoverable cells in the console instead of plaintext


class SudokuView(Frame):

    def __init__(self, game):

        root = Tk()
        console_frame = Frame(master=root)
        vertical_scrollbar = Scrollbar(console_frame)
        text = Text(console_frame, height=2, width=130, wrap=WORD)
        text.config(yscrollcommand=vertical_scrollbar.set)
        vertical_scrollbar.config(command=text.yview)
        label = Label(console_frame, text="Console: ", anchor="w")
        console_frame.pack(side=RIGHT, fill=BOTH, expand=1)
        label.pack(side=TOP, fill=X)
        vertical_scrollbar.pack(side=RIGHT, fill=Y)
        text.pack(side=RIGHT, fill=BOTH, expand=1)

        self.game_model = game
        self.solve_model = SudokuBoard(list(chain.from_iterable(game.board)))
        self.user_board = UserBoard(game, poss_dict=game.possible_values)
        self.console = text
        self.console_scrollbar = vertical_scrollbar
        Frame.__init__(self, root)

        self.row, self.col = 0, 0
        root.title("Sudoku Solver")
        self.pack(fill=BOTH, side=LEFT)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)

        clear_button = Button(self, text="Clear Answers", command=self.clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.hint_button = Button(self, text="Hint", command=self.hint)
        self.hint_button['state'] = 'disabled'
        self.hint_button.pack(fill=BOTH, side=BOTTOM)

        self.solve_button = Button(self, text="Solve", command=self.solve)
        self.solve_button['state'] = 'disabled'
        self.solve_button.pack(fill=BOTH, side=BOTTOM)

        new_puzzle_button = Button(self, text="New Puzzle", command=self.new_puzzle)
        new_puzzle_button.pack(fill=BOTH, side=BOTTOM)

        self.draw_grid()
        self.draw_puzzle()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)
        self.canvas.bind("<FocusOut>", self.clear_cursor)
        self.moves = []
        thread = Thread(target=self.async_solve_model)
        thread.start()
        root.mainloop()
        thread.join()

    def async_solve_model(self):
        pool = ThreadPool(processes=1)
        async_return = pool.apply_async(self.solve_model.solve, callback=self.solve_finished)
        self.moves = async_return.get()

    def draw_grid(self):
        for i in range(10):
            color = MAJOR_LINE_COLOR if i % 3 == 0 else MINOR_LINE_COLOR
            width = 2 if i % 3 == 0 else 1

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

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

        self.draw_cursor(CURSOR_COLOR)

    def draw_cursor(self, color):
        # TODO: hold shift to leave up old cursors
        self.canvas.delete("cursor")
        self.canvas.delete("error_indicator")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, tags="cursor", width=2)

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
            self.draw_cursor(CURSOR_COLOR)
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
        # check for any blank cells
        coords = self.user_board.check_for_blank_cells()
        print(coords)
        if coords:
            for coord in coords:
                self.draw_error_cell_highlight(coord, ERROR_CURSOR_COLOR)
            return

        # check the user model to see if any direct contradictions have been made accidentally and highglight them...
        coords = self.user_board.check_for_simple_contradiction()
        if coords and SudokuBoard.sector_lookup(coords[0][0], coords[0][1]) != SudokuBoard.sector_lookup(coords[1][0], coords[1][1]):
            self.draw_error_line_highlight(coords[0], coords[1], ERROR_CURSOR_COLOR)
            return
        elif coords:
            self.draw_error_sector(coords[0], coords[1], SudokuBoard.sector_lookup(coords[0][0], coords[0][1]), ERROR_CURSOR_COLOR)
            return

        # check if any possibilities can be easily removed.
        coords = self.user_board.check_for_poss_to_eliminate_easily()
        if coords and SudokuBoard.sector_lookup(coords[0][0], coords[0][1]) != SudokuBoard.sector_lookup(coords[1][0], coords[1][1]):
            self.draw_error_line_highlight(coords[0], coords[1], ERROR_CURSOR_COLOR, value=coords[2])
            return
        elif coords:
            self.draw_error_sector(coords[0], coords[1], SudokuBoard.sector_lookup(coords[0][0], coords[0][1]), ERROR_CURSOR_COLOR, value=coords[2])
            return

        # check the user model to see if any cells have missing possibilities


        # check and see if any cells are incorrect, possibilities or solutions; if so highlight them and say so.
        #   possibly attempt to explain why it is wrong?

        # grab the next move, see if the user has already figured it, if so, move on to the next move.
        #   dole out position, then operation, then number with a reason.

        # put a note in the console
        pass

    def solve(self):
        self.solve_button['state'] = 'disabled'
        if not self.moves:
            self.moves = self.solve_model.solve()
        self.moves = self.moves[::-1]
        self.solve_to_screen()

    def solve_to_screen(self):
        if len(self.moves) == 0:
            self.canvas.delete("cursor")
            self.write_to_console("SOLVED!")
            return
        else:
            move = self.moves.pop()
            self.row, self.col = move.get_pos()
            print(move)
            if move.get_operation() == NUMBER_SOLVE:
                self.draw_cursor(AI_SOLVING_CURSOR)
                poss_updates = self.user_board.code_set(move.get_pos()[0], move.get_pos()[1], move.get_number())
                if poss_updates:
                    self.moves.extend(poss_updates)
            else:
                self.draw_cursor(AI_POSS_REDUCING_CURSOR)
                self.user_board.remove_possibility(move.get_pos()[0], move.get_pos()[1], move.get_number())
            self.write_to_console(move.reason)
            self.draw_puzzle()

            self.after(50, self.solve_to_screen)

    def new_puzzle(self):
        # TODO
        # pull a puzzle from online
        pass

    def write_to_console(self, text):
        self.console.insert('end', text + '\n')
        self.console.see('end')

    def clear_cursor(self, event):
        self.row, self.col = -1, -1
        self.draw_cursor(CURSOR_COLOR)

    def solve_finished(self, moves):
        print('done')
        self.hint_button['state'] = 'normal'
        self.solve_button['state'] = 'normal'

    def draw_error_cell_highlight(self, coord, color):
        x0 = MARGIN + coord[1] * SIDE + 1
        y0 = MARGIN + coord[0] * SIDE + 1
        x1 = MARGIN + (coord[1] + 1) * SIDE - 1
        y1 = MARGIN + (coord[0] + 1) * SIDE - 1
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, tags="error_indicator", width=2)
    
    def draw_error_number_highlight(self, coord, color, value=None):
        if coord[0] >= 0 and coord[1] >= 0:
            if type(self.user_board.board[coord[0]][coord[1]]) is int:
                x0 = MARGIN + coord[1] * SIDE + 1
                y0 = MARGIN + coord[0] * SIDE + 1
                x1 = MARGIN + (coord[1] + 1) * SIDE - 1
                y1 = MARGIN + (coord[0] + 1) * SIDE - 1
                self.canvas.create_oval(x0, y0, x1, y1, outline=color, tags="error_indicator", width=3)
            else:
                x0 = MARGIN + coord[1] * SIDE + 14 * ((value - 1) % 3) + 5
                y0 = MARGIN + coord[0] * SIDE + 14 * ((value - 1) // 3) + 5
                x1 = x0 + SIDE / 3 - 5
                y1 = y0 + SIDE / 3 - 5
                self.canvas.create_line(x0, y0, x1, y1, tags="error_indicator", fill=color, width=1)
                self.draw_error_cell_highlight(coord, color)

    def draw_error_line_highlight(self, coord1, coord2, color, value=None):
        # TODO: hold shift to leave up old cursors
        self.canvas.delete("cursor")
        self.canvas.delete("error_indicator")
        self.draw_error_number_highlight(coord1, color, value=value)
        self.draw_error_number_highlight(coord2, color, value=value)
        # draw line between the two
        if coord1[0] == coord2[0]:
            #row
            print("row")
            left = None
            right = None
            if coord1[1] < coord2[1]:
                left = coord1
                right = coord2
            else:
                left = coord2
                right = coord1
            x0 = MARGIN + (left[1] + 1) * SIDE
            y0 = MARGIN + (left[0] + .5) * SIDE
            x1 = MARGIN + (right[1]) * SIDE
            y1 = MARGIN + (right[0] + .5) * SIDE
            self.canvas.create_line(x0, y0, x1, y1, tags="error_indicator", fill=color, width=1)
        elif coord1[1] == coord2[1]:
            # column
            print("column")
            top = None
            bottom = None
            if coord1[0] < coord2[0]:
                top = coord1
                bottom = coord2
            else:
                top = coord2
                bottom = coord1
            x0 = MARGIN + (top[1] + .5) * SIDE
            y0 = MARGIN + (top[0] + 1) * SIDE
            x1 = MARGIN + (bottom[1] + .5) * SIDE
            y1 = MARGIN + (bottom[0]) * SIDE + 1
            self.canvas.create_line(x0, y0, x1, y1, tags="error_indicator", fill=color, width=1)
        
    def draw_error_sector(self, coord1, coord2, sector, color, value=None):
        self.canvas.delete("cursor")
        self.canvas.delete("error_indicator")
        self.draw_error_number_highlight(coord1, color, value=value)
        self.draw_error_number_highlight(coord2, color, value=value)
        self.draw_error_sector_highlight(sector, color)

    def draw_error_sector_highlight(self, sector, color):
        x0 = MARGIN + (sector % 3) * SECTOR
        y0 = MARGIN + (sector // 3) * SECTOR
        x1 = x0 + SECTOR
        y1 = y0 + SECTOR
        self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=2, tags="error_indicator")

