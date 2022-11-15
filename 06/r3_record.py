from typing import Any

# Re-do ‹p6_record›, including the bonus, but using a class
# decorator. That is, implement a decorator ‹record› which takes a
# ‹class› which only contains (class) variables and turn it into a
# proper class with instance attributes of the same names, and with
# appropriate default values.

def record( cls ): pass

class Data: # helper to silence ‹mypy›
    def __init__( self, *args: Any ) -> None: pass

def test_point() -> None:

    @record
    class Point( Data ):
        x = 0
        y = 0

    a = Point()
    assert ( a.x, a.y ) == ( 0, 0 )
    a.x = 7
    assert ( a.x, a.y ) == ( 7, 0 )
    a.y = 8
    assert ( a.x, a.y ) == ( 7, 8 )

    b = Point( 7 )
    assert ( b.x, b.y ) == ( 7, 0 )

def test_list() -> None:

    @record
    class Foo( Data ):
        l = [ 1, 2 ]

    x = Foo()
    y = Foo( [] )
    z = Foo()

    x.l.append( 3 )
    y.l.append( 1 )
    assert y.l == [ 1 ]
    assert z.l == [ 1, 2 ]
    assert x.l == [ 1, 2, 3 ]

if __name__ == '__main__':
    test_point()
    test_list()
