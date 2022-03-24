#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from pyjsdl.pyjsarray import BitSet
from pyjsdl.color import Color
from pyjsdl.pylib import int
# __pragma__ ('skip')
import sys

if sys.version_info < (3,):
    from pyjsdl.util import _range as range
# __pragma__ ('noskip')

__docformat__ = 'restructuredtext'


def from_surface(surface, threshold=127):
    """
    **pyjsdl.mask.from_surface**
    
    Return Mask derived from surface using alpha transparency.
    Optional argument to set alpha threshold.
    """
    mask = Mask((surface.width, surface.height))
    if not mask.bit:
        return None
    imagedata = surface.getImageData(0, 0, surface.width, surface.height)
    data = imagedata.data
    width, height = surface.width*4, surface.height
    for y in range(0, height):
        xpix = 0
        i = (y*width)+3
        bitset = mask.bit[y]
        bit = bitset._bit
        _data = bitset._data._data
        for x in range(0, width, 4):
            if data[i+x] > threshold:
                index = ~(~(xpix/bit))
                _data[index] = _data[index] | bitset._bitmask[xpix%bit]
            xpix += 1
    return mask


def from_threshold(surface, color, threshold=(0,0,0,255)):
    """
    **pyjsdl.mask.from_threshold**
    
    Return Mask from surface using a given color.
    Optional threshold argument to set color range and alpha threshold.
    """
    mask = Mask((surface.width, surface.height))
    if not mask.bit:
        return None
    imagedata = surface.getImageData(0, 0, surface.width, surface.height)
    data = imagedata.data
    if threshold == (0,0,0,255):
        color = Color(color)
        width, height = surface.width*4, surface.height
        for y in range(0, height):
            xpix = 0
            i = y*width
            bitset = mask.bit[y]
            bit = bitset._bit
            _data = bitset._data._data
            for x in range(0, width, 4):
                ix = i+x
                if (data[ix] == color.r and
                    data[ix+1] == color.g and
                    data[ix+2] == color.b and
                    data[ix+3] >= threshold[3]):
                    index = ~(~(xpix/bit))
                    _data[index] = _data[index] | bitset._bitmask[xpix%bit]
                xpix += 1
    else:
        color = Color(color)
        col = {}
        col['r1'] = color.r - threshold[0] - 1
        col['r2'] = color.r + threshold[0] + 1
        col['g1'] = color.g - threshold[1] - 1
        col['g2'] = color.g + threshold[1] + 1
        col['b1'] = color.b - threshold[2] - 1
        col['b2'] = color.b + threshold[2] + 1
        col['a'] = threshold[3] - 1
        width, height = surface.width*4, surface.height
        for y in range(0, height):
            xpix = 0
            i = y*width
            bitset = mask.bit[y]
            bit = bitset._bit
            _data = bitset._data._data
            for x in range(0, width, 4):
                ix = i+x
                if ((col['r1'] < data[ix] < col['r2']) and
                    (col['g1'] < data[ix+1] < col['g2']) and
                    (col['b1'] < data[ix+2] < col['b2']) and
                    (data[ix+3] > col['a'])):
                    index = ~(~(xpix/bit))
                    _data[index] = _data[index] | bitset._bitmask[xpix%bit]
                xpix += 1
    return mask


