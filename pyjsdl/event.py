#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Event module**

The module manages events.
"""

from pyjsdl import env
from pyjsdl import key
from pyjsdl import constants as Const


class Event:
    """
    Event processing construct.
    """

    def __init__(self):
        """
        Initialize Event object.

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
        self.mouseEvt = {'pos':None, 'pre':None, 'rel':None, 'focus':False}
        self.mousePress = {0:False, 1:False, 2:False}
        self.keyPress = {Const.K_ALT: False,
                         Const.K_CTRL: False,
                         Const.K_SHIFT: False}
        self.keyMod = {Const.K_ALT: {True:Const.KMOD_ALT, False:0},
                       Const.K_CTRL: {True:Const.KMOD_CTRL, False:0},
                       Const.K_SHIFT: {True:Const.KMOD_SHIFT, False:0}}
        self.eventName = {Const.MOUSEMOTION: 'MouseMotion',
                          Const.MOUSEBUTTONDOWN: 'MouseButtonDown',
                          Const.MOUSEBUTTONUP: 'MouseButtonUp',
                          Const.MOUSEWHEEL: 'MouseWheel',
                          Const.KEYDOWN: 'KeyDown',
                          Const.KEYUP: 'KeyUp',
                          Const.ACTIVEEVENT: 'ActiveEvent',
                          Const.WINDOWENTER: 'WindowEnter',
                          Const.WINDOWLEAVE: 'WindowLeave',
                          Const.QUIT: 'Quit',
                          'mousemove': 'MouseMotion',
                          'mousedown': 'MouseButtonDown',
                          'mouseup': 'MouseButtonUp',
                          'mousewheel': 'MouseWheel',
                          'keydown': 'KeyDown',
                          'keyup': 'KeyUp',
                          'mousefocus': 'ActiveEvent',
                          'focus': 'ActiveEvent',
                          'blur': 'ActiveEvent',
                          'visibilitychange': 'ActiveEvent',
                          'mouseenter': 'WindowEnter',
                          'mouseleave': 'WindowLeave',
                          'pagehide': 'Quit'}
        self.eventType = [Const.MOUSEMOTION,
                          Const.MOUSEBUTTONDOWN,
                          Const.MOUSEBUTTONUP,
                          Const.MOUSEWHEEL,
                          Const.KEYDOWN,
                          Const.KEYUP,
                          Const.ACTIVEEVENT,
                          Const.WINDOWENTER,
                          Const.WINDOWLEAVE,
                          Const.QUIT,
                          'mousemove', 'mousedown', 'mouseup', 'mousewheel',
                          'keydown', 'keypress', 'keyup',
                          'mousefocus', 'focus', 'blur', 'visibilitychange',
                          'mouseenter', 'mouseleave', 'pagehide']
        self.events = set(self.eventType)
        self.eventTypes = {Const.MOUSEMOTION:
                               set([Const.MOUSEMOTION, 'mousemove']),
                           Const.MOUSEBUTTONDOWN:
                               set([Const.MOUSEBUTTONDOWN, 'mousedown',
                                   'mousewheeldown']),
                           Const.MOUSEBUTTONUP:
                               set([Const.MOUSEBUTTONUP, 'mouseup',
                                   'mousewheelup']),
                           Const.MOUSEWHEEL:
                               set([Const.MOUSEWHEEL, 'mousewheel']),
                           Const.KEYDOWN:
                               set([Const.KEYDOWN, 'keydown', 'keypress']),
                           Const.KEYUP:
                               set([Const.KEYUP, 'keyup']),
                           Const.ACTIVEEVENT:
                               set([Const.ACTIVEEVENT,
                                   'mousefocus', 'focus', 'blur', 'visibilitychange']),
                           Const.WINDOWENTER:
                               set([Const.WINDOWENTER, 'mouseenter']),
                           Const.WINDOWLEAVE:
                               set([Const.WINDOWLEAVE, 'mouseleave']),
                           Const.QUIT:
                               set([Const.QUIT, 'pagehide'])}
        self.eventObj = {'mousedown': MouseDownEvent,
                         'mouseup': MouseUpEvent,
                         'mousemove': MouseMoveEvent,
                         'mousewheel': MouseWheelEvent,
                         'mousewheeldown': MouseWheelDownEvent,
                         'mousewheelup': MouseWheelUpEvent,
                         'keydown': KeyDownEvent,
                         'keyup': KeyUpEvent,
                         'mousefocus': MouseFocusEvent,
                         'focus': InputFocusEvent,
                         'blur': InputFocusEvent,
                         'visibilitychange': VisibilityEvent,
                         'mouseenter': MouseEnterEvent,
                         'mouseleave': MouseLeaveEvent,
                         'pagehide': PageHide}
        self.modKey = key._modKey
        self.specialKey = key._specialKey
        self.modKeyCode = key._modKeyCode
        self.specialKeyCode = key._specialKeyCode
        self.touchlistener = None
        self.keyRepeat = [0, 0]
        self.keyHeld = {}
        self.keyCode = 0
        self.keyPressCode = {}
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
            self._append(event)
        else:
            self._appendTmp(event)
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
        Process event queue.

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
        Return an event from the queue.

        Return event type NOEVENT if none present.
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

        Return None if queue is empty.
        Waiting not implemented.
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

        If None is argument, all event types are blocked.
        """
        if eventType is not None:
            if isinstance(eventType, (tuple,list)):
                for evtType in eventType:
                    self.events = self.events.difference(
                                      self.eventTypes[evtType])
            else:
                self.events = self.events.difference(
                                  self.eventTypes[eventType])
        else:
            self.events.clear()
        return None

    def set_allowed(self, eventType):
        """
        Set allowed event type(s) on queue.

        If None is argument, all event types are allowed.
        """
        if eventType is not None:
            if isinstance(eventType, (tuple,list)):
                for evtType in eventType:
                    self.events = self.events.union(
                                      self.eventTypes[evtType])
            else:
                self.events = self.events.union(
                                  self.eventTypes[eventType])
        else:
            self.events = set(self.eventType)
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

    def _set_mouse_event(self, canvas):
        event = _Evt(canvas)
        self.mouseEvt['pos'] = event
        self.mouseEvt['pre'] = event
        self.mouseEvt['rel'] = event

    def _set_key_event(self):
        self.eventObj['keydown'] = _KeyDownEvent
        self.eventObj['keyup'] = _KeyUpEvent
        self.eventObj['keypress'] = _KeyPressEvent

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
        self.set_grab = lambda *arg: None
        self.get_grab = lambda *arg: False


class UserEvent:
    """
    UserEvent object.
    """

    __slots__ = ['type', 'attr']

    # __pragma__ ('kwargs')

    def __init__(self, eventType, *args, **kwargs):
        """
        UserEvent event object.

        Argument includes eventType (USEREVENT+num).
        Optional attribute argument as dictionary ({str:val}) or keyword arg(s).
        Return user event.
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
            raise AttributeError(
                "'Event' object has no attribute '{}'".format(attr))

    def __setattr__(self, attr, value):
        self.attr[attr] = value

    def toString(self):
        event_name = env.event.event_name(self.type)
        return '<Event({}-{} {})>'.format(self.type, event_name, repr(self.attr))


