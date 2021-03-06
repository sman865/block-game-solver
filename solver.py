#!/usr/bin/env python3

import sys
from tkinter import *

###############################################################################
# GLOBAL VARIABLES
###############################################################################
esc = "\033["
clear        = esc + "2J"
reset_cursor = esc + "H"
reset        = esc + "0m"
bold         = esc + "1m"
underline    = esc + "4m"
red          = esc + "31m"
green        = esc + "32m"
yellow       = esc + "33m"
blue         = esc + "34m"
azul         = esc + "34m"
purple       = esc + "35m"
cyan         = esc + "36m"
white        = esc + "37m"
#block       = u"\u019f"  # for cli, could replace output[<var>]["char"]

# Represent colors. Might make life easier.
w = "w"
b = "b"
output = { 'w'  : { "color" : white,         "char" : "@" }
          ,'b'  : { "color" : reset,         "char" : " " }
          ,'r'  : { "color" : red,           "char" : "@" }
          ,'g'  : { "color" : green,         "char" : "@" }
          ,'y'  : { "color" : yellow,        "char" : "@" }
          ,'a'  : { "color" : azul,          "char" : "@" }
          ,'p'  : { "color" : purple,        "char" : "@" }
          ,'c'  : { "color" : cyan ,         "char" : "@" }
          ,'br' : { "color" : bold + red,    "char" : "X" }
          ,'bg' : { "color" : bold + green,  "char" : "X" }
          ,'by' : { "color" : bold + yellow, "char" : "X" }
          ,'ba' : { "color" : bold + azul,   "char" : "X" }
          ,'bp' : { "color" : bold + purple, "char" : "X" }
          ,'bc' : { "color" : bold + cyan,   "char" : "X" }
         }
colors = ( 'b', 'r', 'g', 'y', 'a', 'p', 'c', 'br', 'bg', 'by', 'ba', 'bp', 'bc', 'w' )
blank = -1
unusable = 0

# Generate sequence of colors for the gui to use when it draws blocks.
gui_colors = [ "#000000" ] # index 0 is used with the "unusable" variable
base_hex   = ["00", "8f", "ff"]
blacklist  = ["000000", "ffffff"]
for a in base_hex:
    for b in base_hex:
        for c in base_hex:
            color = c + b + a
            if color not in blacklist:
                gui_colors.extend(["#" + color])
gui_colors.extend(["#ffffff"]) # if not enough pieces are entered, blank spaces
                               # will be white since 'blank' is -1.

# Not descriptive names. Oh well. Represent a board's max X and Y bounds.
X = 0
Y = 0
sq_len = 10

placed_pieces = 1
all_pieces = [] # just list of coords
piece_list = () # actual Piece objects
window = Tk()
width  = IntVar()
height = IntVar()
board_grid = []
board_grid_buttons = []

