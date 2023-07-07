import sys
import os
sys.path.append('../ChessEngine')
from EnvironmentAPI import get_legal_moves,is_terminal
import chess


class Node():
    def __init__(self,preceding_action,parent,board):
        self.visits=0
        self.value=0
        self.Q=0
        self.P=0

        self.preceding_action=preceding_action
        self.children=[]
        self.parent=parent
        self.board_state=board
        self.terminal=is_terminal(chess.Board(board))
    

        self.whitesTurn=chess.Board(board).turn

    def __str__(self):
        x='root' if not self.preceding_action else 'preceding_action'
        return x+" children:"+str(len(self.children))+" visits:"+str(self.visits)+" total value:"+str(self.value)


    def recalculateNode(self,value,whiteValue):
        if (whiteValue and self.whitesTurn) or (not whiteValue and not self.whitesTurn):
            self.value+=value
            
        else:
            self.value-=value
        self.visits+=1
        self.Q=self.value/self.visits

    def createChildren(self,board):
        #accepts fen value
        temp=chess.Board(board)
        moves=get_legal_moves(temp)
        for r in moves:
            temp.push(r)
            self.children.append(Node(r,self,temp.fen()))
            temp.pop()


    



    


