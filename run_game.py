from game import TicTacToe
from mcts import mcts

def play():
    game = TicTacToe()
    game.display()

    while not game.is_terminal():
        move = input(f"Player {'X' if game.current_player == 1 else '0'}, enter your move (0-8): ")
        if not move.isdigit() or int(move) not in game.get_legal_moves():
            print("Invalid move. Try again.")
            continue


        game = game.make_move(int(move))

        #Use this section instead if running with mcts
        """
        # Human = X
        if game.current_player == 1:
            move = input("Your move (0-8): ")
            if not move.isdigit() or int(move) not in game.get_legal_moves():
                print("Invalid move.")
                continue
            
            game = game.make_move(int(move))

        # MCTS = O
        else:
            print("AI is thinking...")
            game = mcts(game, iterations=10000)
        """
        
        game.display()


    winner = game.check_winner()
    if winner == 0:
        print("its a draw")
    else:
        print(f"Player {'X' if winner == 1 else '0'} wins!")


if __name__ == "__main__":
    play()

    #t
