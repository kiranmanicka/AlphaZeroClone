import random
import torch
import torch.nn as nn
import chess
import numpy as np
from numpy.linalg import norm
import math

#need to revise angle calculation for p2 moves


def upper_confidence_score(parent,training=False,c=.5):
    if training:
        return random.randrange(len(parent.children))
    else:
        return 0
        #should pick smallest Q value and multiply my -1

pieces={'pawn':0,'rook':1,'knight':2,'bishop':3,'queen':4,'king':5}
blackBoard={}
whiteBoard={}
i=0
for rankIndex,r in enumerate(reversed(range(1,9))):
    for fileIndex,j in enumerate(list('ABCDEFGH')):
        whiteBoard[j+str(r)]=(rankIndex,fileIndex)
        blackBoard[j+str(r)]=(-1*rankIndex+7,-1*fileIndex+7)
        i+=1

def encode_target_moves(node):
    children=node.children
    board=chess.Board(node.board_state)
    target_tensor=torch.zeros(73,8,8)

    if node.terminal[0]:
        return target_tensor

    if node.whitesTurn:
        bluePrint=whiteBoard
    else:
        bluePrint=blackBoard 
    visits=[x.visits for x in children]
    visits=torch.tensor(visits,dtype=torch.float64)
    softmax_visits=nn.functional.softmax(visits,dim=0)
    for index,r in enumerate(children):
        move=str(r.preceding_action)
        x=move[0]+move[1]
        piece=str(board.piece_at(chess.parse_square(x)))
        if (piece =='P' or piece=='p')  and len(move)>4:
            plane,index1,index2=pawn_promotion_info(target_tensor,move,bluePrint,node.whitesTurn)
        elif piece=='N' or piece=='n':
            plane,index1,index2=knight_move_info(target_tensor,move,bluePrint,node.whitesTurn)
        else:
            plane,index1,index2=queen_move_info(target_tensor,move,bluePrint,node.whitesTurn)

        target_tensor[plane][index1][index2]=softmax_visits[index]
        
    return target_tensor

directional_promotion={'left':64,'straight':67,'right':70}
underpromotion_index={'n':0,'b':1,'r':2}

def pawn_promotion_info(target_tensor,move,bluePrint,whitesTurn):
    if move[-1]=='q':
        return queen_move_info(target_tensor,move,bluePrint,whitesTurn)
    
    angle,distance=get_angle_distance(move,whitesTurn)
    angle=int(angle/45)
    plane=None
    if angle== 1:
        plane=directional_promotion['right']+underpromotion_index[move[-1]]
    elif angle== 2:
        plane=directional_promotion['straight']+underpromotion_index[move[-1]]
    elif angle== 3:
        plane=directional_promotion['left']+underpromotion_index[move[-1]]
    else:
        raise Exception("angle is invalid for pawn underpromotion")
    square=move[0].upper()+move[1]
    index=bluePrint[square]
    return plane,index[0],index[1]

def knight_move_info(target_tensor,move,bluePrint,whitesTurn):
    angle,distance=get_angle_distance(move,whitesTurn)
    angle=int(angle/45)
    move=move[0].upper()+move[1]
    index=bluePrint[move]
    return 56+angle,index[0],index[1]
    
    
def queen_move_info(target_tensor,move,bluePrint,whitesTurn):
    angle,distance=get_angle_distance(move,whitesTurn)
    angle=int(angle/45)
    plane=angle*7+(distance-1)
    index=bluePrint[move[0].upper()+str(move[1])]
    return plane, index[0], index[1]

def get_angle_distance(move,whitesTurn):
    fq=move[:2]
    sq=move[2:4]
    vector=np.array([ord(sq[0])-ord(fq[0]),int(sq[1])-int(fq[1])])
    base=np.array([1,0])
    angle=np.arccos(vector.dot(base)/(norm(vector)*norm(base)))
    if vector[1]<base[1]:
        angle=(math.pi*2)-angle
    angle=math.degrees(angle)
    if not whitesTurn: angle+=180
    angle=angle-360 if angle>=360 else angle
    distance=np.max(np.abs(vector))
    return angle,distance


def encode_input_board(node):
    #p1=0 when playersTurn=True but when playersTurn=False p1=1
    #use board object of find out if castling move is available
    #board is a string because we will pass in root nodes
    #castling moves for p2= white is p1 e1c1,e1g1  black is p1 e8g8,e8c8
    #castling moves for p1= white is p1
    sample=torch.zeros(16,8,8)
    check_castle(sample,node)
    board=chess.Board(node.board_state)
    if node.whitesTurn:
        bluePrint=whiteBoard
    else:
        bluePrint=blackBoard  
    for j in bluePrint:
        piece=str(board.piece_at(grab_index(j)))
        matcher(sample,piece,bluePrint,j)
            
    return sample

def matcher(sample,piece,bluePrint,j):
    if bluePrint is whiteBoard:
        whiteIndex,blackIndex=0,1
    else:
        whiteIndex,blackIndex=1,0
    if piece=="P":
        sample[6*whiteIndex+pieces['pawn']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="R":
        sample[6*whiteIndex+pieces['rook']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="N":
        sample[6*whiteIndex+pieces['knight']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="B":
        sample[6*whiteIndex+pieces['bishop']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="Q":
        sample[6*whiteIndex+pieces['queen']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="K":
        sample[6*whiteIndex+pieces['king']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="p":
        sample[6*blackIndex+pieces['pawn']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="r":
        sample[6*blackIndex+pieces['rook']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="n":
        sample[6*blackIndex+pieces['knight']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="b":
        sample[6*blackIndex+pieces['bishop']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="q":
        sample[6*blackIndex+pieces['queen']][bluePrint[j][0]][bluePrint[j][1]]=1
    if piece=="k":
        sample[6*blackIndex+pieces['king']][bluePrint[j][0]][bluePrint[j][1]]=1
            
def check_castle(sample,node):
    board=chess.Board(node.board_state)
    player_alignment=(chess.WHITE,chess.BLACK) if node.whitesTurn else (chess.BLACK,chess.WHITE)
    if board.has_kingside_castling_rights(player_alignment[0]):
        sample[12]=torch.ones(8,8)
    if board.has_queenside_castling_rights(player_alignment[0]):
        sample[13]=torch.ones(8,8)
    if board.has_kingside_castling_rights(player_alignment[1]):
        sample[14]=torch.ones(8,8)
    if board.has_queenside_castling_rights(player_alignment[1]):
        sample[15]=torch.ones(8,8)


def grab_index(key):
    keeper={'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
    return (int(key[-1])-1)*8+keeper[key[0]]

def move(str):
    return chess.Move.from_uci(str)




