# Group 8
# Name: Linghao Zhao, Junran Yang
# Date: 12/07/2023
# Description: the class file for Captain

from Creature import Creature


class Captain(Creature):
    def __init__(self, x, y):
        Creature.__init__(self, "V", x, y)
        self._veggies_collected = []

    def add_veggie(self, veggie):
        self._veggies_collected.append(veggie)

    def lose_lastFive_veggies(self):
        """
        delete the last five veggies in that were added to Captain's basket
        :return: None
        """
        lastFive_veggies = self._veggies_collected[-5:]
        self._veggies_collected = self._veggies_collected[:-5]
        return lastFive_veggies

    def get_veggies_collected(self):
        return self._veggies_collected
