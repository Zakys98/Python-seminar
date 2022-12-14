from __future__ import annotations
from e1_geometry import * # as before
from typing import Union
from math import isclose

# In case there are no intersections, it makes sense to ask about
# distances of two objects. In this case, it also makes sense to
# include points, and we will start with those:

def distance_point_point( a: Point, b: Point ) -> float:
    pass

def distance_point_line( a: Point, l: Line ) -> float:
    pass

# If we already have the point-line distance, it's easy to also find
# the distance of two parallel lines:

def distance_line_line( p: Line, q: Line ) -> float:
    pass

# Circles vs points are rather easy, too:

def distance_point_circle( a: Point, c: Circle ) -> float:
    pass

# A similar idea works for circles and lines. Note that if they
# intersect, we set the distance to 0.

def distance_line_circle( l: Line, c: Circle ) -> float:
    pass

# And finally, let's do the friendly dispatch function:

def distance( a: Union[ Point, Line, Circle ],
              b: Union[ Point, Line, Circle ] ) -> float:
    pass

def test_point_point() -> None:
    p1 = Point( 9, 7 )
    p2 = Point( 3, 2 )
    assert isclose( distance_point_point( p1, p2 ), 7.81024967590665 )

def test_point_line() -> None:
    p = Point( 2 , -1 )
    l = Line( Point( 3, 6 ), Point( -4, -2 ) )
    assert isclose( distance_point_line( p, l ), 3.85695556037274 )

def test_line_line() -> None:
    l1 = Line( Point( -3, -6 ), Point( 3 , 1 ) )
    l2 = Line( Point( 3, 6 ), Point( -3 , -1 ) )
    assert isclose( distance_line_line( l1, l2 ), 3.25395686727984 )

def test_point_circle() -> None:

    # point outside circle
    p = Point( 0, -2 )
    c = Circle( Point( 2, 9 ), 2 )
    assert isclose( distance_point_circle( p, c ), 9.18033988749894 )

    # point within circle
    p = Point( 3, 2 )
    c = Circle( Point( 2, 5 ), 4 )
    assert isclose( distance_point_circle( p, c ), 0.83772233983162 )

    # point on circle
    p = Point( 0, 1 )
    c = Circle( Point( 0, 5 ), 4 )
    assert isclose( distance_point_circle( p, c ), 0 )

def test_line_circle() -> None:
    l = Line( Point( 1, -3 ), Point( 2, -1 ) )
    c = Circle( Point( 2, 7 ), 2 )
    assert isclose( distance_line_circle( l, c ), 1.57770876399966 )

def test_distance() -> None:
    p1 = Point( 9, 7 )
    p2 = Point( 3, 2 )
    assert isclose( distance( p1, p2 ), 7.81024967590665 )

    p = Point( 3, 2 )
    c = Circle( Point( 2, 5 ), 4 )
    assert isclose( distance( c, p ), 0.83772233983162 )

if __name__ == "__main__":
    test_point_point()
    test_point_line()
    test_line_line()
    test_point_circle()
    test_line_circle()
    test_distance()
