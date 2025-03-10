#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

"""
**Surface module**

The module provides surface object.
"""

from pyjsdl.pyjsobj import HTML5Canvas
from pyjsdl.rect import Rect, rectPool
from pyjsdl.color import Color
from pyjsdl.pyjsobj import hasattr_v1 as hasattr


_return_rect = True


class Surface(HTML5Canvas):
    """
    Surface object.
    """

    def __init__(self, size, *args, **kwargs):
        """
        Initialize Surface object.

        Return Surface subclassed from a Canvas implementation.
        The size argument is the dimension (width, height) of surface.

        Module initialization places Surface in module's namespace.
        """
        self.width = int(size[0])
        self.height = int(size[1])
        HTML5Canvas.__init__(self, self.width, self.height)
        HTML5Canvas.resize(self, self.width, self.height)
        self._display = None
        self._super_surface = None
        self._offset = (0,0)
        self._colorkey = None
        self._stroke_style = -1
        self._fill_style = -1
        self._alpha = 1.0
        self._nonimplemented_methods()

    def __str__(self):
        s = '<{}({}x{})>'
        return s.format(self.__class__.__name__, self.width, self.height)

    def __repr__(self):
        return self.__str__()

    def get_size(self):
        """
        Return width and height of surface.
        """
        return (self.width, self.height)

    def get_width(self):
        """
        Return width of surface.
        """
        return self.width

    def get_height(self):
        """
        Return height of surface.
        """
        return self.height

    def resize(self, width, height):
        """
        Resize surface.
        """
        self.width = int(width)
        self.height = int(height)
        HTML5Canvas.resize(self, self.width, self.height)

    # __pragma__ ('kwargs')

    def get_rect(self, **attr):
        """
        Return rect of the surface.

        An optional keyword argument of the rect position.
        """
        rect = Rect(0, 0, self.width, self.height)
        for key in attr.keys():
            setattr(rect, key, attr[key])
        return rect

    # __pragma__ ('nokwargs')

    def copy(self):
        """
        Return Surface that is a copy of this surface.
        """
        surface = Surface((self.width, self.height))
        surface.drawImage(self.canvas, 0, 0)
        surface._colorkey = self._colorkey
        surface._alpha = self._alpha
        return surface

    def subsurface(self, rect):
        """
        Return subsurface.

        Return Surface that represents a subsurface.
        The rect argument is the area of the subsurface.
        Argument can be 't'/'f' for data sync to/from subsurface.
        """
        if rect in ('t', 'f'):
            if not self._super_surface:
                return
            if rect == 't':
                self.drawImage(self._super_surface.canvas,
                    self._offset[0], self._offset[1], self.width, self.height,
                    0, 0, self.width, self.height)
            else:
                self._super_surface.drawImage(self.canvas,
                    self._offset[0], self._offset[1])
            return
        if hasattr(rect, 'width'):
            _rect = rect
        else:
            _rect = Rect(rect)
        surf_rect = self.get_rect()
        if not surf_rect.contains(_rect):
            raise ValueError('subsurface outside surface area')
        surface = self.getSubimage(_rect.x, _rect.y, _rect.width, _rect.height)
        surface._super_surface = self
        surface._offset = (_rect.x,_rect.y)
        surface._colorkey = self._colorkey
        surface._alpha = self._alpha
        return surface

    def getSubimage(self, x, y, width, height):
        """
        Return subimage of Surface.

        Arguments include x, y, width, and height of the subimage.
        """
        surface = Surface((width,height))
        surface.drawImage(self.canvas,
                          x, y, width, height, 0, 0, width, height)
        return surface

    def blit(self, surface, position, area=None):
        """
        Draw given surface on this surface at position.

        Optional area delimitates the region of given surface to draw.
        """
        if not hasattr(position, '_x'):
            x = position[0]
            y = position[1]
        else:
            x = position.x
            y = position.y
        ctx = self._ctx
        ctx.globalAlpha = surface._alpha
        if not area:
            ctx.drawImage(surface.canvas, x, y)
            ctx.globalAlpha = 1.0
            if _return_rect:
                rect = rectPool.get(x, y, surface.width, surface.height)
            else:
                return None
        else:
            if not hasattr(area, '_x'):
                ax = area[0]
                ay = area[1]
                aw = area[2]
                ah = area[3]
            else:
                ax = area.x
                ay = area.y
                aw = area.width
                ah = area.height
            ctx.drawImage(surface.canvas, ax, ay, aw, ah, x, y, aw, ah)
            ctx.globalAlpha = 1.0
            if _return_rect:
                rect = rectPool.get(x, y, aw, ah)
            else:
                return None
        if self._display:
            surface_rect = self._display._surface_rect
        else:
            surface_rect = self.get_rect()
        changed_rect = surface_rect.clip(rect)
        rectPool.append(rect)
        return changed_rect

    def blits(self, blit_sequence, doreturn=True):
        """
        Draw a sequence of surfaces on this surface.

        Argument blit_sequence of (source, dest) or (source, dest, area).
        Optional doreturn (defaults to True) to return list of rects.
        """
        ctx = self._ctx
        if doreturn:
            rects = []
            if self._display:
                surface_rect = self._display._surface_rect
            else:
                surface_rect = self.get_rect()
        else:
            rects = None
        for blit in blit_sequence:
            surface = blit[0]
            position = blit[1]
            if not hasattr(position, '_x'):
                x = position[0]
                y = position[1]
            else:
                x = position.x
                y = position.y
            if len(blit) > 2:
                area = blit[2]
                if not hasattr(area, '_x'):
                    ax = area[0]
                    ay = area[1]
                    aw = area[2]
                    ah = area[3]
                else:
                    ax = area.x
                    ay = area.y
                    aw = area.width
                    ah = area.height
            else:
                area = None
            ctx.globalAlpha = surface._alpha
            if not area:
                ctx.drawImage(surface.canvas, x, y)
                if doreturn:
                    rect = rectPool.get(x, y, surface.width, surface.height)
                    rects.append(surface_rect.clip(rect))
                    rectPool.append(rect)
            else:
                ctx.drawImage(surface.canvas, ax, ay, aw, ah, x, y, aw, ah)
                if doreturn:
                    rect = rectPool.get(x, y, aw, ah)
                    rects.append(surface_rect.clip(rect))
                    rectPool.append(rect)
        ctx.globalAlpha = 1.0
        return rects

    def _blits(self, surfaces):
        ctx = self._ctx
        for surface, rect in surfaces:
            ctx.globalAlpha = surface._alpha
            ctx.drawImage(surface.canvas, rect.x, rect.y)
        ctx.globalAlpha = 1.0

    def _blit_clear(self, surface, rect_list):
        ctx = self._ctx
        ctx.globalAlpha = surface._alpha
        for r in rect_list:
            ctx.drawImage(surface.canvas,
                          r.x, r.y, r.width, r.height,
                          r.x, r.y, r.width, r.height)
        ctx.globalAlpha = 1.0

    def set_alpha(self, alpha):
        """
        Set surface alpha.

        Surface alpha can have values of 0 to 255, disabled by passing None.
        """
        if alpha is not None:
            _alpha = alpha/255.0
            if _alpha < 0.0:
                _alpha = 0.0
            elif _alpha > 1.0:
                _alpha = 1.0
            self._alpha = _alpha
        else:
            self._alpha = 1.0

    def get_alpha(self):
        """
        Get surface alpha value.
        """
        return int(self._alpha*255)

    def set_colorkey(self, color, flags=None):
        """
        Set surface colorkey.
        """
        if self._colorkey:
            self.replace_color((0,0,0,0),self._colorkey)
            self._colorkey = None
        if color:
            self._colorkey = Color(color)
            self.replace_color(self._colorkey)
        return None

    def get_colorkey(self):
        """
        Return surface colorkey.
        """
        if self._colorkey:
            return ( self._colorkey.r,
                     self._colorkey.g,
                     self._colorkey.b,
                     self._colorkey.a )
        else:
            return None

    def replace_color(self, color, new_color=None):
        """
        Replace color with with new_color or with alpha.
        """
        pixels = self.getImageData(0, 0, self.width, self.height)
        if hasattr(color, 'a'):
            color1 = color
        else:
            color1 = Color(color)
        if new_color is None:
            alpha_zero = True
        else:
            if hasattr(new_color, 'a'):
                color2 = new_color
            else:
                color2 = Color(new_color)
            alpha_zero = False
        if alpha_zero:
            r1,g1,b1,a1  = color1.r, color1.g, color1.b, color1.a
            a2  = 0
            data = pixels.data
            for i in range(0, len(data), 4):
                if (data[i] == r1 and data[i+1] == g1 and
                            data[i+2] == b1 and data[i+3] == a1):
                    data[i+3] = a2
        else:
            r1,g1,b1,a1 = color1.r, color1.g, color1.b, color1.a
            r2,g2,b2,a2 = color2.r, color2.g, color2.b, color2.a
            data = pixels.data
            for i in range(0, len(data), 4):
                if (data[i] == r1 and data[i+1] == g1 and
                            data[i+2] == b1 and data[i+3] == a1):
                    data[i] = r2
                    data[i+1] = g2
                    data[i+2] = b2
                    data[i+3] = a2
        self.putImageData(pixels, 0, 0, 0, 0, self.width, self.height)
        return None

    def get_at(self, pos):
        """
        Get color of a surface pixel.

        The pos argument represents x,y position of pixel.
        Return color (r,g,b,a) of a surface pixel.
        """
        pixel = self.getImageData(pos[0], pos[1], 1, 1)
        r, g, b, a = pixel.data
        return Color(r, g, b, a)

    def set_at(self, pos, color):
        """
        Set color of a surface pixel.

        The arguments represent position x,y and color of pixel.
        """
        # __pragma__ ('opov')
        if self._fill_style != color:
            # __pragma__ ('noopov')
            self._fill_style = color
            if hasattr(color, 'a'):
                _color = color
            else:
                _color = Color(color)
            self.setFillStyle(_color)
        self.fillRect(pos[0], pos[1], 1, 1)
        return None

    def fill(self, color=None, rect=None):
        """
        Fill surface with color.
        """
        if color is None:
            HTML5Canvas.fill(self)
            return
        # __pragma__ ('opov')
        if self._fill_style != color:
            # __pragma__ ('noopov')
            self._fill_style = color
            if hasattr(color, 'a'):
                self.setFillStyle(color)
            else:
                self.setFillStyle(Color(color))
        if not _return_rect:
            if rect is None:
                self.fillRect(0, 0, self.width, self.height)
            else:
                self.fillRect(rect[0], rect[1], rect[2], rect[3])
            return None
        if rect is None:
            _rect = Rect(0, 0, self.width, self.height)
            self.fillRect(_rect.x, _rect.y, _rect.width, _rect.height)
        else:
            if self._display:
                if hasattr(rect, 'width'):
                    _rect = self._display._surface_rect.clip(rect)
                else:
                    _rect_ = rectPool.get(rect[0],rect[1],rect[2],rect[3])
                    _rect = self._display._surface_rect.clip(_rect_)
                    rectPool.append(_rect_)
            else:
                surface_rect = rectPool.get(0, 0, self.width, self.height)
                if hasattr(rect, 'width'):
                    _rect = surface_rect.clip(rect)
                else:
                    _rect_ = rectPool.get(rect[0],rect[1],rect[2],rect[3])
                    _rect = surface_rect.clip(_rect_)
                    rectPool.append(_rect_)
                rectPool.append(surface_rect)
            if _rect.width and _rect.height:
                self.fillRect(_rect.x, _rect.y, _rect.width, _rect.height)
        return _rect

    def get_parent(self):
        """
        Return parent Surface of subsurface.
        """
        return self._super_surface

    def get_offset(self):
        """
        Return offset of subsurface in surface.
        """
        return self._offset

    def toDataURL(self, datatype=None):
        """
        Return surface data as a base64 data string.

        Optional datatype to set data format, default to 'image/png'.
        Implemented with HTML5 Canvas toDataURL method.
        """
        if not datatype:
            return self.canvas.toDataURL()
        else:
            return self.canvas.toDataURL(datatype)

    def toString(self):
        return self.__str__()

    def _nonimplemented_methods(self):
        self.convert = lambda *arg: self
        self.convert_alpha = lambda *arg: self
        self.lock = lambda *arg: None
        self.unlock = lambda *arg: None
        self.mustlock = lambda *arg: False
        self.get_locked = lambda *arg: False
        self.get_locks = lambda *arg: ()


