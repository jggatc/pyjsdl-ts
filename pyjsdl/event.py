#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl import env
from pyjsdl import locals as Const

__docformat__ = 'restructuredtext'


class Event(object):
    """
    **pyjsdl.event**
    
    * pyjsdl.event.pump
    * pyjsdl.event.get
    * pyjsdl.event.poll
    * pyjsdl.event.wait
    * pyjsdl.event.peek
    * pyjsdl.event.clear
    * pyjsdl.event.event_name
    * pyjsdl.event.set_blocked
    * pyjsdl.event.set_allowed
    * pyjsdl.event.get_blocked
    * pyjsdl.event.post
    * pyjsdl.event.Event
    """

    def __init__(self):
        """
        Maintain events received from browser.
        
        Module initialization creates pyjsdl.event instance.
        """
        self.eventQueue = [None for i in range(256)]
        self.eventNum = 0
        self.eventQueueTmp = [None for i in range(256)]
        self.eventNumTmp = 0
        self.queueLock = False
        self.queueAccess = False
        self.queue = []
        self.queueNil = []
        self.queueTmp = []
        self.mousePress = {0:False, 1:False, 2:False}
        self.mouseMove = {'x':-1, 'y':-1}
        self.mouseMoveRel = {'x':None, 'y':None}
        self.keyPress = {Const.K_ALT:False, Const.K_CTRL:False, Const.K_SHIFT:False}
        self.keyMod = {Const.K_ALT:{True:Const.KMOD_ALT,False:0}, Const.K_CTRL:{True:Const.KMOD_CTRL,False:0}, Const.K_SHIFT:{True:Const.KMOD_SHIFT,False:0}}
        self.eventName = {Const.MOUSEMOTION:'MouseMotion', Const.MOUSEBUTTONDOWN:'MouseButtonDown', Const.MOUSEBUTTONUP:'MouseButtonUp', Const.KEYDOWN:'KeyDown', Const.KEYUP:'KeyUp', 'mousemove':'MouseMotion', 'mousedown':'MouseButtonDown', 'mouseup':'MouseButtonUp', 'keydown':'KeyDown', 'keyup':'KeyUp'}
        self.eventType = [Const.MOUSEMOTION, Const.MOUSEBUTTONDOWN, Const.MOUSEBUTTONUP, Const.KEYDOWN, Const.KEYUP, 'mousemove', 'mousedown', 'mouseup', 'wheel', 'mousewheel', 'DOMMouseScroll', 'keydown', 'keypress', 'keyup']
        self.events = set(self.eventType)
        self.eventTypes = {Const.MOUSEMOTION: set([Const.MOUSEMOTION, 'mousemove']), Const.MOUSEBUTTONDOWN: set([Const.MOUSEBUTTONDOWN, 'mousedown', 'wheel', 'mousewheel',  'DOMMouseScroll']), Const.MOUSEBUTTONUP: set([Const.MOUSEBUTTONUP, 'mouseup']), Const.KEYDOWN: set([Const.KEYDOWN, 'keydown', 'keypress']), Const.KEYUP: set([ Const.KEYUP, 'keyup'])}
        if env.pyjs_mode.optimized:
            self.modKey = set([Const.K_ALT, Const.K_CTRL, Const.K_SHIFT])
            self.specialKey = set([Const.K_UP, Const.K_DOWN, Const.K_LEFT, Const.K_RIGHT, Const.K_HOME, Const.K_END, Const.K_PAGEDOWN, Const.K_PAGEUP, Const.K_BACKSPACE, Const.K_DELETE, Const.K_INSERT, Const.K_RETURN, Const.K_TAB, Const.K_ESCAPE])
        else:   #pyjs-S onKeyDown keycode 'mod' not in set, due to js/pyjs numeric diff
            self.modKey = set([keycode.valueOf() for keycode in (Const.K_ALT, Const.K_CTRL, Const.K_SHIFT)])
            self.specialKey = set([keycode.valueOf() for keycode in (Const.K_UP, Const.K_DOWN, Const.K_LEFT, Const.K_RIGHT, Const.K_HOME, Const.K_END, Const.K_PAGEDOWN, Const.K_PAGEUP, Const.K_BACKSPACE, Const.K_DELETE, Const.K_INSERT, Const.K_RETURN, Const.K_TAB, Const.K_ESCAPE)])
