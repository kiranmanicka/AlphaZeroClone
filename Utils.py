import random
import torch
import chess




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

# print(whiteBoard)
# print('')
# print(blackBoard)

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




