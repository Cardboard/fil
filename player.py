class Player:
    def __init__(self, x, y, rotation=0):
        self.x = x
        self.y = y
        self.rot = rotation

    def set_pos(self, pos):
        self.x, self.y = pos

    def set_rot(self, rotation):
        self.rot = rotation

    def get_pos(self):
        return (self.x, self.y)
    def get_rot(self):
        return self.rot