class JEvent:
    """
    JEvent object.

    Wrapper for:
        * MouseEvent
        * KeyEvent
        * MouseFocusEvent
        * InputFocusEvent
        * VisibilityEvent
        * WindowEnter
        * WindowLeave
        * PageHide
    """

    __slots__ = []

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return self.toString()

    def toString(self):
        event_name = self._eventName[self.type]
        attr = {}
        for name in self.__slots__[1:len(self.__slots__)]:
            attr[name] = getattr(self, name)
        return '<Event({}-{} {})>'.format(self.type, event_name, repr(attr))

    def getEvent(self):
        """
        Return browser event.
        """
        return self.event


class MouseEvent(JEvent):
    """
    MouseEvent object.

    JEvent wrapper for:
        * MouseDownEvent
        * MouseUpEvent
        * MouseMoveEvent
    """

    _types = {'mousemove': Const.MOUSEMOTION,
              'mousedown': Const.MOUSEBUTTONDOWN,
              'mouseup': Const.MOUSEBUTTONUP}
    _eventName = {Const.MOUSEMOTION: 'MouseMotion',
                  Const.MOUSEBUTTONDOWN: 'MouseButtonDown',
                  Const.MOUSEBUTTONUP: 'MouseButtonUp'}

    __slots__ = []


