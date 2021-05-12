class Audio:

    def __init__(self, sound_file):
        self.obj = document.createElement("AUDIO")
        self.obj.src = sound_file
        self.obj.play()

    def play(self):
        self.obj.play()

    def pause(self):
        self.obj.pause()

    def getCurrentTime(self):
        return self.obj.currentTime

    def setCurrentTime(self, time):
        self.obj.currentTime = time

    def isPaused(self):
        return self.obj.paused

    def getSrc(self):
        return self.obj.src

    def getVolume(self):
        return self.obj.volume

    def setVolume(self, volume):
        self.obj.volume = volume

    def getDuration(self):
        return self.obj.duration

