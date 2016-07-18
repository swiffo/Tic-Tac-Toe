import collections
import random
import numpy as np
import board

# A player class must implement the methods,
#     def proposeMove(self, number, matrixBoard): returns move (number from 1 to 9)
#     def receiveReward(self, reward): returns None
#     def reset(self): returns None

class randomPlayer():
    """A player that makes a random move each turn regardless of the legality of the move"""

    def proposeMove(self, number, matrixBoard):
        """Returns random move"""
        return (random.randrange(1,4), random.randrange(1,4))

    def receiveReward(self, reward):
        pass

    def reset(self):
        pass

class humanPlayer():
    """'AI' which will display the board and prompt the user for input at each turn"""

    def proposeMove(self, number, matrixBoard):
        """Prints relevant information and prompts user for input"""

        print("Make a move, player {}".format(number))
        print("Your symbol is {}".format(board.playerSymbols[number]))

        boardString = self.__boardRepresentation(matrixBoard)

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

    def __boardRepresentation(self, matrixBoard):
        def repr(occ):
            if occ == 0:
                return "."
            elif occ==1 or occ==2:
                return board.playerSymbols[occ]
            else:
                raise IllegalPlayerNumber
                
        lines = [ "".join([repr(occ) for occ in row]) for row in matrixBoard]
        boardString = "\n".join(lines)

        return boardString
        

class LearningPlayer1():
    """An AI using simple Q-learning to learn with an epsilon-greedy algorithm"""

    baseEpsilon = 0.05
    baseAlpha   = 0.1

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
        
    def proposeMove(self, playerNumber, currentBoard):
        """Use epsilon-greedy Q-learning to generate moves"""

        # First identify the best move. We need this even if we do an exploratory action
        # to update the action-value function.
        bestActionVal, bestAction = max([(self.__valueMap[(currentBoard, action)], action) for action in self.__actionList])
    
        # Update value of previous state unless it is the first move
        if self.__lastState is not None:
            # Note that we do Q(s_t, a_t) += \alpha * max_a' Q(s_{t+1}, a') here.
            # The remaining adjustment will already have been done in receiveReward 
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
        self.__lastState  = currentBoard

        return move

    def receiveReward(self, reward):
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


    
