from MCT.Tree import MonteCarloTree
import Dataset
from Dataset import Dataset as dataset
import sys
import chess
import chess.svg
from EnvironmentAPI import print_board
from Train import train
from Model import AlphaZeroModel,AlphaZeroNetwork
import multiprocessing as mp
from multiprocessing import Process, Queue,Value
import os
import copy
from Compete import benchmark_test
import torch



def consumer(num_processes,num_games,model,num_improvements):
    q=Queue()
    finished_process_counter=Value('i',0)
    value_count=Value('i',0)
    jobs=[]
    
    i=0
    for j in range(num_processes):
        p=mp.Process(target=producer,args=(q,finished_process_counter,num_games,value_count,model,i))
        jobs.append(p)
        p.start()
        i+=1
    
    while not (finished_process_counter.value==num_processes and value_count.value==0): 
        x=q.get()
        value_count.value-=1
        Dataset.dq.append(x)
        
    
    for r in jobs:
        r.join()



def producer(q,finished_process_counter,num_games,value_count,model,process_id):
    d=dataset()
    finished_games=play(num_games,model,process_id)
    transformed_data=d.encode(finished_games)
    value_count.value+=len(transformed_data)
    for index,n in enumerate(transformed_data):
        q.put(n)
    finished_process_counter.value=finished_process_counter.value+1

def play(num_games,model,process_id):
    finished_games=[]
    for r in range(num_games):
        state_of_game,move_counter=run_game(model)
        finished_games.append(state_of_game)
        print("findshed game: ",r, "on process:",process_id)
        print(chess.Board(finished_games[r].board_state).unicode())
        print(finished_games[r].terminal,finished_games[r].whitesTurn,move_counter)
    return finished_games
    

def run_game(model):
    training_data=[]
    tree=MonteCarloTree(model)
    state_of_game=tree.root
    i=0
    while state_of_game.terminal[0] != True:
        tree.compute_episode(iterations=100)
        state_of_game=tree.make_move()
        # print(chess.Board(state_of_game.board_state).unicode())
        # print('')
    return state_of_game,tree.move_counter

if __name__=="__main__":

    if sys.argv[1]=="compete":
        old_model,new_model=AlphaZeroNetwork(10,16),AlphaZeroNetwork(10,16)
        old_model.load_state_dict(torch.load(sys.argv[2]+".pth"))
        new_model.load_state_dict(torch.load(sys.argv[3]+".pth"))
        old_model.eval(),new_model.eval()
        with torch.no_grad():
            stats=benchmark_test(old_model,new_model,3)
        print(stats)
    elif sys.argv[1]=="play":


        source_version_number=1
        destination_version_number=2
        SOURCE_FILE="model"+str(source_version_number)+".pth"
        DESTINATION_FILE="model"+str(destination_version_number)+".pth"
        
        num_improvements=6
        steps_to_save_file=3

        new_model=AlphaZeroNetwork(10,16)
        new_model.load_state_dict(torch.load(SOURCE_FILE))

        for r in range(1,num_improvements+1):
            new_model.eval()
            print(r," num improvements")
            with torch.no_grad():
                consumer(os.cpu_count(),2,new_model,num_improvements)
            print(len(Dataset.dq))
            new_model.train()
            train(new_model,batch_size=1000)
            if r%steps_to_save_file==0:
                torch.save(new_model.state_dict(),DESTINATION_FILE)
            #save old_model to disk






#play()
#print(len(Dataset.dq))

#inp,value,policy=dataset.query(10)


    
    

    





