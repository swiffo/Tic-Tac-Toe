import numpy as np

playerSymbols = {1:'X', 2:'O'}

def playerNumberToSymbol(playerNumber):
    if playerNumber==1:
        return 'X'
    elif playerNumber==2:
        return 'O'
    else:
        raise IllegalPlayerNumber

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
        
    def placeToken(self, placing, player):
        """x and y between 1 and 3, player either 1 or 2"""

        x,y = placing
        try:
            currentOccupant = self.__board[x-1, y-1] # Legal position?
        except:
            raise IllegalMoveException

        if currentOccupant != 0: # Already occupied?
            raise IllegalMoveException

        self.__board[x-1, y-1] = player

    def printBoard(self):
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


if __name__ == '__main__':
    board = TicTacToeBoard()
    board.placeToken((2,2), 1)
    board.placeToken((1,1),1)
    board.placeToken((1,2),1)
    board.placeToken((3,2),2)
    board.placeToken((3,3),1)
    try:
        board.placeToken((4,2),2)
    except IllegalMoveException:
        pass
    board.printBoard()
    print(board.boardAsMatrix())
    
