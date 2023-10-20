#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from math import pi as _pi, sin as _sin, cos as _cos, ceil as _ceil
from pyjsdl.pyjsobj import fabs as _fabs
from pyjsdl.pylib import int
from pyjsdl.surface import Surface

__docformat__ = 'restructuredtext'

__doc__ = 'Surface transformation'


_deg_rad = _pi/180.0


def rotate(surface, angle):
    """
    Return Surface rotated by the given angle.
    """
    if not angle:
        return surface.copy()
    theta = angle * _deg_rad
    width_i = surface.width
    height_i = surface.height
    cos_theta = _fabs(_cos(theta))
    sin_theta = _fabs(_sin(theta))
    width_f = int((width_i * cos_theta) + (height_i * sin_theta))
    height_f = int((width_i * sin_theta) + (height_i * cos_theta))
    surf = Surface((width_f, height_f))
    surf.saveContext()
    surf.translate(width_f/2.0, height_f/2.0)
    surf.rotate(-theta)
    surf.drawImage(surface.canvas, -width_i/2, -height_i/2)
    surf.restoreContext()
    surf._colorkey = surface._colorkey
    surf._alpha = surface._alpha
    return surf


def rotozoom(surface, angle, size):
    """
    Return Surface rotated and resized by the given angle and size.
    """
    if not angle:
        width = int(surface.width * size)
        height = int(surface.height * size)
        return scale(surface, (width, height))
    theta = angle * _deg_rad
    width_i = int(surface.width * size)
    height_i = int(surface.height * size)
    cos_theta = _fabs(_cos(theta))
    sin_theta = _fabs(_sin(theta))
    width_f = int(_ceil((width_i * cos_theta) + (height_i * sin_theta)))
    if width_f % 2:
        width_f += 1
    height_f = int(_ceil((width_i * sin_theta) + (height_i * cos_theta)))
    if height_f % 2:
        height_f += 1
    surf = Surface((width_f, height_f))
    surf.saveContext()
    surf.translate(width_f/2.0, height_f/2.0)
    surf.rotate(-theta)
    surf.drawImage(surface.canvas,
                   0, 0, surface.width, surface.height,
                   -width_i/2, -height_i/2, width_i, height_i)
    surf.restoreContext()
    surf._colorkey = surface._colorkey
    surf._alpha = surface._alpha
    return surf


def scale(surface, size, dest=None):
    """
    Return Surface resized by the given size.
    An optional destination surface can be provided.
    """
    if not dest:
        surf = Surface(size)
    else:
        surf = dest
    surf.drawImage(surface.canvas,
                   0, 0, surface.width, surface.height,
                   0, 0, size[0], size[1])
    surf._colorkey = surface._colorkey
    surf._alpha = surface._alpha
    return surf


def smoothscale(surface, size):
    """
    Calls scale().
    Return Surface resized by the given size.
    """
    return scale(surface, size)


def scale2x(surface, dest=None):
    """
    Return Surface resized to twice its size.
    An optional destination surface can be provided.
    """
    return scale(surface, (surface.width*2, surface.height*2), dest)


# __pragma__ ('kwargs')

def flip(surface, xbool=True, ybool=False):
    """
    Return Surface that is flipped horizontally, vertically, or both.
    """
    surf = Surface((surface.width, surface.height))
    surf.saveContext()
    if xbool and ybool:
        surf.translate(surface.width, surface.height)
        surf.scale(-1, -1)
    elif xbool:
        surf.translate(surface.width, 0)
        surf.scale(-1, 1)
    elif ybool:
        surf.translate(0, surface.height)
        surf.scale(1, -1)
    surf.drawImage(surface.canvas, 0, 0)
    surf.restoreContext()
    surf._colorkey = surface._colorkey
    surf._alpha = surface._alpha
    return surf

# __pragma__ ('nokwargs')

