import sys
import os
sys.path.append('../ChessEngine')
from EnvironmentAPI import EnvironmentAPI


class Node():
    def __init__(self,preceding_action,parent):
        self.visits=0
        self.value=0
        self.Q=0
        self.P=0
        self.preceding_action=preceding_action
        self.children=[]
        self.parent=parent
        self.board_state=None

    def __str__(self):
        x='root' if not self.preceding_action else 'preceding_action'
        return x+" children:"+str(len(self.children))+" visits:"+str(self.visits)+" total value:"+str(self.value)


    def recalculateNode(self,value):
        self.value+=value
        self.visits+=1
        self.Q=self.value/self.visits

    def createChildren(self,board):
        moves=board.get_legal_moves()
        for r in moves:
            self.children.append(Node(r,self))

    def assign_board_state(board):
        self.board_state=board

    



    


