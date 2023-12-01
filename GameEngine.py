import os.path
import random
from Veggie import Veggie
from Captain import Captain
from Rabbit import Rabbit
import csv


class GameEngine:
    NUMBEROFVEGGIES = 30
    NUMBEROFRABBITS = 5
    HIGHSCOREFILE = "highscore.data"

    def __init__(self):
        self._field = []
        self._rabbits = []
        self._captain = None
        self._veggies = []
        self._score = 0

    def getRandomEmptyLocation(self):
        x, y = random.randint(0, len(self._field) - 1), random.randint(0, len(self._field[0]) - 1)
        while self._field[x][y] is not None:
            x, y = random.randint(0, len(self._field) - 1), random.randint(0, len(self._field[0]) - 1)
        return x, y

    def initVeggies(self):
        file_not_found = True
        filename = ""
        while file_not_found:
            filename = input("Please enter the name of the vegetable point file: ")
            if os.path.exists(filename):
                print(f"{filename} does not exist!", end="")
                file_not_found = False

        with open(filename, 'r') as veggie_file:
            veggie_csv = csv.reader(veggie_file)

            first_line = next(veggie_csv)
            field_size = [int(dim) for dim in first_line[1:]]
            self._field = [[None for _ in range(field_size[1])] for _ in range(field_size[0])]

            for row in veggie_csv:
                inhabitant, name, points = row
                veggie = Veggie(inhabitant, name, int(points))
                self._veggies.append(veggie)

                for _ in range(self.NUMBEROFVEGGIES):
                    x, y = self.getRandomEmptyLocation()
                    self._field[x][y] = veggie

    def initCaptain(self):
        x, y = self.getRandomEmptyLocation()
        self._captain = Captain(x, y)
        self._field[x][y] = self._captain

    def initRabbits(self):
        for _ in range(self.NUMBEROFRABBITS):
            x, y = self.getRandomEmptyLocation()
            rabbit = Rabbit(x, y)
            self._rabbits.append(rabbit)
            self._field[x][y] = rabbit

    def initializeGame(self):
        self.initVeggies()
        self.initCaptain()
        self.initRabbits()

    def remainingVeggies(self):
        return sum(row.count(None) for row in self._field)

    def intro():
        
