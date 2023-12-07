from Creature import Creature


class Captain(Creature):
    def __init__(self, x, y):
        Creature.__init__(self, "V", x, y)
        self._veggies_collected = []

    def add_veggie(self, veggie):
        self._veggies_collected.append(veggie)

    def lose_lastFive_veggies(self):
        lastFive_veggies = self._veggies_collected[-5:]
        self._veggies_collected = self._veggies_collected[:-5]
        return lastFive_veggies

    def get_veggies_collected(self):
        return self._veggies_collected
