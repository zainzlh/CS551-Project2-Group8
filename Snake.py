# Group 8
# Name: Linghao Zhao, Junran Yang
# Date: 12/07/2023
# Description: the class file for Snake

from Creature import Creature


class Snake(Creature):
    def __init__(self, x, y):
        super().__init__("S", x, y)