# pre-set pieces to make life easier for user hopefully.
standard_values = []
standard_pieces = (
     {'row' : 1, 'col' : 0, 'coords' : ((0,0),)}
    ,{'row' : 1, 'col' : 1, 'coords' : ((0,0),(1,0))}
    ,{'row' : 1, 'col' : 2, 'coords' : ((0,0),(1,0),(2,0))}
    ,{'row' : 1, 'col' : 3, 'coords' : ((0,0),(1,0),(2,0),(3,0))}
    ,{'row' : 2, 'col' : 0, 'coords' : ((0,0),(0,1),(1,0),(1,1))}
    ,{'row' : 2, 'col' : 1, 'coords' : ((0,0),(0,1))}
    ,{'row' : 2, 'col' : 2, 'coords' : ((0,0),(0,1),(0,2))}
    ,{'row' : 2, 'col' : 3, 'coords' : ((0,0),(0,1),(0,2),(0,3))}
    ,{'row' : 3, 'col' : 0, 'coords' : ((0,0),(0,1),(1,0))}
    ,{'row' : 3, 'col' : 1, 'coords' : ((0,0),(1,1),(1,0))}
    ,{'row' : 3, 'col' : 2, 'coords' : ((0,0),(0,1),(1,1))}
    ,{'row' : 3, 'col' : 3, 'coords' : ((1,1),(0,1),(1,0))}
    ,{'row' : 4, 'col' : 0, 'coords' : ((0,0),(0,1),(0,2),(1,1))}
    ,{'row' : 4, 'col' : 1, 'coords' : ((1,0),(1,1),(1,2),(0,1))}
    ,{'row' : 4, 'col' : 2, 'coords' : ((1,0),(0,1),(1,1),(2,1))}
    ,{'row' : 4, 'col' : 3, 'coords' : ((0,0),(1,0),(2,0),(1,1))}
    ,{'row' : 5, 'col' : 0, 'coords' : ((1,0),(1,1),(0,1),(0,2))}
    ,{'row' : 5, 'col' : 1, 'coords' : ((0,0),(0,1),(1,1),(1,2))}
    ,{'row' : 5, 'col' : 2, 'coords' : ((1,0),(2,0),(0,1),(1,1))}
    ,{'row' : 5, 'col' : 3, 'coords' : ((0,0),(1,0),(1,1),(2,1))}
    ,{'row' : 6, 'col' : 0, 'coords' : ((0,0),(1,0),(0,1),(0,2))}
    ,{'row' : 6, 'col' : 1, 'coords' : ((0,0),(1,0),(1,1),(1,2))}
    ,{'row' : 6, 'col' : 2, 'coords' : ((0,0),(0,1),(0,2),(1,2))}
    ,{'row' : 6, 'col' : 3, 'coords' : ((1,0),(1,1),(1,2),(0,2))}
    ,{'row' : 7, 'col' : 0, 'coords' : ((0,0),(1,0),(2,0),(0,1))}
    ,{'row' : 7, 'col' : 1, 'coords' : ((0,0),(1,0),(2,0),(2,1))}
    ,{'row' : 7, 'col' : 2, 'coords' : ((0,0),(0,1),(1,1),(2,1))}
    ,{'row' : 7, 'col' : 3, 'coords' : ((2,0),(0,1),(1,1),(2,1))}
    ,{'row' : 8, 'col' : 0, 'coords' : ((1,0),(2,0),(1,1),(0,1),(0,2))}
    ,{'row' : 8, 'col' : 1, 'coords' : ((0,0),(1,0),(1,1),(2,1),(2,2))}
    ,{'row' : 8, 'col' : 2, 'coords' : ((0,0),(0,1),(1,1),(1,2),(2,2))}
    ,{'row' : 8, 'col' : 3, 'coords' : ((0,2),(1,1),(1,2),(2,0),(2,1))}
    ,{'row' : 9, 'col' : 0, 'coords' : ((0,2),(1,2),(1,1),(1,0),(2,0))}
    ,{'row' : 9, 'col' : 1, 'coords' : ((0,0),(1,0),(1,1),(1,2),(2,2))}
    ,{'row' : 9, 'col' : 2, 'coords' : ((0,0),(0,1),(1,1),(2,1),(2,2))}
    ,{'row' : 9, 'col' : 3, 'coords' : ((0,2),(0,1),(1,1),(2,1),(2,0))}
    )

there_are_more_pieces = False
butts = []
blank_grid = []
canceled = False

