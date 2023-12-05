from FieldInhabitant import FieldInhabitant


class Veggie(FieldInhabitant):
    def __init__(self, inhabitant, name, points):
        FieldInhabitant.__init__(self, inhabitant)
        self._name = name
        self._points = points

    def __str__(self):
        return f"{self.get_inhabitant()}: {self._name} {self._points} points"

    def get_name(self):
        return self._name

    def get_points(self):
        return self._points
