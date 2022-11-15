# Implement a class ‹Array› which acts like a list, with the
# following differences:
#
#  • no ‹push›, ‹pop›, ‹remove› and similar ‘list-like’ methods –
#    only item access via indexing,
#  • the constructor takes a default value, which is used as the
#    initial value for cells that have not been explicitly set,
#  • all indices are always valid: both reading and writing an index
#    automatically resizes the underlying list (using the default
#    given above to fill in missing cells).
#
# The default value should be copied into new cells, so that arrays
# with mutable work reasonably. Use shallow copies.
from typing import List, Generic, TypeVar
from copy import copy
from collections import defaultdict

T = TypeVar('T')

class Array(Generic[T]):
    def __init__(self, ini: T) -> None:
        self.initial: T = ini
        self.data: dict[int, T] = defaultdict(lambda: copy(ini))

    def __setitem__(self, key: int, val: T) -> None:
        self.data[key] = val

    def __getitem__(self, key: int) -> T:
        return self.data[key]

def test_int() -> None:
    a = Array( 17 )
    a[ 1 ] = 7
    a[ 3 ] = 3
    assert a[ 0 ] == 17
    assert a[ 1 ] == 7
    assert a[ 2 ] == 17
    assert a[ 3 ] == 3
    assert a[ 4 ] == 17

def test_str() -> None:
    a = Array( '' )
    a[ 1 ] = 'foo'
    a[ 3 ] = 'bar'
    assert a[ 0 ] == ''
    assert a[ 1 ] == 'foo'
    assert a[ 2 ] == ''
    assert a[ 3 ] == 'bar'
    assert a[ 4 ] == ''

def test_list() -> None:
    a : Array[ List[ int ] ] = Array( [] )
    a[ 7 ].append( 3 )
    a[ 2 ].append( 7 )
    a[ 3 ] = [ 1, 2 ]

    assert a[ 0 ] == []
    assert a[ 1 ] == []
    assert a[ 2 ] == [ 7 ]
    assert a[ 3 ] == [ 1, 2 ]
    assert a[ 4 ] == []
    assert a[ 5 ] == []
    assert a[ 6 ] == []
    assert a[ 7 ] == [ 3 ]


if __name__ == '__main__':
    test_int()
    test_str()
    test_list()
