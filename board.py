class TicTacToeBoard:
    """Representation of 3x3 tic-tac-toe board"""
    borderChar = '~'
    
    def __init__(self):
        self._board = [[None for j in range(3)] for i in range(3)]

    def addPiece(self, row, col, player):
        """Add player's piece to board (row,col=0/1/2, player=0/1)"""
        if self._board[row][col] != None:
            raise OccupiedCellException()

        self._board[row][col] = player

    def printBoard(self):
        """Ascii representation of board"""
        rows = []
        
        for row in range(5):
            if row == 0 or row == 4:
                rows.append(self.borderChar*5)
            else:
                boardCells = [self._playerToSymbol(c) for c in self._board[row-1]]
                rows.append( '{0}{1}{2}'.format(self.borderChar, ''.join(boardCells), self.borderChar))

        print( '\n'.join(rows))

    def getState(self):
        """Returns list of lists (matrix) of board"""
        return self._board.copy()
        
    def _playerToSymbol(self, player):
        """Characters for representing player 1/2 and unoccupied cells"""
        if player==0:
            return 'O'
        elif player==1:
            return 'X'
        elif player==None:
            return ' '
        else:
            raise PlayerNumberException()

class OccupiedCellException(BaseException):
    """Signifies that a cell on the board is already taken by a player"""
    pass

class PlayerNumberException(BaseException):
    """Signifies invalid player number"""
    pass

if __name__ == '__main__':
    board = TicTacToeBoard()
    board.addPiece(1,1,0)
    board.addPiece(0,0,1)
    board.addPiece(0,1,0)
    board.addPiece(2,1,1)
    board.addPiece(2,2,0)
    board.printBoard()
    
