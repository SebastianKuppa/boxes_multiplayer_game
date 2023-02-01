import pygame


class BoxesGame:
    def __init__(self):
        pygame.init()
        bounds = (389, 489)
        # init window
        self.window = pygame.display.set_mode(bounds,)
        pygame.display.set_caption('Boxes Multiplayer Game')
        # init clock
        self.clock = pygame.time.Clock()
