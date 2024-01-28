from pygame import Vector2


class Camera:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.target = None

    def set_target(self, target):
        self.target = target

    def set_pos(self, pos):
        self.pos = Vector2(pos)

    def get_pos(self):
        return self.pos.x, self.pos.y
