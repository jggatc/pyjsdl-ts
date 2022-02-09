#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>


class Element:

    def __init__(self, element=None):
        if element is not None:
            self._element = element
        else:
            self._element = None

    @property
    def style(self, attr):
        return self._element.style

    @style.setter
    def style(self, attr, value):
        self._element.style[attr] = value

    def style(self, attr):
        pass

    def getElement(self):
        return self._element

    def setElement(self, element):
        self._element = element

    def setID(self, id):
        self._element.id = id

    def getID(self):
        return self._element.id

    def setSize(self, width, height):
        self.setWidth(width)
        self.setHeight(height)

    def setWidth(self, width):
        if isinstance(width, str):
            self._element.style.width = width
        else:
            self._element.style.width = str(int(width)) + 'px'

    def setHeight(self, height):
        if isinstance(height, str):
            self._element.style['min-height'] = height
        else:
            self._element.style['min-height'] = str(int(height)) + 'px'

    def getAttributes(self):
        return self._element.attributes

    def getClientHeight(self):
        return self._element.clientHeight

    def getClientLeft(self):
        return self._element.clientLeft

    def getClientTop(self):
        return self._element.clientTop

    def getClientWidth(self):
        return self._element.clientWidth

    def getScrollHeight(self):
        return self._element.scrollHeight

    def getScrollLeft(self):
        return self._element.scrollLeft

    def getScrollTop(self):
        return self._element.scrollTop

    def getScrollWidth(self):
        return self._element.scrollWidth

    def addEventListener(self, type, listener, useCapture):
        self._element.addEventListener(type, listener, useCapture)

    def removeEventListener(self, type, listener, useCapture):
        self._element.removeEventListener(type, listener, useCapture)

    def getMouseWheelEventType(self):
        if self._element is not None:
            element = self._element
        else:
            element = document.createElement('div')
        if hasattr(element, 'onwheel'):
            event_type = 'wheel'
        elif hasattr(element, 'onmousewheel'):
            event_type = 'mousewheel'
        else:
            event_type = 'DOMMouseScroll'
        return event_type

    def getAttribute(self):
        return self._element.getAttribute()

    def setAttribute(self, name, value):
        self._element.setAttribute(name, value)

    def getBoundingClientRect(self):
        return self._element.getBoundingClientRect()

    def appendChild(self, el):
        self._element.appendChild(el)

    def removeChild(self, el):
        self._element.removeChild(el)

    def getStyle(self):
        return self._element.style

    def getTitle(self):
        return self._element.title

    def setTitle(self, text):
        self._element.title = text

    def focus(self):
        self._element.focus()

    def  blur(self):
        self._element.blur()

    def click(self):
        self._element.click()


class FocusElement(Element):

    _event_type = None

    def __init__(self):
        Element.__init__(self)
        self._sink_events = None

    def addMouseListener(self, obj):
        element = obj.getElement()
        element.addEventListener('mousemove', self.onMouseMove)
        element.addEventListener('mousedown', self.onMouseDown)
        element.addEventListener('mouseup', self.onMouseUp)
        element.addEventListener('mouseenter', self.onMouseEnter)
        element.addEventListener('mouseleave', self.onMouseLeave)
        if hasattr(element, 'onwheel'):
            element.addEventListener('wheel', self.onMouseWheel)
        elif hasattr(element, 'onmousewheel'):
            element.addEventListener('mousewheel', self.onMouseWheel)
        else:
            element.addEventListener('DOMMouseScroll', self.onMouseWheel)

    def addKeyboardListener(self, obj):
        element = obj.getElement()
        element.setAttribute('tabindex','0')
        element.addEventListener('keydown', self.onKeyDown)
        element.addEventListener('keyup', self.onKeyUp)
        element.addEventListener('keypress', self.onKeyPress)

    def _addKeyboardListener(self, obj):
        element = obj.getElement()
        element.setAttribute('tabindex','0')
        element.addEventListener('keydown', self._onKeyDown)
        element.addEventListener('keyup', self._onKeyUp)
        element.addEventListener('keypress', self._onKeyPress)

    def addKeyEventListener(self, obj):
        element = obj.getElement()
        element.setAttribute('tabindex','0')
        listener = lambda event: self.onKeyEvent(event)
        _listener[self.__name__] = listener
        element.addEventListener('keydown', listener)

    def removeKeyEventListener(self, obj):
        element = obj.getElement()
        listener = _listener[self.__name__]
        element.removeEventListener('keydown', listener)
        del _listener[self.__name__]

    def addFocusListener(self, obj):
        element = obj.getElement()
        element.setAttribute('tabindex','0')
        element.addEventListener('focus', self.onFocus)
        element.addEventListener('blur', self.onBlur)

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

    def onKeyDown(self, event):
        pass

    def onKeyUp(self, event):
        pass

    def onKeyPress(self, event):
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

    def onFocus(self, event):
        pass

    def onBlur(self, event):
        pass

    def focus(self):
        self._element.focus()

    def blur(self):
        self._element.blur()


