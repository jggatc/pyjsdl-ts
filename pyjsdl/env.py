#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

canvas = None

frame = None

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


def set_env(key, val):
    global canvas, frame, event
    if key == 'canvas':
        canvas = val
    elif key == 'frame':
        frame = val
    elif key == 'event':
        event = val