#Const.K_F1, Const.K_F2, Const.K_F3, Const.K_F4, Const.K_F5, Const.K_F6, Const.K_F7, Const.K_F8, Const.K_F9, Const.K_F10, Const.K_F11, Const.K_F12, Const.K_F13, Const.K_F14, Const.K_F15   #IE keypress keycode: id same as alpha keys
        self.touchlistener = None
        self.Event = UserEvent
        self._nonimplemented_methods()

    def _lock(self):
        self.queueLock = True

    def _unlock(self):
        self.queueLock = False

    def _updateQueue(self, event):
        self.queueAccess = True
        if not self.queueLock:
            if self.eventNumTmp:
                 self._appendMerge()
            self._append(JEvent(event))
        else:
            self._appendTmp(JEvent(event))
        self.queueAccess = False

    def _append(self, event):
        if self.eventNum < 255:
            self.eventQueue[self.eventNum] = event
            self.eventNum += 1

    def _appendTmp(self, event):
        if self.eventNumTmp < 255:
            self.eventQueueTmp[self.eventNumTmp] = event
            self.eventNumTmp += 1

    def _appendMerge(self):
        for i in range(self.eventNumTmp):
            self._append( self.eventQueueTmp[i] )
            self.eventQueueTmp[i] = None
        self.eventNumTmp = 0

    def pump(self):
        """
        Process events to reduce queue overflow, unnecessary if processing with other methods.
        """
        if self.eventNum > 250:
            self._lock()
            self._pump()
            self._unlock()
        return None

    def _pump(self):
        queue = self.eventQueue[50:self.eventNum]
        self.eventNum -= 50
        for i in range(self.eventNum):
            self.eventQueue[i] = queue[i]

    def get(self, eventType=None):
        """
        Return list of events, and queue is reset.
        Optional eventType argument of single or list of event type(s) to return.
        """
        if not self.eventNum:
            return self.queueNil
        self._lock()
        if not eventType:
            self.queue = self.eventQueue[0:self.eventNum]
            self.eventNum = 0
        else:
            self.queue = []
            if isinstance(eventType, (tuple,list)):
                for i in range(self.eventNum):
                    if self.eventQueue[i].type not in eventType:
                        self.queueTmp.append(self.eventQueue[i])
                    else:
                        self.queue.append(self.eventQueue[i])
            else:
                for i in range(self.eventNum):
                    if self.eventQueue[i].type != eventType:
                        self.queueTmp.append(self.eventQueue[i])
                    else:
                        self.queue.append(self.eventQueue[i])
            if len(self.queueTmp) == 0:
                self.eventNum = 0
            else:
                self.eventNum = len(self.queueTmp)
                for i in range(self.eventNum):
                    self.eventQueue[i] = self.queueTmp[i]
                self.queueTmp[:] = []
            if self.eventNum > 250:
                self._pump()
        self._unlock()
        return self.queue

    def poll(self):
        """
        Return an event from the queue, or event type NOEVENT if none present.
        """
        self._lock()
        if self.eventNum:
            evt = self.eventQueue.pop(0)
            self.eventNum -= 1
            self.eventQueue.append(None)
            if self.eventNum > 250:
                self._pump()
        else:
            evt = self.Event(Const.NOEVENT)
        self._unlock()
        return evt

    def wait(self):     #not implemented in js
        """
        Return an event from the queue.
        """
        while True:
            if self.eventNum:
                self._lock()
                evt = self.eventQueue.pop(0)
                self.eventNum -= 1
                self.eventQueue.append(None)
                if self.eventNum > 250:
                    self._pump()
                self._unlock()
                return evt
            else:
                self._unlock()
                return None

    def peek(self, eventType=None):
        """
        Check if an event of given type is present.
        Optional eventType argument specifies event type or list, which defaults to all.
        """
        if not self.eventNum:
            return False
        elif eventType is None:
            return True
        self._lock()
        evt = [event.type for event in self.eventQueue[0:self.eventNum]]
        if self.eventNum > 250:
            self._pump()
        self._unlock()
        if isinstance(eventType, (tuple,list)):
            for evtType in eventType:
                if evtType in evt:
                    return True
        else:
            if eventType in evt:
                return True
        return False

    def clear(self, eventType=None):
        """
        Remove events of a given type from queue.
        Optional eventType argument specifies event type or list, which defaults to all.
        """
        if not self.eventNum:
            return None
        self._lock()
        if eventType is None:
            self.eventNum = 0
        else:
            if isinstance(eventType, (tuple,list)):
                for i in range(self.eventNum):
                    if self.eventQueue[i].type not in eventType:
                        self.queueTmp.append(self.eventQueue[i])
            else:
                for i in range(self.eventNum):
                    if self.eventQueue[i].type != eventType:
                        self.queueTmp.append(self.eventQueue[i])
            if len(self.queueTmp) == 0:
                self.eventNum = 0
            else:
                self.eventNum = len(self.queueTmp)
                for i in range(self.eventNum):
                    self.eventQueue[i] = self.queueTmp[i]
                self.queueTmp[:] = []
            if self.eventNum > 250:
                self._pump()
        self._unlock()
        return None

    def event_name(self, eventType):
        """
        Return event name of a event type.
        """
        if str(eventType) in self.eventName.keys():
            return self.eventName[eventType]
        else:
            return None

    def set_blocked(self, eventType):
        """
        Block specified event type(s) from queue.
        """
        if eventType is not None:
            if isinstance(eventType, (tuple,list)):
                for evtType in eventType:
                    self.events = self.events.difference(self.eventTypes[evtType])
            else:
                self.events = self.events.difference(self.eventTypes[eventType])
        else:
            self.events = set(self.eventType)
        return None

    def set_allowed(self, eventType):
        """
        Set allowed event type(s) on queue.
        """
        if eventType is not None:
            if isinstance(eventType, (tuple,list)):
                for evtType in eventType:
                    self.events = self.events.union(self.eventTypes[evtType])
            else:
                self.events = self.events.union(self.eventTypes[eventType])
        else:
            self.events.clear()
        return None

    def get_blocked(self, eventType):
        """
        Check if specified event type is blocked from queue.
        """
        if eventType not in self.events:
            return True
        else:
            return False

    def post(self, event):
        """
        Post event to queue.
        """
        self._lock()
        if event.type in self.events:
            self._append(event)
        self._unlock()
        return None

    def _initiate_touch_listener(self, canvas):
        self.touchlistener = TouchListener(canvas)
        return None

    def _register_event(self, eventType):
        if str(eventType) not in self.eventTypes.keys():
            self.eventTypes[eventType] = eventType
            self.eventName[eventType] = 'UserEvent'
            self.eventType.append(eventType)
            self.events = self.events.union(set([eventType]))

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.set_grab = lambda *arg: None
        self.get_grab = lambda *arg: False


