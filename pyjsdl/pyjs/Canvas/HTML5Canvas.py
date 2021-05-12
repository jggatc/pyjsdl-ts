from pyjsdl.pyjs.ui.FocusWidget import FocusWidget
import time


class HTML5Canvas(FocusWidget):
    _identity = 0

    def __init__(self, width, height):
        FocusWidget.__init__(self)
        if HTML5Canvas._identity:
            self._id = HTML5Canvas._identity
            HTML5Canvas._identity += 1
            self._canvas = document.createElement('canvas')
            self._canvas.id = str(self._id)
        else:
            self._id = HTML5Canvas._identity
            HTML5Canvas._identity += 1
            self._canvas = document.getElementById('canvas')
        self._canvas.width = width
        self._canvas.height = height
        self.width = width
        self.height = height
        self._canvas.style = {'background': 'black', 'id':str(self._id)}
        self.canvas = self._canvas
        self._ctx = self._canvas.getContext('2d')
        self.impl = CanvasImpl(self._ctx)

    def resize(self, width, height):
        self.width = width
        self.height = height

    def drawImage(self, image, *args):
        if len(args) == 2:
            self._ctx.drawImage(image,args[0],args[1])
        if len(args) == 4:
            self._ctx.drawImage(image,args[0],args[1],args[2],args[3])
        elif len(args) == 8:
            self._ctx.drawImage(image,args[0],args[1],args[2],args[3], args[4],args[5],args[6],args[7])

    def fill(self):
        self._ctx.fill()

    def setFillStyle(self, style):
        self._ctx.fillStyle = str(style)

    def fillRect(self, x, y, width, height):
        self._ctx.fillRect(x, y, width, height)

    def clear(self):
        self._ctx.clear()

    def setLineWidth(self, width):
        self._ctx.lineWidth = width

    def setStrokeStyle(self, style):
        self._ctx.strokeStyle = str(style)

    def strokeRect(self, x, y, width, height):
        self._ctx.strokeRect(x, y, width, height)

    def saveContext(self):
        self._ctx.save()

    def restoreContext(self):
        self._ctx.restore()

    def translate(self, x, y):
        self._ctx.translate(x,y)

    def scale(self, x, y):
        self._ctx.scale(x,y)

    def rotate(self, angle):
        self._ctx.rotate(angle)

    def transform(self, m11, m12, m21, m22, dx, dy):
        self._ctx.transform(m11, m12, m21, m22, dx, dy)

    def arc(self, x, y, r, sAngle, eAngle, counterclockwise):
        self._ctx.arc(x, y, r, sAngle, eAngle, counterclockwise)

    def beginPath(self):
        self._ctx.beginPath()

    def closePath(self):
        self._ctx.closePath()

    def moveTo(self, x, y):
        self._ctx.moveTo(x, y)

    def lineTo(self, x, y):
        self._ctx.lineTo(x, y)

    def stroke(self):
        self._ctx.stroke()

    def setFont(self, font):
        self._ctx.font = font

    def setTextAlign(self, align):
        self._ctx.textAlign = align

    def setTextBaseline(self, baseline):
        self._ctx.textBaseline = baseline

    def fillText(self, text, x, y):
        self._ctx.fillText(text, x, y)

    def strokeText(self, text, x, y):
        self._ctx.strokeText(text, x, y)

    def measureText(self, text):
        return self._ctx.measureText(text).width

    def getImageData(self, x, y, width, height):
        return self._ctx.getImageData(x, y, width, height)

    def putImageData(self, *args):
        if len(args) == 3:
            self._ctx.putImageData(args[0], args[1], args[2])
        else:
            self._ctx.putImageData(args[0], args[1], args[2], args[3], args[4], args[5], args[6])

    def toDataURL(self):
        return self._canvas.toDataURL()

    def getElement(self):
        return self._canvas


class CanvasImpl:

    def __init__(self, ctx):
        self.canvasContext = ctx