class MouseDownEvent(MouseEvent):
    """
    MouseDownEvent object.

    JEvent wrapper with MOUSEBUTTONDOWN event interface.
    """

    __slots__ = ['type', 'button', 'pos', 'event']

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: MOUSEBUTTONDOWN
            * button: mouse button pressed (1-3)
            * pos: mouse position (x,y)
            * event: JavaScript event
        """
        self.event = event
        self.type = self._types[event.js_type]
        self.button = event.button + 1
        r = env.canvas.getBoundingClientRect()
        self.pos = (event.clientX - round(r.left),
                    event.clientY - round(r.top))


class MouseUpEvent(MouseEvent):
    """
    MouseUpEvent object.

    JEvent wrapper with MOUSEBUTTONUP event interface.
    """

    __slots__ = ['type', 'button', 'pos', 'event']

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: MOUSEBUTTONUP
            * button: mouse button pressed (1-3)
            * pos: mouse position (x,y)
            * event: JavaScript event
        """
        self.event = event
        self.type = self._types[event.js_type]
        self.button = event.button + 1
        r = env.canvas.getBoundingClientRect()
        self.pos = (event.clientX - round(r.left),
                    event.clientY - round(r.top))


class MouseMoveEvent(MouseEvent):
    """
    MouseMoveEvent object.

    JEvent wrapper with MOUSEMOTION event interface.
    """

    __slots__ = ['type', 'buttons', 'pos', 'rel', 'event']

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: MOUSEMOTION
            * buttons: mouse buttons pressed (1-3)
            * pos: mouse position (x,y)
            * rel: mouse relative position change (x,y)
            * event: JavaScript event
        """
        self.event = event
        self.type = self._types[event.js_type]
        self.buttons = (bool(event.buttons & 1),
                        bool(event.buttons & 4),
                        bool(event.buttons & 2))
        r = env.canvas.getBoundingClientRect()
        self.pos = (event.clientX - round(r.left),
                    event.clientY - round(r.top))
        self.rel = (event.clientX - env.event.mouseEvt['pre'].clientX,
                    event.clientY - env.event.mouseEvt['pre'].clientY)


class MouseWheelDownEvent(JEvent):
    """
    MouseWheelEvent object.

    JEvent wrapper with MOUSEBUTTONDOWN event interface.
    """

    __slots__ = ['type', 'button', 'pos', 'event']

    _eventName = {Const.MOUSEBUTTONDOWN: 'MouseButtonDown'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: MOUSEBUTTONDOWN
            * button: mouse button pressed (4-5)
            * pos: mouse position (x,y)
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.MOUSEBUTTONDOWN
        if event.deltaY < 0:
            self.button = 4
        else:
            self.button = 5
        r = env.canvas.getBoundingClientRect()
        self.pos = (event.clientX - round(r.left),
                    event.clientY - round(r.top))


class MouseWheelUpEvent(JEvent):
    """
    MouseWheelEvent object.

    JEvent wrapper with MOUSEBUTTONUP event interface.
    """

    __slots__ = ['type', 'button', 'pos', 'event']

    _eventName = {Const.MOUSEBUTTONUP: 'MouseButtonUp'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: MOUSEBUTTONUP
            * button: mouse button pressed (4-5)
            * pos: mouse position (x,y)
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.MOUSEBUTTONUP
        if event.deltaY < 0:
            self.button = 4
        else:
            self.button = 5
        r = env.canvas.getBoundingClientRect()
        self.pos = (event.clientX - round(r.left),
                    event.clientY - round(r.top))


class MouseWheelEvent(JEvent):
    """
    MouseWheelEvent object.

    JEvent wrapper with MOUSEWHEEL event interface.
    """

    __slots__ = ['type', 'x', 'y', 'precise_x', 'precise_y', 'event']

    _eventName = {Const.MOUSEWHEEL: 'MouseWheel'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: MOUSEWHEEL
            * x: mouse wheel rotation (-1,0,1)
            * y: mouse wheel rotation (-1,0,1)
            * precise_x: mouse precise wheel rotation (-1,0,1)
            * precise_y: mouse precise wheel rotation (-1,0,1)
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.MOUSEWHEEL
        if event.deltaY != 0:
            self.x = 0
            self.precise_x = 0.0
            if event.deltaY < 0:
                self.y = 1
                self.precise_y = 1.0
            else:
                self.y = -1
                self.precise_y = -1.0
        else:
            self.y = 0
            self.precise_y = 0.0
            if event.deltaX < 0:
                self.x = -1
                self.precise_x = -1.0
            else:
                self.x = 1
                self.precise_x = 1.0


class KeyEvent(JEvent):
    """
    KeyEvent object.

    JEvent wrapper for:
        * KeyDownEvent
        * KeyUpEvent
    """

    _types = {'keydown': Const.KEYDOWN,
              'keyup': Const.KEYUP,
              'keypress': Const.KEYDOWN}
    _eventName = {Const.KEYDOWN: 'KeyDown',
                  Const.KEYUP: 'KeyUp'}
    _code = key._code
    _specialKey = key._specialKey
    _specialKeyCode = key._specialKeyCode

    __slots__ = []


class KeyDownEvent(KeyEvent):
    """
    KeyDownEvent object.

    JEvent wrapper with KEYDOWN event interface.
    """

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: KEYDOWN
            * key: keycode of key pressed (K_a-K_z...)
            * mod: modifier pressed (KMOD_ALT | KMOD_CTRL | KMOD_SHIFT)
            * unicode: keycode of key pressed
            * event: JavaScript event
        """
        self.event = event
        self.type = self._types[event.js_type]
        if event.key in self._specialKey:
            self.key = self._specialKey[event.key]
            if self.key in (9, 13):
                self.unicode = chr(self.key)
            else:
                self.unicode = ''
        else:
            if event.code in self._code:
                self.key = self._code[event.code]
            else:
                self.key = event.code
            self.unicode = event.key
        self.mod = ( (event.altKey * Const.KMOD_ALT) |
                     (event.ctrlKey * Const.KMOD_CTRL) |
                     (event.shiftKey * Const.KMOD_SHIFT) )


