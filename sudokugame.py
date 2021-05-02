import pygame
from sudokusolver import solve, validity

#initialise pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Sudoku")
WHITE = (255,255,255)
FPS = 30

def draw_window():
    screen.fill(WHITE)
    pygame.display.update()




def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        draw_window()

    pygame.quit()




if __name__ == "__main__":
    main()