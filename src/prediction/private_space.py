from space import Space


class PrivateSpace(Space):
    def __init__(self, x, y):
        super()
        super().__init__(x, y)