class KeyUpEvent(KeyEvent):
    """
    KeyUpEvent object.

    JEvent wrapper with KEYUP event interface.
    """

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: KEYUP
            * key: keycode of key pressed (K_a-K_z...)
            * mod: modifier pressed (KMOD_ALT | KMOD_CTRL | KMOD_SHIFT)
            * unicode: keycode of key pressed
            * event: JavaScript event
        """
        self.event = event
        self.type = self._types[event.js_type]
        if event.key in self._specialKey:
            self.key = self._specialKey[event.key]
            if self.key in (9, 13):
                self.unicode = chr(self.key)
            else:
                self.unicode = ''
        else:
            if event.code in self._code:
                self.key = self._code[event.code]
            else:
                self.key = event.code
            self.unicode = event.key
        self.mod = ( (event.altKey * Const.KMOD_ALT) |
                     (event.ctrlKey * Const.KMOD_CTRL) |
                     (event.shiftKey * Const.KMOD_SHIFT) )


class _KeyDownEvent(KeyEvent):

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event):
        self.event = event
        self.type = self._types[event.js_type]
        keycode = event.which or event.keyCode or 0
        self.key = self._specialKeyCode[keycode]
        if self.key in (9, 13):
            self.unicode = chr(self.key)
        else:
            self.unicode = ''
        self.mod = ( (event.altKey * Const.KMOD_ALT) |
                     (event.ctrlKey * Const.KMOD_CTRL) |
                     (event.shiftKey * Const.KMOD_SHIFT) )


class _KeyUpEvent(KeyEvent):

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event):
        self.event = event
        keycode = event.which or event.keyCode or 0
        self.type = self._types[event.js_type]
        if keycode in self._specialKeyCode:
            self.key = self._specialKeyCode[keycode]
            if keycode in (9, 13):
                self.unicode = chr(keycode)
            else:
                self.unicode = ''
        else:
            if keycode in env.event.keyPressCode:
                _keycode = env.event.keyPressCode[keycode]
                self.key = _keycode
                if 65 <= _keycode <= 90:
                    self.unicode = chr(_keycode+32)
                else:
                    self.unicode = chr(_keycode)
            else:
                if 65 <= keycode <= 90:
                    self.key = keycode + 32
                    self.unicode = chr(keycode+32)
                else:
                    self.key = keycode
                    self.unicode = chr(keycode)
        self.mod = ( (event.altKey * Const.KMOD_ALT) |
                     (event.ctrlKey * Const.KMOD_CTRL) |
                     (event.shiftKey * Const.KMOD_SHIFT) )


class _KeyPressEvent(KeyEvent):

    __slots__ = ['type', 'key', 'mod', 'unicode', 'event']

    def __init__(self, event):
        self.event = event
        self.type = self._types[event.js_type]
        keycode = event.which or event.keyCode or 0
        self.key = keycode
        if 65 <= keycode <= 90:
            self.unicode = chr(keycode+32)
        else:
            self.unicode = chr(keycode)
        self.mod = ( (event.altKey * Const.KMOD_ALT) |
                     (event.ctrlKey * Const.KMOD_CTRL) |
                     (event.shiftKey * Const.KMOD_SHIFT) )


class MouseFocusEvent(JEvent):
    """
    MouseFocusEvent object.

    JEvent wrapper with ACTIVEEVENT event interface.
    """

    __slots__ = ['type', 'state', 'gain', 'event']
    _gain = {'mouseenter': 1, 'mouseleave': 0}
    _eventName = {Const.ACTIVEEVENT: 'ActiveEvent'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: ACTIVEEVENT
            * state: focus state (APPFOCUSMOUSE)
            * gain: focus gain (0,1)
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.ACTIVEEVENT
        self.state = Const.APPFOCUSMOUSE
        self.gain = self._gain[event.js_type]


class InputFocusEvent(JEvent):
    """
    InputFocusEvent object.

    JEvent wrapper with ACTIVEEVENT event interface.
    """

    __slots__ = ['type', 'state', 'gain', 'event']
    _gain = {'focus': 1, 'blur': 0}
    _eventName = {Const.ACTIVEEVENT: 'ActiveEvent'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: ACTIVEEVENT
            * state: focus state (APPINPUTFOCUS)
            * gain: focus gain (0,1)
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.ACTIVEEVENT
        self.state = Const.APPINPUTFOCUS
        self.gain = self._gain[event.js_type]


class VisibilityEvent(JEvent):
    """
    VisibilityEvent object.

    JEvent wrapper with ACTIVEEVENT event interface.
    """

    __slots__ = ['type', 'state', 'gain', 'event']
    _gain = {True: 1, False: 0}
    _eventName = {Const.ACTIVEEVENT: 'ActiveEvent'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: ACTIVEEVENT
            * state: focus state (APPACTIVE)
            * gain: focus gain (0,1)
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.ACTIVEEVENT
        self.state = Const.APPACTIVE
        self.gain = self._gain[not document.hidden]


class MouseEnterEvent(JEvent):
    """
    MouseEnterEvent object.

    JEvent wrapper with WINDOWENTER event interface.
    """

    __slots__ = ['type', 'event']
    _eventName = {Const.WINDOWENTER: 'WindowEnter'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: WINDOWENTER
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.WINDOWENTER


class MouseLeaveEvent(JEvent):
    """
    MouseLeaveEvent object.

    JEvent wrapper with WINDOWLEAVE event interface.
    """

    __slots__ = ['type', 'event']
    _eventName = {Const.WINDOWLEAVE: 'WindowLeave'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: MWINDOWLEAVE
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.WINDOWLEAVE


class PageHide(JEvent):
    """
    PageHide object.

    JEvent wrapper with QUIT event interface.
    """

    __slots__ = ['type', 'event']
    _eventName = {Const.QUIT: 'Quit'}

    def __init__(self, event):
        """
        Initialize event.

        Attributes:
            * type: QUIT
            * event: JavaScript event
        """
        self.event = event
        self.type = Const.QUIT


class _Evt:

    def __init__(self, canvas):
        clientRect = canvas.getBoundingClientRect()
        self.clientX = round(clientRect.left) - 1
        self.clientY = round(clientRect.top) - 1


class TouchListener:
    """
    TouchListener object.

        * The event.touches attribute is a list of touch objects.
        * Use len(touches) for touch count and touches.item(<index>) to retrieve touch object.
        * The touch attribute touch.clientX/touch.clientY provides touch position.
        * Position offset checked by display getAbsoluteLeft/getAbsoluteTop/getScrollLeft/getScrollTop.
        * Browser triggers delayed mousedown/mouseup event after touchstart/touchend event.

    Refer to touch event api documentation:
        * https://developer.mozilla.org/en-US/docs/Web/API/TouchEvent.

    Module initialization creates event.touchlistener instance.
    """

    def __init__(self, canvas):
        """
        Initialize touch event listener.

        Add touchstart listener to detect initial touch.
        The event.touchlistener has been instantiated on Canvas.
        """
        global _canvas
        _canvas = canvas
        self.element = canvas.getElement()
        self.element.addEventListener('touchstart', _touch_detect)
        self.active = False
        self.callback = []

    def activate(self):
        """
        Touch event listeners activated.

        Activation of touch events touchstart, touchend, touchmove and touchcancel.
        The event.touchlistener activated on Canvas when initial touch detected.
        """
        self.element.removeEventListener('touchstart', _touch_detect)
        self.element.addEventListener('touchstart', _touch_start)
        self.element.addEventListener('touchend', _touch_end)
        self.element.addEventListener('touchmove', _touch_move)
        self.element.addEventListener('touchcancel', _touch_cancel)
        self.active = True

    def add_callback(self, callback):
        """
        Add callback object to receive touch events.

        Callback requires methods onTouchStart, onTouchEnd, onTouchMove, and onTouchCancel.
        Optional callback method onTouchInitiate to report initial touch event detection.
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