###############################################################################
# MAIN
###############################################################################
def main(args):

    global all_pieces
    global sq_len

    #
    # First things first, get the size of the board.
    #
    label = Label(window, text="Enter the board size:")
    label.grid(row=0, columnspan=2)

    width_label  = Label(window, text="Width:")
    height_label = Label(window, text="Height:")
    width_label.grid(row=1, column=0)
    height_label.grid(row=2, column=0)

    width_entry  = Entry(window, validate="key")
    height_entry = Entry(window, validate="key")
    width_entry.grid(row=1, column=1)
    height_entry.grid(row=2, column=1)

    done_button = Button(window, text="Done",
                         command= lambda: get_width_and_height(width_entry,
                                                      height_entry))
    done_button.grid(row=3, columnspan=2)

    window.mainloop()

    clear_window()

    #
    # Next, let the user click on cells that aren't playable.
    #

    label = Label(window, text="Click on cells that are unusable:")
    label.grid(row=0)

    # This will be updated to save values that are not playable.
    global board_grid
    global board_grid_buttons
    board_grid = [[blank for a in range(int(width))] for b in range(int(height))]

    frame = Frame(window)
    frame.grid(row=1)

    for a in range(int(height)):
        tmp = []
        for b in range(int(width)):
            curr_button = Button(frame, command = lambda curr_row=b, curr_col=a
                                 : toggleCell(frame, curr_row, curr_col))
            curr_button.grid(row=a, column=b)
            tmp.extend([curr_button])
        board_grid_buttons.append(tmp)

    done_button = Button(window, text="Done", command= lambda: quit_window())
    done_button.grid(row=2)

    window.mainloop()

    #
    # Next, let the user choose some pieces that are common to most boards.
    #

    global standard_values # just to remind us what we're dealing with below.
    num = 0

    for piece in standard_pieces:
        standard_values.extend([0])

        frame = Frame(window, highlightbackground="blue", highlightthickness=1)
        frame.grid(row=piece['row'], column=piece['col'])

        canvas = coord_to_piece(frame, piece['coords'])
        canvas.grid(rowspan=3)

        display = StringVar()
        display.set(0)

        label = Label(frame, textvariable=display)
        label.grid(column=1)

        plus_butt  = Button(frame, text="+", command=lambda d=display, n=num:
                                            standard_plus(d, n))
        minus_butt = Button(frame, text="-", command=lambda d=display, n=num:
                                            standard_minus(d, n))
        plus_butt.grid(row=1, column=1)
        minus_butt.grid(row=2, column=1)

        num += 1

    done_butt = Button(window, text="Done", command=quit_window)
    done_butt.grid(row=99, column=1, columnspan=2)

    window.mainloop()

    #
    # Next, let the user input any strange-looking pieces
    #

    global there_are_more_pieces
    there_are_more_pieces = True

    check_for_more_pieces()

    extra_pieces = []

    # Get input until there are no more pieces to enter.
    while there_are_more_pieces:

        global blank_grid
        global butts
        global canceled

        canceled = False

        blank_grid = [[blank for a in range(sq_len) ] for b in range(sq_len)]
        butts = []

        label = Label(window, text="Enter the piece and BE SURE to align it with the NW corner.")

        frame = Frame(window)

        # Create grid of blank buttons
        for y in range(sq_len):
            tmp_list = []
            for x in range(sq_len):
                tmp_butt = Button(frame, command = lambda a=x, b=y: toggle_button_grid(frame, a, b))
                tmp_butt.grid(row=y, column=x)
                tmp_list.extend([tmp_butt])
            butts.append(tmp_list)

        done_butt = Button(window, text="Done", command=quit_window)
        done_butt.grid(row=2, column=0)

        cancel_butt = Button(window, text="Cancel", command=cancel_input, fg="red")
        cancel_butt.grid(row=2, column=1)

        label.grid(row=0, columnspan=2)
        frame.grid(row=1, columnspan=2)

        window.mainloop()

        # Convert user's selection into coordinates
        curr_piece = ()
        for y, row in enumerate(blank_grid):
            for x, cell in enumerate(row):
                if cell != blank:
                    curr_piece += ((x,y),)

        if not canceled:
            extra_pieces.append(curr_piece)

        check_for_more_pieces()

    # User is done inputting pieces, add to all_pieces. These are more likely
    # to be large pieces, so we might have better performance if they're added
    # first.
    for piece in extra_pieces:
        all_pieces.append(piece)

    # Add selected standard pieces to all_pieces
    for index, value in enumerate(standard_values):
        for i in range(value):
            all_pieces.append(standard_pieces[index]["coords"])

    # Convert to Pieces.
    global piece_list

    for piece in all_pieces:
        piece_list += (Piece(piece),)

    # Initialize internal classes
    all_p = Pieces(piece_list)
    board = Board(board_grid)

    # Set a few globals
    global X, Y
    X = board.getMaxX()
    Y = board.getMaxY()

    #
    # Strategy: do some kind of depth-first tree recursion stuff.
    #
    # 1. Call recursive method with the blank board and all pieces.
    # 2. Recursive method will find a spot for the 0th piece given to it, and
    #    then call itself with the updated board and pieces.
    # 3. If the successive piece can't be placed, return false and then place
    #    the current piece on the next possible block.
    # 4. Repeat until solution is found (return true).
    #
    if solve(board, all_p):
        print(board)
    else:
        print("NO SOLUTION FOUND")

    #
    # Display gui representation of the board.
    #
    sq_len = 20

    canvas = Canvas(window, width=sq_len*X+2*sq_len, height=sq_len*Y+2*sq_len)
    for y, row in enumerate(board.getData()):
        for x, value in enumerate(row):
            canvas.create_rectangle(x*sq_len + sq_len,
                                    y*sq_len + sq_len,
                                    x*sq_len + 2*sq_len, 
                                    y*sq_len + 2*sq_len, 
                                    fill=value_to_gui_color(value))

    canvas.grid()
    window.mainloop()

