import numpy as np

from config import ITER_PEDESTRIAN_VELOCITY


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Velocities(metaclass=SingletonMeta):

    def __init__(self):

        self.velocities = [] # id: [ [x, y], velocity]
        self.positions = []  # id: [x, y]

    def add(self, positions):
        self.positions.append(positions)
        self.calculate_velocities()

    def get_latest(self):
        return self.velocities[-1]

    def get_velocity_pedestrian(self, pedestrian_id) -> list:
        if len(self.velocities) == 0:
            return [0, 0]

        n_last = self.velocities[-min(len(self.velocities)-1, ITER_PEDESTRIAN_VELOCITY):]

        x = np.mean([v[pedestrian_id][0][0] for v in n_last if pedestrian_id in v])
        y = np.mean([v[pedestrian_id][0][1] for v in n_last if pedestrian_id in v])
        #
        # means = np.mean(
        #     self.velocities[-min(len(self.velocities[pedestrian_id])-1, ITER_PEDESTRIAN_VELOCITY):][pedestrian_id][0],
        #     axis=0)
        return [round(x), round(y)]

    def calculate_velocities(self):
        current_velocities = dict()

        if len(self.positions) < 2:
            return
        for pedestrian in self.positions[-1]:
            if pedestrian not in self.positions[-2]:
                current_velocities[pedestrian] = [[0, 0], 0]
            else:
                x = self.positions[-1][pedestrian][0] - self.positions[-2][pedestrian][0]
                y = self.positions[-1][pedestrian][1] - self.positions[-2][pedestrian][1]
                current_velocities[pedestrian] = [[x, y], (x ** 2 + y ** 2) ** 0.5]

        self.velocities.append(current_velocities)
