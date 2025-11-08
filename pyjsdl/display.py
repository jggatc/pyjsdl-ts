#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Display module**

The module controls display surface updates and registers interaction events.
"""

from pyjsdl.surface import Surface
from pyjsdl.rect import Rect
from pyjsdl.time import Time
from pyjsdl import env
from pyjsdl import constants as Const
from pyjsdl.pyjsobj import RootPanel, VerticalPanel, TextBox, TextArea
from pyjsdl.pyjsobj import requestAnimationFrameInit, Event
from pyjsdl import pyjsobj
import pyjsdl


_canvas = None
_ctx = None
_img = None
_wnd = None


class Canvas(Surface):

    def __init__(self, size):
        Surface.__init__(self, size)
        self.setID('__canvas__')
        self.surface = Surface(size)
        self.callback = None
        self.time = Time()
        self.event = env.event
        self.addMouseListener(self)
        self.addKeyEventListener(self)
        self.addFocusListener(self)
        self.addVisibilityChangeListener()
        self.addPageHideListener()
        self.addResizeListener()
        self.addScrollListener()
        self.sinkEvents(Event.ONMOUSEDOWN |
                        Event.ONMOUSEUP |
                        Event.ONMOUSEMOVE |
                        Event.ONMOUSEOUT |
                        Event.ONMOUSEWHEEL |
                        Event.ONKEYDOWN |
                        Event.ONKEYPRESS |
                        Event.ONFOCUS |
                        Event.ONBLUR)
        self.onContextMenu = None
        self.preventContextMenu()
        self.evt = self.event.eventObj
        self.modKey = self.event.modKey
        self.specialKey = self.event.specialKey
        self.modKeyCode = self.event.modKeyCode
        self.specialKeyCode = self.event.specialKeyCode
        self.keyRepeat = self.event.keyRepeat
        self.keyHeld = self.event.keyHeld
        self.event._initiate_touch_listener(self)
        self._touch_callback = self.event.touchlistener.callback
        self._clientRect = None
        self._clientRect_update_timeout = False
        self._rect_list = []
        self._rect_len = 0
        self._rect_num = 0
        self._framerate = 0
        self._frametime = 0
        self._rendertime = self.time.time()
        self._pause = False
        self.run = None
        self.initialized = False

    def _initiate(self):
        global _canvas, _ctx, _img, _wnd
        panel = RootPanel()
        panel.add(self)
        _canvas = self
        _ctx = self._ctx
        _img = self.surface.canvas
        _wnd = requestAnimationFrameInit()
        self._clientRect_update()
        self.event._set_mouse_event(self)
        return panel

    def onMouseMove(self, event):
        self.event.mouseEvt['pre'] = self.event.mouseEvt['pos']
        self.event.mouseEvt['pos'] = event
        if event.js_type in self.event.events:
            self.event._updateQueue(self.evt[event.js_type](event))

    def onMouseDown(self, event):
        self.event.mousePress[event.button] = True
        if event.js_type in self.event.events:
            self.event._updateQueue(self.evt[event.js_type](event))

    def onMouseUp(self, event):
        self.event.mousePress[event.button] = False
        if event.js_type in self.event.events:
            self.event._updateQueue(self.evt[event.js_type](event))

    def onMouseEnter(self, event):
        self.event.mouseEvt['pos'] = event
        self.event.mouseEvt['pre'] = event
        self.event.mouseEvt['rel'] = event
        self.event._updateQueue(self.evt['mousefocus'](event))
        self.event._updateQueue(self.evt[event.js_type](event))

    def onMouseLeave(self, event):
        self.event.mousePress[0] = False
        self.event.mousePress[1] = False
        self.event.mousePress[2] = False
        for keycode in self.modKeyCode:
            if self.event.keyPress[keycode]:
                self.event.keyPress[keycode] = False
        self.event._updateQueue(self.evt['mousefocus'](event))
        self.event._updateQueue(self.evt[event.js_type](event))

    def onMouseWheel(self, event):
        if not hasattr(event, 'deltaY'):
            if hasattr(event, 'wheeleventY'):
                event.deltaX = -event.wheeleventX
                event.deltaY = -event.wheeleventY
            elif hasattr(event, 'detail'):
                event.deltaX = 0
                event.deltaY = event.detail
            else:
                return
        if event.deltaY:
            if 'mousedown' in self.event.events:
                self.event._updateQueue(self.evt['mousewheeldown'](event))
            if 'mouseup' in self.event.events:
                self.event._updateQueue(self.evt['mousewheelup'](event))
        if 'mousewheel' in self.event.events:
            self.event._updateQueue(self.evt['mousewheel'](event))
        event.preventDefault()

    def onKeyEvent(self, event):
        self.removeKeyEventListener(self)
        if event.key and event.code:
            self.addKeyboardListener(self)
            self.onKeyDown(event)
        else:
            self.event._set_key_event()
            self._addKeyboardListener(self)
            self._onKeyDown(event)

    def onKeyDown(self, event):
        if event.key in self.modKey:
            self.event.keyPress[self.modKey[event.key]] = True
        if event.js_type in self.event.events:
            if not self._isPaused(event.key):
                self.event._updateQueue(self.evt[event.js_type](event))
        event.preventDefault()

    def onKeyUp(self, event):
        if event.key in self.modKey:
            self.event.keyPress[self.modKey[event.key]] = False
        if event.key in self.keyHeld:
            self.keyHeld[event.key]['pressed'] = False
        if event.js_type in self.event.events:
            self.event._updateQueue(self.evt[event.js_type](event))

    def _onKeyDown(self, event):
        keycode = event.which or event.keyCode or 0
        if keycode in self.modKeyCode:
            self.event.keyPress[keycode] = True
        if event.js_type in self.event.events:
            if not self._isPaused(event.keyCode):
                self.event.keyCode = keycode
                if keycode in self.specialKeyCode:
                    self.event._updateQueue(self.evt[event.js_type](event))
                    event.preventDefault()
            else:
                event.preventDefault()

    def _onKeyUp(self, event):
        keycode = event.which or event.keyCode or 0
        if keycode in self.modKeyCode:
            self.event.keyPress[keycode] = False
        if keycode in self.keyHeld:
            self.keyHeld[keycode]['pressed'] = False
        if event.js_type in self.event.events:
            self.event._updateQueue(self.evt[event.js_type](event))

    def _onKeyPress(self, event):
        if event.js_type in self.event.events:
            keycode = event.which or event.keyCode or 0
            self.event.keyPressCode[self.event.keyCode] = keycode
            self.event._updateQueue(self.evt[event.js_type](event))
        event.preventDefault()

    def onFocus(self, event):
        self.event.mouseEvt['focus'] = True
        self.event._updateQueue(self.evt[event.js_type](event))

    def onBlur(self, event):
        self.event.mouseEvt['focus'] = False
        self.event._updateQueue(self.evt[event.js_type](event))

    def onVisibilityChange(self, event):
        self.event._updateQueue(self.evt[event.js_type](event))

    def onPageHide(self, event):
        self.event._updateQueue(self.evt[event.js_type](event))

    def onResize(self, event):
        if not self._clientRect_update_timeout:
            window.setTimeout(self._clientRect_update, 20)
            self._clientRect_update_timeout = True

    def onScroll(self, event):
        if not self._clientRect_update_timeout:
            window.setTimeout(self._clientRect_update, 20)
            self._clientRect_update_timeout = True

    def _clientRect_update(self):
        self._clientRect = self.getBoundingClientRect()
        self._clientRect_update_timeout = False

    def _isPaused(self, keycode):
        if keycode not in self.keyHeld:
            self.keyHeld[keycode] = {'pressed':False, 'delay':False, 'time':0}
        key = self.keyHeld[keycode]
        if not key['pressed']:
            key['pressed'] = True
            paused = False
            if self.keyRepeat[0]:
                key['delay'] = True
                key['time'] = self.time.time()
        else:
            paused = True
            if self.keyRepeat[0]:
                time = self.time.time()
                if key['delay']:
                    if time - key['time'] > self.keyRepeat[0]:
                        key['time'] = time
                        key['delay'] = False
                        paused = False
                elif time - key['time'] > self.keyRepeat[1]:
                    key['time'] = time
                    paused = False
        return paused

    def onTouchInitiate(self, event):
        self.event.touchlistener.activate()
        for callback in self._touch_callback:
            if hasattr(callback, 'onTouchInitiate'):
                callback.onTouchInitiate(event)
        self.onTouchStart(event)

    def onTouchStart(self, event):
        for callback in self._touch_callback:
            callback.onTouchStart(event)

    def onTouchEnd(self, event):
        for callback in self._touch_callback:
            callback.onTouchEnd(event)

    def onTouchMove(self, event):
        for callback in self._touch_callback:
            callback.onTouchMove(event)

    def onTouchCancel(self, event):
        for callback in self._touch_callback:
            callback.onTouchCancel(event)

    def preventContextMenu(self, setting=True):
        if setting:
            if self.onContextMenu: return
            element = self.getElement()
            self.onContextMenu = lambda event: event.preventDefault()
            element.addEventListener('contextmenu', self.onContextMenu)
        else:
            if not self.onContextMenu: return
            element = self.getElement()
            element.removeEventListener('contextmenu', self.onContextMenu)
            self.onContextMenu = None

    def resize(self, width, height):
        Surface.resize(self, width, height)
        self.surface.resize(width, height)
        self.surface._display._surface_rect = self.surface.get_rect()

    def set_callback(self, cb):
        if not hasattr(cb, 'run'):
            self.callback = Callback(cb)
        else:
            self.callback = cb

    def start(self):
        if not self.initialized:
            self.initialized = True
            _wnd.requestAnimationFrame(run)
            self.run = self._run

    def stop(self):
        global run
        run = lambda ts: None
        self.run = lambda: None

    def _get_rect(self):
        if self._rect_num < self._rect_len:
            return self._rect_list[self._rect_num]
        else:
            self._rect_list.append(Rect(0,0,0,0))
            self._rect_len += 1
            return self._rect_list[self._rect_num]

    def update(self, timestamp):
        if not self._framerate:
            self._frametime = timestamp - self._rendertime
            self.run()
        else:
            self._frametime += timestamp - self._rendertime
            if self._frametime > self._framerate:
                self.run()
                self._frametime = 0
        self._rendertime = timestamp

    def render(self):
        while self._rect_num:
            rect = self._rect_list[self._rect_num-1]
            x,y,width,height = rect.x,rect.y,rect.width,rect.height
            _ctx.drawImage(_img, x,y,width,height, x,y,width,height)
            self._rect_num -= 1

    def _run(self):
        self.callback.run()


def run(timestamp):
    _wnd.requestAnimationFrame(run)
    _canvas.update(timestamp)
    _canvas.render()


class Callback:

    __slots__ = ['run']

    def __init__(self, cb):
        self.run = cb


class CallbackAF:

    def __init__(self):
        self.callback = None
        self.wnd = requestAnimationFrameInit()
        self.running = False
        self.start()

    def run(self):
        if self.running:
            self.wnd.requestAnimationFrame(self.run)
            if self.callback:
                self.callback()

    def start(self):
        if not self.running:
            self.wnd.requestAnimationFrame(self.run)
            self.running = True

    def stop(self):
        self.running = False

    def set_callback(self, cb):
        self.callback = cb


class Display:
    """
    Display object.
    """

    def __init__(self):
        """
        Initialize Display module.

        Module initialization creates pyjsdl.display instance.
        """
        self._initialized = False
        self.init()

    def init(self):
        """
        Initialize display module.
        """
        if not self._initialized:
            self.id = ''
            self.icon = None
            self.canvas = None
            self._callback = None
            self._image_list = []
            self._image_loading = False
            self._canvas_init = False
            self._callbackAF = CallbackAF()
            self._initialized = True

    def set_mode(self, size, flags=None, *args, **kwargs):
        """
        Setup the display Surface.

        Argument size (width, height) of surface.
        Return a reference to the display Surface.
        """
        self.canvas = Canvas(size)
        env.set_env('canvas', self.canvas)
        self.frame = document.body
        env.set_env('frame', self.frame)
        self.panel = self.canvas._initiate()
        self.vpanel = None
        self.textbox = None
        self.textarea = None
        self.Textbox = Textbox
        self.Textarea = Textarea
        self.surface = self.canvas.surface
        self.surface._display = self
        self._surface_rect = self.surface.get_rect()
        if self._canvas_init and not self._image_loading:
            self.canvas.set_callback(self._callback)
            self._callback = None
            self.canvas.start()
            self._callbackAF.stop()
        return self.surface

    def setup(self, callback, images=None):
        """
        Initialize Canvas for script execution.

        Argument include callback function to run and optional images list to preload.
        Callback function can also be an object with a run method to call.
        The images can be image URL, or base64 data in format (name.ext,data).
        """
        if not self._canvas_init:
            if images is not None:
                self._image_list.extend(images)
            if len(self._image_list) > 0:
                pyjsdl.image.preload_images(self._image_list, self._images_loaded)
                self._image_list = None
                self._image_loading = True
            self._canvas_init = True
        if self.canvas:
            if not self._image_loading:
                self.canvas.set_callback(callback)
                if not self.canvas.initialized:
                    self.canvas.start()
                    self._callbackAF.stop()
            else:
                self._callback = callback
        else:
            if not self._image_loading:
                self._callback = callback
                self._callbackAF.set_callback(self._callback)
            else:
                self._callback = callback

    def set_callback(self, callback):
        """
        Set Canvas callback function.

        Argument callback function to run.
        Callback function can also be an object with a run method to call.
        """
        if self.canvas and self.canvas.initialized:
            self.canvas.set_callback(callback)
        else:
            self.setup(callback)

    def setup_images(self, images):
        """
        Add images to image preload list.

        The argument is an image or list of images representing an image URL, or base64 data in format (name.ext,data).
        Image preloading occurs at display.setup call.
        """
        if isinstance(images, str):
            images = [images]
        self._image_list.extend(images)

    def _images_loaded(self):
        self._image_loading = False
        if self.canvas:
            self.canvas.set_callback(self._callback)
            self._callback = None
            self.canvas.start()
            self._callbackAF.stop()
        else:
            self._callbackAF.set_callback(self._callback)

    def textbox_init(self):
        """
        Initiate textbox functionality.

        Creates instances of display.textbox and display.textarea in lower VerticalPanel.
        """
        if not self.textbox:
            self.textbox = Textbox()
            self.textarea = Textarea()

    def get_surface(self):
        """
        Return display Surface.
        """
        return self.surface

    def get_canvas(self):
        """
        Return Canvas.
        """
        return self.canvas

    def set_panel(self, id):
        """
        Set panel.

        Argument id is the dom element id. App default id is '__panel__'.
        Call at app start to change default.
        """
        RootPanel._set_root_panel(id)
        return None

    def get_panel(self):
        """
        Return Panel.
        """
        return self.panel

    def get_vpanel(self):
        """
        Return VerticalPanel positioned under Panel holding Canvas.
        """
        if not self.vpanel:
            self.vpanel = VerticalPanel()
            RootPanel().add(self.vpanel)
        return self.vpanel

    def resize(self, width, height):
        """
        Resize canvas display.

        Arguments width and height of display.
        """
        self.canvas.resize(width, height)

    def clientRect_update(self, element=None):
        """
        Update client rect.

        Refresh bounding client rect if manually change canvas positioning.
        Optional element, such as scrollable div, to attach scroll event listener.
        """
        if not element:
            self.canvas._clientRect_update()
        else:
            self.canvas.addDivScrollListener(element)

    def getAbsoluteLeft(self):
        """
        Return canvas left-offset position.
        """
        return self.canvas.getAbsoluteLeft()

    def getAbsoluteTop(self):
        """
        Return canvas top-offset position.
        """
        return self.canvas.getAbsoluteTop()

    def getScrollLeft(self):
        """
        Return page horizontal scroll offset.
        """
        return self.frame.scrollLeft

    def getScrollTop(self):
        """
        Return page vertical scroll offset.
        """
        return self.frame.scrollTop

    def quit(self):
        """
        Uninitialize display.
        """
        self._initialized = False
        return None

    def get_init(self):
        """
        Check that display module is initialized.
        """
        return self._initialized

    def get_active(self):
        """
        Check if display is visible.
        """
        if hasattr(self, 'canvas'):
            return True
        else:
            return False

    def set_icon(self, icon):
        """
        Set page icon.

        Argument is the icon image URL or relative path.
        Icon can be a surface including images that were preloaded.
        """
        pyjsobj.set_icon(icon)
        return None

    def set_caption(self, text):
        """
        Set Canvas element id.

        Argument is the id text.
        """
        self.id = text
        if self.canvas:
            self.canvas.setID(self.id)
        return None

    def get_caption(self):
        """
        Get Canvas element id.
        """
        if self.canvas:
            return self.canvas.getID()
        else:
            return self.id

    def flip(self):
        """
        Repaint display.
        """
        self.canvas._ctx.drawImage(self.surface.canvas, 0, 0)
        return None

    def update(self, rect_list=None):
        """
        Repaint display.

        Optional rect or rect list to specify regions to repaint.
        """
        if hasattr(rect_list, 'append'):
            _update(self.canvas, rect_list)
        elif rect_list:
            _update(self.canvas, [rect_list])
        else:
            self.flip()
        return None

    def js_update(self, rect_list=None):
        self.update(rect_list)


def _update(canvas, rect_list):
    for rect in rect_list:
        if hasattr(rect, 'width'):
            if (rect.width > 0) and (rect.height > 0):
                repaint_rect = canvas._get_rect()
                repaint_rect.x = rect.x
                repaint_rect.y = rect.y
                repaint_rect.width = rect.width
                repaint_rect.height = rect.height
                canvas._rect_num += 1
        elif rect:
            if (rect[2] > 0) and (rect[3] > 0):
                repaint_rect = canvas._get_rect()
                repaint_rect.x = rect[0]
                repaint_rect.y = rect[1]
                repaint_rect.width = rect[2]
                repaint_rect.height = rect[3]
                canvas._rect_num += 1


class Textbox(TextBox):
    """
    TextBox object for text input.

    Optional argument size (width, height) of textbox and panel to hold element.
    Default size derived from Canvas size placed in lower VerticalPanel.
    """

    def __init__(self, size=None, panel=None):
        TextBox.__init__(self)
        if size is None:
            self.width = '100%'
            self.height = '20px'
            self.setSize(self.width, self.height)
        else:
            self.width = int(size[0])
            self.height = int(size[1])
            self.setSize(str(self.width)+'px', str(self.height)+'px')
        self.setVisible(False)
        if panel:
            panel.add(self)
        else:
            if env.canvas.surface._display.vpanel is not None:
                env.canvas.surface._display.vpanel.add(self)
            else:
                panel = VerticalPanel()
                env.canvas.surface._display.vpanel = panel
                panel._element.style.width = str(env.canvas.surface.width-2) + 'px'
                RootPanel().add(panel)
                panel.add(self)

    def resize(self, width=None, height=None):
        if not (width or height):
            self.width = '100%'
            self.height = '20px'
            self.setSize(self.width, self.height)
        else:
            if width:
                self.width = int(width)
            if height:
                self.height = int(height)
            self.setSize(str(self.width)+'px', str(self.height)+'px')

    def toggle(self, visible=None):
        if visible:
            self.setVisible(visible)
        else:
            self.setVisible(not self.getVisible())


class Textarea(TextArea):
    """
    TextArea object for text input/output.

    Optional argument size (width, height) of textarea and panel to hold element.
    Default size derived from Canvas size placed in lower VerticalPanel.
    """

    def __init__(self, size=None, panel=None):
        TextArea.__init__(self)
        if size is None:
            self.width = '100%'
            self.height = str(int(env.canvas.surface.height/2)) + 'px'
            self.setSize(self.width, self.height)
        else:
            self.width = int(size[0])
            self.height = int(size[1])
            self.setSize(str(self.width)+'px', str(self.height)+'px')
        self.setVisible(False)
        if panel:
            panel.add(self)
        else:
            if env.canvas.surface._display.vpanel is not None:
                env.canvas.surface._display.vpanel.add(self)
            else:
                panel = VerticalPanel()
                env.canvas.surface._display.vpanel = panel
                panel._element.style.width = str(env.canvas.surface.width-2) + 'px'
                RootPanel().add(panel)
                panel.add(self)

    # __pragma__ ('kwargs')

    def resize(self, width=None, height=None):
        if not (width or height):
            self.width = '100%'
            self.height = str(int(env.canvas.surface.height/2)) + 'px'
            self.setSize(self.width, self.height)
        else:
            if width:
                self.width = int(width)
            if height:
                self.height = int(height)
            self.setSize(str(self.width)+'px', str(self.height)+'px')

    # __pragma__ ('nokwargs')

    def toggle(self, visible=None):
        if visible:
            self.setVisible(visible)
        else:
            self.setVisible(not self.getVisible())