###############################################################################
# HELPER FUNCTIONS
###############################################################################
def solve(board, pieces):

    # Base case: when there are no pieces left to place.
    if pieces.isEmpty():
        return True

    piece = pieces.peek()
    
    for currY in range(Y):
        for currX in range(X):
            if board.can_fit(piece, currX, currY):

                board.place(piece, currX, currY, placed_pieces)
                save_piece = pieces.pop()

                if solve(board, pieces):
                    return True
                else:
                    board.remove(piece, currX, currY)
                    pieces.push(save_piece)
    return False
        
#
# Board values are stored as numbers but need to be converted for CLI output.
#  0 is reserved for 'unusable' so don't roll over to that
# -1 is reserved for 'blank' so don't use the last value
#
def piece_num_to_color(num):
    if num == 0 or num == -1:
        return colors[num]
    else:
        return colors[((int(num)-1) % (len(colors)-2))+1]

#
# Same idea as above function.
#  0 is reserved for 'unusable' so don't roll over to that
# -1 is reserved for 'blank' so don't use the last value
#
def value_to_gui_color(value):
    if value == 0 or value == -1:
        return gui_colors[value]
    else:
        # only returns values of an array that are not at the ends.
        return gui_colors[((int(value)-1) % (len(gui_colors)-2))+1]

#
# Adjusts the global count of pieces played.
#
def pieceNumber(value):
    global placed_pieces
    placed_pieces += value

#
# Sets global variables used in main.
#
def get_width_and_height(w_e, h_e):
    global width
    global height

    width  = w_e.get()
    height = h_e.get()
    quit_window()

#
# removes button and switches its color from white to black or vice versa.
#
def toggleCell(frame, currX, currY):
    global board_grid
    global board_grid_buttons

    # Just to make it a little cleaner...
    buttons = board_grid_buttons
    values  = board_grid

    buttons[currY][currX].destroy()

    # Switch button from white to black
    if values[currY][currX] == blank:
        buttons[currY][currX] = Button(frame, text = 'X', bg = "black",
                                       activebackground="black",
                                       command = lambda row=currY, col=currX:
                                       toggleCell(frame, col, row))
        values[currY][currX] = unusable

    # Switch button from black to white
    else:
        buttons[currY][currX] = Button(frame,
                                       command = lambda row=currY, col=currX:
                                       toggleCell(frame, col, row))
        values[currY][currX] = blank

    buttons[currY][currX].grid(row=currY, column=currX)

#
# Takes a list of x,y coordinates and creates gui rectangles based on them.
#
def coord_to_piece(frame, coord_list):
    ret = Canvas(frame, width=60, height=50)

    for coord in coord_list:
        x = coord[0]
        y = coord[1]

        ret.create_rectangle(sq_len*x + sq_len,
                             sq_len*y + sq_len,
                             sq_len*x + 2*sq_len,
                             sq_len*y + 2*sq_len,
                             fill="yellow")
    return ret

#
# Increments pre-set pieces
#
def standard_plus(display, index):
    global standard_values
    standard_values[index] += 1
    display.set(standard_values[index])

#
# Decrements pre-set pieces
#
def standard_minus(display, index):
    global standard_values
    if standard_values[index] > 0:
        standard_values[index] -= 1
        display.set(standard_values[index])

#
# Prompts user for more input
#
def check_for_more_pieces():
    label = Label(window, text="Are there any more pieces to enter?")
    yes_butt = Button(window, text="Yes", command=lambda: more_pieces(1))
    no_butt  = Button(window, text="No", command=lambda: more_pieces(0))

    label.grid(row=0)
    yes_butt.grid(row=1)
    no_butt.grid(row=2)

    window.mainloop()
    return

