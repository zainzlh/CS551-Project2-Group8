# Group 8
# Name: Linghao Zhao, Junran Yang
# Date: 12/07/2023
# Description: the main function

from GameEngine import GameEngine


def main():
    game = GameEngine()
    game.initializeGame()
    game.intro()

    remaining_veggies = game.remainingVeggies()

    # While there are still vegetables left in the game
    while remaining_veggies > 0:
        print(f"{remaining_veggies} veggies remaining. Current score: {game.getScore()}")
        game.printField()

        game.moveRabbits()
        game.moveCaptain()

        game.moveSnake()

        remaining_veggies = game.remainingVeggies()

    game.gameOver()
    game.highScore()


main()
