# Group 8
# Name: Linghao Zhao, Junran Yang
# Date: 12/07/2023
# Description: the class file for Rabbit

from Creature import Creature


class Rabbit(Creature):
    def __init__(self, x, y):
        Creature.__init__(self, "R", x, y)
