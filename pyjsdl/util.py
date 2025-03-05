#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Util module**

The module provides profiling functionality.
"""

from pyjsdl.time import Time
from pyjsdl.rect import Rect
from pyjsdl import env


class Timer:
    """
    Simple profiling timer.

    Output log can be directed to 'console' or to 'textarea'.
    If output is to textarea, may specify log length.
    """

    # __pragma__ ('kwargs')
    def __init__(self, log='console', log_length=5):
        """
        Initialize timer object.
        """
        self.time = Time()
        self.time_i = self.get_time()
        self.dtime = []
        self.number = 0
        self.log = None
        self.log_list = None
        self.log_num = 0
        self.log_scroll = True
        self.set_log(log, log_length)
    # __pragma__ ('nokwargs')

    def get_time(self):
        """
        Get current time.
        """
        return self.time.time()

    def set_time(self):
        """
        Set current time.
        """
        self.time_i = self.get_time()

    # __pragma__ ('kwargs')
    def lap_time(self, time_i=None, time_f=None, number=100, print_result=True):
        """
        Time lapsed since previous set_time.

        Optional arguments time_i and time_f, number of calls to average, and print_results to output result.
        Return lapsed time on completion.
        """
        if time_i is None:
            time_i = self.time_i
        if time_f is None:
            time_f = self.get_time()
        self.dtime.append(time_f-time_i)
        self.number += 1
        if self.number >= number:
            t_ave = ( sum(self.dtime)/number )
            self.dtime = []
            self.number = 0
            if print_result:
                if self.log_type == 'console':
                    self.log_num += 1
                    entry = 'Time {}: {}'.format(self.log_num, t_ave)
                    print(entry)
                else:
                    self.log_num += 1
                    entry = 'Time {}: {}'.format(self.log_num, t_ave)
                    self.print_log(entry)
            return t_ave
    # __pragma__ ('nokwargs')

    # __pragma__ ('kwargs')
    def set_log(self, log, log_length=5):
        """
        Set log output.

        Argument log can be 'console' or 'textarea'.
        """
        if log in ('console','textarea'):
            self.log_type = log
            if log == 'textarea':
                if not self.log:
                    size = env.canvas.surface.width-5, 102
                    self.log = env.canvas.surface._display.Textarea(size)
                    self.log.setReadonly(True)
                    self.log.addMouseListener(self)
                    self.onMouseUp = lambda sender,x,y: None
                    self.onMouseMove = lambda sender,x,y: None
                    self.onMouseEnter = lambda sender: None
                    self.log_list = ['' for i in range(log_length)]
                self.log.toggle(True)
            else:
                if self.log:
                    self.log.toggle(False)
                    self.log_list = []
    # __pragma__ ('nokwargs')

    def onMouseDown(self, sender, x, y):
        """
        Control log scroll.
        """
        self.log_scroll = False

    def onMouseLeave(self, sender):
        """
        Control log scroll.
        """
        self.log_scroll = True

    def print_log(self, text):
        """
        Print text to output.
        """
        if self.log_type == 'console':
            print(text)
        else:
            self.log_list.pop(0)
            self.log_list.append(text+'\n')
            text = ''.join(self.log_list)
            self.log.setText(text)
            if self.log_scroll:
                self.log.setCursorPos(len(text))


def call(obj, func, args=()):
    """
    Call unbound method.

    Argument obj is the object, func is the unbound method, and optional args is a tuple of arguments for the method.
    Returns the method's return value.
    """
    __pragma__('js', {},
        "return func.apply(obj, args);")


def createEvent(eventObject, eventType, eventOptions=None):
    """
    Create JavaScript event.

    For instance:
        MouseEvent type 'mousedown', handled as a MouseButtonDown event.
        PageTransitionEvent type 'pagehide', handled as a Quit event.
    Default options are {'bubbles':True, 'cancelable':True}.
    """
    options = {'bubbles':True, 'cancelable':True}
    if eventOptions is not None:
        for key in eventOptions:
            options[key] = eventOptions[key]
    event = __new__(eventObject(eventType, options))
    return event


def dispatchEvent(event, element=None):
    """
    Dispatch JavaScript event.

    The event is dispatched from the element.
    Default element is the canvas.
    """
    if element is None:
        element = document.getElementsByTagName('canvas').item(0)
        if element is None:
            return False
    element.dispatchEvent(event)
    return True


def id(obj):
    return obj._identity


class Dict:
    """
    Dictionary object.

    Dict can use an object key as Transcrypt is restricted to str keys.
    Object requires an unique identifier _identity attribute (int/str).
    """

    def __init__(self):
        self._dk = {}
        self._dv = {}

    def __str__(self):
        s = ['{}: {}'.format(k,v) for k,v in self.items()]
        return '{{}}'.format(', '.join(s))

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for k in self._dk.keys():
            yield self._dk[k]

    def __getitem__(self, key):
        return self._dv[id(key)]

    def __setitem__(self, key, val):
        self._dk[id(key)] = key
        self._dv[id(key)] = val

    def get(self, key):
        """
        Get value by object key.
        """
        return self.__getitem__(key)

    def setdefault(self, key, val=None):
        """
        Set value of object key.
        """
        self.__setitem__(key, val)

    def keys(self):
        """
        Retrieve object keys.
        """
        return self._dk.values()

    def values(self):
        """
        Retrieve values.
        """
        return self._dv.values()

    def items(self):
        """
        Retrieve object key, value items.
        """
        for k in self._dk.keys():
            yield (self._dk[k], self._dv[k])

    def toString(self):
        return self.__str__()

