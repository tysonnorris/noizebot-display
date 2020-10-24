

class Spotify:
    def __init__(self):
        self.playing = False
    def play(self):
        print("Spotify Start Playing...")
    def pause(self):
        print("Spotify Pause Playing...")

    def togglePlay(self):
        if self.playing:
            self.play()
        else:
            self.pause()
        self.playing = not self.playing
