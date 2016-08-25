"""The engine for playing the tic-tac-toe game.

Classes:
    TicTacToeGame: Initialized with two players, lets them play tic-tac-toe
        against each other.
"""

import board
import players 

REWARD_LEGAL_MOVE = 0 # Reward for making legal move neither winning nor losing
REWARD_DRAW = 0
REWARD_WIN = 1
REWARD_LOSS = -1
REWARD_ILLEGAL_MOVE = -2 # Bad move, penalized more than losing honestly


# The tic-tac-toe game takes as initializing input two AI/player classes. These classes must implement the following methods:

# A player class must implement the methods,
#     def propose_move(self, number, matrixBoard): must return move (2-tuple (1,1), (1,2), ..., (3,3))
#     def receive_reward(self, reward): return ignored
#     def reset(self): return ignored

# They will be called as follows:
# For each episode:
#     [propose_move] will be called with the player number and a matrix-board as given by the TicTacBoard.boardAsMatrix(). 
#     [receive_reward] will be called with the reward for the last action
# [reset] will be called, signalling that the player should be ready for a new episode.

# Points are: 1 point for winning the game, -1 point for losing and -2 points for making an illegal move (winner gets nothing in that case)

class TicTacToeGame():
    """Class for controlling a game between two specified players."""

    def __init__(self, player1, player2):
        """Register the competing players"""
        self.player1 = player1
        self.player2 = player2

    def play(self, quiet=False):
        """Play tic-tac-toe to completion"""

        self.player1.reset()
        self.player2.reset()
        game_board = board.TicTacToeBoard()
        
        for turn in range(1, 10):
            player_number = (turn+1)%2 + 1 # Order is 1,2,1,2,1,2, ...

            player = self._current_player(turn)
            other_player = self._waiting_player(turn)

            move = player.propose_move(player_number, game_board)
            
            # Enact the move
            try:
                game_board.place_token(move, player_number)
            except board.IllegalMoveException:
                player.receive_reward(REWARD_ILLEGAL_MOVE)
                if not quiet:
                    print("Illegal move by player {} (proposed {})".format(player_number, str(move)))
                    print("Player {} wins!".format(player_number%2 + 1)) # The other guy wins
                    game_board.print_board()
                break

            # Check for winner
            if turn >= 5:  # No need to check for a winner till turn 5
                winner = game_board.check_winner()
                if winner != 0:
                    player.receive_reward(REWARD_WIN) # You won, have a cookie!
                    other_player.receive_reward(REWARD_LOSS) # You lose the game and a cookie
                    if not quiet:
                        print("Player {} wins!".format(player_number))
                        game_board.print_board()
                    break

            if turn > 1:
                # Note that we wait for the player A to make his move
                # before deciding on player B's reward
                other_player.receive_reward(REWARD_LEGAL_MOVE)
 
        else:
            # Having made it to here means 9 tokens have been placed legally on the board
            # with no winner being found. Hence, it's a draw.
            player.receive_reward(REWARD_DRAW)
            other_player.receive_reward(REWARD_DRAW)
            if not quiet:
                print("Draw!")
                game_board.print_board()


    def _current_player(self, turn):
        """Return the number of the player making a move in the specified turn."""
        if turn % 2 == 0:
            return self.player2
        else:
            return self.player1

    def _waiting_player(self, turn):
        """Return the number of the player *not* making a move in the specified turn."""
        if turn % 2 == 0:
            return self.player1
        else:
            return self.player2
                    

def test_game():
    """Run simple test"""
    player1 = players.RandomPlayer()
    player2 = players.QLearningPlayer()
    game = TicTacToeGame(player1, player2)
    for game_number in range(100):
        game.play(True) # play quietly

if __name__ == "__main__":
    test_game()


