import collections
import random
import numpy as np
import board

# See comments ot start of tictactoe.py for what a player class must implement and satisfy.

class randomPlayer():
    """A player that makes a random move each turn regardless of the legality of the move"""

    def propose_move(self, number, board):
        """Returns random move"""
        return (random.randrange(1,4), random.randrange(1,4))

    def receive_reward(self, reward):
        pass 

    def reset(self):
        pass

class humanPlayer():
    """'AI' which will display the board and prompt the user for input at each turn"""

    def propose_move(self, number, gameBoard):
        """Prints relevant information and prompts user for input"""

        print("Make a move, player {} (symbol={})".format(number, board.player_number_to_symbol(number)))

        gameBoard.print_board()
        print(np.array([1,2,3,4,5,6,7,8,9]).reshape((3,3)))

        choice = int(input())
        x = (choice+2) // 3 
        y = choice - (x-1)*3

        return (x, y)

    def receive_reward(self, reward):
        pass

    def reset(self):
        print('Game ended')
        

class QLearningPlayer1():
    """An AI using simple Q-learning to learn with an epsilon-greedy algorithm"""

    baseEpsilon = 0.05
    baseAlpha = 0.1

    def __init__(self):
        self.__valueMap = collections.defaultdict(lambda:0.1) # (state,action) -> value (i.e., the action-value function)
        self.__epsilon = self.baseEpsilon # Chance of doing random move
        self.__alpha = self.baseAlpha # Learning speed
        self.__actionList = [(x,y) for x in range(1,4) for y in range(1,4)] # Possible actions
        self.__lastAction = None # Memory of last taken action
        self.__lastState = None # Memory of last state

    def reset(self):
        self.__lastAction = None
        self.__lastState  = None
        
    def propose_move(self, playerNumber, board):
        """Use epsilon-greedy Q-learning to generate moves"""

        # We use the board identifier as representative of the state
        boardIdentifier = board.identifier()

        # First identify the best move. We need this even if we do an exploratory action
        # to update the action-value function.
        bestActionVal, bestAction = max([(self.__valueMap[(boardIdentifier, action)], action) for action in self.__actionList])
    
        # Update value of previous state unless it is the first move
        if self.__lastState is not None:
            # Note that we do Q(s_t, a_t) += \alpha * max_a' Q(s_{t+1}, a') here.
            # The remaining adjustment will already have been done in receive_reward 
            # (see explanation there)
            lastQKey = (self.__lastState, self.__lastAction)
            self.__valueMap[lastQKey] += self.__alpha * bestActionVal 

        # Decide on actual move to play (/action)
        if random.random() < self.__epsilon:
            move = random.choice(self.__actionList)
        else:
            move = bestAction

        # Remember this state and action
        self.__lastAction = move
        self.__lastState = boardIdentifier

        return move

    def receive_reward(self, reward):
        """Reward received for previous move"""

        # Q-learning uses a backup of the reward and the estimated value of the best action in the 
        # next state UNLESS the chosen action terminates the episode.
        # Here we modify Q(s_t, a_t) += \alpha * (r_{t+1} - Q(s_t, a_t))
        # **IF** we do not terminate and reach another state, **THEN** do we add the remaining
        # modification, Q(s_t, a_t) += \alpha * (max_a' Q(s_{t+1}, a')).

        lastQKey = (self.__lastState, self.__lastAction)
        self.__valueMap[lastQKey] += self.__alpha * (reward - self.__valueMap[lastQKey])


    def setLearningState(self, val):
        """Takes in boolean to decide with to learn using epsilon-greedy method or simply play greedily 
        without learning
        """
        if val:
            self.__epsilon = self.baseEpsilon
            self.__alpha = self.baseAlpha
        else:
            self.__epsilon = 0
            self.__alpha = 0


class AfterStateLearningPlayer:
    def __init__(self):
        self.__valueMap = collections.defaultdict(lambda: 0.1)
        self.__alpha = 0.1
        self.__epsilon = 0.05
        self.__lastAfterState = None

    def propose_move(self, playerNumber, board):
        """Use epsilon-greedy strategy on afterstates to choose move"""

        # Find the best possible legal move
        boardCopy = board.board_as_matrix()

        legalMoves = [(x,y) for x in range(3) for y in range(3) if boardCopy[x, y]==0]

        bestMove = None
        bestAfterState = None
        bestAfterStateVal = float('-inf')

        for move in legalMoves:
            tempBoard = boardCopy.copy()
            tempBoard[move] = playerNumber

            state    = tuple(tempBoard.flat)
            stateVal = self.__valueMap[state]

            if stateVal > bestAfterStateVal:
                bestAfterState = state
                bestAfterStateVal = stateVal
                bestMove = move

        # Decide on actual move to play (/action)
        if random.random() < self.__epsilon:
            move = random.choice(legalMoves)
        else:
            move = bestMove

        # Update the value map
        if self.__lastAfterState is not None:
            self.__valueMap[self.__lastAfterState] += self.__alpha * bestAfterStateVal

        # Remember this afterstate 
        self.__lastAfterState  = bestAfterState

        #M Moves are returned with upper left being (1,1) [not (0,0)]
        return move[0]+1, move[1]+1

    def receive_reward(self, reward):
        """Update value map with reward for the last move"""
        self.__valueMap[self.__lastAfterState] += self.__alpha * (reward - self.__valueMap[self.__lastAfterState])

    def reset(self):
        """Must be called between games"""
        self.__lastAfterState = None

    def setLearningState(self, val):
        """Takes in boolean to decide with to learn using epsilon-greedy method or simply play greedily 
        without learning
        """
        if val:
            self.__epsilon = 0.05
            self.__alpha = 0.1
        else:
            self.__epsilon = 0
            self.__alpha = 0





    
