#Pyjsdl - Copyright (C) 2021 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from math import ceil as _ceil, floor as _floor, sqrt as _sqrt
from math import log as _log, sin as _sin, cos as _cos, pi as _pi
from random import random as _random, randint as _randint
from random import choice as _choice, shuffle as _shuffle


# __pragma__ ('skip')
class window:
    Uint8ClampedArray = Uint8Array = Uint16Array = Uint32Array = None
    Int8Array = Int16Array = Int32Array = None
    Float32Array = Float64Array = None

class Object:
    def getPrototypeOf(*args):
        return None
# __pragma__ ('noskip')


# __pragma__ ('noopov')
# __pragma__ ('noalias', 'isNaN')


def Uint8ClampedArray(*args):
    """
    Uint8ClampedArray TypedArray constructor.
    """
    return __new__(window.Uint8ClampedArray(*args))


def Int8Array(*args):
    """
    Int8Array TypedArray constructor.
    """
    return __new__(window.Int8Array(*args))


def Uint8Array(*args):
    """
    Uint8Array TypedArray constructor.
    """
    return __new__(window.Uint8Array(*args))


def Int16Array(*args):
    """
    Int16Array TypedArray constructor.
    """
    return __new__(window.Int16Array(*args))


def Uint16Array(*args):
    """
    Uint16Array TypedArray constructor.
    """
    return __new__(window.Uint16Array(*args))


def Int32Array(*args):
    """
    Int32Array TypedArray constructor.
    """
    return __new__(window.Int32Array(*args))


def Uint32Array(*args):
    """
    Uint32Array TypedArray constructor.
    """
    return __new__(window.Uint32Array(*args))


def Float32Array(*args):
    """
    Float32Array TypedArray constructor.
    """
    return __new__(window.Float32Array(*args))


def Float64Array(*args):
    """
    Float64Array TypedArray constructor.
    """
    return __new__(window.Float64Array(*args))


