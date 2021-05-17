from sudokusolver import validity
import time
board = [[7, 0, 6, 0, 5, 8, 1, 0, 3], [8, 9, 0, 3, 0, 0, 0, 4, 5], [5, 3, 0, 7, 2, 4, 0, 8, 6], [0, 0, 5, 6, 7, 0, 8, 0, 4], [6, 0, 0, 0, 4, 9, 0, 5, 2], [0, 0, 0, 2, 0, 0, 6, 0, 0], [0, 0, 0, 4, 9, 0, 0, 0, 1], [1, 0, 0, 8, 0, 7, 0, 6, 0], [2, 7, 0, 5, 6, 0, 0, 0, 8]]

def sort(board):
    sorted_dict = {8:[], 7:[], 6:[], 5:[], 4:[], 3:[], 2:[], 1:[]}
    empty_coords = []

    # Finds all empty coords
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_coords.append((i,j))

    # Rates coord according to info
    for coord in empty_coords:
        info = []
        coord_x = coord[1]
        coord_y = coord[0]
        
        # Scans row and col
        for val in range(9):
            info.append(board[val][coord_x])
            info.append(board[coord_y][val])

        # Scans box
        box_x = coord_x // 3
        box_y = coord_y // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                info.append(board[i][j])
        
        # Filter unique numbers
        info = set(info)
        info.remove(0)
        
        # Adds them to dict
        sorted_dict[len(info)].append(coord)
    
    return sorted_dict

# Finds the first coord in dict
def sorted_find(sorted_dict):
    for i in list(sorted_dict):

        # Deletes empty keys
        if len(sorted_dict[i]) != 0:
            return sorted_dict[i][0]
    return False

def sorted_solve(board, sorted_dict):
    # Finds a coord from sorted dict
    if sorted_find(sorted_dict):
        row, col = sorted_find(sorted_dict)
    else:
        print(board)
        return True

    for i in range(1,10):
        # If valid, change coord in dict to "filled", call func recursively on updated dict
        if validity(board, row, col, i):
            board[row][col] = i

            for key in list(sorted_dict.keys()):
                if len(sorted_dict[key]) != 0:
                    first_key = key
                    break

            sorted_dict[first_key].remove((row, col))

            if sorted_solve(board, sorted_dict):
                return True

            board[row][col] = 0
            sorted_dict[first_key].insert(0, (row,col))

    return False