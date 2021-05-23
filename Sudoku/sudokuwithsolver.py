from boardgenerator import generate_full, generate_sudoku, board_template
import pygame, copy, time
from sudokusolver import solve, validity, find

'''
This is the version with more functionalities and a board generator.
'''
# Initialise pygame
pygame.init()

# Create the screen
WIDTH, HEIGHT = 500, 500
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
cube_side = 500/9

class Grid:
    '''
    A class to represent an entire sudoku board.
    '''
    def __init__(self, board, rows, cols, width, height, screen):
        '''
        Parameters:
        -----------
        rows: int
            Number of rows in the board.
        cols: int
            Number of columns in the board.
        width: int
            Width of the pygame window.
        height: int
            Height of the pygame window.
        '''
        self.board = board
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = self.board
        self.selected = None
        self.screen = screen
    
    def update_model(self):
        '''
        Makes a model board which is a deep copy of the main board.
        '''
        # Model is temp board that is sent for analysis, not actual board. set this as actual board when confirmed valid.
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def draw_board(self, screen):
        '''
        Draws in all lines and calls cube.draw to draw numbers.
        '''
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
        '''
        Sets actual value if value is valid.
        '''
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
        '''
        Sets a temporary value.
        '''
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def select(self, row, col):
        '''
        Sets self.selected of all other cubes to False

        Sets self.selected of selected cube to True.
        '''
        # Selects square that is clicked
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        '''
        Clears all temporary values in currently selected cube.
        '''
        # Clears currently selected cube
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        '''
        Returns coordinates of cube clicked on.
        '''
        # Returns pos of cube clicked on
        if pos[0] < self.width and pos[1] < self.height:
            x = pos[0] // cube_side
            y = pos[1] // cube_side
            return (int(y), int(x))
        else:
            return None

    def isFinished(self):
        '''
        Returns True if board is complete, false otherwise.
        '''
        # Checks if there are empty squares on board
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve_gui(self):
        '''
        Solves the board and visualises the process with a GUI.
        '''
        # This line is just so the code doesn't hang
        pygame.event.get()

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
    '''
    A class to represent individual squares on a sudoku board.
    '''
    rows = 9
    cols = 9

    def __init__(self, value, row, col):
        '''
        Parameters:
        -----------
        value: int
            Correct and determined value of a square.
        row: int
            row that square is in.
        col: int
            column that square is in.
        '''
        self.value = value
        self.temp = []
        self.row = row
        self.col = col
        self.selected = False

    def draw(self, screen):
        '''
        Draws numbers and red box if selected.
        '''
        font = pygame.font.SysFont("comicsans", 50)
        small_font = pygame.font.SysFont("comicsans", 25)
        
        # Row is actually the y coord while col is the x coord
        x = self.col * cube_side
        y = self.row * cube_side

        # Temp nums
        if len(self.temp) != 0 and self.value == 0:
            x1, x2, x3 = x+4, x+22.5, x+41
            y1, y2, y3 = y+4, y+21, y+37
            for val in self.temp:
                txt = small_font.render(str(val), True, (169,169,169))
                if val == 1:
                    screen.blit(txt, (x1, y1))
                if val == 2:
                    screen.blit(txt, (x2, y1))
                if val == 3:
                    screen.blit(txt, (x3, y1))

                if val == 4:
                    screen.blit(txt, (x1, y2))
                if val == 5:
                    screen.blit(txt, (x2, y2))
                if val == 6:
                    screen.blit(txt, (x3, y2))

                if val == 7:
                    screen.blit(txt, (x1, y3))
                if val == 8:
                    screen.blit(txt, (x2, y3))
                if val == 9:
                    screen.blit(txt, (x3, y3))

        # Confirmed nums
        elif self.value != 0:
            txt = font.render(str(self.value), True, (BLACK))
            screen.blit(txt, (x+(cube_side - txt.get_width())/2, y+(cube_side - txt.get_width())/2))

        # Draws red box if box selected
        if self.selected:
            pygame.draw.rect(screen, (RED), (x,y, cube_side, cube_side), 3)

    def draw_changes(self, screen, resolved):
        '''
        Illustrates the solver process.

        Solved cubes are highlighted with a green box.
        '''
        font = pygame.font.SysFont("comicsans", 50)

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
        '''
        Sets locked value.
        '''
        self.value = val

    def set_temp(self, val):
        '''
        Sets temp value(s).
        '''
        if val not in self.temp and val != 0:
            self.temp.append(val)
        elif val == 0:
            self.temp = []

# Other functions
def redraw_window(screen, board, time):
    '''
    Calls other functions to draw pygame window.
    '''
    screen.fill(WHITE)
    font = pygame.font.SysFont("comicsans", 40)
    small_font = pygame.font.SysFont("comicsans", 20)
    # Draw board
    board.draw_board(screen)
    # Draw time
    txt = font.render("Time: " + format_time(time), True, BLACK)
    screen.blit(txt, (30, 540))
    # Draw esc message
    esc_txt = small_font.render("Press ESC to exit", True, BLACK)
    screen.blit(esc_txt, (380, 580))

def format_time(secs):
    '''
    Returns formatted time in H:M:S.
    '''
    sec = secs%60
    minute = secs//60
    hour = minute//60

    if len(str(sec)) == 1:
        sec = "0" + str(sec)
    
    time = str(hour) + ":" + str(minute) + ":" + str(sec)
    return time

