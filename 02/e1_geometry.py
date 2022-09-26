from __future__ import annotations
from typing import Tuple
from math import sqrt, acos
from math import isclose, pi

# In this exercise, you will implement basic types for planar
# analytic geometry. First define classes ‹Point› and ‹Vector›
# (tests expect the coordinate attributes to be named ‹x› and ‹y›):

class Point:
    def __init__( self, x: float, y: float ) -> None:
        self.x = x
        self.y = y
    def __sub__( self, other: Point ) -> Vector: # self - other
        pass # compute a vector
    def translated( self, vec: Vector ) -> Point:
        pass # compute a new point

class Vector:
    def __init__( self, x: float, y: float ) -> None:
        pass
    def length( self ) -> float:
        pass
    def dot( self, other: Vector ) -> float: # dot product
        pass
    def angle( self, other: Vector ) -> float: # in radians
        pass

# Let us define a line next. The vector returned by ‹get_direction›
# should have a unit length and point from ‹p1› to ‹p2›. The point
# returned by ‹get_point› should be ‹p1›.

class Line:
    def __init__( self, p1: Point, p2: Point ) -> None:
        pass
    def translated( self, vec: Vector ) -> Line:
        pass
    def get_point( self ) -> Point:
        pass
    def get_direction( self ) -> Vector:
        pass

# The ‹Segment› class is a finite version of the same. Also add a
# ‹get_direction› method, like above (or perhaps inherit it, your
# choice).

class Segment:
    def __init__( self, p1: Point, p2: Point ) -> None:
        pass
    def length( self ) -> float:
        pass
    def translated( self, vec: Vector ) -> Segment:
        pass
    def get_endpoints( self ) -> Tuple[ Point, Point ]:
        pass

# And finally a circle, using a center (a ‹Point›) and a radius (a
# ‹float›).

class Circle:
    def __init__( self, c: Point, r: float ) -> None:
        pass
    def center( self ) -> Point:
        pass
    def radius( self ) -> float:
        pass
    def translated( self, vec: Vector ) -> Circle:
        pass

# Equality comparison.

def point_eq( p1: Point, p2: Point ) -> bool:
    return isclose( p1.x, p2.x ) and \
           isclose( p1.y, p2.y )


def dir_eq( u: Vector, v: Vector ) -> bool:
    return isclose( u.angle( v ), 0 ) or \
           isclose( u.angle( v ), pi )

def line_eq( l1: Line, l2: Line ) -> bool:
    return dir_eq( l1.get_direction(), l2.get_direction() ) and \
           ( point_eq( l1.get_point(), l2.get_point() ) or
             dir_eq( l1.get_point() - l2.get_point(),
                 l1.get_direction() ) )

# Please make sure that your implementation is finished before
# consulting tests; specifically, try to avoid reverse-engineering
# the tests to find out how to write your program.

def test_point() -> None:
    p1 = Point( 1, -1 )
    p2 = Point( -7, 2 )

    assert isclose( Vector( -8, 3 ).angle( p2 - p1 ), 0 )
    assert isclose( Vector( 8, -3 ).angle( p1 - p2 ), 0 )

    # check that it did not affect original points
    assert point_eq( p1, Point( 1, -1 ) )
    assert point_eq( p2, Point( -7, 2 ) )

    v_0 = Vector( 0, 0 )
    assert point_eq( p1.translated( v_0 ), p1 )

    v_24 = Vector( 2, 4 )
    assert point_eq( p1.translated( v_24 ), Point( 3, 3 ) )
    assert point_eq( p1, Point( 1, -1 ) )  # remains unaffected

def test_vector() -> None:
    v1 = Vector( 2, 7 )
    v2 = Vector( -5, 0 )

    assert isclose( v1.length(), 7.28010988928 )
    assert isclose( v2.length(), 5 )

    assert isclose( v1.dot( v2 ), -10 )
    assert isclose( v1.angle( v2 ), 1.8490959858 )

def test_line() -> None:
    ln_1 = Line( Point( 2, -1 ), Point( 3, 4 ) )
    ln_2 = Line( Point( 0, -3 ), Point( 1, 2 ) )

    assert line_eq( ln_1, ln_1 )
    assert not line_eq( ln_1, ln_2 )

    # Translation.
    assert line_eq( ln_2, ln_1.translated( Vector( -2, -2 ) ) )
    assert line_eq( ln_1, ln_2.translated( Vector(  2,  2 ) ) )

    assert isclose( ln_1.get_direction()
                        .angle( ln_2.get_direction() ), 0 )

    # Parallel lines.
    l1 = Line( Point( 2, 0 ), Point( 3.5, -3 ) )
    l2 = Line( Point( 5, 2 ), Point( 7, -2 ) )
    assert not line_eq( l1, l2 )

    # l1 represented by different points
    l2 = Line( Point( 1.5, 1 ), Point( -1, 6 ) )
    assert line_eq( l1, l2 )

    # Intersecting lines.
    l2 = Line( Point( -3, 2 ), Point( 1, 9 ) )
    assert not line_eq( l1, l2 )

def test_segment() -> None:
    p1 = Point( 2, -1 )
    p2 = Point( 3, 4 )
    sg = Segment( p1, p2 )

    sg_t = sg.translated( Vector( -1, 3 ) )
    assert isclose( sg.length(), sg_t.length() )
    p1_t, p2_t = sg_t.get_endpoints()
    assert point_eq( p1_t, Point( 1, 2 ) )
    assert point_eq( p2_t, Point( 2, 7 ) )

def test_circle() -> None:
    c = Circle( Point( 1, -1 ), 4 )
    assert point_eq( c.center(), Point( 1, -1 ) )
    assert c.radius() == 4

    c_t = c.translated( Vector( -11, -3 ) )
    assert point_eq( c_t.center(), Point( -10, -4 ) )
    assert c_t.radius() == 4

    assert point_eq( c.center(), Point( 1, -1 ) )
    assert c.radius() == 4

# Since we will want to import this file into the next two
# exercises, we use the ‘current module is the main program’ trick
# below, which prevents the test code from running on import.

if __name__ == "__main__":
    test_point()
    test_vector()
    test_line()
    test_segment()
    test_circle()
