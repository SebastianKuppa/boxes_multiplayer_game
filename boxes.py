import pygame


class BoxesGame:
    def __init__(self):
        pygame.init()
        bounds = (400, 489)
        # init window
        self.window = pygame.display.set_mode(bounds,)
        pygame.display.set_caption('Boxes Multiplayer Game')
        # init clock
        self.clock = pygame.time.Clock()
        # init lists for board values
        self.boardh = [[False for x in range(6)] for y in range(7)]  # horizontal bars
        self.boardv = [[False for x in range(7)] for y in range(6)]  # vertical bars

        # debugging
        # self.boardv[3][3] = True
        # self.boardh[3][3] = True

        # init line images
        self.initGraphics()

    def initGraphics(self):
        self.normal_line_v = pygame.image.load('images/normalline.png')
        self.normal_line_h = pygame.transform.rotate(pygame.image.load('images/normalline.png'),
                                                     -90)
        self.bar_h = pygame.image.load('images/bar_done.png')
        self.bar_v = pygame.transform.rotate(pygame.image.load('images/bar_done.png'), -90)
        self.hoverline_v = pygame.image.load('images/hover.png')
        self.hoverline_h = pygame.transform.rotate(pygame.image.load('images/hover.png'), -90)

    def drawBoard(self):
        for x in range(6):
            for y in range(7):
                pass
                if not self.boardh[y][x]:
                    self.window.blit(self.normal_line_v, [x*64+5, y*64])
                else:
                    self.window.blit(self.bar_h, [x * 64 + 5, y * 64])
        for x in range(7):
            for y in range(6):
                if not self.boardv[y][x]:
                    self.window.blit(self.normal_line_h, [x * 64 + 5, y * 64])
                else:
                    self.window.blit(self.bar_v, [x * 64 + 5, y * 64])

    def update(self):
        # sleep function
        self.clock.tick(60)
        # clear screen
        self.window.fill(0)
        # draw the current state of the board
        self.drawBoard()
        for event in pygame.event.get():
            # exit game when quit button is pressed
            if event.type == pygame.QUIT:
                exit()
        # update the window screen
        pygame.display.flip()

