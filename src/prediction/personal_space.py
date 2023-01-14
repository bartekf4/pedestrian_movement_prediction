from config import *
from space import Space


class PersonalSpace(Space):
    def __init__(self, x, y):
        super()
        super().__init__(x, y)
        self.radius = PERSONAL_SPACE_RADIUS