# Difficulty settings
EASY = 45
MEDIUM = 55
HARD = 65

def draw_text(text, font, colour, screen, x, y):
    txt = font.render(text, True, colour)
    screen.blit(txt, (x, y))

def main_menu():
    '''
    Runs the main menu when called.

    Displayed on the menu are: Easy, Medium, Hard, Instructions
    '''
    run = True
    click = False
    pygame.display.set_caption("Sudoku Main Menu")
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
    screen.fill(WHITE)
    font = pygame.font.SysFont("comicsans", 40)
    pygame.display.update()

    while run:
        draw_text('main menu', font, BLACK, screen, 20, 20)
        
        mx, my = pygame.mouse.get_pos()

        # Forming buttons
        easy_button = pygame.Rect(150, 155, 200, 50)
        med_button = pygame.Rect(150, 225, 200, 50)
        hard_button = pygame.Rect(150, 295, 200, 50)
        instructions_button = pygame.Rect(150, 365, 200, 50)

        # Drawing buttons
        pygame.draw.rect(screen, BLACK, easy_button, width=3, border_radius=10)
        pygame.draw.rect(screen, BLACK, med_button, width=3, border_radius=10)
        pygame.draw.rect(screen, BLACK, hard_button, width=3, border_radius=10)
        pygame.draw.rect(screen, BLACK, instructions_button, width=3, border_radius=10)
        

        # Filling buttons
        txt = font.render('easy', True, BLACK)
        screen.blit(txt, ((250-txt.get_width()/2), (180-txt.get_height()/2)))

        txt = font.render('medium', True, BLACK)
        screen.blit(txt, ((250-txt.get_width()/2), (250-txt.get_height()/2)))

        txt = font.render('hard', True, BLACK)
        screen.blit(txt, ((250-txt.get_width()/2), (320-txt.get_height()/2)))
        
        txt = font.render('instructions', True, BLACK)
        screen.blit(txt, ((250-txt.get_width()/2), (390-txt.get_height()/2)))

        # Clicking buttons
        if easy_button.collidepoint((mx,my)):
            if click:
                game(EASY)
                screen.fill(WHITE)
                pygame.display.update()
        if med_button.collidepoint((mx,my)):
            if click:
                game(MEDIUM)
                screen.fill(WHITE)
                pygame.display.update()
        if hard_button.collidepoint((mx,my)):
            if click:
                game(HARD)
                screen.fill(WHITE)
                pygame.display.update()
        if instructions_button.collidepoint((mx,my)):
            if click:
                instructions()
                screen.fill(WHITE)
                pygame.display.update()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()

def instructions():
    '''
    Instructions page for sudoku game.
    '''
    run = True
    pygame.display.set_caption("Sudoku Instructions")
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
    screen.fill(WHITE)
    title_font = pygame.font.SysFont("comicsans", 40)
    body_font = pygame.font.SysFont("comicsans", 30)
    small_font = pygame.font.SysFont("comicsans",20)
    pygame.display.update()

    while run:
        # Title
        draw_text('Instructions', title_font, BLACK, screen, 20, 20)

        # Body
        draw_text('1. Temporary numbers will appear gray.', body_font, BLACK, screen, 20, 70)
        draw_text('2. To key in a number, ensure that the box only', body_font, BLACK, screen, 20, 100)
        draw_text('contains one temporary number before pressing', body_font, BLACK, screen, 20, 130)
        draw_text('ENTER.', body_font, BLACK, screen, 20, 160)
        draw_text('3. Only correct numbers are accepted.', body_font, BLACK, screen, 20, 190)
        draw_text('4. Press BACKSPACE to delete temporary', body_font, BLACK, screen, 20, 220)       
        draw_text('numbers.', body_font, BLACK, screen, 20, 250) 
        draw_text('5. Press SPACE to solve board.', body_font, BLACK, screen, 20, 280) 
        draw_text('6. Reload game if loading HARD takes too long.', body_font, BLACK, screen, 20, 310)

        # Small text
        draw_text('Press ESC to exit', small_font, BLACK, screen, 380, 580)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        pygame.display.update()

def game(difficulty):
    '''
    Runs the game with a newly generated sudoku board with difficulty specified by integer input.
    '''
    run = True
    key = None
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
    pygame.display.set_caption("Sudoku Game")

    # Loading screen
    screen.fill(WHITE)
    font = pygame.font.SysFont("comicsans", 30)
    txt = font.render("Loading... This may take a while for HARD.", True, BLACK)
    screen.blit(txt, (30, 560))
    pygame.display.update()

    '''Deep copy of template is to ensure game does not hang when difficulty modes are reloaded multiple times. 
    Hanging is due to passing a non-filled board_template into generate_sudoku, due to previous iterations, hence resulting in unintended difficulty levels.'''
    board_template_template = copy.deepcopy(board_template)
    sudoku_board = generate_sudoku(generate_full(board_template_template), difficulty)
    board = Grid(sudoku_board, 9, 9, WIDTH, HEIGHT, screen)
    start = time.time()
    
    while run:
        play_time = round(time.time() - start)
        redraw_window(screen, board, play_time)
        pygame.display.update()

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
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RETURN:
                    if board.selected == None:
                        key = None
                    else:
                        i, j = board.selected
                        if len(board.cubes[i][j].temp) == 1:
                            val = board.cubes[i][j].temp[0]
                            if board.place(val):
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

if __name__ == "__main__":
    main_menu()
    pygame.quit()