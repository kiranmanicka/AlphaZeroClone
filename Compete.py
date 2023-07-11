from MCT.Tree import MonteCarloTree


def benchmark_test(old_model,new_model,num_games):
    new_model_is_white=True
    new_model_wins=0
    draws=0
    for _ in range(num_games):
        result=play_one_game(old_model,new_model,new_model_is_white)
        new_model_is_white= not new_model_is_white
        if result=="new model":
            new_model_wins+=1
            continue
        if result=="draw":
            draws+=1
            continue
    return new_model_wins/num_games,draws/num_games
    


def play_one_game(old_model,new_model,new_model_is_white):
    if new_model_is_white:
        players=[oldTree,newTree]=[MonteCarloTree(old_model),MonteCarloTree(new_model)]
    else:
        players=[newTree,oldTree]=[MonteCarloTree(new_model),MonteCarloTree(old_model)]
    currTurn=True

    state_of_game=players[currTurn].root
    while state_of_game.terminal[0]!=True:
        oldTree.compute_episode()
        newTree.compute_episode()

        x=players[currTurn].make_move()
        recentTurn=players[currTurn].root.preceding_action
        y=players[not currTurn].make_move(recentTurn)

        if x.board_state!=y.board_state:
            raise Exception("moves don't match up")

        state_of_game=oldTree.root

        currTurn=not currTurn
    if state_of_game.terminal[1]=="draw":
        return "draw"
    if state_of_game.whitesTurn==new_model_is_white:
        return "old model"
    else:
        return "new model"

#                 modelis white    model is white
#                         0               1
# whtiesturn 0            old model     new model
# whitesturn 1            new model       oldmodel






thing=[1,2]
print(thing[False])