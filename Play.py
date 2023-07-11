from MCT.Tree import MonteCarloTree
import Dataset
from Dataset import Dataset as dataset
import sys
import chess
import chess.svg
from EnvironmentAPI import print_board
from Train import train
from Model import AlphaZeroModel







def play(num_games):
    finished_games=[]
    d=dataset(max_samples=20000)
    for _ in range(num_games):
        state_of_game=run_game()
        finished_games.append(state_of_game)
        print("findshed game")
    d.add_games(finished_games)


def run_game():
    training_data=[]
    tree=MonteCarloTree(AlphaZeroModel)
    state_of_game=tree.root
    i=0
    while state_of_game.terminal[0] != True and i<20:
        tree.compute_episode(iterations=100)
        state_of_game=tree.make_move()
        #print(chess.Board(state_of_game.board_state).unicode())
        
        #print('')
        i+=1
    return state_of_game


play(5)
train(batch_size=20)
print('')
#play()
#print(len(Dataset.dq))

#inp,value,policy=dataset.query(10)


    
    

    





