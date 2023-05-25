from tetris import Tetris
import pygame
import random


if __name__ == "__main__":
    pygame.init()
    size = (width, height) = (1360, 800)
    screen1 = pygame.display.set_mode(size)
    clock1 = pygame.time.Clock()
    ai_clock = pygame.time.Clock()
    running = True

    key_states = {
        'left': False,
        'right': False,
        'down': False
    }

    game = Tetris(1)
    ai_game = Tetris(2)

    timer = 0
    ai_timer = 0
    flag = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_states['left'] = True
                if event.key == pygame.K_RIGHT:
                    key_states['right'] = True
                if event.key == pygame.K_DOWN:
                    key_states['down'] = True
                if event.key == pygame.K_SPACE:
                    game.drop()
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_p:
                    flag = not flag
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key_states['left'] = False
                if event.key == pygame.K_RIGHT:
                    key_states['right'] = False
                if event.key == pygame.K_DOWN:
                    key_states['down'] = False

        # 방향키 상태에 따라 함수 호출
        if key_states['left']:
            game.left()
        elif key_states['right']:
            game.right()
        elif key_states['down']:
            game.down()

        game.update_board()
        game.update_next_board()
        game.draw_board(screen=screen1)
        game.draw_next_board(screen=screen1)
        game.draw_score(screen=screen1)
        clock1.tick(game.fps)
        running = game.running

        timer += clock1.get_time()
        if timer > 1000 and not flag:
            game.down()
            timer = 0

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

        if running == False:
            # print("You Lose")
            game = Tetris(1)
            running = True
        if ai_running == False:
            # print("You win")
            ai_game = Tetris(2)
            ai_running = True

    print("Game over!")
    print("Your score is", game.line)
    # while running:
    #     for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False
    #     game = Tetris(1)
    #     ai_game = Tetris(2)
    #     game.main(screen=screen1, clock=clock1)
    pygame.quit()