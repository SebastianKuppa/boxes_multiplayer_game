import PodSixNet.Channel
import PodSixNet.Server

from time import sleep


class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print(data)


class BoxesServer(PodSixNet.Server.Server):
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0

    channelClass = ClientChannel

    def Connected(self, channel, addr):
        print('new connection: ', channel)
        if self.queue is None:
            self.currentIndex += 1
            channel.gameid = self.currentIndex
        else:
            channel.gameid = self.currentIndex
            self.queue.player1 = channel
            self.queue.player0.Send({"action": "startgame", "player": 0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame", "player": 1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue = None


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


print("STARTING SERVER ON LOCALHOST.")
boxesServe = BoxesServer()
while True:
    boxesServe.Pump()
    sleep(.01)
