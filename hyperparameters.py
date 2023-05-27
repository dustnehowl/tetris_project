class HYPERPARAMETERS:
    def __init__(self):
        self.REPLAY_MEMORY_SIZE = 20000
        self.BATCH_SIZE = 128
        self.GAMMA = 0.99
        self.EPSILON_INITIAL = 1.0 
        self.EPSILON_DECAY = 0.9995
        self.EPSILON_MIN = 0.0001 
        self.LEARNING_RATE = 0.001
        self.TARGET_UPDATE_INTERVAL = 1000 
        self.NUM_EPISODES = 5000