import sys
import chess


def print_board(board):
    x=chess.Board(board)
    print(x.unicode())
    print(' ')
        
    
def get_legal_moves(board):
    return list(board.legal_moves)

def is_terminal(board):
    if board.is_check() and len(get_legal_moves(board))==0:
        return(True,"checkmate")
    if not board.is_check() and len(get_legal_moves(board))==0:
        return(True,"draw")
    if board.is_insufficient_material():
        return (True,"draw")
    return(False,None)



