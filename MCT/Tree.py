import sys
import os
#sys.path.append('../ChessEngine')
from MCT.Node import Node
from EnvironmentAPI import print_board
import random
import chess
import math
from Utils import encode_input_board
import collections

class MonteCarloTree():
    def __init__(self,model,board=chess.Board().fen()):
        self.root=Node(None,None,board)
        self.model=model
        self.three_fold_tracker=collections.defaultdict(int)
        self.move_counter=0
        self.points={'P':1,'R':5,'N':3,'B':3,'Q':9,'p':-1,'r':-5,'n':-3,'b':-3,'q':-9,'K':100,'k':-100}

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
            print(otherMove)
            raise Exception("move not found among child nodes")    
        def process(x):
            if self.three_fold_tracker[self.process_fen(x.board_state)]>=2:
                return -1
            else:
                return x.visits
        total_visits=[process(x) for x in self.root.children]
        maximum_value=max(total_visits)
        indices = [i for i, x in enumerate(total_visits) if x ==maximum_value ]
        next_node_index=random.choice(indices)
        next_node=self.root.children[next_node_index]
        self.root=next_node
        self.three_fold_tracker[self.process_fen(self.root.board_state)]+=1
        self.move_counter+=1
        if self.move_counter>400:
            value=self.point_value(chess.Board(self.root.board_state))
            if value==0:
                self.root.terminal=(True,"draw")
            else:
                if self.root.whitesTurn:
                    self.root.terminal=(True,"checkmate") if value<0 else self.root.terminal
                else:
                    self.root.terminal=(True,"checkmate") if value>0 else self.root.terminal
        return self.root

    def point_value(self,board):
        total=0
        for z in range(64):
            piece=str(board.piece_at(z))
            if piece!='None':
                total+=self.points[piece]
        return total

    def compute_episode(self,iterations=1600):
        for r in range(iterations):
            node=self.select()
            if node.visits>0 and node.terminal[0]==False:
                print(chess.Board(node.board_state).unicode())
                raise Exception("modified mct algorithm bug")
            if node.terminal[0]:
                result=node.terminal[1]
                if result=="checkmate":
                    value=-1
                else:
                    value=0
            else:
                input_board=encode_input_board(node).reshape(1,16,8,8)
                output=self.model(input_board)
                value=output[1].item()
                node.createChildren(output[0])

            self.backprop(value,node,node.whitesTurn)

    def select(self):
        curr_node=self.root
        while curr_node.children:
            index=self.upper_confidence_score(curr_node,training=False)
            curr_node=curr_node.children[index]
        return curr_node

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
                return (-1*node.Q)+c*node.P*math.sqrt(math.log(parent_visits)/max(.0005,node.visits))

            UCB_scores=[score(x) for x in children]
            return UCB_scores.index(max(UCB_scores))

    def process_fen(self,fen):
        x=fen.split(' ')
        return x[0]


