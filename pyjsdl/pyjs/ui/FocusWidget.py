from pyjsdl.pyjs.ui.Widget import Widget


class FocusWidget(Widget):

    def __init__(self):
        Widget.__init__(self)
        self._sink_events = None

    def addMouseListener(self, obj):
        element = obj.getElement()
        if not element:
            return
        element.addEventListener('mousemove', self.onMouseMove)
        element.addEventListener('mousedown', self.onMouseDown)
        element.addEventListener('mouseup', self.onMouseUp)
        element.addEventListener('mouseenter', self.onMouseEnter)
        element.addEventListener('mouseleave', self.onMouseLeave)
        element.addEventListener('mousewheel', self.onMouseWheel)

    def addKeyboardListener(self, obj):
        element = obj.getElement()
        if not element:
            return
        element.setAttribute('tabindex','0')
        element.focus()
        element.addEventListener('keypress', self.onKeyPress)
        element.addEventListener('keydown', self.onKeyDown)
        element.addEventListener('keyup', self.onKeyUp)

    def sinkEvents(self, events):
        self._sink_events = events

    def onMouseMove(self, event):
        pass

    def onMouseDown(self, event):
        pass

    def onMouseUp(self, event):
        pass

    def onMouseEnter(self, event):
        pass

    def onMouseLeave(self, event):
        pass

    def onMouseWheel(self, event):
        pass

    def onKeyPress(self, event):
        pass

    def onKeyDown(self, event):
        pass

    def onKeyUp(self, event):
        pass

    def onTouchInitiate(self, event):
        pass

    def onTouchStart(self, event):
        pass

    def onTouchEnd(self, event):
        pass

    def onTouchMove(self, event):
        pass

    def onTouchCancel(self, event):
        pass

