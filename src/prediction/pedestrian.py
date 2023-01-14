import numpy as np


class Pedestrian:
    def __init__(self, id, x, y, velocity):
        self.destination = None
        self.path = None
        self.id = id
        self.x = x
        self.y = y
        self.velocity = velocity
        self.color = self.__randomColor()

    def update_position(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.destination = self.x + (5 * self.velocity[0]), self.y + (5 * self.velocity[1])

    def __randomColor(self) -> tuple:
        return tuple(
            (int(np.random.choice(range(150, 256))), int(np.random.choice(range(150, 256))),
             int(np.random.choice(range(150, 256)))))

    @property
    def position(self):
        return self.x, self.y
