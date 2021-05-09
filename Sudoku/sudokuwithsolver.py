import pygame, time
from sudokusolver import solve, validity, find

# Initialise pygame
pygame.init()

"""Plan is for the sudoku board to be 500x500 with 200 pixels below for instructions & time """
# Create the screen
WIDTH, HEIGHT = 500, 500
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
cube_side = 500/9

class Grid:
    board = [[0, 0, 0, 9, 5, 8, 0, 0, 0], [0, 0, 2, 0, 0, 6, 7, 0, 0], [0, 3, 0, 7, 0, 0, 0, 8, 6], [9, 0, 5, 0, 0, 0, 8, 0, 0], [0, 0, 7, 0, 0, 0, 0, 5, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0], [3, 0, 0, 0, 9, 0, 0, 0, 0], [0, 0, 4, 0, 3, 0, 0, 6, 0], [2, 0, 9, 5, 0, 0, 0, 0, 0]]

    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = self.board
        self.selected = None
        self.screen = screen
    
    def update_model(self):
        # Model is temp board that is sent for analysis, not actual board. set this as actual board when confirmed valid.
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def draw_board(self, screen):
        # Draw bolder lines
        screen.fill(WHITE)
        pygame.draw.rect(screen, (BLACK), pygame.Rect(0, 0, WIDTH, HEIGHT), width = 10)

        for i in range(3):
            pygame.draw.line(screen, (BLACK), (0, cube_side*3*(i+1)), (WIDTH, cube_side*3*(i+1)), width = 5)
            pygame.draw.line(screen, (BLACK), (cube_side*3*(i+1), 0), (cube_side*3*(i+1), HEIGHT), width = 5)

        # Draw thinner cube lines
        for i in range(self.rows):
            for j in range(self.cols):
                # Horizontal lines
                pygame.draw.line(screen, (BLACK), (0, cube_side*(i+1)), (WIDTH, cube_side*(i+1)))
                # Vertical lines
                pygame.draw.line(screen, (BLACK), (cube_side*(i+1), 0), (cube_side*(i+1), HEIGHT))

        # Fills cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(screen)

    def place(self, val):
        # Sets actual value when confirmed
        row, col = self.selected
        if self.cubes[row][col].value == 0:

            if validity(self.board, row, col, val):
                self.cubes[row][col].set(val)
                self.update_model()

                if solve(self.model):
                    return True

                else:
                    self.cubes[row][col].set(0)
                    self.cubes[row][col].set_temp(0)
                    self.update_model()
                    return False

    def temp_place(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def select(self, row, col):
        # Selects square that is clicked
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        # Clears currently selected cube
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """get_pos() -> (x, y)
            param: pos(x, y)
            output: (x, y)
        """
        # Returns pos of cube clicked on
        if pos[0] < self.width and pos[1] < self.height:
            x = pos[0] // cube_side
            y = pos[1] // cube_side
            return (int(y), int(x))
        else:
            return None

    def isFinished(self):
        # Checks if there are empty squares on board
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve_gui(self):
        self.update_model()
        if find(self.model):
            row, col = find(self.model)
        else:
            return True

        for i in range(1,10):
            if validity(self.model, row, col, i):
                self.cubes[row][col].set(i)
                self.update_model()
                self.cubes[row][col].draw_changes(self.screen, True)
                pygame.display.update()

                if self.solve_gui():
                    return True

                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_changes(self.screen, False)
                pygame.display.update()

        return False


        
class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    # Draws boxes and numbers
    def draw(self, screen):
        font = pygame.font.SysFont("comicsans", 40)
        
        # Row is actually the y coord while col is the x coord
        x = self.col * cube_side
        y = self.row * cube_side

        # Temp nums
        if self.temp != 0 and self.value == 0:
            txt = font.render(str(self.temp), True, (169,169,169))
            screen.blit(txt, (x+5, y+5))
        # Confirmed nums
        elif self.value != 0:
            txt = font.render(str(self.value), True, (BLACK))
            screen.blit(txt, (x+(cube_side - txt.get_width())/2, y+(cube_side - txt.get_width())/2))

        # Draws red box if box selected
        if self.selected:
            pygame.draw.rect(screen, (RED), (x,y, cube_side, cube_side), 3)

    def draw_changes(self, screen, resolved):
        font = pygame.font.SysFont("comicsans", 40)

        x = self.col * cube_side
        y = self.row * cube_side

        # Fills cube white to cover previous num
        pygame.draw.rect(screen, (WHITE), (x,y, cube_side, cube_side), 0)
        
        # Fills in new number
        txt = font.render(str(self.value), True, (BLACK))
        screen.blit(txt, (x+(cube_side - txt.get_width())/2, y+(cube_side - txt.get_width())/2))

        if resolved:
            # Green if cube is filled with non-zero
            pygame.draw.rect(screen, (GREEN), (x,y, cube_side, cube_side), 3)
        else:
            # Red if backtracked and filled with zero
            pygame.draw.rect(screen, (RED), (x,y, cube_side, cube_side), 3)

    def set(self, val):
        # Sets locked value
        self.value = val

    def set_temp(self, val):
        # Sets temp value
        self.temp = val



# Other functions
def redraw_window(screen, board, time):
    screen.fill(WHITE)
    font = pygame.font.SysFont("comicsans", 40)
    # Draw board
    board.draw_board(screen)
    # Draw time
    txt = font.render("Time: " + format_time(time), True, (0,0,0))
    screen.blit(txt, (310, 540))

def format_time(secs):
    sec = secs%60
    minute = sec//60
    hour = minute//60

    if len(str(sec)) == 1:
        sec = "0" + str(sec)
    
    time = str(hour) + ":" + str(minute) + ":" + str(sec)
    return time

def main():
    run = True
    key = None
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
    pygame.display.set_caption("Sudoku")
    start = time.time()
    board = solving_board = Grid(9, 9, WIDTH, HEIGHT, screen)

    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                        key = None

                        if board.isFinished():
                            print("Game Over")
                            run = False
                            
                if event.key == pygame.K_SPACE:
                    board.solve_gui()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.temp_place(key)

        redraw_window(screen, board, play_time)
        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()