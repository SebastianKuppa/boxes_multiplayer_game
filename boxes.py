from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

import pygame
import math


class BoxesGame(ConnectionListener):
    def __init__(self):
        pygame.init()
        pygame.display.list_modes()
        # init window
        self.window = pygame.display.set_mode((400, 589))
        pygame.display.set_caption('Boxes Multiplayer Game')
        # init clock
        self.clock = pygame.time.Clock()
        # init lists for board values
        self.boardh = [[False for _ in range(6)] for _ in range(7)]  # horizontal bars
        self.boardv = [[False for _ in range(7)] for _ in range(6)]  # vertical bars

        # init line images
        self.initGraphics()
        # init sounds
        self.initSounds()

        self.turn = True
        self.me = 0
        self.enemy = 0
        self.didIwin = False

        self.gameid = None
        self.num = None

        self.justplaced = 10

        # keeping track of the squares which are won by player
        self.owner = [[0 for x in range(6)] for y in range(6)]

        self.Connect(address=("127.0.0.1", 5071))
        # connection.DoConnect(address=("127.0.0.1", 5071))
        print("Connected..")

        self.running = False
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(.01)
        # get player attribs
        if self.num == 0:
            self.turn = True
            self.marker = self.greenplayer
            self.othermarker = self.blueplayer
        else:
            self.turn = False
            self.marker = self.blueplayer
            self.othermarker = self.greenplayer

    def initSounds(self):
        pygame.mixer.music.load("./sounds/game.mp3")
        self.winsound = pygame.mixer.Sound("./sounds/win.mp3")
        self.losesound = pygame.mixer.Sound("./sounds/lose.mp3")
        self.placesound = pygame.mixer.Sound("./sounds/win_box.mp3")
        # play background music
        # pygame.mixer.music.play()

    def initGraphics(self):
        self.normal_line_v = pygame.image.load('images/normalline.png')
        self.normal_line_h = pygame.transform.rotate(pygame.image.load('images/normalline.png'), -90)

        self.bar_h = pygame.image.load('images/bar_done.png')
        self.bar_v = pygame.transform.rotate(pygame.image.load('images/bar_done.png'), -90)

        self.hoverline_v = pygame.image.load('images/hover.png')
        self.hoverline_h = pygame.transform.rotate(pygame.image.load('images/hover.png'), -90)

        self.green_light = pygame.image.load('images/green_light.png')
        self.red_light = pygame.image.load('images/red_light.png')

        self.gameover = pygame.image.load('images/gameover.png')
        self.youwin = pygame.image.load('images/youwin.png')

        self.greenplayer = pygame.image.load("images/green_rect.png")
        self.blueplayer = pygame.image.load("images/blue_rect.png")

    def drawOwnerMap(self):
        for x in range(6):
            for y in range(6):
                if self.owner[x][y] != 0:
                    if self.owner[x][y] == "win":
                        self.window.blit(self.marker, (x*64+10, y*64+5))
                    if self.owner[x][y] == "lose":
                        self.window.blit(self.othermarker, (x*64+10, y*64+5))

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

    def drawHUD(self):
        # init font for text "Your turn"
        font = pygame.font.Font('freesansbold.ttf', 32)
        # render text
        text = font.render('Your turn:', True, 'blue')
        # draw background for the area below the gameboard
        self.window.blit(text, (10, 400))
        # add light bulb to see if it is your turn or not
        self.window.blit(self.green_light if self.turn else self.red_light, (170, 400))
        # adding different sized fonts
        font_withsize20 = pygame.font.SysFont(None, 20)
        font_withsize64 = pygame.font.SysFont(None, 64)

        score_me = font_withsize64.render(str(self.me), True, [255, 255, 255])
        score_other = font_withsize64.render(str(self.enemy), True, [255, 255, 255])
        score_text_me = font_withsize64.render("YOU", True, [255, 255, 255])
        score_text_other = font_withsize64.render("ENEMY", True, [255, 255, 255])

        blueplayer_icon = pygame.transform.scale(self.blueplayer, (30, 30))
        greenplayer_icon = pygame.transform.scale(self.greenplayer, (30, 30))

        self.window.blit(score_text_me, (10, 450))
        self.window.blit(score_me, (10, 500))
        self.window.blit(score_text_other, (240, 450))
        self.window.blit(score_other, (240, 500))

        if self.num == 0:
            self.window.blit(greenplayer_icon, (10, 550))
            self.window.blit(blueplayer_icon, (240, 550))
        else:
            self.window.blit(blueplayer_icon, (10, 550))
            self.window.blit(greenplayer_icon, (240, 550))

    def update(self):
        # check if the game has finished, and set win attribute accordingly
        if self.me + self.enemy == 36:
            self.didIwin = True if self.me > self.enemy else False
            return 1

        self.justplaced -= 1
        connection.Pump()
        self.Pump()
        # sleep function
        self.clock.tick(60)
        # clear screen
        self.window.fill(0)
        # draw the current state of the board
        self.drawBoard()
        # draw HUD
        self.drawHUD()
        self.drawOwnerMap()
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

        if pygame.mouse.get_pressed()[0] and not alreadyPlaced and not isOutOfBounds \
                and self.turn is True and self.justplaced <= 0:
            if is_horizontal:
                self.boardh[y_pos][x_pos] = True
                self.Send({"action": "place", "x": x_pos, "y": y_pos, "is_horizontal": is_horizontal,
                           "gameid": self.gameid, "num": self.num})
            else:
                self.boardv[y_pos][x_pos] = True
                self.Send({"action": "place", "x": x_pos, "y": y_pos, "is_horizontal": is_horizontal,
                           "gameid": self.gameid, "num": self.num})
            self.justplaced = 100
        # update the window screen
        pygame.display.flip()

    def finished(self):
        self.window.blit(self.gameover if not self.didIwin else self.youwin, (20, 20))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()

    # def Network(self, data):
        # print("random data: ")
        # print("Network:", data)

    def Network_startgame(self, data):
        print("Network_startgame:", data)
        self.running = True
        self.num = data["player"]
        self.gameid = data["gameid"]

    def Network_close(self, data):
        exit()

    def Network_place(self, data):
        # print("Received placing Data")
        # get attributes
        x = data["x"]
        y = data["y"]
        hv = data["is_horizontal"]
        # horizontal or vertical
        if hv:
            self.boardh[y][x] = True
        else:
            self.boardv[y][x] = True
        # play sound
        self.placesound.play()

    def Network_yourturn(self, data):
        # print('Network_yourturn:')
        # print("Network:", data)
        self.turn = data["torf"]

    def Network_win(self, data):
        self.owner[data['x']][data['y']] = "win"
        self.boardh[data['y']][data['x']] = True
        self.boardv[data['y']][data['x']] = True
        self.boardh[data['y'] + 1][data['x']] = True
        self.boardv[data['y']][data['x'] + 1] = True
        self.me += 1
        # play sound
        self.winsound.play()

    def Network_lose(self, data):
        self.owner[data['x']][data['y']] = "lose"
        self.boardh[data['y']][data['x']] = True
        self.boardv[data['y']][data['x']] = True
        self.boardh[data['y'] + 1][data['x']] = True
        self.boardv[data['y']][data['x'] + 1] = True
        self.enemy += 1
        # play sound
        self.losesound.play()
