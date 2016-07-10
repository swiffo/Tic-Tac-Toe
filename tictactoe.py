import numpy as np
import random
import collections

playerSymbols ={1:'X', 2:'O'}

class IllegalMoveException(BaseException):
    """Indicates an illegal move. E.g., putting a token in an occupied cell"""
    pass

class IllegalPlayerNumber(BaseException):
    """Indicates a non-valid player number"""
    pass

class IllegalPositionException(BaseException):
    """Indicates an impossible state of the game. E.g., two winners or 5 X's and only 2 O's"""
    pass

class TicTacToeBoard():
    """Represents a standard 3x3 tic-tac-toe board and its state"""
    
    def __init__(self):
        """Set up the initial state (3x3 board)"""
        self.__board = np.zeros((3,3), dtype='int')
        
    def placeToken(self, x, y, player):
        """x and y between 1 and 3, player either 1 or 2"""

        try:
            currentOccupant = self.__board[x-1, y-1]
        except:
            raise IllegalMoveException

        if currentOccupant != 0:
            raise IllegalMoveException

        self.__board[x-1, y-1] = player

    def print(self):
        """Print ascii representation of the board"""
        
        def repr(occ):
            if occ == 0:
                return "."
            elif occ==1 or occ==2:
                return playerSymbols[occ]
            else:
                raise IllegalPlayerNumber
                
        lines = ["".join([repr(occ) for occ in row]) for row in self.__board]
        output = "\n".join(lines)

        print("\n"+output+"\n")

    def boardAsMatrix(self):
        """Returns board represented as 3x3 matrix with entries 0 (empty cell), 1 (X) and 2 (O)."""
        return tuple([tuple(row) for row in self.__board])

    def checkWinner(self):
        """Returns 0 for no winner. Otherwise 1 or 2 indicating the winning player"""

        winners = dict()
        # Check rows
        for row in self.__board:
            mx=max(row)
            mn=min(row)
            if mx==mn and mx!=0:
                winners[mx] = 1

        # Check columns
        b = self.__board.transpose()
        for row in b:
            mx=max(row)
            mn=min(row)
            if mx==mn and mx!=0:
                winners[mx] = 1

        # Check diagonals
        b = self.__board
        if b[0,0] == b[1,1] and b[1,1] == b[2,2]:
            winners[b[1,1]] = 1
        elif b[2,0] == b[1,1] and b[1,1] == b[0,2]:
            winners[b[1,1]] = 1

        winnerCount = len(winners)
        if winnerCount==0:
            return 0
        elif winnerCount==1:
            return list(winners.keys())[0]
        else:
            raise IllegalPositionException



class TicTacToeGame():
    """Class for controlling a game between two specified players.

Players are classes that must implement methods:
    proposeMove(playerNumber, boardAsMatrix) [returns (x,y) indicating where to put token]
    receiveReward(reward) [Reward for the last move taken]
"""
    def __init__(self, player1, player2):
        """Set everything up"""
        print("Init game")
        self.board = TicTacToeBoard() # Unnecessary
        self.player1 = player1
        self.player2 = player2

    def play(self, quiet=False):
        """Play tic-tac-toe to completion"""

        self.player1.reset()
        self.player2.reset()
        self.board = TicTacToeBoard()
        
        turn = 1
        while True:
            playerNumber = (turn+1)%2 + 1

            player = self.__currentPlayer(turn)
            otherPlayer = self.__waitingPlayer(turn)

            matrixBoard = self.board.boardAsMatrix()
            move = player.proposeMove(playerNumber, matrixBoard)
            x,y = move
            
            try:
                self.board.placeToken(x, y, playerNumber)
            except IllegalMoveException:
                player.receiveReward(-2) # Bad move, penalized more than losing honestly
                if not quiet:
                    print("Illegal move by player {} (proposed ({},{})".format(playerNumber, x, y))
                    print("Player {} wins!".format(playerNumber%2 + 1))
                    self.board.print()
                break

            winner = self.board.checkWinner()
            if winner != 0:
                player.receiveReward(1) # You won, have a cookie!
                otherPlayer.receiveReward(-1) # You lose the game and a cookie
                if not quiet:
                    print("Player {} wins!".format(playerNumber))
                    self.board.print()
                break

            if turn > 1:
                otherPlayer.receiveReward(0) # Note that we wait for the player A to make his move before deciding on player B's reward

            turn += 1
            if turn == 10:
                player.receiveReward(0)
                if not quiet:
                    print("Draw!")
                    self.board.print()
                break

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
                      

