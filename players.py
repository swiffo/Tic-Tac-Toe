import collections
import random
import numpy as np
import board

# A player class must implement the methods,
#     def proposeMove(self, number, matrixBoard): returns move (number from 1 to 9)
#     def receiveReward(self, reward): returns None
#     def reset(self): returns None

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
        print("Your symbol is {}".format(board.playerSymbols[number]))

        def repr(occ):
            if occ == 0:
                return "."
            elif occ==1 or occ==2:
                return board.playerSymbols[occ]
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
        bestActionVal = float('-inf')
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
        self.__valueMap[lastQKey] += self.__alpha * reward # Looks wrong


    def setLearningState(self, val):
        if val:
            self.__epsilon = 0.05
            self.__alpha = 0.1
        else:
            self.__epsilon = 0
            self.__alpha = 0
