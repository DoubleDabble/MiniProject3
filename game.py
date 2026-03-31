class TicTacToe:
    #Initialize an empty 3x3 board. Board is a list of 9 elemetns: 0 = empty, 1 = x, - 1 = o. 
    # X always moves first

    def __init__(self):
        self.board = [0] * 9
        self.current_player = 1

    def get_legal_moves(self):
        #Return a list of indices (0,8). Corresponding to the empty squasres. Pass.

        return [i for i, x in enumerate(self.board) if x == 0]

    def make_move(self, move):

        #Place the current player's mark at the 
        # given index. Return a NEW tictactoe
        # object; do not modify self. Pass.
        new_game = TicTacToe()
        new_game.board = self.board.copy()
        new_game.board[move] = self.current_player
        new_game.current_player = -self.current_player
        return new_game

    def is_terminal(self):
        #Return true if the game is over, eitherbecause someone has won or because all squares are filled *(a draw pass)
        return self.check_winner() != 0 or all(x != 0 for x in self.board)

    def utility(self):
        #Return +1 if X has won. Return -1 if O has one. Or 0 for a ddraw. Onl,y avlid when is_Termianl returns true.
        winner = self.check_winner()
        if winner != 0:
            return winner
        return 0  # draw

    def check_winner(self):
        #Return 1 if X has three in a row, -1 if 0 has three in a row, or 0 otherwise. Pass)
        lines = [
            (0,1,2), (3,4,5), (6,7,8),  # rows
            (0,3,6), (1,4,7), (2,5,8),  # cols
            (0,4,8), (2,4,6)            # diags
        ]
        for a,b,c in lines:
            if self.board[a] == self.board[b] == self.board[c] != 0:
                return self.board[a]
        return 0

    def display(self):
        #Print the board in a readable 3x3 format. Use 'X' for 1, O for -1 . for 0.
        symbols = {1: 'X', -1: 'O', 0: '.'}
        for i in range(0,9,3):
            print(' '.join(symbols[x] for x in self.board[i:i+3]))


            #t