from sudokusolver import solve, validity, find
from sorted_solver import sort, sorted_solve
import random, copy, time

# Complete board template
board_template = [[7, 4, 6, 9, 5, 8, 1, 2, 3], [8, 9, 2, 3, 1, 6, 7, 4, 5], [5, 3, 1, 7, 2, 4, 9, 8, 6], [9, 2, 5, 6, 7, 3, 8, 1, 4], [6, 8, 7, 1, 4, 9, 3, 5, 2], [4, 1, 3, 2, 8, 5, 6, 9, 7], [3, 6, 8, 4, 9, 2, 5, 7, 1], [1, 5, 4, 8, 3, 7, 2, 6, 9], [2, 7, 9, 5, 6, 1, 4, 3, 8]]

def mapping(rows, cols):
    ''' 
    Takes in integers rows and cols, and returns a list of coordinates in a row x col grid.
    '''
    coords = []
    for row in range(rows):
        for col in range(cols):
            coord = (row, col)
            coords.append(coord)

    # Returns 81 coords
    return coords

def swap(board, i, j):
    '''
    Takes two lists in the board and swaps their positions.
    '''
    if i != j:
        board[i], board[j] = board[j], board[i]

def row_shuffle(board):
    '''
    Returns shuffled board.

    Rows are shuffled within their groups of three rows — 0 to 2, 3 to 5, 6 to 8.
    The shuffling is done by choosing two random rows and swapping them.
    '''
    # Top
    i, j = random.randint(0,2), random.randint(0,2)
    swap(board, i, j)

    # Middle
    i, j = random.randint(3,5), random.randint(3,5)
    swap(board, i, j)

    # Bottom
    i, j = random.randint(6,8), random.randint(6,8)
    swap(board, i, j)

    return board

def generate_full(board):
    '''
    Shuffles and returns a full, valid board template to generate a new, full, valid board.

    Initially, rows are shuffled with row_shuffle.
    Then, there is a 50% chance to rotate the board 90 degrees.
    Lastly, rows are shuffled again with row_shuffle. Note that if rotation is done, cols will then act as rows.
    '''
    row_shuffle(board)

    # 50/50 chance to rotate board
    if random.randint(0,1):
        board = [[i[j] for i in board] for j in range(9)]
    
    row_shuffle(board)
    return board

def solve_for_more(board, row, col):
    '''
    Checks if current board has more than 1 solution.

    Returns 1 if only 1 solution.
    Returns 2 if more than 1 solution.
    '''
    valid_vals = []
    solutions = 0

    # Finds possible values
    for i in range(1, 10):
        if validity(board, row, col, i):
            valid_vals.append(i)

    # Tests each value
    for val in valid_vals:
        temp_board = copy.deepcopy(board)
        temp_board[row][col] = val

        if sorted_solve(temp_board, sort(temp_board)):
            solutions += 1
        
        if solutions > 1:
            break
        
    return solutions

def generate_sudoku(board, difficulty):
    '''
    Generates and returns a partially filled sudoku board from a full, valid board.

    Takes in an integer difficulty, and analyses a corresponding number of random coordinates to determine if they can be removed.
    '''
    # Generates map coords
    coords = mapping(9,9)

    # 45 for easy, 55 for medium, 65 for hard
    for i in range(difficulty):

        # Finds random coord
        coords_index = random.randint(0, len(coords) - 1)
        row, col = curr_coord = coords[coords_index]

        # Sets the coord in a board copy to 0
        temp_board = copy.deepcopy(board)
        temp_board[row][col] = 0

        # If multiple sols, value stays, remove coord
        if solve_for_more(temp_board, row, col) > 1:
            coords.remove(curr_coord)

        # If single, replace value at coord with 0, remove coord
        else:
            board[row][col] = 0
            coords.remove(curr_coord)

    return board
    