class Mask(object):
    """
    **pyjsdl.mask.Mask**
    
    * Mask.get_size
    * Mask.get_at
    * Mask.set_at
    * Mask.fill
    * Mask.clear
    * Mask.invert
    * Mask.count
    * Mask.overlap
    * Mask.toString
    """

    def __init__(self, size):
        """
        Return a Mask object.
        The size argument is (width, height) of the mask.
        The mask is represented by a list of Bitset.
        """
        self.width = int(size[0])
        self.height = int(size[1])
        self.bit = []
        for bitset in range(self.height):
            self.bit.append(BitSet(self.width))

    def __str__(self):
        return self.toString()

    def __repr__(self):
        return '{}({})'.format(self.__class__, repr(self.__dict__))

    def get_size(self):
        """
        Return width, height of mask.
        """
        return (self.width, self.height)

    def get_at(self, pos):
        """
        Return bit setting for given pos.
        """
        return self.bit[pos[1]].get(pos[0])

    def set_at(self, pos, value=1):
        """
        Set bit for given pos.
        Optional value to set bit, eith 1 or 0, defaults to 1.
        """
        self.bit[pos[1]].set(pos[0], value)
        return None

    def fill(self):
        """
        Fill mask.
        """
        for bitset in self.bit:
            bitset.fill()
        return None

    def clear(self):
        """
        Clear mask.
        """
        for bitset in self.bit:
            bitset.clear()
        return None

    def invert(self):
        """
        Invert bit value in mask.
        """
        for bitset in self.bit:
            bitset.flip(0,self.width)
        return None

    def count(self):
        """
        Return count of true bits in mask.
        """
        true_bits = 0
        for bitset in self.bit:
            true_bits += bitset.cardinality()
        return true_bits

    def overlap(self, mask, offset):
        """
        Return True if mask at offset position overlap with this mask.
        """
        if offset[0] > 0:
            x1 = offset[0]
            x2 = 0
        else:
            x1 = 0
            x2 = -offset[0]
        if offset[1] > 0:
            y1 = offset[1]
            y2 = 0
        else:
            y1 = 0
            y2 = -offset[1]
        w = min(self.width-x1, mask.width-x2)
        h = min(self.height-y1, mask.height-y2)
        if w > 0 and h > 0:
            for y in range(h):
                if self.bit[y1+y].get(x1, x1+w).intersects(
                              mask.bit[y2+y].get(x2, x2+w)):
                    return True
        return None

    def toString(self, bit=('1','0')):
        """
        Return string representation of mask.
        Optional bit argument specify bit character.
        """
        cbit = {True:bit[0], False:bit[1]}
        cbitset = []
        for bitset in self.bit:
            cbitset.append('\n')
            cbitset.extend([cbit[bitset.get(i)]
                            for i in range(self.width)])
        bitstr = ''.join(cbitset)
        return bitstr


def _overlap(mask1, mask2, offset):
    if offset[0] > 0:
        x1 = offset[0]
        x2 = 0
    else:
        x1 = 0
        x2 = -offset[0]
    if offset[1] > 0:
        y1 = offset[1]
        y2 = 0
    else:
        y1 = 0
        y2 = -offset[1]
    w = min(mask1.width-x1, mask2.width-x2)
    h = min(mask1.height-y1, mask2.height-y2)
    if w > 0 and h > 0:
        for y in range(h):
            bitset1 = mask1.bit[y1+y]
            bitset2 = mask2.bit[y2+y]
            _bitset1 = _bitset_get(bitset1, x1, x1+w)
            _bitset2 = _bitset_get(bitset2, x2, x2+w)
            intersect = _intersects(_bitset1, _bitset2)
            _bitsetPool_set(_bitset1)
            _bitsetPool_set(_bitset2)
            if intersect:
                return True
    return False


def _intersects(bitset1, bitset2):
    for dat in range(bitset1._data._data.length):
        data1 = bitset1._data._data
        data2 = bitset2._data._data
        intersect = data1[dat] & data2[dat]
        if intersect:
            return True
    return False


def _bitset_get(bitset, index, toIndex):
    data = bitset._data._data
    _bitset = _bitsetPool_get(toIndex-index)
    ix = 0
    if toIndex > bitset._width:
        toIndex = bitset._width
    for i in range(index, toIndex):
        _bitset_set(_bitset, ix,
            bool(data[int(i/bitset._bit)] & bitset._bitmask[i%bitset._bit]))
        ix += 1
    return _bitset


def _bitset_set(bitset, index, value):
    data = bitset._data._data
    if value:
        data[int(index/bitset._bit)] = (
            data[int(index/bitset._bit)] | bitset._bitmask[index%bitset._bit])
    else:
        data[int(index/bitset._bit)] = (
            data[int(index/bitset._bit)] & ~(bitset._bitmask[index%bitset._bit]))


_bitsetPool = {}

def _bitsetPool_get(size):
    if size not in _bitsetPool:
        _bitsetPool[size] = []
    if len(_bitsetPool[size]) > 0:
        bitset = _bitsetPool[size].pop()
    else:
        bitset = BitSet(size)
    return bitset

def _bitsetPool_set(bitset):
    data = bitset._data._data
    for i in range(data.length):
        data[i] = 0
    _bitsetPool[bitset._width].append(bitset)

