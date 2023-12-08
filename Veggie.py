# Group 8
# Name: Linghao Zhao, Junran Yang
# Date: 12/07/2023
# Description: the class file for Veggie

from FieldInhabitant import FieldInhabitant


class Veggie(FieldInhabitant):
    def __init__(self, inhabitant, name, points):
        FieldInhabitant.__init__(self, inhabitant)
        self._name = name
        self._points = points

    def __str__(self):
        return f"{self._inhabitant}: {self._name} {self._points} points"

    def get_name(self):
        return self._name

    def get_points(self):
        return self._points
