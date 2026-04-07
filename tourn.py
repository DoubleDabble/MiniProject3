import time
import random
from game import TicTacToe
from minimax_agent import minimax, node_count
from mcts import mcts




#num of games recommended amount was 100.
NUM_GAMES = 100


# so we have our number of simulations that we have taken into account here
MCTS_ITERATIONS = 1000

#This is our random player functionality

#A agent that creates a random move.
def random_player(game,label):
    return random.choice(game.get_legal_moves())

#Singular 1 = x ||  -1 = 0 ||  0 = draw


#Handles a single game instance.
def play_game(Xturn, Oturn):
    game = TicTacToe()
    timer = {'X': 0.0, 'O' : 0.0}
    move_count = {'X': 0, 'O' : 0}


#Tracking the execution time and move counts for each player, so avg speed acn be calculated later.
    while not game.is_terminal():
        current = game.current_player

        #Here we are determing whos turn it is, and their decision process.
        if current == 1:
            start = time.time()
            move = Xturn(game, 'X')
            end = time.time()
            timer['X'] += end - start
            move_count['X'] += 1
        else:
            start = time.time()
            move = Oturn(game, 'O')
            end = time.time()
            timer ['O'] += end - start
            move_count['O'] += 1

        game = game.make_move(move)

#Then we retrn the game outcome so (-1, 1, 0) along with all of the performance metrics that we got (avg time etc)
    return game.check_winner(), timer, move_count


#match counter


#Run a bunch of games (depending on num games ) between TWO agents and does all the stat stuff.
def hundredmatches(Xturn, Oturn, name_x, name_o):
    total_time = {'X': 0.0, 'O': 0.0}
    total_moves = {'X': 0, 'O': 0}
    results = {'X': 0, 'O': 0, 'Draw': 0}
    for _ in range(NUM_GAMES):
        winner, timer, move_count = play_game(Xturn, Oturn)

        #This is where we update the win loss draw records.
        if winner == 1:
            results['X'] += 1
        elif winner == -1:
            results ['O'] += 1
        else:
            results['Draw'] += 1

#ACCUMULATING time and the move data for the final average that we got from before.
        for player in ['X', 'O']:
            total_time[player] += timer[player]
            total_moves[player] += move_count[player]


#This is the calculation for efficiency. So pretty much how long the algoirrhtm takes.
    avg_time_x = total_time['X'] / total_moves['X'] if total_moves['X'] > 0 else 0
    avg_time_o = total_time['O'] / total_moves['O'] if total_moves['O'] > 0 else 0

  

    print(f"{name_x} (X) vs {name_o} (O): {results}")
    print(f"Average time per move: {name_x} = {avg_time_x:.6f}(s), {name_o} = {avg_time_o:.6f}(s)")
    return results

#wrappers for arguments.
def mcts_agent(game,label):
    return mcts(game, iterations= MCTS_ITERATIONS)

#fixes 2 given arguments but only takes 1 wrappers
def minimax_agent(game,label):
    return minimax(game)


#finally the actual tournament

if __name__ == "__main__":
    print("The tournament results are in\n")

    #Minimax X versus Random O

    hundredmatches(minimax_agent, random_player, "Minimax", "Random")

    # MCTS with 1k iterations (X), Versus random

    hundredmatches (mcts_agent, random_player, "MCTS", "Random")

    # Minimax (X) versus MCTS with 1k iterations O
    hundredmatches(minimax_agent, mcts_agent, "Minimax", "MCTS")

    #MCTS WITH 1k iterations, versus minimax
    hundredmatches(mcts_agent,minimax_agent, "MCTS", "Minimax")