class Ndarray:

    _typedarray = {'uint8c':  window.Uint8ClampedArray,
                   'int8':    window.Int8Array,
                   'uint8':   window.Uint8Array,
                   'int16':   window.Int16Array,
                   'uint16':  window.Uint16Array,
                   'int32':   window.Int32Array,
                   'uint32':  window.Uint32Array,
                   'float32': window.Float32Array,
                   'float64': window.Float64Array}

    _dtypes = {'uint8c':'uint8c', 'x':'uint8c', 0:'uint8c',
               'int8':'int8', 'b':'int8', 4:'int8',
               'uint8':'uint8', 'B':'uint8', 1:'uint8',
               'int16':'int16', 'h':'int16', 5:'int16',
               'uint16':'uint16', 'H':'uint16', 2:'uint16',
               'int32':'int32', 'i':'int32', 6:'int32',
               'uint32':'uint32', 'I':'uint32', 3:'uint32',
               'float32':'float32', 'f':'float32', 7:'float32',
               'float64':'float64', 'd':'float64', 8:'float64'}

    _opts = {'precision':4, 'nanstr':'nan', 'infstr':'inf'}

    def __init__(self, dim, dtype='float64'):
        """
        Generate an N-dimensional array of TypedArray data.
        Argument can be size (int or tuple) or data (list or TypedArray).
        Optional argument dtype specifies TypedArray data type:
                'uint8c'    Uint8ClampedArray
                'int8'      Int8Array
                'uint8'     Uint8Array
                'int16'     Int16Array
                'uint16'    Uint16Array
                'int32'     Int32Array
                'uint32'    Uint32Array
                'float32'   Float32Array
                'float64'   Float64Array
        Operator and index functionality requires __pragma__ ('opov'). 
        """
        self._dtype = self._dtypes[dtype]
        typedarray = self._typedarray[self._dtype]
        if isinstance(dim, tuple):
            size = 1
            for i in dim:
                size *= i
            self._data = __new__(typedarray(size))
            self._shape = dim
            indices = []
            for i in self._shape:
                size /= i
                indices.append(size)
            self._indices = tuple(indices)
        elif isinstance(dim, int):
            self._data = __new__(typedarray(dim))
            self._shape = (dim,)
            self._indices = (self._shape[0],)
        elif isinstance(dim, list):
            if not (len(dim)>0 and isinstance(dim[0], list)):
                self._data = __new__(typedarray(dim))
                self._shape = (len(dim),)
                self._indices = (self._shape[0],)
            else:
                _dat = self._lflatten(dim)
                _dim = self._lshape(dim)
                self._data = __new__(typedarray(list(_dat)))
                self._shape = (len(self._data),)
                self.setshape(tuple(list(_dim)))
        else:
            self._data = dim
            self._shape = (dim.length,)
            self._indices = (self._shape[0],)

    def getshape(self):
        """
        Return array shape.
        """
        return self._shape

    def setshape(self, *dim):
        """
        Set shape of array.
        Argument is new shape.
        Raises TypeError if shape is not appropriate.
        """
        if isinstance(dim[0], tuple):
            dim = dim[0]
        size = 1
        for i in dim:
            size *= i
        array_size = 1
        for i in self._shape:
            array_size *= i
        if size != array_size:
            raise TypeError("array size cannot change")
        self._shape = dim
        indices = []
        for i in self._shape:
            size /= i
            indices.append(size)
        self._indices = tuple(indices)
        return None

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, val):
        self.setshape(val)

    def _lflatten(self, l):
        for el in l:
            if isinstance(el, list):
                yield from self._lflatten(el)
            else:
                yield el

    def _lshape(self, l):
        _l = l
        while isinstance(_l, list):
            yield len(_l)
            _l = _l[0]

    def __getitem__(self, index):
        if hasattr(index, '__iter__'):
            if not hasattr(index, '_dtype'):
                indexLn, shapeLn = len(index), len(self._shape)
                if indexLn == shapeLn:
                    return self._data[sum([index[i]*self._indices[i] for i in range(indexLn)])]
                else:
                    begin = sum([index[i]*self._indices[i] for i in range(indexLn)])
                    end = begin + self._indices[indexLn-1]
                    subarray = self._data.subarray(begin, end)
                    array = Ndarray(subarray, self._dtype)
                    array._shape = self._shape[indexLn:]
                    array._indices = self._indices[indexLn:]
                    return array
            else:
                true_value = sum(index._data)
                array = Ndarray(true_value, self._dtype)
                _i = 0
                for i, val in enumerate(index._data):
                    if val:
                        array._data[_i] = self._data[i]
                        _i += 1
                return array
        else:
            if len(self._shape) == 1:
                return self._data[index]
            else:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self._data.subarray(begin, end)
                array = Ndarray(subarray, self._dtype)
                array._shape = self._shape[1:]
                array._indices = self._indices[1:]
                return array

    def __setitem__(self, index, value):
        def unpack(obj, lst=None):
            if lst is None:
                lst = []
            for element in obj:
                if isinstance(element, (list,tuple)):
                    unpack(element, lst)
                else:
                    lst.append(element)
            return lst
        if hasattr(index, '__iter__'):
            if not hasattr(index, '_dtype'):
                indexLn, shapeLn = len(index), len(self._shape)
                if indexLn == shapeLn:
                    self._data[sum([index[i]*self._indices[i] for i in range(indexLn)])] = value
                else:
                    begin = sum([index[i]*self._indices[i] for i in range(indexLn)])
                    end = begin + self._indices[indexLn-1]
                    subarray = self._data.subarray(begin, end)
                    if isinstance(value, Ndarray):
                        value = value._data
                    elif isinstance(value[0], (list,tuple)):
                        value = unpack(value)
                    subarray.set(value)
            else:
                if not hasattr(value, '__iter__'):
                    for i, val in enumerate(index._data):
                        if val:
                            self._data[i] = value
                else:
                    _i = 0
                    for i, val in enumerate(index._data):
                        if val:
                            self._data[i] = value._data[_i]
                            _i += 1
        else:
            if len(self._shape) == 1:
                self._data[index] = value
            else:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self._data.subarray(begin, end)
                if isinstance(value, Ndarray):
                    value = value._data
                elif isinstance(value[0], (list,tuple)):
                    value = unpack(value)
                subarray.set(value)
        return None

    def __getslice__(self, lower, upper):
        subarray = self._data.subarray(lower, upper)
        return Ndarray(subarray, self._dtype)

    def __setslice__(self, lower, upper, data):
        subarray = self._data.subarray(lower, upper)
        subarray.set(data)
        return None

    def __iter__(self):
        if len(self._shape) > 1:
            index = 0
            while index < self._shape[0]:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self._data.subarray(begin, end)
                array = Ndarray(subarray, self._dtype)
                array._shape = self._shape[1:]
                array._indices = self._indices[1:]
                yield array
                index += 1
        else:
            index = 0
            while index < self._shape[0]:
                yield self._data[index]
                index += 1

    def _array_dim(self):
        if 'int' in self._dtype:
            vmax = len(str(max(self._data)))
            vmin = len(str(min(self._data)))
            vlen = vmax if (vmax>vmin) else vmin
        else:
            s = '{}.' + ('0' * Ndarray._opts['precision'])    # __:opov
            vlen = max(len(s.format(int(round(v,Ndarray._opts['precision']))))
                       for v in self._data if Number.isFinite(v))
        return vlen

    def _array_str(self, array, vlen, vstr):
        if len(array._shape) == 1:
            s = []
            if 'int' in self._dtype:
                for val in array:
                    sv = '{}'.format(val)
                    sv = '{}{}'.format((vlen-len(sv))*' ', sv)    # __:opov
                    s.append(sv)
            else:
                for val in array:
                    if Number.isFinite(val):
                        sv = '{}'.format(round(val,Ndarray._opts['precision']))
                        if '.' not in sv:
                            sv += '.'
                        sv += (Ndarray._opts['precision']-len(sv.split('.')[1]))*'0'    # __:opov
                    else:
                        if Number.isNaN(val):
                            sv = '{}'.format(Ndarray._opts['nanstr'])
                        elif val == Number.POSITIVE_INFINITY:
                            sv = '{}'.format(Ndarray._opts['infstr'])
                        elif val == Number.NEGATIVE_INFINITY:
                            sv = '-{}'.format(Ndarray._opts['infstr'])
                        else:
                            sv = '{}'.format(val)
                    sv = '{}{}'.format((vlen-len(sv))*' ', sv)    # __:opov
                    s.append(sv)
            vstr.append('[{}]'.format(' '.join(s)))
        else:
            for i, a in enumerate(array):
                if i == 0:
                    vstr.append('[')
                else:
                    vstr.append(' '*(len(self._shape)-len(a._shape)))    # __:opov
                self._array_str(a, vlen, vstr)
                if i < len(array)-1:
                    vstr.append('\n')
                else:
                    # __pragma__ ('opov')
                    if vstr[-1] == ']\n':
                        vstr[-1] = ']'
                    # __pragma__ ('noopov')
                    if array._shape != self._shape:
                        vstr.append(']\n')
                    else:
                        vstr.append(']')
        return vstr

    def __str__(self):
        vlen = self._array_dim()
        vstr = self._array_str(self, vlen, [])
        return ''.join(vstr)

    def __repr__(self):
        s = str(self.tolist())
        sl = len(self._shape)
        for d in range(1, sl):
            s = s.replace(' '+'['*d, '\n'+' '*(sl+6-d)+'['*d)    # __:opov
        return 'array({}, dtype={})'.format(s, self._dtype)

    def __len__(self):
        return self._shape[0]

    def __lt__(self, other):
        ndarray = Ndarray(len(self._data), 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] < other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] < other_data[i]
        return ndarray

    def __le__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] <= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] <= other_data[i]
        return ndarray
    
    def __eq__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] == other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] == other_data[i]
        return ndarray
    
    def __ne__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] != other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] != other_data[i]
        return ndarray
    
    def __gt__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] > other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] > other_data[i]
        return ndarray

    def __ge__(self, other):
        ndarray = Ndarray(self._shape, 'uint8')
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] >= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] >= other_data[i]
        return ndarray

    def __add__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] + other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] + other_data[i]
        return ndarray

    def __sub__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] - other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] - other_data[i]
        return ndarray

    def __mul__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] * other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] * other_data[i]
        return ndarray

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] / other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] / other_data[i]
        return ndarray

    def __floordiv__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = _floor(data[i] / other)
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = _floor(data[i] / other_data[i])
        return ndarray

    def __divmod__(self, other):
        return self.__floordiv__(other), self.__mod__(other)

    def __mod__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] % other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] % other_data[i]
        return ndarray

    def __pow__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] ** other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] ** other_data[i]
        return ndarray

    def __neg__(self):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        for i in range(len(data)):
            ndarray_data[i] = -data[i]
        return ndarray

    def __pos__(self):
        ndarray = self.copy()
        return ndarray

    def __abs__(self):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        for i in range(len(data)):
            if data[i] < 0:
                ndarray_data[i] = -data[i]
        return ndarray

    def __matmul__(self, other):
        _other = self._get_array(other)
        x_dim = len(self._shape)
        y_dim = len(_other._shape)
        if x_dim != y_dim:
            raise ValueError('incompatible array shapes for matmul')
        if x_dim == 1:
            if self._shape[0] == _other._shape[0]:
                data = self._data
                other_data = _other._data
                result = 0
                for i in range(len(data)):
                    result += (data[i] * other_data[i])
                return result
            else:
                raise ValueError('incompatible array shapes for matmul')
        xshape = self._shape[-2:]
        yshape = _other._shape[-2:]
        if xshape[1] == yshape[0]:
            m = xshape[1]
            n = xshape[0]
            p = yshape[1]
            d = self._shape[:-2]
            d_len = 1
            for v in d:
                d_len*=v
        else:
            raise ValueError('incompatible array shapes for matmul')
        _data = __new__(self._typedarray[self._dtype](d_len*n*p))
        array = Ndarray(_data, self._dtype)
        # __pragma__ ('opov')
        array.setshape(tuple(d+(n,p)))
        if x_dim == 2:
            arrays = [(self, _other, array)]
        elif x_dim == 3:
            arrays = [(self[i], _other[i], array[i])
              for i in range(d[0])]
        elif x_dim == 4:
            arrays = [(self[i,j], _other[i,j], array[i,j])
              for i,j in [(i,j) for i in range(d[0]) for j in range(d[1])]]
        elif x_dim == 5:
            arrays = [(self[i,j,k], _other[i,j,k], array[i,j,k])
              for i,j,k in [(i,j,k) for i in range(d[0]) for j in range(d[1]) for k in range(d[2])]]
        else:
            raise ValueError('incompatible array shapes for matmul')
        # __pragma__ ('noopov')
        for _x, _y, _array in arrays:
            _x_data = _x._data
            _y_data = _y._data
            _array_data = _array._data
            for i in range(n):
                for j in range(p):
                    result = 0
                    for k in range(m):
                        result += (_x_data[i*m+k] * _y_data[k*p+j])
                    _array_data[i*p+j] = result
        return array

    def __iadd__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] += other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] += other_data[i]
        return self

    def __isub__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] -= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] -= other_data[i]
        return self

    def __imul__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] *= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] *= other_data[i]
        return self

    def __idiv__(self, other):
        return self.__itruediv__(other)

    def __itruediv__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] /= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] /= other_data[i]
        return self

    def __ifloordiv__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = _floor(data[i] / other)
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = _floor(data[i] / other_data[i])
        return self

    def __imod__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] %= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] %= other_data[i]
        return self

    def __ipow__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] **= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] **= other_data[i]
        return self

    def __lshift__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] << other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] << other_data[i]
        return ndarray

    def __rshift__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] >> other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] >> other_data[i]
        return ndarray

    def __and__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] & other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] & other_data[i]
        return ndarray

    def __or__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] | other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] | other_data[i]
        return ndarray

    def __xor__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] ^ other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] ^ other_data[i]
        return ndarray

    def __ilshift__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] << other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] << other_data[i]
        return self

    def __irshift__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] >> other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] >> other_data[i]
        return self

    def __iand__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] & other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] & other_data[i]
        return self

    def __ior__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] | other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] | other_data[i]
        return self

    def __ixor__(self, other):
        data = self._data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] ^ other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] ^ other_data[i]
        return self

    def __invert__(self):
        ndarray = self.empty()
        ndarray_data = ndarray._data
        data = self._data
        for i in range(len(data)):
            ndarray_data[i] = ~data[i]
        return ndarray

    def _get_data(self, other):
        if not isinstance(other, Ndarray):
            if isinstance(other, list):
                other = Ndarray(other, self._dtype)
            else:
                other = Ndarray(list(other), self._dtype)
        # __pragma__ ('opov')
        if self._shape != other._shape:
            raise TypeError("array shapes are not compatible")
        # __pragma__ ('noopov')
        return other._data

    def _get_array(self, other):
        if not isinstance(other, Ndarray):
            if isinstance(other, list):
                other = Ndarray(other, self._dtype)
            else:
                other = Ndarray(list(other), self._dtype)
        return other

    def matmul(self, other):
        """
        Return matrix multiplied array.
        """
        return self.__matmul__(other)

    # __pragma__ ('kwargs')
    def max(self, axis=None):
        """
        Return maximum of array or of given axis.
        """
        if axis is None:
            return max(self._data)
        if axis > len(self._shape)-1:
            raise IndexError('axis out of bound')
        shape = tuple([i for index, i in enumerate(self._shape)
                       if index != axis])
        result = Ndarray(shape, self._dtype)
        result.fill(min(self._data))
        return self._max(self, axis, 0, self._shape, 0, result)
    # __pragma__ ('nokwargs')

    def _max(self, array, axis, curr_axis, shape, dim, result):
        if curr_axis == axis:
            if axis != len(shape)-1:
                res_dat = result._data
                for i in range(len(array)):
                    arr_dat = array[i]._data    # __:opov
                    for j in range(result._data.length):
                        if res_dat[j] < arr_dat[j]:
                            res_dat[j] = arr_dat[j]
            else:
                res_dat = result._data
                arr_dat = array._data
                for i in range(len(array)):
                    if res_dat[dim] < arr_dat[i]:
                        res_dat[dim] = arr_dat[i]
        elif curr_axis < len(shape):
            if len(result._shape) > 1:
                for dim in range(shape[curr_axis]):
                    self._max(array[dim], axis, curr_axis+1, shape, dim, result[dim])    # __:opov
            else:
                for dim in range(shape[curr_axis]):
                    self._max(array[dim], axis, curr_axis+1, shape, dim, result)    # __:opov
        return result

    # __pragma__ ('kwargs')
    def min(self, axis=None):
        """
        Return minimum of array or of given axis.
        """
        if axis is None:
            return min(self._data)
        if axis > len(self._shape)-1:
            raise IndexError('axis out of bound')
        shape = tuple([i for index, i in enumerate(self._shape)
                       if index != axis])
        result = Ndarray(shape, self._dtype)
        result.fill(max(self._data))
        return self._min(self, axis, 0, self._shape, 0, result)
    # __pragma__ ('nokwargs')

    def _min(self, array, axis, curr_axis, shape, dim, result):
        if curr_axis == axis:
            if axis != len(shape)-1:
                res_dat = result._data
                for i in range(len(array)):
                    arr_dat = array[i]._data    # __:opov
                    for j in range(result._data.length):
                        if res_dat[j] > arr_dat[j]:
                            res_dat[j] = arr_dat[j]
            else:
                res_dat = result._data
                arr_dat = array._data
                for i in range(len(array)):
                    if res_dat[dim] > arr_dat[i]:
                        res_dat[dim] = arr_dat[i]
        elif curr_axis < len(shape):
            if len(result._shape) > 1:
                for dim in range(shape[curr_axis]):
                    self._min(array[dim], axis, curr_axis+1, shape, dim, result[dim])    # __:opov
            else:
                for dim in range(shape[curr_axis]):
                    self._min(array[dim], axis, curr_axis+1, shape, dim, result)    # __:opov
        return result

    # __pragma__ ('kwargs')
    def sum(self, axis=None):
        """
        Return sum of array or of given axis.
        """
        if axis is None:
            return sum(self._data)
        if axis > len(self._shape)-1:
            raise IndexError('axis out of bound')
        shape = tuple([i for index, i in enumerate(self._shape)
                       if index != axis])
        result = Ndarray(shape, self._dtype)
        return self._sum(self, axis, 0, self._shape, 0, result)
    # __pragma__ ('nokwargs')

    def _sum(self, array, axis, curr_axis, shape, dim, result):
        if curr_axis == axis:
            if axis != len(shape)-1:
                res_dat = result._data
                for i in range(len(array)):
                    arr_dat = array[i]._data    # __:opov
                    for j in range(result._data.length):
                        res_dat[j] += arr_dat[j]
            else:
                res_dat = result._data
                arr_dat = array._data
                for i in range(len(array)):
                    res_dat[dim] += arr_dat[i]
        elif curr_axis < len(shape):
            if len(result._shape) > 1:
                for dim in range(shape[curr_axis]):
                    self._sum(array[dim], axis, curr_axis+1, shape, dim, result[dim])    # __:opov
            else:
                for dim in range(shape[curr_axis]):
                    self._sum(array[dim], axis, curr_axis+1, shape, dim, result)    # __:opov
        return result

    # __pragma__ ('kwargs')
    def mean(self, axis=None):
        """
        Return mean of array or of given axis.
        """
        if axis is None:
            return sum(self._data) / self._data.length
        if axis > len(self._shape)-1:
            raise IndexError('axis out of bound')
        shape = tuple([i for index, i in enumerate(self._shape)
                       if index != axis])
        result = Ndarray(shape, 'float64')
        return self._mean(self, axis, 0, self._shape, 0, result)
    # __pragma__ ('nokwargs')

    def _mean(self, array, axis, curr_axis, shape, dim, result):
        if curr_axis == axis:
            if axis != len(shape)-1:
                res = result._data
                arr_len = len(array)
                for i in range(arr_len):
                    arr = array[i]._data    # __:opov
                    for j in range(result._data.length):
                        res[j] += arr[j]
                for j in range(result._data.length):
                    res[j] /= arr_len
            else:
                res = result._data
                arr = array._data
                arr_len = len(array)
                for i in range(arr_len):
                    res[dim] += arr[i]
                res[dim] /= arr_len
        elif curr_axis < len(shape):
            if len(result._shape) > 1:
                for dim in range(shape[curr_axis]):
                    self._mean(array[dim], axis, curr_axis+1, shape, dim, result[dim])    # __:opov
            else:
                for dim in range(shape[curr_axis]):
                    self._mean(array[dim], axis, curr_axis+1, shape, dim, result)    # __:opov
        return result

    # __pragma__ ('kwargs')
    def var(self, axis=None):
        """
        Return variance of array or of given axis.
        """
        if axis is None:
            mean = sum(self._data) / self._data.length
            return sum((val-mean)**2 for val in self._data) / self._data.length
        mean = self.mean(axis)
        shape = tuple([i for index, i in enumerate(self._shape)
                       if index != axis])
        result = Ndarray(shape, 'float64')
        return self._var(self, axis, 0, self._shape, 0, mean, result)
    # __pragma__ ('nokwargs')

    def _var(self, array, axis, curr_axis, shape, dim, mean, result):
        if curr_axis == axis:
            if axis != len(shape)-1:
                mean_dat = mean._data
                res_dat = result._data
                arr_len = len(array)
                for i in range(arr_len):
                    arr_dat = array[i]._data    # __:opov
                    for j in range(result._data.length):
                        res_dat[j] += (arr_dat[j]-mean_dat[j])**2
                for j in range(result._data.length):
                    res_dat[j] /= arr_len
            else:
                mean_dat = mean._data
                arr_dat = array._data
                res_dat = result._data
                arr_len = len(array)
                for i in range(arr_len):
                    res_dat[dim] += (arr_dat[i]-mean_dat[dim])**2
                res_dat[dim] /= arr_len
        elif curr_axis < len(shape):
            if len(result._shape) > 1:
                for dim in range(shape[curr_axis]):
                    self._var(array[dim], axis, curr_axis+1, shape, dim, mean[dim], result[dim])    # __:opov
            else:
                for dim in range(shape[curr_axis]):
                    self._var(array[dim], axis, curr_axis+1, shape, dim, mean, result)    # __:opov
        return result

    # __pragma__ ('kwargs')
    def std(self, axis=None):
        """
        Return standard deviation of array or of given axis.
        """
        if axis is None:
            mean = sum(self._data) / self._data.length
            return (sum((val-mean)**2 for val in self._data)
                    / self._data.length)**0.5
        result = self.var(axis)
        res_dat = result._data
        for i in range(result._data.length):
            res_dat[i] **= 0.5
        return result
    # __pragma__ ('nokwargs')

    def reshape(self, dim):
        """
        Return view of array with new shape.
        Argument is new shape.
        Raises TypeError if shape is not appropriate.
        """
        size = 1
        for i in dim:
            size *= i
        array_size = 1
        for i in self._shape:
            array_size *= i
        if size != array_size:
            raise TypeError("array size cannot change")
        subarray = self._data.subarray(0)
        array = Ndarray(subarray, self._dtype)
        array._shape = dim
        indices = []
        for i in array._shape:
            size /= i
            indices.append(size)
        array._indices = tuple(indices)
        return array

    def set(self, data):
        """
        Set array elements.
        Data argument can be a 1d/2d array or number used to set Ndarray elements, data used repetitively if consists of fewer elements than Ndarray.
        """
        if isinstance(data, (list,tuple)):
            if isinstance(data[0], (list,tuple)):
                _data = [value for dat in data for value in dat]
            else:
                _data = data
            dataLn = len(_data)
        elif isinstance(data, Ndarray):
            _data = data._data
            dataLn = _data.length
        elif istypedarray(data):
            _data = data
            dataLn = data.length
        else:
            for index in range(self._data.length):
                self._data[index] = data
            return None
        if dataLn == self._data.length:
            for index in range(self._data.length):
                self._data[index] = _data[index]
        else:
            for index in range(self._data.length):
                self._data[index] = _data[index%dataLn]
        return None

    def fill(self, value):
        """
        Set array elements to value argument.
        """
        for index in range(self._data.length):
            self._data[index] = value
        return None

    def copy(self):
        """
        Return copy of array.
        """
        array = __new__(self._typedarray[self._dtype](self._data))
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def empty(self):
        """
        Return empty copy of array.
        """
        ndarray = Ndarray(len(self._data), self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def astype(self, dtype):
        """
        Return copy of array.
        Argument dtype is TypedArray data type.
        """
        array = __new__(self._typedarray[self._dtypes[dtype]](self._data))
        ndarray = Ndarray(array, dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def view(self):
        """
        Return view of array.
        """
        subarray = self._data.subarray(0)
        array = Ndarray(subarray, self._dtype)
        array._shape = self._shape
        array._indices = self._indices
        return array

    def swapaxes(self, axis1, axis2):
        """
        Swap axes of array.
        Arguments are the axis to swap.
        Return view of array with axes changed.
        """
        subarray = self._data.subarray(0)
        array = Ndarray(subarray, self._dtype)
        shape = list(self._shape)
        shape[axis1], shape[axis2] = shape[axis2], shape[axis1]
        array.setshape(tuple(shape))
        return array

    def tolist(self):
        """
        Return array as a list.
        """
        def to_list(array, l):
            _array = array[0]    # __:opov
            if hasattr(_array, '__iter__'):
                if len(l) == 0:
                    _l = l
                else:
                    l = [l]
                    _l = l[0]
                for i, a in enumerate(array):
                    _l.append([])
                    to_list(a, _l[i])
            else:
                l.extend([v for v in array])
            return l
        return to_list(self, [])

    def getArray(self):
        """
        Return JavaScript TypedArray.
        """
        return self._data


ndarray = Ndarray
array = Ndarray


class NP:

    def __init__(self):
        self.uint8c = 'uint8c'
        self.int8 = 'int8'
        self.uint8 = 'uint8'
        self.int16 = 'int16'
        self.uint16 = 'uint16'
        self.int32 = 'int32'
        self.uint32 = 'uint32'
        self.float32 = 'float32'
        self.float64 = 'float64'
        self.random = None

    def array(self, obj, dtype=None):
        """
        Return Ndarray from an obj iterable. If optional dtype is not provided,
        an an appropriate array will be inferred.
        """
        if dtype is None:
            dtype = self._get_dtype(obj)
        return Ndarray(obj, dtype)

    def zeros(self, shape, dtype='float64'):
        """
        Return Ndarray of shape and optional dtype with zeroed values.
        """
        return Ndarray(shape, dtype)

    def ones(self, shape, dtype='float64'):
        """
        Return Ndarray of shape and optional dtype with one values.
        """
        array = Ndarray(shape, dtype)
        array.set(1)
        return array

    # __pragma__ ('kwargs')
    def arange(self, start=0, stop=None, step=None, dtype=None):
        """
        Return Ndarray in range start to stop in step interval. If optional
        dtype is not provided, an an appropriate array will be inferred.
        """
        if stop is None:
            stop = start
            start = 0
        if step is None:
            step = 1
        array = range(start, stop, step)
        if dtype is None:
            dtype = self._get_dtype(array)
        return Ndarray(array, dtype)
    # __pragma__ ('nokwargs')

    def swapaxes(self, array, axis1, axis2):
        """
        Return array with axes swapped.
        """
        return array.swapaxes(axis1, axis2)

    def append(self, array, values):
        """
        Return Ndarray set with array extended with values.
        """
        if isinstance(values[0], (list,tuple)):
            values = [value for dat in values for value in dat]
        newarray = Ndarray(len(array)+len(values), array._dtype)
        newarray._data.set(array._data)
        newarray._data.set(values, len(array))
        return newarray

    # __pragma__ ('kwargs')
    def set_printoptions(self, precision=None, nanstr=None, infstr=None):
        """
        Set array print options.
        """
        if precision is not None:
            Ndarray._opts['precision'] = int(precision)
        if nanstr is not None:
            Ndarray._opts['nanstr'] = str(nanstr)
        if infstr is not None:
            Ndarray._opts['infstr'] = str(infstr)
    # __pragma__ ('nokwargs')

    def get_printoptions(self):
        """
        Get array print options.
        """
        return dict(Ndarray._opts)

    def _lflatten(self, obj):
        for el in obj:
            if hasattr(el, '__iter__'):
                yield from self._lflatten(el)
            else:
                yield el

    def _get_dtype(self, obj):
        dtype = 'int32'
        for value in self._lflatten(obj):
            if not (Number.isFinite(value) and
                    Number.isInteger(value)):
                if typeof(value) != 'boolean':
                    dtype = 'float64'
                    break
        return dtype


np = NP()


class Random:

    def __init__(self):
        self._gauss_next = None
        self._pi2 = _pi * 2

    def normal(self, mu, sigma, size=None):
        """
        Sample from gaussian distribution of mean mu and standard deviation sigma.
        Return as an array defined by size or a single value if None.
        """
        if size is None:
            return self._gauss(mu, sigma)
        array = Ndarray(size, 'float64')
        data = array._data
        gauss = self._gauss
        for i in range(data.length):
            data[i] = gauss(mu, sigma)
        return array

    def _gauss(self, mu, sigma):
        z = self._gauss_next
        self._gauss_next = None
        if z is None:
            x2pi = _random() * self._pi2
            g2rad = _sqrt(-2.0 * _log(1.0 - _random()))
            z = _cos(x2pi) * g2rad
            self._gauss_next = _sin(x2pi) * g2rad
        return mu + z * sigma

    def random(self, size=None):
        """
        Sample from random values between 0.0 and 1.0.
        Return as an array defined by size or a single value if None.
        """
        if size is None:
            return _random()
        array = Ndarray(size, 'float64')
        data = array._data
        for i in range(data.length):
            data[i] = _random()
        return array

    # __pragma__ ('kwargs')
    def randint(self, low, high=None, size=None, dtype='int32'):
        """
        Sample from random integers between low and high.
        If high is None, values will be 0 to low.
        Return as an array defined by size or a single value if None.
        """
        if high is None:
            a = 0
            b = low
        else:
            a = low
            b = high
        if size is None:
            return _randint(a, b)
        array = Ndarray(size, dtype)
        data = array._data
        for i in range(data.length):
            data[i] = _randint(a, b)
        return array
    # __pragma__ ('nokwargs')

    def choice(self, seq, size=None):
        """
        Sample from random values from seq iterable.
        If seq is an int, then values from range(seq).
        Return as an array defined by size or a single value if None.
        """
        if Number.isInteger(seq):
            _seq = range(seq)
        else:
            _seq = seq
        if size is None:
            return _choice(_seq)
        dtype = np._get_dtype(_seq)
        array = Ndarray(size, dtype)
        data = array._data
        for i in range(data.length):
            data[i] = _choice(_seq)
        return array

    def shuffle(self, array):
        """
        Shuffle first axis of array.
        """
        if not hasattr(array, '_shape'):
            _shuffle(array)
            return None
        if len(array._shape) == 1:
            _shuffle(array._data)
        else:
            for i in range(len(array)-1, 0, -1):
                j = _randint(0, i)
                if i == j:
                    continue
                # __pragma__ ('opov')
                temp = array[i].copy()
                array[i] = array[j]
                array[j] = temp
                # __pragma__ ('noopov')
        return None

    def permutation(self, seq):
        """
        Return array with permutated values from seq iterable.
        If seq is an int, then values from range(seq).
        """
        if Number.isInteger(seq):
            _seq = range(seq)
        else:
            _seq = seq
        if not hasattr(_seq, '_shape'):
            dtype = np._get_dtype(_seq)
            array = Ndarray(_seq, dtype)
        else:
            array = _seq.copy()
        self.shuffle(array)
        return array


np.random = Random()


class ImageData:

    def __init__(self, imagedata):
        """
        Provides an interface to canvas ImageData.
        The argument required is the ImageData instance to be accessed.
        """
        self._imagedata = imagedata
        self.data = Uint8ClampedArray(imagedata.data)
        self.width = imagedata.width
        self.height = imagedata.height

    def getImageData(self):
        """
        Return JavaScript ImageData instance.
        """
        return self._imagedata


class ImageMatrix(Ndarray):

    def __init__(self, imagedata):
        """
        Provides an interface to canvas ImageData as an Ndarray array.
        The argument required is the ImageData instance to be accessed.
        """
        self._imagedata = ImageData(imagedata)
        Ndarray.__init__(self, self._imagedata.data, 'uint8c')
        self.setshape(self._imagedata.height,self._imagedata.width,4)

    def getWidth(self):
        """
        Return ImageData width.
        """
        return self._imagedata.width

    def getHeight(self):
        """
        Return ImageData height.
        """
        return self._imagedata.height

    def getPixel(self, index):
        """
        Get pixel RGBA.
        The index argument references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return (self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2], self._imagedata.data[i+3])

    def setPixel(self, index, value):
        """
        Set pixel RGBA.
        The arguments index references the 2D array element and value is pixel RGBA.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2], self._imagedata.data[i+3] = value[0], value[1], value[2], value[3]
        return None

    def getPixelRGB(self, index):
        """
        Get pixel RGB.
        The index argument references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return (self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2])

    def setPixelRGB(self, index, value):
        """
        Set pixel RGB.
        The arguments index references the 2D array element and value is pixel RGB.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2] = value[0], value[1], value[2]
        return None

    def getPixelAlpha(self, index):
        """
        Get pixel alpha.
        The index argument references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return self._imagedata.data[i+3]

    def setPixelAlpha(self, index, value):
        """
        Set pixel alpha.
        The arguments index references the 2D array element and value is pixel alpha.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self._imagedata.data[i+3] = value
        return None

    def getPixelInteger(self, index):
        """
        Get pixel integer color.
        The index argument references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return self._imagedata.data[i]<<16 | self._imagedata.data[i+1]<<8 | self._imagedata.data[i+2] | self.imagedata.data[i+3]<<24

    def setPixelInteger(self, index, value):
        """
        Set pixel integer color.
        The arguments index references the 2D array element and value is pixel color.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self._imagedata.data[i], self._imagedata.data[i+1], self._imagedata.data[i+2], self._imagedata.data[i+3] = value>>16 & 0xff, value>>8 & 0xff, value & 0xff, value>>24 & 0xff
        return None

    def getImageData(self):
        """
        Return JavaScript ImageData instance.
        """
        return self._imagedata.getImageData()


