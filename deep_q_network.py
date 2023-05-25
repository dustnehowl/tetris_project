import numpy as np
import tensorflow as tf
from collections import deque, Counter
import random
from datetime import datetime
from hyperparameters import HYPERPARAMETERS

class DeepQNetwork:
    def __init__(self, state_size, action_size):
        self.hyperparameters = HYPERPARAMETERS()
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=self.hyperparameters.REPLAY_MEMORY_SIZE)
        self.epsilon = self.hyperparameters.EPSILON_INITIAL
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_model()

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3,3), padding='SAME', activation='relu', input_shape=self.state_size),
            tf.keras.layers.Conv2D(64, (3,3), padding='SAME', activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='softmax')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.hyperparameters.LEARNING_RATE))
        return model
    
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        return np.argmax(self.model.predict(np.expand_dims(state, axis=0)))
    
if __name__ == "__main__":
    # model test
    board = np.array([[x for x in range(10)] for _ in range(20)])
    board = np.expand_dims(board, axis=2)
    state_size = board.shape
    action_size = 40

    print(state_size)
    deepQNetwork = DeepQNetwork(state_size=state_size, action_size=action_size)
    action = deepQNetwork.choose_action(board)
    print(action)