class Surf:
    """
    Surf object.
    """

    def __init__(self, image):
        """
        Initialize Surf object.

        Image argument wrapped to provide limited Surface functionality.
        """
        self.canvas = image
        self.width = self.canvas.width
        self.height = self.canvas.height
        self._display = None
        self._colorkey = None
        self._alpha = 1.0
        self.convert = lambda *arg: self
        self.convert_alpha = lambda *arg: self

    def __str__(self):
        s = '<{}({}x{})>'
        return s.format(self.__class__.__name__, self.width, self.height)

    def get_size(self):
        """
        Return size of surface.
        """
        return (self.width, self.height)

    def get_width(self):
        """
        Return width of surface.
        """
        return self.width

    def get_height(self):
        """
        Return height of surface.
        """
        return self.height

    # __pragma__ ('kwargs')

    def get_rect(self, **attr):
        """
        Return rect of the surface.

        An optional keyword argument of the rect position.
        """
        rect = Rect(0, 0, self.width, self.height)
        for key in attr.keys():
            setattr(rect, key, attr[key])
        return rect

    # __pragma__ ('nokwargs')

    def set_alpha(self, alpha):
        """
        Set surface alpha.

        Surface alpha can have values of 0 to 255, disabled by passing None.
        """
        if alpha is not None:
            _alpha = alpha/255.0
            if _alpha < 0.0:
                _alpha = 0.0
            elif _alpha > 1.0:
                _alpha = 1.0
            self._alpha = _alpha
        else:
            self._alpha = 1.0

    def get_alpha(self):
        """
        Get surface alpha value.
        """
        return int(self._alpha*255)

    def toString(self):
        return self.__str__()


class IndexSizeError(Exception):
    """
    Exception object.
    """
    pass


def bounding_rect_return(setting):
    """
    Bounding rect return.

    Set whether surface blit/fill functions return bounding Rect.
    Setting (bool) defaults to True on module initialization.
    """
    global _return_rect
    _return_rect = setting

