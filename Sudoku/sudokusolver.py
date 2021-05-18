# Solves the board
def solve(bo):
    # Break condition for recursion
    if find(bo):
        row, col = find(bo)
    else:
        return True

    # From 1 to 9, try to fit a number and call solve again on the updated board
    for i in range(1, 10):
        if validity(bo, row, col, i):
            bo[row][col] = i

            # If num is valid, continue on valid board, until path ends
            if solve(bo):
                return True

            # If path ends, backtrack to previous working path
            bo[row][col] = 0
    
    # Returns false is no valid number, allows for backtracking
    return False

def check_row(bo, col, num):
    for i in range(9):
        if bo[i][col] == num:
            return False
    return True

def check_col(bo, row, num):
    for i in range(9):
        if bo[row][i] == num:
            return False
    return True

def check_box(bo, row, col, num):
    for i in range(3):
        for j in range(3):
            if bo[row+i][col+j] == num:
                return False
    return True

# Checks all criterias
def validity(bo, row, col, num):
    box_row = row - row % 3
    box_col = col - col % 3
    return check_row(bo, col, num) and check_col(bo, row, num) and check_box(bo, box_row, box_col, num)

# Finds an empty square in the board
def find(bo):
    # Returns an x,y coord if 0 is found on board
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                return i, j

    # Returns false if board is filled
    return None

def sudoku(bo):
    if solve(bo):
        print(bo)
    else:
        print("This board is invalid and unsolvable.")