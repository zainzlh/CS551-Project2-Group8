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

    def get_veggies_collected(self):
        return self._veggies_collected
