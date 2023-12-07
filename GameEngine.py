import os.path
import random
from Veggie import Veggie
from Captain import Captain
from Rabbit import Rabbit
import csv
import pickle


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
            if not os.path.exists(filename):
                print(f"{filename} does not exist!", end="")
            else:
                file_not_found = False

        with open(filename, 'r') as veggie_file:
            veggie_csv = csv.reader(veggie_file)

            first_line = next(veggie_csv)
            field_size = [int(dim) for dim in first_line[1:]]
            self._field = [[None for _ in range(field_size[1])] for _ in range(field_size[0])]

            for row in veggie_csv:
                name, inhabitant, points = row
                veggie = Veggie(inhabitant, name, int(points))
                self._veggies.append(veggie)

            for _ in range(self.NUMBEROFVEGGIES):
                x, y = self.getRandomEmptyLocation()
                self._field[x][y] = random.choice(self._veggies)

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
        return sum(row.count(veggie) for row in self._field for veggie in self._veggies)

    def intro(self):
        """
        intro the game
        :return: None
        """
        print("Welcome to Captain Veggie!")
        print("The rabbits have invaded your garden and you must harvest")
        print("as many vegetables as possible before the rabbits eat them")
        print("all! Each vegetable is worth a different number of points")
        print("so go for the high score!")

        print("\nThe vegetables are:")
        for veggie in self._veggies:
            print(f"{veggie.__str__()}")

        print("\nCaptain Veggie is V, and the rabbits are R's.")
        print("\nGood luck!")

    def printField(self):
        """
        print boundary and field
        :return: None
        """
        # get boundary length
        max_length = 0
        for item in self._field[0]:
            if item is None:
                max_length += 1
            else:
                max_length += len(item.get_inhabitant())
        print("#" * ((max_length*3) + 2))
        # print field
        for row in self._field:
            line = ""
            for item in row:
                if item is None:
                    line += "   "
                else:
                    line += " "
                    line += item.get_inhabitant()
                    line += " "
            print("#" + line + "#")
        print("#" * ((max_length*3) + 2))

    def getScore(self):
        """
        :return: current score
        """
        return self._score

    def moveRabbits(self):
        """
        the function control rabbits movement, they can move 1 steps each time(up, down, left, right or diagonal direction)
        when new position out of boundary or new position occupied by other rabbits or captains, skip
        if there is veggie on new position, remove veggie.
        :return: None
        """
        field_x = len(self._field)
        field_y = len(self._field[0])

        for rabbit in self._rabbits:
            new_x, new_y = rabbit.get_x(), rabbit.get_y()
            # get random number, 0-up, 1-down, 2-left, 3-right, 4-upper left, 5-upper right, 6-lower left, 7-lower right
            direction = random.randrange(8)
            if direction == 0:  # up
                new_y -= 1
            elif direction == 1:  # down
                new_y += 1
            elif direction == 2:  # left
                new_x -= 1
            elif direction == 3:  # right
                new_x += 1
            elif direction == 4:  # upper left
                new_x -= 1
                new_y -= 1
            elif direction == 5:  # upper right
                new_x += 1
                new_y -= 1
            elif direction == 6:  # lower left
                new_x -= 1
                new_y += 1
            else:  # lower right
                new_x += 1
                new_y += 1
    
            # determine out of boundary
            if 0 <= new_x < field_x and 0 <= new_y < field_y:
                # determine new position have other rabbit or captain or snake
                if not (isinstance(self._field[new_x][new_y], Rabbit) or isinstance(self._field[new_x][new_y], Captain) or isinstance(self._field[new_x][new_y], Snake)):
                    # determine new position have veggie, remove veggie
                    if isinstance(self._field[new_x][new_y], Veggie):
                        self._field[new_x][new_y] = None
                        # move rabbit to new position
                        self._field[rabbit.get_x()][rabbit.get_y()] = None
                        rabbit.set_position(new_x, new_y)
                        self._field[new_x][new_y] = rabbit
                    else:
                        self._field[rabbit.get_x()][rabbit.get_y()] = None
                        rabbit.set_position(new_x, new_y)
                        self._field[new_x][new_y] = rabbit
                        
    def moveCptVertical(self, vertical):
        """
        Realize the movement of the captain in the vertical direction
        :param vertical: 1 or -1, the value of vertical direction
        :return: None
        """
        # captain's current position
        position_x = self._captain.get_x() + vertical
        position_y = self._captain.get_y()
        # if new position is None, move captain to new position
        if self._field[position_x][position_y] is None:
            self._field[self._captain.get_x()][position_y] = None
            self._captain.set_position(position_x, position_y)
            self._field[position_x][position_y] = self._captain
        # if new position have veggie, can collect and add score
        elif isinstance(self._field[position_x][position_y], Veggie):
            veggie = self._field[position_x][position_y]
            print(f"Yummy! A delicious {veggie.get_name()}")
            self._captain.add_veggie(veggie)
            self._score += veggie.get_points()
            self._field[self._captain.get_x()][position_y] = None
            self._captain.set_position(position_x, position_y)
            self._field[position_x][position_y] = self._captain
        # if new position is rabbit, informed user, captain's position no change
        elif isinstance(self._field[position_x][position_y], Rabbit):
            print("Don't step on the bunnies!")

    def moveCptHorizontal(self, horizontal):
        """
        Realize the movement of the captain in the horizontal direction
        :param horizontal: 1 or -1, the value of horizontal direction
        :return: None
        """
        # captain's current position
        position_x = self._captain.get_x()
        position_y = self._captain.get_y() + horizontal
        # if new position is None, move captain to new position
        if self._field[position_x][position_y] is None:
            self._field[position_x][self._captain.get_y()] = None
            self._captain.set_position(position_x, position_y)
            self._field[position_x][position_y] = self._captain
        # if new position have veggie, can collect and add score
        elif isinstance(self._field[position_x][position_y], Veggie):
            veggie = self._field[position_x][position_y]
            print(f"Yummy! A delicious {veggie.get_name()}")
            self._captain.add_veggie(veggie)
            self._score += veggie.get_points()
            self._field[position_x][self._captain.get_y()] = None
            self._captain.set_position(position_x, position_y)
            self._field[position_x][position_y] = self._captain
        # if new position is rabbit, informed user, captain's position no change
        elif isinstance(self._field[position_x][position_y], Rabbit):
            print("Don't step on the bunnies!")

    def moveCaptain(self):
        """
        move Captain direction, accept both uppercase and lowercase of input
        if input other words, skip
        :return: None
        """
        direction = input("Would you like to move up(W), down(S), left(A), or right(D):")
        if direction == "w" or direction == "W":
            position_x = self._captain.get_x() - 1
            if 0 <= position_x < len(self._field):
                self.moveCptVertical(-1)
            else:
                print("You can't move that way!")
        elif direction == "s" or direction == "S":
            position_x = self._captain.get_x() + 1
            if 0 <= position_x < len(self._field):
                self.moveCptVertical(1)
            else:
                print("You can't move that way!")
        elif direction == "a" or direction == "A":
            position_y = self._captain.get_y() - 1
            if 0 <= position_y < len(self._field[0]):
                self.moveCptHorizontal(-1)
            else:
                print("You can't move that way!")
        elif direction == "d" or direction == "D":
            position_y = self._captain.get_y() + 1
            if 0 <= position_y < len(self._field[0]):
                self.moveCptHorizontal(1)
            else:
                print("You can't move that way!")
        else:
            print(f"{direction} is not a valid option")

    def gameOver(self):
        """
        when veggies all clear, show game over message and related information
        :return: None
        """
        print("GAME OVER!")
        print("You managed to harvest the following vegetables:")
        for item in self._captain.get_veggies_collected():
            print(item)
        print(f"Your score was: {self.getScore()}")

    def highScore(self):
        """
        store user's name and score in high_score file. sort all score, show as a list
        :return: None
        """
        curr_score = None
        if os.path.exists("highscore.data"):
            with open("highscore.data", "rb") as file:
                high_scores = pickle.load(file)
        else:
            high_scores = []
        name = input("Please enter your three initials to go on the scoreboard: ")
        if not high_scores:
            curr_score = (name, self.getScore())
            high_scores.append(curr_score)
        else:
            curr_score = (name, self.getScore())
            high_scores.append(curr_score)
            high_scores.sort(key=lambda x: x[1], reverse=True)

        print("HIGH SCORES")
        print("Name\tScore")
        for name, score in high_scores:
            print(f"{name}\t\t{score}")

        with open("highscore.data", 'wb') as file:
            pickle.dump(high_scores, file)