_listener = {}


class HTML5Canvas(FocusElement):
    _identity = 0

    def __init__(self, width, height):
        FocusElement.__init__(self)
        self._id = HTML5Canvas._identity
        HTML5Canvas._identity += 1
        self._canvas = document.createElement('canvas')
        self._element = self._canvas
        self._element.id = str(self._id)
        self._element.width = width
        self._element.height = height
        self.width = width
        self.height = height
        self._element.style.margin = '0px'
        self._element.style.padding = '0px'
        self._element.style['vertical-align'] = 'bottom'
        self._element.style.id = str(self._id)
        self.canvas = self._element
        self._ctx = self._element.getContext('2d')
        self.impl = CanvasImpl(self._ctx)

    def resize(self, width, height):
        self.width = width
        self.height = height

    def drawImage(self, image, *args):
        ln = len(args)
        if ln == 2:
            self._ctx.drawImage(image,args[0],args[1])
        elif ln == 4:
            self._ctx.drawImage(image,args[0],args[1],args[2],args[3])
        elif ln == 8:
            self._ctx.drawImage(image,args[0],args[1],args[2],args[3],
                                      args[4],args[5],args[6],args[7])

    def fill(self):
        self._ctx.fill()

    def setFillStyle(self, style):
        self._ctx.fillStyle = str(style)

    def fillRect(self, x, y, width, height):
        self._ctx.fillRect(x, y, width, height)

    def py_clear(self):
        #clear()
        self._ctx.clearRect(0, 0, self.width, self.height)

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

    def getContext(self, ctx_type='2d', ctx_attr=None):
        if ctx_attr is None:
            return self._element.getContext(ctx_type)
        else:
            return self._element.getContext(ctx_type, ctx_attr)

    def toDataURL(self, img_type='image/png', enc_options=0.92):
        return self._element.toDataURL(img_type, enc_options)

    def toBlob(self, callback, img_type='image/png', quality=0.92):
        return self._element.toBlob(callback, img_type, quality)

    def getElement(self):
        return self._element


class CanvasImpl:

    def __init__(self, ctx):
        self.canvasContext = ctx


class Panel(Element):

    def __init__(self):
        self._element = document.createElement('div')

    def setID(self, id):
        self._element.id = id

    def getID(self):
        return self._element.id

    def appendChild(self, element):
        self._element.appendChild(element._element)

    def removeChild(self, element):
        self._element.removeChild(element._element)

    def append(self, element):
        self._element.appendChild(element._element)

    def add(self, element):
        self.append(element)

    def remove(self, element):
        self._element.removeChild(element._element)


class RootPanel(Panel):

    _id = None

    def __init__(self):
        if self._id is None:
            self._id = '__panel__'
        self._element = document.getElementById(self._id)

    @classmethod
    def _set_root_panel(cls, id):
        if cls._id is None:
            cls._id = id

    def setId(self, id):
        self._id = id

    def getId(self):
        return self._id

    def add(self, element):
        if isinstance(element, Element):
            self._element.appendChild(element.getElement())
        else:
            self._element.appendChild(element)


class FocusPanel(Panel):
    pass


class VerticalPanel(Panel):

    def __init__(self):
        Panel.__init__(self)
        self._element.style.display = 'flex'
        self._element.style['flex-direction'] = 'column'

    def append(self, element):
        el = element._element
        el.display = 'inline-block'
        el.style.flex = '1'
        el.style.width = '100%'
        self._element.appendChild(el)


