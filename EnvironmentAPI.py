import gym
import gym_chess
import sys
from gym_chess.alphazero import BoardEncoding

class EnvironmentAPI():
    def __init__(self):
        self.env=gym.make('Chess-v0')
        self.env.reset()
        self.whitesTurn=True

    def __str__(self):
        print(self.env.render(mode='unicode'))
        return""

    def make_move(self,move):
        if move in self.get_legal_moves():
            self.env.step(move)
            self.whitesTurn= not self.whitesTurn
            return True
        else:
            return False
        
    
    def get_legal_moves(self):
        return self.env.legal_moves

    def is_terminal(self):
        if len(self.get_legal_moves==0):
            if whitesTurn:
                return (True,True)
            else:
                return (True,False)
        return (False,None)



