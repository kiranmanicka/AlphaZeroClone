from collections import deque
import random

class Dataset():
    def __init__(self,max_samples):
        self.dq=deque(maxlen=max_samples)


    def add_game(self,arr):
        self.dq.extend(arr)

    def query(self,num_samples):
        return random.sample(self.dq,num_samples)


