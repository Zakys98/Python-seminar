from __future__ import annotations
from e1_geometry import *
from typing import Union, Tuple
from math import isclose

# We first import all the classes from ‹e1_geometry›, since we will
# want to use them.

# What we will do now is compute intersection points of a few object
# type combinations. We will start with lines, which are the
# simplest. You can find closed-form general solutions for all the
# problems in this exercise on the internet. Use them.

# Line-line intersect either returns a points, or a Line, if the two
# lines are coincident, or ‹None› if they are parallel.

def intersect_line_line( p: Line, q: Line ) \
        -> Union[ Point, Line, None ]:
    pass

# A variation. Re-use the line-line case.

def intersect_line_segment( p: Line, s: Segment ) \
        -> Union[ Point, Segment, None ]:
    pass

# Intersecting lines with circles is a little more tricky. Checking
# e.g. MathWorld sounds like a good idea. It might be helpful to
# translate both objects so that the circle is centered at the
# origin. The function returns a either ‹None› (the line and circle
# do not intersect), a single ‹Point› (the line is tangent to the
# circle) or a pair of points.

def intersect_line_circle( p: Line, c: Circle ) \
        -> Union[ None, Point, Tuple[ Point, Point ] ]:
    pass

# It's probably quite obvious that users won't like the above API.
# Let's make a single ‹intersect()› that will work on anything (that
# we know how to intersect, anyway). You can use ‹type( a )› or
# ‹isinstance( a, some_type )› to find the type of object ‹a›. You
# can compare types for equality, too: ‹type( a ) == Circle› will do
# what you think it should.

def intersect( a: Union[ Line, Segment, Circle ],
               b: Union[ Line, Segment, Circle ] ) \
        -> Union[ None, Point, Line, Segment,
                  Tuple[ Point, Point ] ]:
    pass


def test_line_line() -> None:

    l1 = Line( Point( 2, 1 ), Point( -3, 7 ) )
    l_i = intersect_line_line( l1, l1 )
    assert type( l_i ) == Line
    assert l_i == l1

    # Same as ‹l1›, but represented using different points.

    l2 = Line( Point( -0.5, 4 ), Point( 7, -5 ) )
    l_i = intersect_line_line( l1, l2 )
    assert type( l_i ) == Line
    assert line_eq( l_i, l1 )
    assert line_eq( l_i, l2 )

    l3 = Line( Point( 2, 2 ), Point( -1, 4 ) )
    for line in [ l1, l2 ]:
        p = intersect_line_line( line, l3 )
        assert type( p ) == Point
        assert isclose( p.x, 0.125 )
        assert isclose( p.y, 3.25 )

    # Parallel lines.

    l1 = Line( Point( 1, 1 ), Point( 3, 5 ) )
    l2 = Line( Point( 6, 4 ), Point( 7, 6 ) )
    assert intersect_line_line( l1, l2 ) is None

def test_line_segment() -> None:

    # Segment which lies on a line.

    l = Line( Point( -2, -3 ), Point( -1, -2 ) )
    s = Segment( Point( 3, 2 ), Point( 5, 4 ) )
    assert intersect_line_segment( l, s ) == s

    # Line which crosses a segment.

    s = Segment( Point( -1, -5 ), Point( -4, -2 ) )
    p = intersect_line_segment( l, s )
    assert type( p ) == Point
    assert isclose( p.x, -2.5 )
    assert isclose( p.y, -3.5 )

    # Line crosses the line in which a segment lies, but not the
    # segment itself.

    s = Segment( Point( -5, -1 ), Point( -4, -2 ) )
    assert intersect_line_segment( l, s ) is None

    # A line parallel to a segment.

    s = Segment( Point( 1, -2 ), Point( 2, -1 ) )
    assert intersect_line_segment( l, s ) is None

def test_line_circle() -> None:

    # A tangent line.

    l = Line( Point( 0, 5 ), Point( 3, 5 ) )
    c = Circle( Point( 3, 3 ), 2 )
    res = intersect_line_circle( l, c )
    assert type( res ) == Point
    assert isclose( res.x, 3 )
    assert isclose( res.y, 5 )

    # Line which crosses a circle.

    l = Line( Point( 0, 3 ), Point( 7, 3 ) )
    res = intersect_line_circle( l, c )
    assert type( res ) == tuple
    p1, p2 = res
    assert ( isclose( p1.x, 1 ) and isclose( p2.x, 5 ) ) or \
           ( isclose( p2.x, 1 ) and isclose( p1.x, 5 ) )
    assert isclose( p1.y, 3 )
    assert isclose( p2.y, 3 )

    # No intersection.

    l = Line( Point( 6, -1 ), Point( 8, 3 ) )
    assert intersect_line_circle( l, c ) is None

def test_intersect() -> None:

    # Circle with a line, swapped order.

    l = Line( Point( 1, 3 ), Point( -1, -3 ) )
    c = Circle( Point( 2, 0 ), 3 )
    res_ = intersect( c, l )
    assert type( res_ ) == tuple
    res = sorted( res_, key = lambda point: point.x )
    p1_exp = Point( -0.5348469228349533, -1.6045407685048603 )
    p2_exp = Point( 0.9348469228349539, 2.80454076850486 )

    assert isclose( res[0].x, p1_exp.x ) and isclose( res[0].y, p1_exp.y )
    assert isclose( res[1].x, p2_exp.x ) and isclose( res[1].y, p2_exp.y )

if __name__ == "__main__":
    test_line_line()
    test_line_segment()
    test_line_circle()
    test_intersect()
