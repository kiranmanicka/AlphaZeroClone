from MonteCarloTree.Tree import MonteCarloTree
from Dataset import Dataset
import sys
import chess
import chess.svg
from EnvironmentAPI import print_board




dataset=Dataset(max_samples=30000)


def run_game():
    training_data=[]
    tree=MonteCarloTree(None)
    state_of_game=tree.root
    while state_of_game.terminal[0] != True:
        tree.compute_episode(iterations=100)
        state_of_game=tree.make_move()
    if state_of_game.terminal[1]=='checkmate':
        if state_of_game.whitesTurn==True:
            winner="black"
        else:
            winner="white"
    else:
        winner=None


    return (state_of_game,winner)
winner=None
while winner==None or winner=='white':
    state_of_game,winner=run_game()
    print(winner)
    print_board(state_of_game.board_state)
    

    