class UserEvent(object):

    __slots__ = ['type', 'attr']

    # __pragma__ ('kwargs')

    def __init__(self, eventType, *args, **kwargs):
        """
        Return user event.
        Argument includes eventType (USEREVENT+num).
        Optional attribute argument as dictionary ({str:val}) or keyword arg(s).
        """
        if len(args) > 0:
            attr = args[0]
        else:
            attr = kwargs
        self.type = eventType
        self.attr = attr
        env.event._register_event(eventType)

    # __pragma__ ('nokwargs')

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

    def __getattr__(self, attr):
        if attr in self.attr.keys():
            return self.attr[attr]
        else:
            raise AttributeError("'Event' object has no attribute '{}'".format(attr))

    def __setattr__(self, attr, value):
        self.attr[attr] = value

    def toString(self):
        event_name = env.event.event_name(self.type)
        return '<Event({}-{} {})>'.format(self.type, event_name, repr(self.attr))


class JEvent(object):

    _types = {'mousemove':Const.MOUSEMOTION, 'mousedown':Const.MOUSEBUTTONDOWN, 'mouseup':Const.MOUSEBUTTONUP, 'wheel':Const.MOUSEBUTTONDOWN, 'mousewheel':Const.MOUSEBUTTONDOWN, 'DOMMouseScroll':Const.MOUSEBUTTONDOWN, 'keydown':Const.KEYDOWN, 'keypress':Const.KEYDOWN, 'keyup':Const.KEYUP}
    _charCode = {33:Const.K_EXCLAIM, 34:Const.K_QUOTEDBL, 35:Const.K_HASH, 36:Const.K_DOLLAR, 38:Const.K_AMPERSAND, 39:Const.K_QUOTE, 40:Const.K_LEFTPAREN, 41:Const.K_RIGHTPAREN, 42:Const.K_ASTERISK, 43:Const.K_PLUS, 44:Const.K_COMMA, 45:Const.K_MINUS, 46:Const.K_PERIOD, 97:Const.K_a, 98:Const.K_b, 99:Const.K_c, 100:Const.K_d, 101:Const.K_e, 102:Const.K_f, 103:Const.K_g, 104:Const.K_h, 105:Const.K_i, 106:Const.K_j, 107:Const.K_k, 108:Const.K_l, 109:Const.K_m, 110:Const.K_n, 111:Const.K_o, 112:Const.K_p, 113:Const.K_q, 114:Const.K_r, 115:Const.K_s, 116:Const.K_t, 117:Const.K_u, 118:Const.K_v, 119:Const.K_w, 120:Const.K_x, 121:Const.K_y, 122:Const.K_z}

    __slots__ = ['type', 'attr']

    def __init__(self, event):
        """
        Event object wraps browser event.
        
        Event object attributes:
        
        * type: MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, KEYDOWN, KEYUP
        * button: mouse button pressed (1-3, 4-5 V-scroll, and 6-7 H-scroll)
        * buttons: mouse buttons pressed (1,2,3)
        * pos: mouse position (x,y)
        * rel: mouse relative position change (x,y)
        * key: keycode of key pressed (K_a-K_z...)
        """
        event_type = event.js_type
        self.type = self.__class__._types[event_type]
        self.attr = {}
        if event_type in ('mousedown', 'mouseup'):
            self.attr['button'] = event.button + 1
            self.attr['pos'] = (event._x, event._y)
        elif event_type == 'mousemove':
            self.attr['buttons'] = (bool(event.buttons & 1),
                                    bool(event.buttons & 4),
                                    bool(event.buttons & 2))
            self.attr['pos'] = (event._x, event._y)
            self.attr['rel'] = (event._relx, event._rely)
        elif event_type in ('wheel', 'mousewheel', 'DOMMouseScroll'):
            if event.deltaY < 0:
                self.attr['button'] = 4
            else:
                self.attr['button'] = 5
            self.attr['pos'] = (event._x, event._y)
        elif event_type in ('keydown', 'keyup'):
            self.attr['key'] = event.keyCode
        elif event_type == 'keypress':
            if event.keyCode:
                code = event.keyCode
            else:
                code = event.which
            if code in self.__class__._charCode:
                self.attr['key'] = self.__class__._charCode[code]
            else:
                self.attr['key'] = code
        self.attr['event'] = event

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

    def __getattr__(self, attr):
        if attr in self.attr.keys():
            return self.attr[attr]
        else:
            raise AttributeError("'Event' object has no attribute '{}'".format(attr))

    def __setattr__(self, attr, value):
        self.attr[attr] = value

    def toString(self):
        event_name = env.event.event_name(self.type)
        return '<Event({}-{} {})>'.format(self.type, event_name, repr(self.attr))

    def getEvent(self):
        """
        Return browser event.
        """
        return self.attr['event']


