import sys
import os
#sys.path.append('../ChessEngine')
from MCT.Node import Node
from EnvironmentAPI import print_board
import random
import chess
import math

class MonteCarloTree():
    def __init__(self,model,board=chess.Board().fen()):
        self.root=Node(None,None,board)
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


    def make_move(self,otherMove=None):
        if otherMove:
            for r in self.root.children:
                if str(r.preceding_action)==otherMove:
                    self.root=r
                    return self.root
            raise Exception("move not found among child nodes")    
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
            elif node.visits==0:
                value=self.simulate(node,training=False)
            else:
                self.expand(node)
                node=node.children[0]
                value=self.simulate(node,training=False)

            self.backprop(value,node,node.whitesTurn)

    def select(self):
        curr_node=self.root
        while curr_node.children:
            index=self.upper_confidence_score(curr_node,training=False)
            curr_node=curr_node.children[index]
        return curr_node
    
    def expand(self,node):
        node.createChildren(self.model)

    def simulate(self,node,training=False):
        if training:
            return .1* random.randint(-10,10)
        else:
            #model will return predicted value
            return (self.model(encode_input_board(node))[1]).item()

    def backprop(self,value,node,whiteValue):
        while node:
            node.recalculateNode(value,whiteValue)
            node=node.parent

    def upper_confidence_score(self,parent,training=False,c=.5):
        #print(type(parent))
        #print(training)
        if training:
            return random.randrange(len(parent.children))
        else:
            parent_visits=parent.visits
            children=parent.children
            
            def score(node):
                return (-1*node.Q)+c*node.P*math.sqrt(math.log(parent_visits)/max(1,node.visits))

            UCB_scores=[score(x) for x in children]
            return UCB_scores.index(max(UCB_scores))



            #should pick smallest Q value and multiply my -1


