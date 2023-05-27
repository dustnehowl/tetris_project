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
    
    def save_model(self, url):
        self.model.save_weights(url)
        print("Save Done!")

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3,3), padding='SAME', activation='relu', input_shape=self.state_size),
            tf.keras.layers.Conv2D(64, (3,3), padding='SAME', activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='softmax')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.hyperparameters.LEARNING_RATE))
        model.summary()
        return model
    
    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        return np.argmax(self.model.predict(np.expand_dims(state, axis=0)))
    
    def replay(self):
        if len(self.memory) < self.hyperparameters.BATCH_SIZE:
            return
        batch = random.sample(self.memory, self.hyperparameters.BATCH_SIZE)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = np.reshape(states, (self.hyperparameters.BATCH_SIZE, 20, 10, 1))
        next_states = np.reshape(next_states, (self.hyperparameters.BATCH_SIZE, 20, 10, 1))

        targets = self.model.predict(states)
        target_next = self.target_model.predict(next_states)
        
        # Calculate target Q values
        dones = np.array(dones, dtype=np.float32)
        targets[range(self.hyperparameters.BATCH_SIZE), actions] = rewards + self.hyperparameters.GAMMA * np.max(target_next, axis=1) * (1 - dones)

        self.model.fit(states, targets, epochs=1, verbose=0)

        if self.epsilon > self.hyperparameters.EPSILON_MIN:
            self.epsilon *= self.hyperparameters.EPSILON_DECAY
    
if __name__ == "__main__":
    # model test
    board = np.array([[x for x in range(10)] for _ in range(20)])
    board = np.expand_dims(board, axis=2)
    state_size = board.shape
    action_size = 40

    model = DeepQNetwork(state_size=state_size, action_size=action_size)
    action = model.choose_action(board)
    print(action)
