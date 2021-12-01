#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

canvas = None

frame = None

pyjs_mode = None

event = None


def get_canvas():
    """
    Return Canvas object.
    """
    return canvas


def get_frame():
    """
    Return Webpage frame.
    """
    return frame


def get_pyjsmode():
    """
    Return Pyjs mode object.
    """
    return pyjs_mode


def set_env(key, val):
    global canvas, frame, event, pyjs_mode
    if key == 'canvas':
        canvas = val
    elif key == 'frame':
        frame = val
    elif key == 'event':
        event = val
    elif key == 'pyjs_mode':
        pyjs_mode = val

