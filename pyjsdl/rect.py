#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.pylib import int

__docformat__ = 'restructuredtext'


class Rect(object):
    """
    **pyjsdl.Rect**
    
    * Rect.copy
    * Rect.move
    * Rect.move_ip
    * Rect.inflate
    * Rect.inflate_ip
    * Rect.contains
    * Rect.union
    * Rect.union_ip
    * Rect.unionall
    * Rect.unionall_ip
    * Rect.clamp
    * Rect.clamp_ip
    * Rect.clip
    * Rect.collidepoint
    * Rect.colliderect
    * Rect.collidelist
    * Rect.collidelistall
    * Rect.collidedict
    * Rect.collidedictall
    """

    __slots__ = ['_x', '_y', '_width', '_height']

    def __init__(self, *args):
        """
        Return Rect object.
        
        Alternative arguments:
        
        * x, y, width, height
        * (x, y), (width, height)
        * (x, y, width, height)
        * Rect
        * Obj with rect attribute

        Rect has the attributes::
        
        x, y, width, height
        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        center, centerx, centery
        size, w, h

        Operator and index functionality requires __pragma__ ('opov').

        Module initialization places pyjsdl.Rect in module's namespace.
        """
        ln = len(args)
        if ln == 1:
            if args.index:
                arg = args[0]
                ln = len(arg)
            else:
                arg = args
        else:
            arg = args
        if ln == 4 and arg.index:
            x = arg[0]
            y = arg[1]
            width = arg[2]
            height = arg[3]
        elif ln == 2:
            x = arg[0][0]
            y = arg[0][1]
            width = arg[1][0]
            height = arg[1][1]
        else:
            if arg.rect:
                arg = arg.rect
            x = arg.x
            y = arg.y
            width = arg.width
            height = arg.height
        self._x = ~(~(x))
        self._y = ~(~(y))
        self._width = ~(~(width))
        self._height = ~(~(height))

    def __str__(self):
        return '<rect({}, {}, {}, {})>'.format(self._x,
                                               self._y,
                                               self._width,
                                               self._height)

    def __repr__(self):
        class_name = self.__class__.__name__
        return '{}({}, {}, {}, {})'.format(class_name, self._x,
                                                       self._y,
                                                       self._width,
                                                       self._height)

    def __getitem__(self, index):
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        elif index == 2:
            return self._width
        elif index == 3:
            return self._height

    def __setitem__(self, index, val):
        if index == 0:
            self._x = int(val)
        elif index == 1:
            self._y = int(val)
        elif index == 2:
            self._width = int(val)
        elif index == 3:
            self._height = int(val)

    def __iter__(self):
        return iter([self._x, self._y, self._width, self._height])

    def __len__(self):
        return 4

    def __bool__(self):
        return self._width and self._height

    def __nonzero__(self):
        return self._width and self._height

    def __eq__(self, other):
        return (self._x == other._x and
                self._y == other._y and
                self._width == other._width
                and self._height == other._height)

    def __ne__(self, other):
        return (self._x != other._x or
                self._y != other._y or
                self._width != other._width or
                self._height != other._height)

    def copy(self):
        """
        Returns Rect that is a copy of this rect.
        """
        return Rect(self._x, self._y, self._width, self._height)

    def move(self, *offset):
        """
        Return Rect of same dimension at position offset by x,y.
        """
        if len(offset) == 2:
            x = offset[0]
            y = offset[1]
        else:
            _offset = offset[0]
            x = _offset[0]
            y = _offset[1]
        return Rect(self._x + x, self._y + y, self._width, self._height)

    def move_ip(self, *offset):
        """
        Moves this rect to position offset by x,y.
        """
        if len(offset) == 2:
            x = offset[0]
            y = offset[1]
        else:
            _offset = offset[0]
            x = _offset[0]
            y = _offset[1]
        self._x = self._x + int(x)
        self._y = self._y + int(y)
        return None

    def inflate(self, *offset):
        """
        Return Rect at same position but size offset by x,y.
        """
        if len(offset) == 2:
            x = offset[0]
            y = offset[1]
        else:
            _offset = offset[0]
            x = _offset[0]
            y = _offset[1]
        return Rect(self._x - int(x/2), self._y - int(y/2),
                    self._width + x, self._height + y)

    def inflate_ip(self, *offset):
        """
        Change size of this rect offset by x,y.
        """
        if len(offset) == 2:
            x = offset[0]
            y = offset[1]
        else:
            _offset = offset[0]
            x = _offset[0]
            y = _offset[1]
        self._x = self._x - int(x/2)
        self._y = self._y - int(y/2)
        self._width = self._width + int(x)
        self._height = self._height + int(y)
        return None

    def clip(self, rect):
        """
        Return Rect representing this rect clipped by rect.
        """
        if not (self._x < (rect._x + rect._width) and
                rect._x < (self._x + self._width) and
                self._y < (rect._y + rect._height) and
                rect._y < (self._y + self._height)):
            return Rect(0,0,0,0)
        else:
            x = self._x if self._x > rect._x else rect._x
            y = self._y if self._y > rect._y else rect._y
            s = self._x + self._width
            r = rect._x + rect._width
            w = (s if s < r else r) - x
            s = self._y + self._height
            r = rect._y + rect._height
            h = (s if s < r else r) - y
            return Rect(x, y, w, h)

    def contains(self, rect):
        """
        Check if rect is in this rect.
        """
        return (self._x <= rect._x and
                (self._x + self._width) >= (rect._x + rect._width) and
                self._y <= rect._y and
                (self._y + self._height) >= (rect._y + rect._height))

    def intersects(self, rect):
        """
        Check if rect intersects this rect.
        """
        return (self._x < (rect._x + rect._width) and
                rect._x < (self._x + self._width) and
                self._y < (rect._y + rect._height) and
                rect._y < (self._y + self._height))

    def union(self, rect):
        """
        Return Rect representing the union of rect and this rect.
        """
        x = self._x if self._x < rect._x else rect._x
        y = self._y if self._y < rect._y else rect._y
        s = self._x + self._width
        r = rect._x + rect._width
        w = (s if s > r else r) - x
        s = self._y + self._height
        r = rect._y + rect._height
        h = (s if s > r else r) - y
        return Rect(x, y, w, h)

    def union_ip(self, rect):
        """
        Change this rect to represent the union of rect and this rect.
        """
        x = self._x if self._x < rect._x else rect._x
        y = self._y if self._y < rect._y else rect._y
        s = self._x + self._width
        r = rect._x + rect._width
        w = (s if s > r else r) - x
        s = self._y + self._height
        r = rect._y + rect._height
        h = (s if s > r else r) - y
        self._x = x
        self._y = y
        self._width = w
        self._height = h
        return None

    def unionall(self, rect_list):
        """
        Return Rect representing the union of rect list and this rect.
        """
        x1 = self._x
        y1 = self._y
        x2 = self._x + self._width
        y2 = self._y + self._height
        for r in rect_list:
            if r._x < x1:
                x1 = r._x
            if r._y < y1:
                y1 = r._y
            rx2 = r._x + r._width
            if rx2 > x2:
                x2 = rx2
            ry2 = r._y + r._height
            if ry2 > y2:
                y2 = ry2
        return Rect(x1, y1, x2 - x1, y2 - y1)

    def unionall_ip(self, rect_list):
        """
        Change this rect to represent the union of rect list and this rect.
        """
        x1 = self._x
        y1 = self._y
        x2 = self._x + self._width
        y2 = self._y + self._height
        for r in rect_list:
            if r._x < x1:
                x1 = r._x
            if r._y < y1:
                y1 = r._y
            rx2 = r._x + r._width
            if rx2 > x2:
                x2 = rx2
            ry2 = r._y + r._height
            if ry2 > y2:
                y2 = ry2
        self._x = x1
        self._y = y1
        self._width = x2 - x1
        self._height = y2 - y1
        return None

    def clamp(self, rect):
        """
        Return Rect of same dimension as this rect moved within rect.
        """
        if self._width < rect._width:
            if self._x < rect._x:
                x = rect._x
            elif self._x + self._width > rect._x + rect._width:
                x = rect._x + rect._width - self._width
            else:
                x = self._x
        else:
            x = rect._x - int((self._width - rect._width)/2)
        if self._height < rect._height:
            if self._y < rect._y:
                y = rect._y
            elif self._y + self._height > rect._y + rect._height:
                y = rect._y + rect._height - self._height
            else:
                y = self._y
        else:
            y = rect._y - int((self._height - rect._height)/2)
        return Rect(x, y, self._width, self._height)

    def clamp_ip(self, rect):
        """
        Move this rect within rect.
        """
        if self._width < rect._width:
            if self._x < rect._x:
                x = rect._x
            elif self._x + self._width > rect._x + rect._width:
                x = rect._x + rect._width - self._width
            else:
                x = self._x
        else:
            x = rect._x - int((self._width - rect._width)/2)
        if self._height < rect._height:
            if self._y < rect._y:
                y = rect._y
            elif self._y + self._height > rect._y + rect._height:
                y = rect._y + rect._height - self._height
            else:
                y = self._y
        else:
            y = rect._y - int((self._height - rect._height)/2)
        self._x = x
        self._y = y
        return None

    def set(self, *args):
        """
        Set rect x,y,width,height attributes to argument.
        Alternative arguments:
        * x,y,w,h
        * (x,y),(w,h)
        * (x,y,w,h)
        * Rect
        * Obj with rect attribute
        """
        ln = len(args)
        if ln == 1:
            if args.index:
                arg = args[0]
                ln = len(arg)
            else:
                arg = args
        else:
            arg = args
        if ln == 4 and arg.append:
            x = arg[0]
            y = arg[1]
            width = arg[2]
            height = arg[3]
        elif ln == 2:
            x = arg[0][0]
            y = arg[0][1]
            width = arg[1][0]
            height = arg[1][1]
        else:
            if arg.rect:
                arg = arg.rect
            x = arg.x
            y = arg.y
            width = arg.width
            height = arg.height
        self._x = ~(~(x))
        self._y = ~(~(y))
        self._width = ~(~(width))
        self._height = ~(~(height))

    def collidepoint(self, *point):
        """
        Return True if point is in this rect.
        """
        if len(point) == 2:
            return (self._x <= point[0] < (self._x + self._width) and
                    self._y <= point[1] < (self._y + self._height))
        else:
            return (self._x <= point[0][0] < (self._x + self._width) and
                    self._y <= point[0][1] < (self._y + self._height))

    def colliderect(self, rect):
        """
        Return True if rect collides with this rect.
        """
        return (self._x < (rect._x + rect._width) and
                rect._x < (self._x + self._width) and
                self._y < (rect._y + rect._height) and
                rect._y < (self._y + self._height))

    def collidelist(self, rects):
        """
        Return index of rect in list that collide with this rect, otherwise returns -1.
        """
        for i, rect in enumerate(rects):
            if (self._x < (rect._x + rect._width) and
                rect._x < (self._x + self._width) and
                self._y < (rect._y + rect._height) and
                rect._y < (self._y + self._height)):
                return i
        return -1

    def collidelistall(self, rects):
        """
        Return list of indices of rects list that collide with this rect.
        """
        collided = []
        for i, rect in enumerate(rects):
            if (self._x < (rect._x + rect._width) and
                rect._x < (self._x + self._width) and
                self._y < (rect._y + rect._height) and
                rect._y < (self._y + self._height)):
                collided.append(i)
        return collided

    def collidedict(self, rects):
        """
        Return (key,value) of first rect from rects dict that collide with this rect, otherwise returns None.
        """
        for rect_key in rects.keys():
            rect = rects[rect_key]
            if (self._x < (rect._x + rect._width) and
                rect._x < (self._x + self._width) and
                self._y < (rect._y + rect._height) and
                rect._y < (self._y + self._height)):
                return (rect_key, rect)
        return None

    def collidedictall(self, rects):
        """
        Return list of (key,value) from rects dict that collide with this rect.
        """
        collided = []
        for rect_key in rects.keys():
            rect = rects[rect_key]
            if (self._x < (rect._x + rect._width) and
                rect._x < (self._x + self._width) and
                self._y < (rect._y + rect._height) and
                rect._y < (self._y + self._height)):
                collided.append((rect_key, rect))
        return collided

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def center(self):
        return (self._x + int(self._width/2), self._y + int(self._height/2))

    @property
    def centerx(self):
        return self._x + int(self._width/2)

    @property
    def centery(self):
        return self._y + int(self._height/2)

    @property
    def top(self):
        return self._y

    @property
    def left(self):
        return self._x

    @property
    def bottom(self):
        return self._y + self._height

    @property
    def right(self):
        return self._x + self._width

    @property
    def topleft(self):
        return (self._x, self._y)

    @property
    def bottomleft(self):
        return (self._x, self._y + self._height)

    @property
    def topright(self):
        return (self._x + self._width, self._y)

    @property
    def bottomright(self):
        return (self._x + self._width, self._y + self._height)

    @property
    def midtop(self):
        return (self._x + int(self._width/2), self._y)

    @property
    def midleft(self):
        return (self._x, self._y + int(self._height/2))

    @property
    def midbottom(self):
        return (self._x + int(self._width/2), self._y + self._height)

    @property
    def midright(self):
        return (self._x + self._width, self._y + int(self._height/2))

    @property
    def size(self):
        return (self._width, self._height)

    @property
    def w(self):
        return self._width

    @property
    def h(self):
        return self._height

    @x.setter
    def x(self, val):
        self._x = int(val)

    @y.setter
    def y(self, val):
        self._y = int(val)

    @width.setter
    def width(self, val):
        self._width = int(val)

    @height.setter
    def height(self, val):
        self._height = int(val)

    @center.setter
    def center(self, val):
        self._x = int(val[0]) - int(self._width/2)
        self._y = int(val[1]) - int(self._height/2)

    @centerx.setter
    def centerx(self, val):
        self._x = int(val) - int(self._width/2)

    @centery.setter
    def centery(self, val):
        self._y = int(val) - int(self._height/2)

    @top.setter
    def top(self, val):
        self._y = int(val)

    @left.setter
    def left(self, val):
        self._x = int(val)

    @bottom.setter
    def bottom(self, val):
        self._y = int(val) - self._height

    @right.setter
    def right(self, val):
        self._x = int(val) - self._width

    @topleft.setter
    def topleft(self, val):
        self._x = int(val[0])
        self._y = int(val[1])

    @bottomleft.setter
    def bottomleft(self, val):
        self._x = int(val[0])
        self._y = int(val[1]) - self._height

    @topright.setter
    def topright(self, val):
        self._x = int(val[0]) - self._width
        self._y = int(val[1])

    @bottomright.setter
    def bottomright(self, val):
        self._x = int(val[0]) - self._width
        self._y = int(val[1]) - self._height

    @midtop.setter
    def midtop(self, val):
        self._x = int(val[0]) - int(self._width/2)
        self._y = int(val[1])

    @midleft.setter
    def midleft(self, val):
        self._x = int(val[0])
        self._y = int(val[1]) - int(self._height/2)

    @midbottom.setter
    def midbottom(self, val):
        self._x = int(val[0]) - int(self._width/2)
        self._y = int(val[1]) - self._height

    @midright.setter
    def midright(self, val):
        self._x = int(val[0]) - self._width
        self._y = int(val[1]) - int(self._height/2)

    @size.setter
    def size(self, val):
        self._width = int(val[0])
        self._height = int(val[1])

    @w.setter
    def w(self, val):
        self._width = int(val)

    @h.setter
    def h(self, val):
        self._height = int(val)