class TouchListener:
    """
    **event.touchlistener**

    * event.touchlistener.add_callback
    * event.touchlistener.is_active
    """

    def __init__(self, canvas):
        """
        Touch event listener.

        Refer to touch event api documentation:
          https://developer.mozilla.org/en-US/docs/Web/API/TouchEvent.
        Notes:
          The event.touches attribute is a list of touch objects.
          Use len(touches) for touch count and touches.item(<index>) to retrieve touch object.
          The touch attribute touch.clientX/touch.clientY provides touch position.
          Position offset checked by display getAbsoluteLeft/getAbsoluteTop/getScrollLeft/getScrollTop.
          Browser triggers delayed mousedown/mouseup event after touchstart/touchend event.
        Module initialization creates pyjsdl.event.touchlistener instance.
        """
        global _canvas
        _canvas = canvas
        self.element = canvas.getElement()
        self.element.addEventListener('touchstart', _touch_detect)
        self.active = False
        self.callback = []

    def activate(self):
        self.element.removeEventListener('touchstart', _touch_detect)
        self.element.addEventListener('touchstart', _touch_start)
        self.element.addEventListener('touchend', _touch_end)
        self.element.addEventListener('touchmove', _touch_move)
        self.element.addEventListener('touchcancel', _touch_cancel)
        self.active = True

    def add_callback(self, callback):
        """
        Add callback object to receive touch events.
        The callback should have methods onTouchStart, onTouchEnd, onTouchMove, and onTouchCancel.
        Optional callback method onTouchInitiate used to report initial touch event detection.
        Callback methods will be called with an event argument.
        """
        self.callback.append(callback)
        return None

    def is_active(self):
        """
        Check if touch event is registered.
        """
        return self.active

_canvas = None

def _touch_detect(event):
    _canvas.onTouchInitiate(event)

def _touch_start(event):
    _canvas.onTouchStart(event)

def _touch_end(event):
    _canvas.onTouchEnd(event)

def _touch_move(event):
    _canvas.onTouchMove(event)

def _touch_cancel(event):
    _canvas.onTouchCancel(event)

