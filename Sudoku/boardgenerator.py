from sudokusolver import solve, validity, find
from sorted_solver import sort, sorted_solve
import random, copy, time

# Complete board template
board_template = [[7, 4, 6, 9, 5, 8, 1, 2, 3], [8, 9, 2, 3, 1, 6, 7, 4, 5], [5, 3, 1, 7, 2, 4, 9, 8, 6], [9, 2, 5, 6, 7, 3, 8, 1, 4], [6, 8, 7, 1, 4, 9, 3, 5, 2], [4, 1, 3, 2, 8, 5, 6, 9, 7], [3, 6, 8, 4, 9, 2, 5, 7, 1], [1, 5, 4, 8, 3, 7, 2, 6, 9], [2, 7, 9, 5, 6, 1, 4, 3, 8]]

# Maps each coord on the board
def mapping(rows, cols):
    coords = []
    for row in range(rows):
        for col in range(cols):
            coord = (row, col)
            coords.append(coord)

    # Returns 81 coords
    return coords

# Swaps two lists
def swap(board, i, j):
    if i != j:
        board[i], board[j] = board[j], board[i]

# Shuffles rows within 3 rows
def row_shuffle(board):
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

# Shuffles board template to generate new board
def generate_full(board):
    row_shuffle(board)

    # 50/50 chance to rotate board
    if random.randint(0,1):
        board = [[i[j] for i in board] for j in range(9)]
    
    row_shuffle(board)
    return board

# Checks if current board has more than 1 solution
def solve_for_more(board, row, col):
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

# Generates sudoku board with 0s from a valid full board
def generate_sudoku(board, difficulty):
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