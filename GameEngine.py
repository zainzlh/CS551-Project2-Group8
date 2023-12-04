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

        def moveRabbits(self):
        """
        the function controls rabbits movement, they can move 1 step each time(up, down, left or right)
        when the new position is out of the boundary or the new position is occupied by other rabbits or captains, skip
        if have veggie in the new position, remove the veggie.
        :return: None
        """
        field_x = len(self._field[0])
        field_y = len(self._field)

        for rabbit in self._rabbits:
            new_x, new_y = rabbit.get_x(), rabbit.get_y()
            # get random number, 0-up, 1-down, 2-left, 3-right
            direction = random.randrange(4)
            if direction == 0:
                new_y += 1
            elif direction == 1:
                new_y -= 1
            elif direction == 2:
                new_x -= 1
            else:
                new_x += 1

            # determine out of boundary
            if 0 <= new_x < field_x and 0 <= new_y < field_y:
                # determine new position have other rabbit or captain
                if not isinstance(self._field[new_x][new_y], Rabbit) or isinstance(self._field[new_x][new_y], Captain):
                    # determine new position have veggie, remove veggie
                    if isinstance(self._field[new_x][new_y], Veggie):
                        self._field[new_x][new_y] = None
                        # move rabbit to new position
                        rabbit.set_position(new_x, new_y)
                        self._field[new_x][new_y] = rabbit
                        self._field[rabbit.get_x()][rabbit.get_y()] = None
        
