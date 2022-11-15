# pragma mypy relaxed
from typing import Any

# Implement ‹Field›, a data descriptor which can be used to create
# classes that simply keep attributes (records, data classes),
# without having to type out the ‹__init__› method. The use case is
# similar to the ‹dataclass› decorator, though our approach will be
# much simpler (and also much more limited). When initializing an
# instance, make sure that the default value is copied, so that
# default lists and other mutable values are not accidentally shared
# between instances (see also standard module ‹copy›).

# Hint: The data descriptor can keep the value in the regular
# «instance» ‹__dict__›. Remember the diagram used by the default
# ‹__getattribute__› for lookup? You can even use the same name, so
# the value is not directly exposed.

# Bonus: If you like a challenge, extend ‹Field› so that it
# monkey-patches an ‹__init__› method into the ‘data’ class (i.e.
# the one with ‹Field›-typed attributes). This synthetic ‹__init__›
# should accept arguments in the declaration order of the fields and
# initialize them to non-default values, if provided (see tests
# below).

# PS: You can make ‹Field› a ‹Generic› and with some fiddling, make
# the types sort of work (may need a ‹cast› in ‹__get__›)

class Field: pass

class Data: # helper to silence ‹mypy› in the bonus part
    def __init__( self, *args: Any ) -> None: pass

def test_point() -> None:

    class Point( Data ):
        x = Field( 0 )
        y = Field( 0 )

    a = Point()
    assert ( a.x, a.y ) == ( 0, 0 )
    a.x = 7
    assert ( a.x, a.y ) == ( 7, 0 )
    a.y = 8
    assert ( a.x, a.y ) == ( 7, 8 )

    # if you implement the bonus, the following should work
    # b = Point( 7 )
    # assert ( b.x, b.y ) == ( 7, 0 )

def test_list() -> None:

    class Foo:
        l = Field( [ 1, 2 ] )

    x = Foo()
    # bonus: y = Foo( [] )
    z = Foo()

    x.l.append( 3 )
    # bonus: y.l.append( 1 )
    # bonus: assert y.l == [ 1 ]
    assert z.l == [ 1, 2 ]
    assert x.l == [ 1, 2, 3 ]

if __name__ == '__main__':
    test_point()
    test_list()
