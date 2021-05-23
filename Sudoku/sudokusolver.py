def solve(board):
    '''
    Solves the board recursively.

    Returns True if board is solvable, and False if unsolvable.
    '''
    # Break condition for recursion
    if find(board):
        row, col = find(board)
    else:
        return True

    # From 1 to 9, try to fit a number and call solve again on the updated board
    for i in range(1, 10):
        if validity(board, row, col, i):
            board[row][col] = i

            # If num is valid, continue on valid board, until path ends
            if solve(board):
                return True

            # If path ends, backtrack to previous working path
            board[row][col] = 0
    
    # Returns false is no valid number, allows for backtracking
    return False

def check_row(board, col, num):
    '''
    Checks row for same number.

    Returns True or False accordingly.
    '''
    for i in range(9):
        if board[i][col] == num:
            return False
    return True

def check_col(board, row, num):
    '''
    Checks col for same number.

    Returns True or False accordingly.
    '''
    for i in range(9):
        if board[row][i] == num:
            return False
    return True

def check_box(board, row, col, num):
    '''
    Checks 3x3 box for same number.

    Returns True or False accordingly.
    '''
    for i in range(3):
        for j in range(3):
            if board[row+i][col+j] == num:
                return False
    return True

def validity(board, row, col, num):
    '''
    Using check_row, check_col, check_box, determine validity of number entered on a specific coordinate in a board.

    Returns True or False accordingly.
    '''
    box_row = row - row % 3
    box_col = col - col % 3
    return check_row(board, col, num) and check_col(board, row, num) and check_box(board, box_row, box_col, num)

def find(board):
    '''
    Returns the coordinates of an empty spot in the board.

    Returns False if board is filled.
    '''
    # Returns an x,y coord if 0 is found on board
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j

    # Returns false if board is filled
    return None