#solves the board
def solve(bo):
    #break because this is recursive
    if find(bo):
        row, col = find(bo)
        print(row, col)
    else:
        return True


    #from 1 to 9, try to fit a number and call solve again on the updated board
    for i in range(1, 10):
        if validity(bo, row, col, i):
            bo[row][col] = i
            print(bo)

            if solve(bo):
                return True

            bo[row][col] = 0
    
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

#checks all criterias
def validity(bo, row, col, num):
    box_row = row - row % 3
    box_col = col - col % 3
    return check_row(bo, col, num) and check_col(bo, row, num) and check_box(bo, box_row, box_col, num)

#finds an empty square in the board
def find(bo):
    #returns an x,y coord if 0 is found on board
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                return i, j

    #returns false if board is filled
    return False


def sudoku(bo):
    if solve(bo):
        print(bo)
    else:
        print("This board is invalid and unsolvable.")

board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]]

sudoku(board)