# Helper to above
def more_pieces(val):
    if not val:
        global there_are_more_pieces
        there_are_more_pieces = False
    quit_window()
    return

#
# For use in letting user input specific piece. Changes button from white to
# black and vice-versa.
#
def toggle_button_grid(frame, x, y):

    butts[y][x].destroy()
    if blank_grid[y][x] == blank:
        tmp = Button(frame, command = lambda a=x, b=y: toggle_button_grid(frame, a, b),
                     bg="black", activebackground="black", text="X")
        blank_grid[y][x] = unusable
    else:
        tmp = Button(frame, command = lambda a=x, b=y: toggle_button_grid(frame, a, b))
        blank_grid[y][x] = blank
    tmp.grid(row=y, column=x)
    butts[y][x] = tmp

# Clears widgets
def clear_window():
    for widget in window.grid_slaves():
        widget.destroy()

# Kills a window
def quit_window():
    clear_window()
    window.quit()

def cancel_input():
    global canceled
    canceled = True
    quit_window()

###############################################################################
# BACK END CLASSES
###############################################################################

#
# Board class: represents a game board which a player has to fill in.
#
class Board:

    #######################################
    # OVERRIDES AND BASIC BOARD FUNCTIONS #
    #######################################

    # Relies on the user entering a fully formed rectangle with blank/dead
    # cells. Might be a good idea to make sure all rows are the same size.
    def __init__(self, board_list):

        # Set max X and Y values.
        self.__maxY = len(board_list)
        longest = 0
        for row in board_list:
            longest = len(row) if len(row) > longest else longest
        self.__maxX = longest

        self.__data = board_list

    def __str__(self):
        ret = ""
        for row in self.__data:
            for cell in row:
                color = piece_num_to_color(cell)
                ret += output[color]["color"] + output[color]["char"] + reset
            ret += "\n"
        return ret

    # Return longest row
    def getMaxX(self):
        return self.__maxX

    # Return number of columns
    def getMaxY(self):
        return self.__maxY
        return len(self.__data)

    def getData(self):
        return self.__data

    ###########################
    # PRIMARY BOARD FUNCTIONS #
    ###########################

    def can_fit(self, piece, currX, currY):
        for coords in piece.getData():
            cumulativeX = currX + coords[0]
            cumulativeY = currY + coords[1]

            if (cumulativeX >= self.__maxX or
                cumulativeY >= self.__maxY or
                self.__data[cumulativeY][cumulativeX] != blank):
                return False

        return True

    def place(self, piece, currX, currY, number):
        for coords in piece.getData():
            cumulativeX = currX + coords[0]
            cumulativeY = currY + coords[1]
            self.__data[cumulativeY][cumulativeX] = number
        pieceNumber(1)

    def remove(self, piece, currX, currY):
        for coords in piece.getData():
            cumulativeX = currX + coords[0]
            cumulativeY = currY + coords[1]
            self.__data[cumulativeY][cumulativeX] = blank
        pieceNumber(-1)

#
# Pieces class: Represents a list of pieces
#
class Pieces:

    # pieces_list is tuple of Pieces.
    def __init__(self, pieces_list):
        self.__data = pieces_list

    def __str__(self):
        ret = ""
        for piece in self.__data:
            ret += str(piece.getData())
            ret += "\n"
        return ret

    def peek(self):
        return self.__data[0]

    def pop(self):
        ret = self.__data[0]
        self.__data = self.__data[1:]
        return ret

    def push(self, piece):
        self.__data = (piece,) + self.__data

    # "return if self.__data"?
    def isEmpty(self):
        if self.__data:
            return False
        else:
            return True


#
# Piece class: Represents a single piece which needs to fit onto a board.
#              Is really just a list of points which will be used as offsets.
#
class Piece:

    # coord_list is tuple of x, y coordinates saved as a tuple.
    def __init__(self, coord_list):
        self.__data = coord_list

    def __str__(self):
        return str(self.__data)

    def getData(self):
        return self.__data

###############################################################################
# END CODE
###############################################################################

if __name__ == "__main__":
    #f = open('debug.txt', 'w')
    #f.close()
    main(sys.argv)
