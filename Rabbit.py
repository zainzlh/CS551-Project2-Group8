from Creature import Creature


class Rabbit(Creature):
    def __init__(self, x, y):
        Creature.__init__(self, "R", x, y)
