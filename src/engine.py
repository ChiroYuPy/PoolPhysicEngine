import pygame as pg
from pygame import NOFRAME
from src.entity import Entity
from src.camera import Camera


color_palette = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (255, 165, 0),
    (0, 255, 255),
    (139, 69, 19),
    (0, 255, 0),
    (0, 128, 128),
    (128, 0, 0),
    (0, 0, 128),
    (128, 128, 0),
    (192, 192, 192),
    (128, 128, 128),
    (255, 215, 0),
    (255, 192, 203),
    (250, 128, 114),
    (135, 206, 235),
    (0, 100, 0),
    (75, 0, 130),
    (255, 105, 180),
    (0, 139, 139),
    (255, 0, 255),
    (238, 130, 238),
    (240, 230, 140),
    (64, 224, 208),
    (218, 112, 214),
    (112, 128, 144),
    (255, 127, 80)]


class Engine:
    def __init__(self, screen_size):
        self.last_collision_check = 0
        self.sW = screen_size[0]
        self.sH = screen_size[1]
        self.screen = pg.display.set_mode((self.sW, self.sH), NOFRAME)
        self.clock = pg.time.Clock()
        self.camera = Camera()
        self.entity_index = 0
        self.entities = [Entity(pos=(300, self.sH / 2+1), velocity=(10, 0), color=color_palette[0]),
                         Entity(pos=(self.sW - 300, self.sH / 2), velocity=(0, 0),
                                color=color_palette[1]),
                         Entity(pos=(self.sW / 2, self.sH / 2), velocity=(0, 0),
                                color=color_palette[2])]
        self.initializing()

    def initializing(self):
        self.camera.set_target(self.entities[self.entity_index])

    def switch_to_next_player(self):
        self.entity_index = (self.entity_index + 1) % len(self.entities)
        self.camera.set_target(self.entities[self.entity_index])

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()

    def update(self):
        self.collision_handler()

        for player in self.entities:
            player.move()

        self.camera.set_pos((self.sW / 2 - self.camera.target.pos.x, self.sH / 2 - self.camera.target.pos.y))

    def collision_handler(self):
        def collide(entity1, entity2):
            distance = entity1.pos.distance_to(entity2.pos)
            if distance < entity1.size / 2 + entity2.size / 2:
                return True
            return False

        for entity1 in self.entities:
            entity1.clamp_pos(0, 0, self.sW, self.sH)
            current_time = pg.time.get_ticks()
            for entity2 in self.entities:
                if entity1 != entity2 and collide(entity1, entity2) and current_time - self.last_collision_check > 10:
                    self.last_collision_check = current_time

                    relative_position = entity2.pos - entity1.pos
                    relative_velocity = entity2.velocity - entity1.velocity
                    distance_sq = relative_position.length_squared()

                    if distance_sq != 0:
                        dot_product = relative_position.dot(relative_velocity)
                        new_velocity1 = entity1.velocity + (2 * entity2.mass / (
                                    entity1.mass + entity2.mass)) * dot_product * relative_position / distance_sq
                        new_velocity2 = entity2.velocity - (2 * entity1.mass / (
                                    entity1.mass + entity2.mass)) * dot_product * relative_position / distance_sq

                        entity1.velocity = new_velocity1
                        entity2.velocity = new_velocity2

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        return True

    def render(self):
        self.screen.fill((0, 0, 0))
        self.draw()
        pg.display.update()
        self.clock.tick(60)
        pg.display.set_caption(str(self.clock.get_fps()))

    def draw(self):
        for entity in self.entities:
            entity.draw(self.screen)