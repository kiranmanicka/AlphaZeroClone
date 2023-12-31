import sys
import os
sys.path.append('../ChessEngine')
from EnvironmentAPI import get_legal_moves,is_terminal
import chess
from Utils import get_indices,whiteBoard,blackBoard,encode_input_board


class Node():
    def __init__(self,preceding_action,parent,board,P=0):
        self.visits=0
        self.value=0
        self.Q=0
        self.P=P

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
        if whiteValue==self.whitesTurn:
            self.value+=value
            
        else:
            self.value-=value
        self.visits+=1
        self.Q=self.value/self.visits

    def createChildren(self,probabilities):
        #accepts fen value
        temp=chess.Board(self.board_state)
        moves=get_legal_moves(temp)
        move_probabilities=probabilities.reshape(73,8,8).detach()
        
        bluePrint=whiteBoard if self.whitesTurn else blackBoard
        
        for r in moves:
            plane,index1,index2=get_indices(None,bluePrint,self.whitesTurn,chess.Board(self.board_state),move=r)
            probability=move_probabilities[plane][index1][index2]

            temp.push(r)
            self.children.append(Node(r,self,temp.fen(),P=probability))
            temp.pop()


    



    


