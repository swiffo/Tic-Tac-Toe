from tictactoe import *
import timeit

def testAI(numEpisodes):
    ai1 = AfterStateLearningPlayer()
    ai2 = QLearningPlayer1()
    game = TicTacToeGame(ai1, ai2)
    t_start = timeit.default_timer()
    for n in range(numEpisodes):
        if n%10000 == 0:
            print('Have trained {} times ...'.format(n))
        game.play(quiet=True)
    t_end = timeit.default_timer()
    print('Done training in {:.0f}s'.format(t_end-t_start))
    ai1.setLearningState(False) # Stop exploratory actions
    ai2.setLearningState(False)
    human = humanPlayer()
    game1 = TicTacToeGame(human, ai2)
    game2 = TicTacToeGame(ai1, human)

    while True:
        game1.play()
        game2.play()

        answer = None
        while answer != 'Y' and answer != 'N':
            answer = input('Continue playing (Y/N)? ').upper()
        if answer == 'N':
            break

if __name__ == "__main__":
    numEpisodes = int(input('How many training episodes? '))
    testAI(numEpisodes)
        
