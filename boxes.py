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

    def update(self):
        # sleep function
        self.clock.tick(60)
        # clear screen
        self.window.fill(0)

        for event in pygame.event.get():
            # exit game when quit button is pressed
            if event.type == pygame.QUIT:
                exit()
        # update the window screen
        pygame.display.flip()

