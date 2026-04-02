import time
import random
from game import TicTacToe
from minimax_agent import minimax, node_count
from mcts import mcts


NUM_GAMES = 100

MCTS_ITERATIONS = 1000

#This is our random player functionality

#does not pick random agent, but picks a random space that is allowed

def random_player(game,label):
    return random.choice(game.get_legal_moves())

#Singular 1 = x ||  -1 = 0 ||  0 = draw

def play_game(agent_x, agent_o):
    game = TicTacToe()
    timer = {'X': 0.0, 'O' : 0.0}
    move_count = {'X': 0, 'O' : 0}

    while not game.is_terminal():
        current = game.current_player
        if current == 1:
            start = time.time()
            move = agent_x(game, 'X')
            end = time.time()
            timer['X'] += end - start
            move_count['X'] += 1
        else:
            start = time.time()
            move = agent_o(game, 'O')
            end = time.time()
            timer ['O'] += end - start
            move_count['O'] += 1

        game = game.make_move(move)

    return game.check_winner(), timer, move_count


#match counter

def run_matchup(agent_x, agent_o, name_x, name_o):
    total_time = {'X': 0.0, 'O': 0.0}
    total_moves = {'X': 0, 'O': 0}
    results = {'X': 0, 'O': 0, 'Draw': 0}
    for _ in range(NUM_GAMES):
        winner, timer, move_count = play_game(agent_x, agent_o)
        if winner == 1:
            results['X'] += 1
        elif winner == -1:
            results ['O'] += 1
        else:
            results['Draw'] += 1

        for player in ['X', 'O']:
            total_time[player] += timer[player]
            total_moves[player] += move_count[player]

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

    run_matchup(minimax_agent, random_player, "Minimax", "Random")

    # MCTS with 1k iterations (X), Versus random

    run_matchup (mcts_agent, random_player, "MCTS", "Random")

    # Minimax (X) versus MCTS with 1k iterations O
    run_matchup(minimax_agent, mcts_agent, "Minimax", "MCTS")

    #MCTS WITH 1k iterations, versus minimax
    run_matchup(mcts_agent,minimax_agent, "MCTS", "Minimax")