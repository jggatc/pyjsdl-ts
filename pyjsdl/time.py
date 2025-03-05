#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Time module**

The module provides time monitoring functionality.
"""

from pyjsdl import env
from pyjsdl.pyjsobj import performanceNowInit


class Clock:
    """
    Clock object.
    """

    _wnd = None

    def __init__(self):
        """
        Initialize clock object.
        """
        self._time = self.time()
        self._time_init = self._time
        self._time_diff = 0
        self._framerate = 0

    def get_time(self):
        """
        Return time (in ms) between last two calls to tick().
        """
        return self._time_diff

    def tick(self, framerate=0):
        """
        Call once per program cycle.

        An optional framerate will add pause to limit rate.
        Returns ms since last call.
        """
        if self._framerate != framerate and not env.canvas._pause:
            self._framerate = framerate
            if framerate:
                env.canvas._framerate = 1000.0 / framerate
            else:
                env.canvas._framerate = 0.0
        self._time = self._wnd.performance.now()
        self._time_diff = self._time - self._time_init
        self._time_init = self._time
        return self._time_diff

    def tick_busy_loop(self, framerate=0):
        """
        Call once per program cycle.

        An optional framerate will add pause to limit rate.
        Returns ms since last call.
        """
        return self.tick(framerate)

    def get_fps(self):
        """
        Return fps.
        """
        if not env.canvas._pause:
            return 1000.0 / env.canvas._frametime
        else:
            return 0.0

    def time(self):
        """
        Return system time (in ms).
        """
        return self._wnd.performance.now()


class Time:
    """
    Time object.
    """

    _wnd = None

    def __init__(self):
        """
        Initialize time object.
        """
        self.Clock = Clock
        Time._wnd = performanceNowInit()
        Clock._wnd = Time._wnd
        self._time_init = self.time()
        self._framerate = 0
        self._timers = {}
        self.run = lambda: self.wait()

    def get_ticks(self):
        """
        Get time ticks.

        Return ms since program start.
        """
        return self._wnd.performance.now() - self._time_init

    def delay(self, time):
        """
        Time delay.

        Pause for given time (in ms). Return ms paused.
        Suspends the program, preferably use time.wait.
        """
        start = self._wnd.performance.now()
        while True:
            if self._wnd.performance.now() - start > time:
                return self._wnd.performance.now() - start

    def wait(self, time=0):
        """
        Wait function.

        Timeout program callback for given time (in ms).
        """
        if time:
            if not env.canvas._pause:
                self._framerate = env.canvas._framerate
                env.canvas._framerate = time * 10
                env.canvas._pause = True
                self.set_timeout(self, time)
        else:
            if env.canvas._pause:
                env.canvas._framerate = self._framerate
                env.canvas._rendertime = self._wnd.performance.now()
                env.canvas._pause = False
        return time

    def set_timer(self, event, time, once=False):
        """
        Set timer.

        Post event on queue at time (ms) intervals.
        Optional argument once set no timer repeat, defaults to False.
        Disable timer with time of 0.
        """
        if event.type:
            eventType = event.type
            if str(eventType) not in self._timers.keys():
                self._timers[eventType] = _EventTimer(event)
        else:
            eventType = event
            if str(eventType) not in self._timers.keys():
                evt = env.event.Event(eventType)
                self._timers[eventType] = _EventTimer(evt)
        repeat = not once
        self._timers[eventType].set_timer(time, repeat)

    def _stop_timers(self):
        for eventType in self._timers.keys():
            self._timers[eventType].set_timer(0, False)

    def time(self):
        """
        Return system time (in ms).
        """
        return self._wnd.performance.now()

    def set_timeout(self, obj, time):
        """
        Set timeout.

        Timeout time (in ms) before triggering obj.run method.
        Return timer id.
        """
        run = lambda: obj.run()
        id = window.setTimeout(run, time)
        return id

    def clear_timeout(self, id):
        """
        Clear timeout.

        Argument timer id of set_timeout.
        """
        window.clearTimeout(id)
        return None

    def set_interval(self, obj, time):
        """
        Set interval timeout.

        Recurring timeout time (in ms) before triggering obj.run method.
        Return timer id.
        """
        run = lambda: obj.run()
        id = window.setInterval(run, time)
        return id

    def clear_interval(self, id):
        """
        Clear interval timeout.

        Argument timer id of set_interval.
        """
        window.clearInterval(id)
        return None


class _EventTimer:

    def __init__(self, event):
        self.event = event
        self.timer = None
        self.time = 0
        self.repeat = True

    def set_timer(self, time, repeat):
        if self.timer:
            self.repeat = False
            self.clear_timeout()
        if time:
            self.time = time
            self.repeat = repeat
            self.set_timeout()

    def set_timeout(self):
        run = lambda: self.run()
        timer = window.setTimeout(run, self.time)
        self.timer = timer

    def clear_timeout(self):
        window.clearTimeout(self.timer)
        self.timer = None

    def run(self):
        env.event.post(self.event)
        if self.repeat:
            self.set_timeout()

