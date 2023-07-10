from collections import deque
import random
from Utils import encode_input_board,encode_target_moves
import torch

dq=deque(maxlen=20000)
unencoded_states_holder=[]

class Dataset():
    def __init__(self,max_samples):
        pass


    def add_games(self,arr):
        unencoded_states_holder.extend(arr)
        self.encode()

    def encode(self):
        encoded_states=[self.encode_state(r) for r in unencoded_states_holder]
        print('insdide encode')
        unencoded_states_holder.clear()
        encoded_states = sum(encoded_states, [])
        dq.extend(encoded_states)
    
    def encode_state(self,node):
        keeper=[]
        if node.terminal[1]=='checkmate':
            value=-1
        elif node.terminal[1]=="draw":
            value=0
        else:
            value=node.value
        keeper.append((encode_input_board(node),value,encode_target_moves(node)))
        node=node.parent
        while node:
            value*=-1
            keeper.append((encode_input_board(node),torch.tensor(value),encode_target_moves(node)))
            node=node.parent
        del(node)
        return keeper

    def query(self,batch_size):
        samples=random.sample(dq,batch_size)
        inp=torch.stack([x[0] for x in samples])
        print(inp.shape)
        value=torch.stack([x[1] for x in samples])
        print(value.shape)
        policy=torch.stack([x[2] for x in samples])
        print(policy.shape)
        return inp,value,policy