class RectPool(object):
    """
    **pyjsdl.rect.rectPool**
    
    * rectPool.append
    * rectPool.extend
    * rectPool.get
    * rectPool.copy

    Rect pool accessed by rectPool instance through append method to add Rect, extend method to add Rect list, get method to return Rect set with x,y,width,height attributes, and copy method to return copy of a given Rect. If pool is empty, return is a new Rect.
    """

    def __init__(self):
        self._cache = []
        self._length = 0
        self.add = self.append
        self.addAll = self.extend

    def append(self, item):
        """
        Add Rect to pool.
        """
        self._cache.append(item)
        self._length += 1

    def extend(self, lst):
        """
        Add Rect list to pool.
        """
        self._cache.extend(lst)
        self._length += len(lst)

    def get(self, x, y, width, height):
        """
        Return a Rect with x,y,width,height attributes.
        """
        if self._length > 0:
            rect = self._cache.pop()
            self._length -= 1
            rect._x = x
            rect._y = y
            rect._width = width
            rect._height = height
            return rect
        else:
            return Rect(x, y, width, height)

    def copy(self, r):
        """
        Return a Rect with x,y,width,height attributes of the Rect argument.
        """
        if self._length > 0:
            rect = self._cache.pop()
            self._length -= 1
            rect._x = r._x
            rect._y = r._y
            rect._width = r._width
            rect._height = r._height
            return rect
        else:
            return Rect(r._x, r._y, r._width, r._height)

rectPool = RectPool()

