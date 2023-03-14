import PodSixNet.Channel
import PodSixNet.Server
import random

from time import sleep


class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print(f"Network data as follows {data}")

    def Network_place(self, data):
        # deconsolidate all of the data from the dictionary
        print("Network_place is executed...")
        # horizontal or vertical?
        hv = data["is_horizontal"]
        # x of placed line
        x = data["x"]

        # y of placed line
        y = data["y"]

        # player number (1 or 0)
        num = data["num"]

        # id of game given by server at start of game
        self.gameid = data["gameid"]

        # tells server to place line
        self._server.placeLine(hv, x, y, data, self.gameid, num)

    def Close(self):
        self._server.close(self.gameid)


class BoxesServer(PodSixNet.Server.Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0

    def Connected(self, channel, addr):
        print('new connection: ', channel)
        if self.queue is None:
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
        else:
            channel.gameid = self.currentIndex
            self.queue.player1 = channel
            self.queue.player0.Send({"action": "startgame", "player": 0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame", "player": 1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue = None

    def close(self, gameid):
        try:
            game = [a for a in self.games if a.gameid == gameid][0]
            game.player0.Send({'action': 'close'})
            game.player1.Send({'action': 'close'})
        except:
            pass

    def placeLine(self, is_h, x, y, data, gameid, num):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            self.games[0].placeLine(is_h, x, y, data, num)

    def tick(self):
        # 1
        index = 0
        change = 3
        # 2
        for game in self.games:
            change = 3
            for time in range(2):
                # 3
                for y in range(6):
                    for x in range(6):
                        if game.boardh[y][x] and game.boardv[y][x] and game.boardh[y+1][x] and game.boardv[y][x+1] and \
                                not game.owner[x][y]:
                            rand_no = random.randint(1, 9)
                            rand_box_val = random.randint(1, 2)
                            if self.games[index].turn == 0:
                                self.games[index].owner[x][y] = 2
                                game.player1.Send({'action': 'win', 'x': x, 'y': y, 'randInt': rand_no, 'rand_box_val': rand_box_val})
                                game.player0.Send({'action': 'lose', 'x': x, 'y': y, 'randInt': rand_no, 'rand_box_val': rand_box_val})
                                change = 1
                            else:
                                self.games[index].owner[x][y] = 1
                                game.player0.Send({'action': 'win', 'x': x, 'y': y, 'randInt': rand_no, 'rand_box_val': rand_box_val})
                                game.player1.Send({'action': 'lose', 'x': x, 'y': y, 'randInt': rand_no, 'rand_box_val': rand_box_val})
                                change = 0
            # 5
            self.games[index].turn = change if change != 3 else self.games[index].turn
            game.player1.Send({'action': 'yourturn', 'torf': True if self.games[index].turn == 1 else False})
            game.player0.Send({'action': 'yourturn', 'torf': True if self.games[index].turn == 0 else False})
            index += 1
        self.Pump()


class Game:
    def __init__(self, player0, currentindex):
        # whos turn is it 1 or 0
        self.turn = 0
        # owner map
        self.owner = [[False for x in range(6)] for y in range(6)]
        # vertical and horizontal boards of bars
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        # init players
        self.player0 = player0
        self.player1 = None
        # init gameID
        self.gameid = currentindex

    def placeLine(self, is_h, x, y, data, num):
        # make sure it's their turn
        if num == self.turn:
            self.turn = 0 if self.turn == 1 else 1
            # place line in game
            if is_h:
                self.boardh[y][x] = True
            else:
                self.boardv[y][x] = True
            # send data and turn data to each player
            self.player0.Send(
                {'action': 'place', 'x': x, 'y': y, 'is_horizontal': is_h, 'gameid': self.gameid, 'num': num}
            )
            self.player1.Send(
                {'action': 'place', 'x': x, 'y': y, 'is_horizontal': is_h, 'gameid': self.gameid, 'num': num}
            )
            self.player1.Send({'action': 'yourturn', 'torf': True if self.turn == 1 else False})
            self.player0.Send({'action': 'yourturn', 'torf': True if self.turn == 0 else False})


print("STARTING SERVER ON LOCALHOST.")
boxesServer = BoxesServer()
while True:
    boxesServer.tick()
    sleep(.01)
