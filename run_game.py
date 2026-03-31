from game import TicTacToe

def play():
    game = TicTacToe()
    game.display()

    while not game.is_terminal():
        move = input(f"Player {'X' if game.current_player == 1 else '0'}, enter your move (0-8): ")
        if not move.isdigit() or int(move) not in game.get_legal_moves():
            print("Invalid move. Try again.")
            continue


        game = game.make_move(int(move))
        game.display()


    winner = game.check_winner()
    if winner == 0:
        print("its a draw")
    else:
        print(f"Player {'X' if winner == 1 else '0'} wins!")


if __name__ == "__main__":
    play()

    #t