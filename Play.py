from MCT.Tree import MonteCarloTree
import Dataset
from Dataset import Dataset as dataset
import sys
import chess
import chess.svg
from EnvironmentAPI import print_board
from Model import AlphaZeroNetwork






def play():
    finished_games=[]
    for _ in range(1):
        state_of_game=run_game()
        finished_games.append(state_of_game)
        print("finished game")
    d=dataset(max_samples=30000)
    d.add_games(finished_games)



def run_game():
    training_data=[]
    tree=MonteCarloTree(None)
    state_of_game=tree.root
    i=0
    while state_of_game.terminal[0] != True:
        tree.compute_episode(iterations=100)
        state_of_game=tree.make_move()
        print(chess.Board(state_of_game.board_state).unicode())
        i+=1
    return state_of_game


play()
#play()
print(len(Dataset.dq))

#inp,value,policy=dataset.query(10)


    
    

    





