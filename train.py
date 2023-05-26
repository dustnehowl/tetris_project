from tetris import Tetris
import pygame
import random
import numpy as np
from hyperparameters import HYPERPARAMETERS
from deep_q_network import DeepQNetwork


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

    board = np.array([[x for x in range(10)] for _ in range(20)])
    board = np.expand_dims(board, axis=2)
    state_size = board.shape
    action_size = 40

    deepQNetwork = DeepQNetwork(state_size=state_size, action_size=action_size)
    params = HYPERPARAMETERS()
    epoch = 1
    while epoch <= params.NUM_EPISODES:
        ai_game = Tetris(1)
        done = False
        total_reward = 0

        while not done and ai_game.running:

            ai_game.update_board()
            ai_game.update_next_board()
            ai_game.draw_board(screen=screen1)
            ai_game.draw_next_board(screen=screen1)
            ai_game.draw_score(screen=screen1)
            ai_clock.tick(ai_game.fps)
            ai_timer += ai_clock.get_time()

            if ai_timer > 100 and not flag:
                ai_timer = 0

                state = ai_game.get_state()
                state = np.expand_dims(state, axis=2)
                action = deepQNetwork.choose_action(state)
                reward, _ = ai_game.step(action)
                done = not ai_game.running
                print(reward, action)
                total_reward += reward
                next_state = ai_game.get_state()
                next_state = np.expand_dims(next_state, axis=2)
                deepQNetwork.remember(state, action, reward, next_state, done)
                state = next_state
                deepQNetwork.replay()

            pygame.display.flip()

        if epoch % params.TARGET_UPDATE_INTERVAL == 0:
            deepQNetwork.update_target_model()

        print(f"Episode: {epoch}, Total Reward: {total_reward}")
        epoch += 1



        
        
        

    pygame.quit()