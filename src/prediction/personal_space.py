from space import Space
from config import *


class PersonalSpace(Space):
    def __init__(self, x, y):
        super()
        super().__init__(x, y)
        self.radius = PERSONAL_SPACE_RADIUS


