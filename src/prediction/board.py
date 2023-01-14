import numpy as np

from config import *
from pedestrian import Pedestrian
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
            self.grid[min(person.x, self.grid.shape[0]-1)][min(person.y, self.grid.shape[1]-1)] = person

    # def __init__(self, dict_pedestrian_positions: dict):
    #
    #     self.list_of_pedestrians = []
    #     # key->id, value->position [id, (x,y)]
    #     for pedestrian_id in dict_pedestrian_positions:
    #         new_pedestrian = Pedestrian(pedestrian_id,
    #                                     np.mean(dict_pedestrian_positions[pedestrian_id][0],  # bottom X mean
    #                                             dict_pedestrian_positions[pedestrian_id][2]),
    #                                     dict_pedestrian_positions[pedestrian_id][1])  # bottom Y
    #         self.grid[new_pedestrian.x][new_pedestrian.y] = new_pedestrian
    #         self.list_of_pedestrians.append(new_pedestrian)
    #
    #     self.add_spaces()
    #
    #     # alternatywa: zamiast dicta, konstruktor BOard moze przyjmowac liste Pedestrianow i
    #     # bedziemy wydobywac przez atrybuty

    def add_spaces(self):

        for person in self.list_of_pedestrians:
            self.create_circle((person.x, person.y), PERSONAL_SPACE_RADIUS, PersonalSpace(person.x, person.y))
            self.create_circle((person.x, person.y), PRIVATE_SPACE_RADIUS, PrivateSpace(person.x, person.y))

            # personal
            # print(self.grid.dtype)
            # cv2.circle(self.grid, (person.x, person.y), PERSONAL_SPACE_RADIUS, 1, 1, cv2.FILLED)
            # cv2.circle(self.grid, (person.x, person.y), PRIVATE_SPACE_RADIUS, 1, 1, cv2.FILLED)

        #     self.grid = np.array(self.grid).reshape(BOARD_SIZE_X, BOARD_SIZE_Y)
        #     # private
        #
        #     self.grid = [PersonalSpace() if i == 1 else i for j in self.grid for i in j]
        #
        #     self.grid = np.array(self.grid).reshape(BOARD_SIZE_X, BOARD_SIZE_Y)
        #
        # self.grid = [PrivateSpace(person.x, person.y) if i == 1 else i for j in self.grid for i in j]
        # self.grid = np.array(self.grid).reshape(BOARD_SIZE_X, BOARD_SIZE_Y)
        #
        # self.grid[person.x][person.y] = person

    def predict_movement(self):
        for person in self.list_of_pedestrians:
            person.predict_movement(self.grid)

    def create_circle(self, center, radius, o):
        # Iterate over the elements of the array
        for x in range(min(0, center[0] - 2 * radius), BOARD_SIZE_X):
            for y in range(min(0, center[0] - 2 * radius), BOARD_SIZE_Y):
                if (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2:
                    self.grid[x, y] = o
    def add_prediction(self, prediction):
        for person in prediction:
            self.grid[person.x][person.y] = person
