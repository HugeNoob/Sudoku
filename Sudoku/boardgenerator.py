from sudokusolver import solve, validity, find
import random
import copy

# Empty board template
board = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]

# Maps each coord on the board
def mapping(rows, cols):
    coords = []
    for row in range(rows):
        for col in range(cols):
            coord = (row, col)
            coords.append(coord)

    # Returns 81 coords
    return coords

# Generates a full valid sudoku board
def generate_full(board):
    coords = mapping(9,9)

    for i in range(81):
        # Finds random coord
        coords_index = random.randint(0, len(coords) - 1)
        row, col = curr_coord = coords[coords_index]
        
        # Fills coord with valid num
        temp_board = copy.deepcopy(board)
        for val in range(1,10):

            if validity(temp_board, row, col, val):
                temp_board[row][col] = val
                
                if solve(temp_board):
                    board[row][col] = val
                    break
        coords.remove(curr_coord)
            
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

        if solve(temp_board):
            solutions += 1
        
        if solutions > 1:
            break
        
    return solutions

# Generates sudoku board with 0s from a valid full board
def generate_sudoku(board):
    # Generates map coords
    coords = mapping(9,9)
    
    # 65 is honestly an arbitrary number to increase efficiency
    for i in range(60):

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



#test_board = [[7, 4, 6, 9, 5, 8, 1, 2, 3], [8, 9, 2, 3, 1, 6, 7, 4, 5], [5, 3, 1, 7, 2, 4, 9, 8, 6], [9, 2, 5, 6, 7, 3, 8, 1, 4], [6, 8, 7, 1, 4, 9, 3, 5, 2], [4, 1, 3, 2, 8, 5, 6, 9, 7], [3, 6, 8, 4, 9, 2, 5, 7, 1], [1, 5, 4, 8, 3, 7, 2, 6, 9], [2, 7, 9, 5, 6, 1, 4, 3, 8]]
#print(generate_sudoku(test_board))
#print(generate_full(board))