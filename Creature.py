# Group 8
# Name: Linghao Zhao, Junran Yang
# Date: 12/07/2023
# Description: the class file for Creature

from FieldInhabitant import FieldInhabitant


class Creature(FieldInhabitant):
    def __init__(self, inhabitant, x, y):
        FieldInhabitant.__init__(self, inhabitant)
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_position(self, x, y):
        self._x = x
        self._y = y
