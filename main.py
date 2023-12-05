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

        remaining_veggies = game.remainingVeggies()

    game.gameOver()
    game.highScore()


main()
