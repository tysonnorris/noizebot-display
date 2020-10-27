

class Spotify:
    def __init__(self):
        self.playing = False
    def play(self):
        print("Spotify Start Playing...")
    def pause(self):
        print("Spotify Pause Playing...")

    def getPlaylists(self):
        return [{"name": "playlist1", "id":"1234"}, {"name":"playlist2","id":"4567"}]
    def togglePlay(self):
        if self.playing:
            self.play()
        else:
            self.pause()
        self.playing = not self.playing
