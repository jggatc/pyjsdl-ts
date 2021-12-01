#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.pyjsobj import Color as _Color

__docformat__ = 'restructuredtext'


class Color(_Color):

    # __pragma__ ('opov')

    def __init__(self, *color):
        """
        Return Color object.
        
        Alternative arguments:
        
        * r,g,b,a
        * r,g,b
        * (r,g,b,a)
        * (r,g,b)
        * integer rgba
        * Color

        Color has the attributes::
        
            r, g, b, a

        Module initialization places pyjsdl.Color in module's namespace.
        """
        ln = len(color)
        if ln == 1:
            _color = color[0]
            if isinstance(_color, (tuple,list,Color)):
                ln = len(_color)
        else:
            _color = color
        if ln == 4:
            self.r,self.g,self.b,self.a = _color[0],_color[1],_color[2],_color[3]
        elif ln == 3:
            self.r,self.g,self.b,self.a = _color[0],_color[1],_color[2],255
        else:
            if hasattr(_color, 'startswith') and _color.startswith('#'):
                _color = '0x' + _color[1:]
            self.r,self.g,self.b,self.a = (_color>>16) & 0xff, (_color>>8) & 0xff, _color & 0xff, (_color>>24) & 0xff

    # __pragma__ ('noopov')

    def __str__(self):
        return 'rgba({}, {}, {}, {})'.format(self.r, self.g, self.b, self.a/255.0)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.r, self.g, self.b, self.a)

    def __getitem__(self, index):
        return {0:self.r, 1:self.g, 2:self.b, 3:self.a}[index]

    def __setitem__(self, index, val):
        if index == 0:
            self.r = val
        elif index == 1:
            self.g = val
        elif index == 2:
            self.b = val
        elif index == 3:
            self.a = val

    def __iter__(self):
        return iter([self.r, self.g, self.b, self.a])

    def __len__(self):
        return 4

    def __eq__(self, other):
        if hasattr(other, 'a'):
            return self.r==other.r and self.g==other.g and self.b==other.b and self.a==other.a
        else:
            if len(other) == 4:
                return self.a==other[3] and self.r==other[0] and self.g==other[1] and self.b==other[2]
            else:
                return self.r==other[0] and self.g==other[1] and self.b==other[2]

    def __ne__(self, other):
        if hasattr(other, 'a'):
            return self.r!=other.r or self.g!=other.g or self.b!=other.b or self.a!=other.a
        else:
            if len(other) == 4:
                return self.a!=other[3] or self.r!=other[0] or self.g!=other[1] or self.b!=other[2]
            else:
                return self.r!=other[0] or self.g!=other[1] or self.b!=other[2]

