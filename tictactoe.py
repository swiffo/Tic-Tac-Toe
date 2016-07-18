import numpy as np
import random
import collections
import board 
from players import *


# The tic-tac-toe game takes as initializing input two AI/player classes. These classes must implement the following methods:

# A player class must implement the methods,
#     def proposeMove(self, number, matrixBoard): must return move (number from 1 to 9)
#     def receiveReward(self, reward): return ignored
#     def reset(self): return ignored

# They will be called as follows:
# For each episode:
#     [proposeMove] will be called with the player number and a matrix-board as given by the TicTacBoard.boardAsMatrix(). 
#     [receiveReward] will be called with the reward for the last action
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
        self.board = board.TicTacToeBoard()
        
        for turn in range(1,10):
            playerNumber = (turn+1)%2 + 1 # Order is 1,2,1,2,1,2, ... 

            player      = self.__currentPlayer(turn)
            otherPlayer = self.__waitingPlayer(turn)

            matrixBoard = self.board.boardAsMatrix()
            move = player.proposeMove(playerNumber, matrixBoard)
            
            # Enact the move
            try:
                self.board.placeToken(move, playerNumber)
            except board.IllegalMoveException:
                player.receiveReward(-2) # Bad move, penalized more than losing honestly
                if not quiet:
                    print("Illegal move by player {} (proposed {})".format(playerNumber, str(move)))
                    print("Player {} wins!".format(playerNumber%2 + 1)) # The other guy wins
                    self.board.printBoard()
                break

            # Check for winner
            if turn >= 5:  # No need to check for a winner till turn 5
                winner = self.board.checkWinner()
                if winner != 0:
                    player.receiveReward(1) # You won, have a cookie!
                    otherPlayer.receiveReward(-1) # You lose the game and a cookie
                    if not quiet:
                        print("Player {} wins!".format(playerNumber))
                        self.board.printBoard()
                    break

            if turn > 1:
                otherPlayer.receiveReward(0) # Note that we wait for the player A to make his move before deciding on player B's reward
        else:
            # Having made it to here means 9 tokens have been placed legally on the board with no winner being found. Hence, it's a draw.
            player.receiveReward(0)
            otherPlayer.receiveReward(0)
            if not quiet:
                print("Draw!")
                self.board.printBoard()


    def __currentPlayer(self, turn):
        if turn % 2 == 0:
            return self.player2
        else:
            return self.player1

    def __waitingPlayer(self, turn):
        if turn % 2 == 0:
            return self.player1
        else:
            return self.player2
                    

def testGame():
    p1 = randomPlayer()
    p2 = LearningPlayer1()
    game = TicTacToeGame(p1, p2)
    for n in range(100):
        game.play(True) # play quietly

if __name__ == "__main__":
    testGame()


