from tetris import Tetris
import pygame


if __name__ == "__main__":
    pygame.init()
    size = (width, height) = (1200, 800)
    screen1 = pygame.display.set_mode(size)
    clock1 = pygame.time.Clock()
    while True:
        game = Tetris(1)
        game.main(screen=screen1, clock=clock1)
    pygame.quit()