class BitSet:

    """
    BitSet provides a bitset object to use in a Python-to-JavaScript application. The object stores data in a JavaScript Uint8Array 8-bit typedarray. BitSet16 and BitSet32 stores data in Uint16Array (16-bit) and Uint32Array (32-bit) typedarray. The BitSet will dynamically expand to hold the bits required, an optional width argument define number of bits the BitSet instance will initially hold.
    """

    _bit = 8
    _bitmask = None
    _typedarray = window.Uint8Array

    def __init__(self, width=None):
        if self._bitmask is None:
            self._bitmask = dict([(self._bit-i-1,1<<i) for i in range(self._bit-1,-1,-1)])
        if width:
            self._width = abs(width)
        else:
            self._width = self._bit
        self._data = __new__(self._typedarray(_ceil(self._width/(self._bit*1.0))))

    def __str__(self):
        v = {True:'1', False:'0'}
        s = []
        for i in range(self.size()):
            s.append(v[self.get(i)])
            if not (i+1)%64:
                s.append('\n')
        return ''.join(s)

    def __repr__(self):
        setBit = []
        for index in range(self._width):
            if self.get(index):
                setBit.append(str(index))
        return "{" + ", ".join(setBit) + "}"

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)

    def __len__(self):
        for index in list(range(self._width-1, -1, -1)):
            if self.get(index):
                break
        return index+1

    def __iter__(self):
        index = 0
        while index < self._width:
            yield self.get(index)
            index += 1

    def get(self, index, toIndex=None):
        """
        Get bit by index.
        Arguments include index of bit, and optional toIndex that return a slice as a BitSet.
        """
        if index > self._width-1:
            if not toIndex:
                return False
            else:
                size = toIndex-index
                if size > 0:
                    return self.__class__(size)
                else:
                    return None
        if toIndex is None:
            return bool(self._data[ int(index/self._bit) ] & self._bitmask[ index%self._bit ])
        else:
            size = toIndex-index
            if size > 0:
                bitset = self.__class__(size)
                ix = 0
                if toIndex > self._width:
                    toIndex = self._width
                for i in range(index, toIndex):
                    bitset.set(ix, bool(self._data[ int(i/self._bit) ] & self._bitmask[ i%self._bit ]))
                    ix += 1
                return bitset
            else:
                return None

    def set(self, index, value=1):
        """
        Set bit by index.
        Optional argument value is the bit state of 1(True) or 0(False). Default:1
        """
        if index > self._width-1:
            if value:
                self.resize(index+1)
            else:
                return
        if value:
            self._data[int(index/self._bit)] = self._data[ int(index/self._bit) ] | self._bitmask[ index%self._bit ]
        else:
            self._data[ int(index/self._bit) ] = self._data[ int(index/self._bit) ] & ~(self._bitmask[ index%self._bit ])
        return None

    def fill(self, index=None, toIndex=None):
        """
        Set the bit. If no argument provided, all bits are set.
        Optional argument index is bit index to set, and toIndex to set a range of bits.
        """
        if index is None and toIndex is None:
            for i in range(0, self._width):
                self.set(i, 1)
        else:
            if toIndex is None:
                self.set(index, 1)
            else:
                for i in range(index, toIndex):
                    self.set(i, 1)

    def clear(self, index=None, toIndex=None):
        """
        Clear the bit. If no argument provided, all bits are cleared.
        Optional argument index is bit index to clear, and toIndex to clear a range of bits.
        """
        if index is None:
            for i in range(len(self._data)):
                self._data[i] = 0
        else:
            if toIndex is None:
                self.set(index, 0)
            else:
                if index == 0 and toIndex == self._width:
                    for dat in range(len(self._data)):
                        self._data[dat] = 0
                else:
                    for i in range(index, toIndex):
                        self.set(i, 0)

    def flip(self, index, toIndex=None):
        """
        Flip the state of the bit.
        Argument index is the bit index to flip, and toIndex to flip a range of bits.
        """
        if toIndex is None:
            self.set(index, not self.get(index))
        else:
            if toIndex > self._width:
                self.resize(toIndex)
                toIndex = self._width
            if index == 0 and toIndex == self._width:
                for dat in range(len(self._data)):
                    self._data[dat] = ~self._data[dat]
            else:
                for i in range(index, toIndex):
                    self.set(i, not self.get(i))

    def cardinality(self):
        """
        Return the count of bit set.
        """
        count = 0
        for bit in range(self._width):
            if self.get(bit):
                count += 1
        return count

    def intersects(self, bitset):
        """
        Check if set bits in this BitSet are also set in the bitset argument.
        Return True if bitsets intersect, otherwise return False.
        """
        for dat in range(len(bitset._data)):
            intersect = bitset._data[dat] & self._data[dat]
            if intersect:
                return True
        return False

    def andSet(self, bitset):
        """
        BitSet and BitSet.
        """
        data = min(len(self._data), len(bitset._data))
        for dat in range(data):
            self._data[dat] = self._data[dat] & bitset._data[dat]

    def orSet(self, bitset):
        """
        BitSet or BitSet.
        """
        data = min(len(self._data), len(bitset._data))
        for dat in range(data):
            self._data[dat] = self._data[dat] | bitset._data[dat]

    def xorSet(self, bitset):
        """
        BitSet xor BitSet.
        """
        data = min(len(self._data), len(bitset._data))
        for dat in range(data):
            self._data[dat] = self._data[dat] ^ bitset._data[dat]

    def resize(self, width):
        """
        Resize the BitSet to width argument.
        """
        if width > self._width:
            self._width = width
            if self._width > len(self._data) * self._bit:
                array = __new__(self._typedarray(_ceil(self._width/(self._bit*1.0))))
                array.set(self._data)
                self._data = array
        elif width < self._width:
            if width < len(self):
                width = len(self)
            self._width = width
            if self._width <= len(self._data) * self._bit - self._bit:
                array = __new__(self._typedarray(_ceil(self._width/(self._bit*1.0))))
                array.set(self._data.subarray(0,_ceil(self._width/(self._bit*1.0))))
                self._data = array

    def size(self):
        """
        Return bits used by BitSet storage array.
        """
        return len(self._data) * self._bit

    def isEmpty(self):
        """
        Check whether any bit is set.
        Return True if none set, otherwise return False.
        """
        for data in self._data:
            if data:
                return False
        return True

    def clone(self):
        """
        Return a copy of the BitSet.
        """
        new_bitset = self.__class__(1)
        data = __new__(self._typedarray(self._data))
        new_bitset._data = data
        new_bitset._width = self._width
        return new_bitset


class BitSet16(BitSet):
    """
    BitSet using Uint16Array typedarray.
    """
    _bit = 16
    _bitmask = None
    _typedarray = window.Uint16Array

    def __init__(self, width=None):
        BitSet.__init__(self, width)


class BitSet32(BitSet):
    """
    BitSet using Uint32Array typedarray.
    """
    _bit = 32
    _bitmask = None
    _typedarray = window.Uint32Array

    def __init__(self, width=None):
        BitSet.__init__(self, width)


TypedArray = Object.getPrototypeOf(window.Int32Array)


def istypedarray(obj):
    """
    Check if obj is instanceof TypedArray.
    """
    return __pragma__('js', {}, 'obj instanceof TypedArray;')


def isinstanceof(obj, classobj):
    """
    Check if obj is instanceof classobj.
    """
    return __pragma__('js', {}, 'obj instanceof classobj;')

