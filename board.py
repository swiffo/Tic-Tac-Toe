"""The module defines the the Tic-Tac-Toe board (class) and exceptions used
to enforce the rules of Tic-Tac-Toe."""

import numpy as np

def player_number_to_symbol(player_number):
    """Converts the player number into the symbol used to display the tokens
    on the board.

    Args:
        playernumber: int

    Yields:
        str: single character (e.g., 'X')
    """

    if player_number == 1:
        return 'X'
    elif player_number == 2:
        return 'O'
    else:
        raise IllegalPlayerNumber

def occupancy_number_to_symbol(number):
    """Converts the number used to indicate occupancy on the board into the
    the symbol used to display the occupancy.

    Args:
        number: int

    Yields:
        str: single character (e.g., 'X' or ' ')
    """

    if number == 0:
        return '.'
    else:
        return player_number_to_symbol(number)

class IllegalMoveException(Exception):
    """Indicates an illegal move. E.g., putting a token in an occupied cell"""
    pass

class IllegalPlayerNumber(Exception):
    """Indicates a non-valid player number"""
    pass

class IllegalPositionException(Exception):
    """Indicates an impossible state of the game. E.g., two winners or 5 X's and only 2 O's"""
    pass

class TicTacToeBoard():
    """Represents a standard 3x3 tic-tac-toe board and its state"""

    def __init__(self):
        """Set up the initial state (3x3 board)"""
        self._board = np.zeros((3, 3), dtype='int')

    def place_token(self, placing, player):
        """x and y between 1 and 3, player either 1 or 2"""

        x, y = placing
        try:
            current_occupant = self._board[x-1, y-1] # Legal position?
        except:
            raise IllegalMoveException

        if current_occupant != 0: # Already occupied?
            raise IllegalMoveException

        self._board[x-1, y-1] = player

    def print_board(self):
        """Print ascii representation of the board"""

        lines = ["".join([occupancy_number_to_symbol(occupant) for occupant in row]) for row in self._board]
        output = "\n".join(lines)

        print("\n"+output+"\n")

    def board_as_matrix(self):
        """Returns board represented as 3x3 numpy-matrix with entries 0 (empty cell), 
        1 (X) and 2 (O)."""
        
        return self._board.copy()

    def check_winner(self):
        """Returns 0 for no winner. Otherwise 1 or 2 indicating the winning player"""

        winners = set()
        # Check rows
        for row in self._board:
            mx = max(row)
            mn = min(row)
            if mx == mn and mx != 0:
                winners.add(mx)

        # Check columns
        b = self._board.transpose()
        for row in b:
            mx = max(row)
            mn = min(row)
            if mx == mn and mx != 0:
                winners.add(mx)

        # Check diagonals
        b = self._board
        if b[0, 0] == b[1, 1] and b[1, 1] == b[2, 2]:
            winners.add(b[1, 1])
        elif b[2, 0] == b[1, 1] and b[1, 1] == b[0, 2]:
            winners.add(b[1, 1])

        winner_count = len(winners)
        if winner_count == 0:
            return 0
        elif winner_count == 1:
            return winners.pop()
        else:
            raise IllegalPositionException

    def identifier(self):
        """Integer uniquely identifying the board positions"""

        val = 0
        for n, x in enumerate(self._board.flat):
            val += x * 3**n

        return val


def test_board():
    """Runs a quick, simple test on the TicTacToeBoard class"""
    board = TicTacToeBoard()
    board.place_token((2, 2), 1)
    board.place_token((1, 1), 1)
    board.place_token((1, 2), 1)
    board.place_token((3, 2), 2)
    board.place_token((3, 3), 1)
    try:
        board.place_token((4, 2), 2)
    except IllegalMoveException:
        pass
    board.print_board()
    print(board.board_as_matrix())

if __name__ == '__main__':
    test_board()
