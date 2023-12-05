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

    def printField(self):
        """
        print boundary and field
        :return: None
        """
        # get boundary length
        max_length = 0
        for row in self._field:
            for col in self._field:
                if self._field[row][col] is None:
                    max_length += 1
                else:
                    max_length += self._field[row][col]
        print("#" * (max_length + 2))
        # print field
        for row in self._field:
            line = ""
            for col in self._field:
                if self._field[row][col] is None:
                    line += " "
                else:
                    line += self._field[row][col]
                print("#" + line + "#")
            print("#" * (max_length + 2))

    def getScore(self):
        """
        :return: current score
        """
        return self._score

    def moveRabbits(self):
        """
        the function control rabbits movement, they can move 1 steps each time(up, down, left or right)
        when new position out of boundary or new position occupied by other rabbits or captains, skip
        if have veggie on new position, remove veggie.
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
                if not isinstance(self._field[new_y][new_x], Rabbit) or isinstance(self._field[new_y][new_x], Captain):
                    # determine new position have veggie, remove veggie
                    if isinstance(self._field[new_y][new_x], Veggie):
                        self._field[new_y][new_x] = None
                        # move rabbit to new position
                        rabbit.set_position(new_x, new_y)
                        self._field[new_y][new_x] = rabbit
                        self._field[rabbit.get_y()] [rabbit.get_x()] = None
                        
    def moveCptVertical(self, vertical):
        """
        Realize the movement of the captain in the vertical direction
        :param vertical: 1 or -1, the value of vertical direction
        :return: None
        """
        # captain's current position
        position_x = self._captain.get_x()
        position_y = self._captain.get_y() + vertical
        # if new position is None, move captain to new position
        if self._field[position_y][position_x] is None:
            self._captain.set_position(position_x, position_y)
            self._field[self._captain.get_y()][position_x] = None
        # if new position have veggie, can collect and add score
        elif isinstance(self._field[position_y][position_x], Veggie):
            veggie = self._field[position_y][position_x]
            print(f"Yummy! A delicious {veggie.get_name()}")
            self._captain.add_veggie(veggie)
            self._score += veggie.get_points()
            self._captain.set_position(position_x, position_y)
            self._field[position_y][position_x] = self._captain
            self._field[self._captain.get_y()][position_x] = None
        # if new position is rabbit, informed user, captain's position no change
        elif isinstance(self._field[position_y][position_x], Rabbit):
            print("Don't step on the bunnies!")

    def moveCptHorizontal(self, horizontal):
        """
        Realize the movement of the captain in the horizontal direction
        :param horizontal: 1 or -1, the value of horizontal direction
        :return: None
        """
        # captain's current position
        position_x = self._captain.get_x() + horizontal
        position_y = self._captain.get_y()
        # if new position is None, move captain to new position
        if self._field[position_y][position_x] is None:
            self._captain.set_position(position_x, position_y)
            self._field[self._captain.get_y()][position_x] = None
        # if new position have veggie, can collect and add score
        elif isinstance(self._field[position_y][position_x], Veggie):
            veggie = self._field[position_y][position_x]
            print(f"Yummy! A delicious {veggie.get_name()}")
            self._captain.add_veggie(veggie)
            self._score += veggie.get_points()
            self._captain.set_position(position_x, position_y)
            self._field[position_y][position_x] = self._captain
            self._field[self._captain.get_y()][position_x] = None
        # if new position is rabbit, informed user, captain's position no change
        elif isinstance(self._field[position_y][position_x], Rabbit):
            print("Don't step on the bunnies!")

    def moveCaptain(self):
        """
        move Captain direction, accept both uppercase and lowercase of input
        if input other words, skip
        :return: None
        """
        direction = input("Would you like to move up(W), down(S), left(A), or right(D):")
        if direction == "w" or direction == "W":
            position_y = self._captain.get_y() + 1
            if 0 <= position_y < len(self._field):
                self.moveCptVertical(1)
            else:
                print("You can't move that way!")
        elif direction == "s" or direction == "S":
            position_y = self._captain.get_y() -1
            if 0 <= position_y < len(self._field):
                self.moveCptVertical(-1)
            else:
                print("You can't move that way!")
        elif direction == "a" or direction =="A":
            position_x = self._captain.get_x() -1
            if 0 <= position_x < len(self._field[0]):
                self.moveCptHorizontal(-1)
            else:
                print("You can't move that way!")
        elif direction == "d" or direction == "D":
            position_x = self._captain.get_x() + 1
            if 0 <= position_x < len(self._field[0]):
                self.moveCptHorizontal(1)
            else:
                print("You can't move that way!")
        else:
            print(f"{direction} is not a valid option")
