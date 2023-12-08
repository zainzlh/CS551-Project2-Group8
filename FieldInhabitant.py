# Group 8
# Name: Linghao Zhao, Junran Yang
# Date: 12/07/2023
# Description: the class file for FieldInhabitant

class FieldInhabitant:
    def __init__(self, inhabitant):
        self._inhabitant = inhabitant

    def get_inhabitant(self):
        return self._inhabitant

    def set_inhabitant(self, inhabitant):
        self._inhabitant = inhabitant
