"""
Classes for Tic-Tac-Toe players.

See comments at tictactoe.py for what a player class must implement and satisfy.

Classes available:
- RandomPlayer: Makes random and possibly illegal moves. This player is blind
    to the board.

- HumanPlayer: Does not make moves on its own but requests input from the
    user for each move.

- QLearningPlayer: AI based on Q-learning. Has no initial knowledge of the
    game other than knowing that there are 9 cells and will initially
    make illegal moves.

- AfterStateLearningPlayer: AI based on learning a value map for afterstates.
    As it understands the consequences of its actions, unlike the
    QLearningPlayer, it can be said to at least understand the basic rules
    of tic-tac-toe from the beginning.
"""

import collections
import random
import numpy as np
import board

# See comments ot start of tictactoe.py for what a player class must implement and satisfy.

class RandomPlayer():
    """A player that makes a random move each turn regardless of the legality of the move"""

    def propose_move(self, _number, _board):
        """Returns random move"""
        return (random.randrange(1, 4), random.randrange(1, 4))

    def receive_reward(self, reward):
        """Do nothing"""
        pass

    def reset(self):
        """Do nothing"""
        pass

class HumanPlayer():
    """'AI' which will display the board and prompt the user for input at each turn"""

    def propose_move(self, number, game_board):
        """Prints relevant information and prompts user for input"""

        print("Make a move, player {} (symbol={})".format(number, board.player_number_to_symbol(number)))
        game_board.print_board()
        print(np.arange(1, 10).reshape((3, 3)))
        choice = int(input())

        move_x = (choice+2) // 3
        move_y = (choice-1)%3 + 1

        return move_x, move_y

    def receive_reward(self, reward):
        """Do nothing"""
        pass

    def reset(self):
        """Do nothing"""
        pass

class QLearningPlayer():
    """An AI using simple Q-learning to learn with an epsilon-greedy algorithm"""

    base_epsilon = 0.05
    base_alpha = 0.1

    def __init__(self):
        """Set up QLearningPlayer()"""

        self._value_map = collections.defaultdict(lambda: 0.1) # (state,action) -> value (i.e., the action-value function)
        self._epsilon = self.base_epsilon # Chance of doing random move
        self._alpha = self.base_alpha # Learning speed
        self._action_list = [(x, y) for x in range(1, 4) for y in range(1, 4)] # Possible actions
        self._last_action = None # Memory of last taken action
        self._last_state = None # Memory of last state

    def reset(self):
        """Reset internal state. Learned behaviour is retained."""
        self._last_action = None
        self._last_state = None

    def propose_move(self, player_number, board):
        """Use epsilon-greedy Q-learning to generate moves"""

        # We use the board identifier as representative of the state
        state_identifier = board.identifier()

        # First identify the best move. We need this even if we do an exploratory action
        # to update the action-value function.
        best_action_val, best_action = max([(self._value_map[(state_identifier, action)], action)
                                            for action in self._action_list])

        # Update value of previous state unless it is the first move
        if self._last_state is not None:
            # Note that we do Q(s_t, a_t) += \alpha * max_a' Q(s_{t+1}, a') here.
            # The remaining adjustment will already have been done in receive_reward
            # (see explanation there)
            last_key = (self._last_state, self._last_action)
            self._value_map[last_key] += self._alpha * best_action_val

        # Decide on actual move to play (/action)
        if random.random() < self._epsilon:
            move = random.choice(self._action_list)
        else:
            move = best_action

        # Remember this state and action
        self._last_action = move
        self._last_state = state_identifier

        return move

    def receive_reward(self, reward):
        """Reward received for previous move"""

        # Q-learning uses a backup of the reward and the estimated value of the best action in the
        # next state UNLESS the chosen action terminates the episode.
        # Here we modify Q(s_t, a_t) += \alpha * (r_{t+1} - Q(s_t, a_t))
        # **IF** we do not terminate and reach another state, **THEN** do we add the remaining
        # modification, Q(s_t, a_t) += \alpha * (max_a' Q(s_{t+1}, a')).

        last_Q_key = (self._last_state, self._last_action)
        self._value_map[last_Q_key] += self._alpha * (reward - self._value_map[last_Q_key])


    def set_learning_state(self, val):
        """Takes in boolean to decide with to learn using epsilon-greedy method or simply play greedily
        without learning
        """
        if val:
            self._epsilon = self.base_epsilon
            self._alpha = self.base_alpha
        else:
            self._epsilon = 0
            self._alpha = 0


def _move_to_afterstate_identifier(current_board, move, player_number):
    """
    Convert tictactoe board and move to hashable identifier

    Args:
        current_board: the Tic-Tac-Toe board as a numpy matrix
        move: Coordinates (0,0), ... (2,2) signifying move
        player_number: What number on the current_board signifying this player

    Returns:
        Hashable identifier for the afterstate.
    """
    board_copy = current_board.copy()
    board_copy[move] = player_number
    return tuple(board_copy.flat)

class AfterStateLearningPlayer:
    """A Tic-Tac-Toe learning AI using a afterstate value map to generate
    behaviour."""

    def __init__(self):
        """Init AfterStateLearningPlayer()"""
        self._value_map = collections.defaultdict(lambda: 0.1)
        self._alpha = 0.1
        self._epsilon = 0.05
        self._last_afterstate = None

    def propose_move(self, player_number, board):
        """Use epsilon-greedy strategy on afterstates to choose move"""

        # Find the best possible legal move
        board_copy = board.board_as_matrix()

        legal_moves = [(x, y) for x in range(3) for y in range(3) if board_copy[x, y] == 0]
        legal_afterstates = [_move_to_afterstate_identifier(board_copy, m, player_number) for m in legal_moves]
        legal_afterstate_values = [self._value_map[afterstate] for afterstate in legal_afterstates]

        best_afterstate_val, best_index = max(zip(legal_afterstate_values, range(len(legal_afterstate_values))))

        # Decide on actual move to play (/action)
        if random.random() < self._epsilon:
            move, afterstate = random.choice(list(zip(legal_moves, legal_afterstates)))
        else:
            move = legal_moves[best_index]
            afterstate = legal_afterstate_values[best_index]

        # Update the value map
        if self._last_afterstate is not None:
            self._value_map[self._last_afterstate] += self._alpha * best_afterstate_val

        # Remember this afterstate
        self._last_afterstate = afterstate

        #M Moves are returned with upper left being (1,1) [not (0,0)]
        return move[0]+1, move[1]+1

    def receive_reward(self, reward):
        """Update value map with reward for the last move"""
        self._value_map[self._last_afterstate] += self._alpha * (reward - self._value_map[self._last_afterstate])

    def reset(self):
        """Must be called between games"""
        self._last_afterstate = None

    def set_learning_state(self, val):
        """Takes in boolean to decide with to learn using epsilon-greedy method or simply play greedily
        without learning.
        """
        if val:
            self._epsilon = 0.05
            self._alpha = 0.1
        else:
            self._epsilon = 0
            self._alpha = 0
