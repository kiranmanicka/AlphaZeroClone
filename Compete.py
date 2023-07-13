from MCT.Tree import MonteCarloTree
import chess


def benchmark_test(old_model,new_model,num_games):
    new_model_is_white=True
    new_model_wins=0
    draws=0
    for r in range(num_games):
        result=play_one_game(old_model,new_model,new_model_is_white,r)
        #new_model_is_white= not new_model_is_white
        if result=="new model":
            new_model_wins+=1
            continue
        if result=="draw":
            draws+=1
            continue
    return new_model_wins/num_games,draws/num_games
    


def play_one_game(old_model,new_model,new_model_is_white,r):
    if new_model_is_white:
        players=[oldTree,newTree]=[MonteCarloTree(old_model),MonteCarloTree(new_model)]
    else:
        players=[newTree,oldTree]=[MonteCarloTree(new_model),MonteCarloTree(old_model)]
    currTurn=True
    i=0
    state_of_game=players[currTurn].root
    while state_of_game.terminal[0]!=True:
        oldTree.compute_episode(iterations=10)
        newTree.compute_episode(iterations=10)

        x=players[currTurn].make_move()
        recentTurn=players[currTurn].root.preceding_action
        y=players[not currTurn].make_move(str(recentTurn))


        if x.board_state!=y.board_state:
            raise Exception("moves don't match up")

        print(chess.Board(x.board_state).unicode())
        print(r,i)
        if x.terminal[0] and  x.whitesTurn:
            "black won"
            state_of_game=x.root
        if x.terminal[0] and x.whitesTurn==False:
            "white won"
            state_of_game=x.root
        if y.terminal[0] and  y.whitesTurn:
            "black won"
            state_of_game=y.root
        if y.terminal[0] and y.whitesTurn==False:
            "white won"
            state_of_game=y.root




        
        i+=1

        currTurn=not currTurn
    print(state_of_game.whitesTurn,state_of_game.terminal)
    if state_of_game.terminal[1]=="draw":
        del(state_of_game)
        return "draw"
    if state_of_game.whitesTurn==new_model_is_white:
        del(state_of_game)
        return "old model"
    else:
        del(state_of_game)
        return "new model"

                #                 modelis white    model is white
                #            0:new model is black  1:new model is white
# whtiesturn 0: white won            old model     new model
# whitesturn 1: black won            new model       oldmodel



