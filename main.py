"""When run trains two tic-tac-toe AIs and lets a human player play against them"""

import timeit
from tictactoe import TicTacToeGame
import players

def run_game(num_episodes):
    """Trains two AIs over the specified number of episodes and
    then let's human play against them"""

    ai1 = players.AfterStateLearningPlayer()
    ai2 = players.QLearningPlayer()
    game = TicTacToeGame(ai1, ai2)
    t_start = timeit.default_timer()
    for episode in range(num_episodes):
        if episode%10000 == 0:
            print('Have trained {} times ...'.format(episode))
        game.play(quiet=True)
    t_end = timeit.default_timer()
    print('Done training in {:.0f}s'.format(t_end-t_start))
    ai1.set_learning_state(False) # Stop exploratory actions
    ai2.set_learning_state(False)
    human = players.HumanPlayer()
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
    num_episodes = int(input('How many training episodes? '))
    run_game(num_episodes)
