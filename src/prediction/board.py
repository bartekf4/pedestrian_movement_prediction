import numpy as np

from config import *
from personal_space import PersonalSpace
from private_space import PrivateSpace


class Board:
    """A class representing pedestrian's location on single video shot"""

    def __init__(self, list_of_pedestrians: list):
        self.list_of_pedestrians = list_of_pedestrians
        self.grid = np.empty((BOARD_SIZE_X + 1, BOARD_SIZE_Y + 1), dtype=np.dtype(object))
        self.x = BOARD_SIZE_X
        self.y = BOARD_SIZE_Y
        self.add_spaces()
        for person in list_of_pedestrians:
            self.grid[min(person.x, self.grid.shape[0] - 1)][min(person.y, self.grid.shape[1] - 1)] = person

    def add_spaces(self):

        for person in self.list_of_pedestrians:
            self.create_circle((person.x, person.y), PERSONAL_SPACE_RADIUS, PersonalSpace(person.x, person.y))
            self.create_circle((person.x, person.y), PRIVATE_SPACE_RADIUS, PrivateSpace(person.x, person.y))

    def predict_movement(self):
        for person in self.list_of_pedestrians:
            person.predict_movement(self.grid)

    def create_circle(self, center, radius, o):
        for x in range(min(0, center[0] - 2 * radius), BOARD_SIZE_X):
            for y in range(min(0, center[0] - 2 * radius), BOARD_SIZE_Y):
                if (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2:
                    self.grid[x, y] = o

    def add_prediction(self, prediction):
        for person in prediction:
            self.grid[person.x][person.y] = person
