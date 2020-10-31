

class Spotify:
    def __init__(self):
        self.playing = False
    def play(self):
        print("Spotify Start Playing...")
    def pause(self):
        print("Spotify Pause Playing...")

    def getPlaylists(self):
        return [{"name": "playlist1", "id":"1234"},
                {"name":"playlist2","id":"4567"},
                {"name":"playlist3","id":"4568"},
                {"name":"playlist4","id":"4569"},
                {"name":"playlist5","id":"45601"},
                {"name":"playlist6","id":"45602"},
                {"name":"playlist7","id":"45603"},
                {"name":"playlist8","id":"45604"},
                {"name":"playlist9","id":"45605"},
                {"name":"playlist10","id":"45606"},
                {"name":"playlist11","id":"45607"},
                {"name":"playlist12","id":"45608"}]
    def togglePlay(self):
        if self.playing:
            self.play()
        else:
            self.pause()
        self.playing = not self.playing