class TextBox(Element):

    _type = 'input'

    def __init__(self):
        Element.__init__(self)
        self._element = document.createElement(self._type)
        self._element.style.display = 'inline-block'
        self._element.style.flex = '1'
        self._element.style.border = '1px solid rgb(118, 118, 118)'
        self._element.style.margin = '0px'
        self._element.style.padding = '0px'

    @property
    def value(self):
        return self._element.value

    @value.setter
    def value(self, text):
        self._element.value = text

    def setVisible(self, visible):
        if visible:
            self._element.style.display = 'inline-block'
        else:
            self._element.style.display = 'none'

    def getVisible(self):
        if self._element.style.display != 'none':
            return True
        else:
            return False

    def getText(self):
        return self._element.value

    def setText(self, text):
        self._element.value = text


class TextArea(TextBox):

    _type = 'textarea'

    def __init__(self):
        TextBox.__init__(self)
        self._element.style.resize = 'vertical'


class ImageLoader:

    def __init__(self, imagelist, callback):
        self.imagelist = imagelist
        self.callback = callback
        self.images = []
        self.image_toload = len(self.imagelist)
        for image in self.imagelist:
            self.load(image)

    def load(self, imageurl):
        image = __new__(Image())
        self.images.append(image)
        image.addEventListener('load', self.loaded, False)
        image.src = imageurl

    def loaded(self):
        self.image_toload -= 1
        if not self.image_toload:
            self.callback.onImagesLoaded(self.images)


def loadImages(imagelist, callback):
    ImageLoader(imagelist, callback)


class Color:

    def __init__(self):
        pass


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


class DOM:

    @staticmethod
    def eventGetCurrentEvent():
        return Event()

    @staticmethod
    def setStyleAttribute(element, attr, val):
        element.style[attr] = val

class Event:
    pass


def doc():
    return document


def get_main_frame():
    return document


def wnd():
    return window


def requestAnimationFrameInit():
    requestAnimationFramePolyfill()
    return wnd()


def performanceNowInit():
    performanceNowPolyfill()
    return wnd()


def requestAnimationFramePolyfill():
    __pragma__('js', {},
    """
// http://paulirish.com/2011/requestanimationframe-for-smart-animating/
// http://my.opera.com/emoller/blog/2011/12/20/requestanimationframe-for-smart-er-animating

// requestAnimationFrame polyfill by Erik Möller. fixes from Paul Irish and Tino Zijdel

// MIT license

(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame'] 
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }
 
    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); }, 
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
 
    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());
    """)


def performanceNowPolyfill():
    __pragma__('js', {},
    """
// @license http://opensource.org/licenses/MIT
// copyright Paul Irish 2015


// Date.now() is supported everywhere except IE8. For IE8 we use the Date.now polyfill
//   github.com/Financial-Times/polyfill-service/blob/master/polyfills/Date.now/polyfill.js
// as Safari 6 doesn't have support for NavigationTiming, we use a Date.now() timestamp for relative values

// if you want values similar to what you'd get with real perf.now, place this towards the head of the page
// but in reality, you're just getting the delta between now() calls, so it's not terribly important where it's placed


(function(){

  if ("performance" in window == false) {
      window.performance = {};
  }
  
  Date.now = (Date.now || function () {  // thanks IE8
	  return new Date().getTime();
  });

  if ("now" in window.performance == false){
    
    var nowOffset = Date.now();
    
    if (performance.timing && performance.timing.navigationStart){
      nowOffset = performance.timing.navigationStart
    }

    window.performance.now = function now(){
      return Date.now() - nowOffset;
    }
  }

})();
    """)


fabs = Math.abs


if not String.prototype.count:
    __pragma__ ('js', {},
    """
String.prototype.count = function (sub, start, end) {
    if (start === undefined && start === null) {
        return (this.match (new RegExp (sub, 'g')) || []).length;
    }
    if (start === undefined || start === null) {
        start = 0;
    }
    if (end === undefined || end === null) {
        end = this.length;
    }
    return (this.slice (start, end)
                .match (new RegExp (sub, 'g')) || []).length;
};
    """)


if not String.prototype.splitlines:
    __pragma__ ('js', {},
    """
String.prototype.splitlines = function () {
    return this.split (/\\r\\n|\\r|\\n/g);
};
    """)

