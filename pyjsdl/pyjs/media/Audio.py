class Audio:

    def __init__(self, sound_file):
        self.element = document.createElement("AUDIO")
        self.element.src = sound_file

    def play(self):
        self.element.play()

    def pause(self):
        self.element.pause()

    def getCurrentTime(self):
        return self.element.currentTime

    def setCurrentTime(self, time):
        self.element.currentTime = time

    def isPaused(self):
        return self.element.paused

    def getSrc(self):
        return self.element.src

    def getVolume(self):
        return self.element.volume

    def setVolume(self, volume):
        self.element.volume = volume

    def getDuration(self):
        return self.element.duration

