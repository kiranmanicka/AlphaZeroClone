import sys
import os
#sys.path.append('../ChessEngine')
from MonteCarloTree.Node import Node
from EnvironmentAPI import print_board
from Utils import upper_confidence_score
import random
import chess

class MonteCarloTree():
    def __init__(self,model):
        self.root=Node(None,None,chess.Board().fen(),whitesTurn=True)
        self.model=model

    def __str__(self):
        def dfs(node,depth):
            if not node:
                return
            print("depth: ",depth) 
            print(node)
            print_board(node.board_state)
            for r in node.children:
                if r.visits>0:
                    dfs(r,depth+1)

        dfs(self.root,0)
        return ""


    def make_move(self):
        total_visits=[x.visits for x in self.root.children]
        next_node_index=total_visits.index(max(total_visits))
        next_node=self.root.children[next_node_index]
        self.root=next_node
        return self.root


    def compute_episode(self,iterations=1600):
        for r in range(iterations):
            node=self.select()
            if node.terminal[0]:
                result=node.terminal[1]
                if result=="checkmate":
                    #print('here')
                    value=-1
                else:
                    value=0
                whiteValue=node.whitesTurn
            elif node.visits==0:
                whiteValue=node.whitesTurn
                value=self.simulate(node,training=True)
            else:
                self.expand(node)
                node=node.children[0]
                whiteValue=node.whitesTurn
                value=self.simulate(node,training=True)

            self.backprop(value,node,whiteValue)

    def select(self):
        curr_node=self.root
        while curr_node.children:
            index=upper_confidence_score(curr_node,training=True)
            curr_node=curr_node.children[index]
        return curr_node
    
    def expand(self,node):
        node.createChildren(node.board_state)

    def simulate(self,node,training=False):
        if training:
            return .1* random.randint(-10,10)
        else:
            #model will return predicted value
            return 1

    def backprop(self,value,node,whiteValue):
        while node:
            node.recalculateNode(value,whiteValue)
            node=node.parent