class randomPlayer():
    def proposeMove(self, number, matrixBoard):
        x = random.randrange(1,4)
        y = random.randrange(1,4)
        return (x,y)

    def receiveReward(self, reward):
        pass

    def reset(self):
        pass

class humanPlayer():
    def proposeMove(self, number, matrixBoard):
        print("Make a move, player {}".format(number))
        print("Your symbol is {}".format(playerSymbols[number]))

        def repr(occ):
            if occ == 0:
                return "."
            elif occ==1 or occ==2:
                return playerSymbols[occ]
            else:
                raise IllegalPlayerNumber
                
        lines = [ "".join([repr(occ) for occ in row]) for row in matrixBoard]
        boardString = "\n".join(lines)

        print("\n"+boardString+"\n")
        print(np.array([1,2,3,4,5,6,7,8,9]).reshape((3,3)))

        choice = input()
        choice = int(choice)
        x = (choice+2) // 3 
        y = choice - (x-1)*3

        return (x,y)

    def receiveReward(self, reward):
        pass

    def reset(self):
        print('Game ended')
        
class LearningPlayer1():
    def __init__(self):
        self.__valueMap = collections.defaultdict(lambda:0) # (state,action) -> value
        self.__board = np.zeros((3,3), dtype='int')
        self.__epsilon = 0.05 # Chance of doing random move
        self.__alpha = 0.1 # Learning speed
        self.__actionList = [(x,y) for x in range(1,4) for y in range(1,4)]
        self.__lastAction = None
        self.__lastState = None

    def reset(self):
        self.__lastAction = None
        self.__lastState = None
        
    def proposeMove(self, playerNumber, currentBoard):

        # First identify the next move
        bestActionVal = -10
        bestAction = None
        for a in self.__actionList:
            qKey = (currentBoard, a)
            if self.__valueMap[qKey] > bestActionVal:
                bestActionVal = self.__valueMap[qKey]
                bestAction = a

        if random.random() < self.__epsilon:
            move = random.choice(self.__actionList)
        else:
            move = bestAction

        # Update value of previous state if any
        if self.__lastState is not None:
            lastQKey = (self.__lastState, self.__lastAction)
            self.__valueMap[lastQKey] += self.__alpha * (bestActionVal - self.__valueMap[lastQKey])

        # Remember this state and action
        self.__lastAction = move
        self.__lastState = currentBoard

        # Finally unveil the chosen move to the waiting world
        return move

    def receiveReward(self, reward):
        lastQKey = (self.__lastState, self.__lastAction)
        self.__valueMap[lastQKey] += self.__alpha * reward

        
            
            
                    
                        
def testBoard():
    b = TicTacToeBoard()
    b.placeToken(2,2,1)
    b.placeToken(1,1,2)
    b.placeToken(1,2,1)
    b.placeToken(3,2,2)
    b.print()

def testGame():
    p1 = randomPlayer()
    p1 = LearningPlayer1()
    p2 = humanPlayer()
    game = TicTacToeGame(p1, p2)
    game.play()

def testAI():
    ai1 = LearningPlayer1()
    ai2 = LearningPlayer1()
    game = TicTacToeGame(ai1, ai2)
    for n in range(100000):
        game.play(quiet=True)

    print('Done training')
    human = humanPlayer()

    game1 = TicTacToeGame(human, ai2)
    game2 = TicTacToeGame(ai1, human)

    while True:
        game1.play()
        game2.play()

        
