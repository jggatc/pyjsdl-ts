class Widget:

    def __init__(self):     ###
        self._id = None

    def setID(self, id):    ###
        document.getElementById('canvas').id = id
        self._id = id

    def getID(self):        ###
        if self._id:
            return self._id
        else:
            return ''

