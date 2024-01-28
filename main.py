import pygame
from src.engine import Engine

if __name__ == "__main__":
    pygame.init()
    engine = Engine(screen_size=(1280, 720))
    engine.run()
    pygame.quit()
