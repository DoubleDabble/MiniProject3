from game import TicTacToe
from minimax_agent import minimax, node_count
from mcts import mcts

def get_move_human(game, label):
    while True:
        move = input(f"Player {label}, enter your move (0-8): ")
        if not move.isdigit() or int(move) not in game.get_legal_moves():
            print("Invalid move. Try again.")
        else:
            return int(move)

def get_move_minimax(game, label):
    print(f"Player {label} (Minimax AI): ")
    return minimax(game)

def get_move_mcts(game, label):
    print(f"Player {label} (MCTS AI): ")
    return mcts(game,iterations=10000)

def play():
    print("=== Tic Tac Toe ===")
    print("1. Two players")
    print("2. Player vs Minimax AI")
    print("3. Player vs MCTS AI")
    print("4. Minimax vs Minimax")
    print("5. MCTS vs MCTS")
    print("6. Minimax vs MCTS")

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
        players = {
            human_player: get_move_human,
            -human_player: ai_func,
        }
    elif mode == "4":
        players = {1: get_move_minimax, -1: get_move_minimax}
    elif mode == "5":
        players = {1: get_move_mcts, -1: get_move_mcts}
    elif mode == "6":
        players = {1: get_move_minimax, -1: get_move_mcts}
    else:
        players = {1: get_move_human, -1: get_move_human}

    game = TicTacToe()
    game.display()

    while not game.is_terminal():
        current = game.current_player
        label = 'X' if current == 1 else 'O'
        move = players[current](game, label)
        game = game.make_move(move)
        game.display()


    winner = game.check_winner()
    if winner == 0:
        print("It's a draw!")
        print(f"Total Minimax nodes evaluated: {node_count[0]}")
    else:
        print(f"Player {'X' if winner == 1 else 'O'} wins!")

if __name__ == "__main__":
    play()
