import pygame
import math


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
        # self.boardv[0][1] = True
        # self.boardh[0][0] = True

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
        # get current mouse position in pixels (as tuple)
        mouse = pygame.mouse.get_pos()
        # get boolean if mouse button is currently pressed
        mouse_pressed = pygame.mouse.get_pressed()[0]
        # calculate bar index, which the mouse is closest to
        x_pos = int(math.ceil((mouse[0] - 32)/64.0))
        y_pos = int(math.ceil((mouse[1] - 32)/64.0))
        # divide the area inside the cube into 4 triangles and determine, based on the mouse position
        # if the mouse position is closer to one of the horizontal bars or the vertical ones
        is_horizontal = abs(mouse[1] - y_pos*64) < abs(mouse[0] - x_pos*64)
        # print(f'is_horizontal: {is_horizontal}')

        x_pos = x_pos - 1 if (mouse[0] - x_pos*64 < 0) and is_horizontal else x_pos
        y_pos = y_pos - 1 if (mouse[1] - (y_pos*64) < 0) and not is_horizontal else y_pos

        board = self.boardh if is_horizontal else self.boardv
        isOutOfBounds = False

        try:
            if not board[y_pos][x_pos]:
                # if not mouse_pressed:
                self.window.blit(self.hoverline_v if is_horizontal else self.hoverline_h,
                                 [(x_pos * 64)+5,
                                  (y_pos * 64)])
        except IndexError:
            isOutOfBounds =True
            pass
        if not isOutOfBounds:
            alreadyPlaced = board[y_pos][x_pos]
        else:
            alreadyPlaced = False

        if pygame.mouse.get_pressed()[0] and not alreadyPlaced and not isOutOfBounds:
            board[y_pos][x_pos] = True

        # update the window screen
        pygame.display.flip()

