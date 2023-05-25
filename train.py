from tetris import Tetris
import pygame
import random


if __name__ == "__main__":
    pygame.init()
    size = (width, height) = (1360 / 2, 800)
    screen1 = pygame.display.set_mode(size)
    clock1 = pygame.time.Clock()
    ai_clock = pygame.time.Clock()
    ai_running = True
    ai_game = Tetris(1)

    ai_timer = 0
    flag = False
    while ai_running:

        ai_game.update_board()
        ai_game.update_next_board()
        ai_game.draw_board(screen=screen1)
        ai_game.draw_next_board(screen=screen1)
        ai_game.draw_score(screen=screen1)
        ai_clock.tick(ai_game.fps)
        ai_running = ai_game.running

        ai_timer += ai_clock.get_time()
        if ai_timer > 100 and not flag:
            random_action = random.randint(0,39)
            ai_game.step(random_action)
            ai_timer = 0

        pygame.display.flip()

        if ai_running == False:
            ai_game = Tetris(1)
            ai_running = True

    pygame.quit()