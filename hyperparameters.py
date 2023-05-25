class HYPERPARAMETERS:
    def __init__(self):
        self.REPLAY_MEMORY_SIZE = 10000
        self.BATCH_SIZE = 32
        self.GAMMA = 0.99
        self.EPSILON_INITIAL = 1.0 
        self.EPSILON_DECAY = 0.995
        self.EPSILON_MIN = 0.01 
        self.LEARNING_RATE = 0.001
        self.TARGET_UPDATE_INTERVAL = 1000 