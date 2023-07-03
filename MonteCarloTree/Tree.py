import sys
import os
from Node import Node
sys.path.append('../ChessEngine')
from EnvironmentAPI import EnvironmentAPI
from Utils import upper_confidence_score
import copy
import random

class MonteCarloTree():
    def __init__(self,model):
        self.simulation_board=EnvironmentAPI()
        self.root=Node(None,None)
        self.root.board_state=EnvironmentAPI()
        self.model=model

    def __str__(self):
        def dfs(node,board,depth):
            if not node:
                return
            print("depth:",depth) 
            print(node)
            board.make_move(node.preceding_action)
            print(board)
            for r in node.children:
                if r.visits>0:
                    dfs(r,copy.deepcopy(board),depth+1)

        dfs(self.root,copy.deepcopy(self.root.board_state),0)
        return ""


    def make_move(self):
        total_visits-[x.visits for x in root.children]
        next_node_index=total_visits.index(max(total_visits))
        next_node=root.children[next_node_index]
        temp_board=root.board_state
        temp_board.make_move(next_node.preceding_action)
        next_node.board_state=temp_board
        self.root=next_node


    def compute_episode(self,iterations=1600):
        for r in range(iterations):
            node=self.select()
            if node.visits==0:
                value=self.simulate(training=True)
            else:
                self.expand(node)
                node=node.children[0]
                self.simulation_board.make_move(node.preceding_action)
                value=self.simulate(training=True)

            self.backprop(value,node)
            self.simulation_board=copy.deepcopy(self.root.board_state)

    def select(self):
        curr_node=self.root
        while curr_node.children:
            index=upper_confidence_score(curr_node,training=True)
            curr_node=curr_node.children[index]
            self.simulation_board.make_move(curr_node.preceding_action)
        return curr_node
    
    def expand(self,node):
        node.createChildren(self.simulation_board)

    def simulate(self,training=False):
        if training:
            return .1* random.randint(-10,10)
        else:
            #model will return predicted value
            return 1

    def backprop(self,value,node):
        curr_node=node
        while node:
            node.recalculateNode(value)
            node=node.parent



tree=MonteCarloTree(None)
tree.compute_episode(iterations=5)
print(tree)

