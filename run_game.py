from game import TicTacToe
from minimax_agent import minimax, node_count
from mcts import mcts

#Hadnles the input. Also checks to make sure that the input IS a number, and that the spot isn't taken.
def get_move_human(game, label):
    while True:
        move = input(f"Player {label}, enter your move (0-8): ")
        if not move.isdigit() or int(move) not in game.get_legal_moves():
            print("Invalid move. Try again.")
        else:
            return int(move)
#This calls the miimax function. Does minimax things (Calls entire tree, evaluates)
def get_move_minimax(game, label):
    print(f"Player {label} (Minimax AI): ")
    return minimax(game)
#This runs the CMTS with 10k, see how it performs with amoutn of simulations.
def get_move_mcts(game, label):
    print(f"Player {label} (MCTS AI): ")
    return mcts(game,iterations=10000)
#Main logic to play (interface)
def play():
    print("====== Tic Tac Toe ======")
    print("1. Two players")
    print("2. Player vs Minimax AI")
    print("3. Player vs MCTS AI")
    print("4. Minimax vs Minimax")
    print("5. MCTS vs MCTS")
    print("6. Minimax vs MCTS")
#Logic for human vs AI nodes
    mode = input("Choose mode (1-6): ").strip()
    while mode not in ("1", "2", "3", "4", "5", "6"):
        print("Invalid choice. Enter a number from 1 to 6.")
        mode = input("Choose mode (1-6): ").strip()

    if mode in ("2", "3"):
        side = input("Do you want to play as X (first) or O (second)? ").strip().upper()
        while side not in ("X", "O"):
            print("Invalid choice. Enter X or O.")
            side = input("Do you want to play as X (first) or O (second)? ").strip().upper()
        human_player = 1 if side == "X" else -1
        ai_func = get_move_minimax if mode == "2" else get_move_mcts
        #Connects human and AI functions to their turn based actions.
        players = {
            human_player: get_move_human,
            -human_player: ai_func,
        }
        #Everything here are all of the AI nodes
    elif mode == "4":
        players = {1: get_move_minimax, -1: get_move_minimax}
    elif mode == "5":
        players = {1: get_move_mcts, -1: get_move_mcts}
    elif mode == "6":
        players = {1: get_move_minimax, -1: get_move_mcts}
        #Otherwise go back to the 2 player human nodes
    else:
        players = {1: get_move_human, -1: get_move_human}


#Here we will initilaze the board and begin the main loop
    game = TicTacToe()
    game.display()

#Game will run until twe get to a win loss draw.
    while not game.is_terminal():
        current = game.current_player
        label = 'X' if current == 1 else 'O'
        
        #Execute the move function assigned to whatever player is playing.
        move = players[current](game, label)
        game = game.make_move(move)
        game.display()

#This is where we get our reports
    winner = game.check_winner()
    if winner == 0:
        print("It's a draw!")
        print(f"Total Minimax nodes evaluated: {node_count[0]}")
    else:
        print(f"Player {'X' if winner == 1 else 'O'} wins!")

if __name__ == "__main__":
    play()
