from collections import deque
import random
from Utils import encode_input_board,encode_target_moves
import torch


dq=deque(maxlen=30000)

class Dataset():
    def __init__(self):
        pass


    def encode(self,finished_games):
        encoded_states=[self.encode_state(r) for r in finished_games]
        #print('insdide encode')
        encoded_states = sum(encoded_states, [])
        #print(len(encoded_states))
        return encoded_states
    
    def encode_state(self,node):
        keeper=[]
        if node.terminal[1]=='checkmate':
            value=-1.0
        elif node.terminal[1]=="draw":
            value=0.0
        else:
            raise Exception("encoded state is not terminal")
        keeper.append((encode_input_board(node),torch.tensor(value),encode_target_moves(node)))
        node=node.parent
        while node:
            value*=-1
            keeper.append((encode_input_board(node),torch.tensor(value),encode_target_moves(node)))
            node=node.parent
        del(node)
        return keeper

    def query(self):
        samples=random.sample(dq,8000 if len(dq)>8000 else len(dq))
        inp=torch.stack([x[0] for x in samples])
        value=torch.stack([x[1] for x in samples])
        policy=torch.stack([x[2] for x in samples])

        inp.detach()
        value.detach()
        policy.detach()
        return inp,value,policy



