from __future__ import annotations
from typing import Callable, TypeVar

# Write a function ‹each› that accepts a unary callback and a
# traversable data structure (one that is either iterable, or
# provides an ‹each› method). Arrange for ‹f› to be called once on
# each element.

def each( f, data ): pass

# Use ‹each› to implement:
#
#  • ‹each_len› – count the number of elements
#  • ‹each_sum› – count the sum of all the elements
#  • ‹each_avg› – compute the average of all elements
#  • ‹each_median› – likewise, but median instead of average
#                   (return the ⌊n/2⌋ element if there is no
#                    definite median, or None on an empty list)

def each_len( data ): pass
def each_sum( data ): pass
def each_avg( data ): pass
def each_median( data ): pass

def test_each_1() -> None:
    data = [ [ 1 ], [ 2 ], [ 3 ] ]
    each( lambda x : x.append( 1 ), data )
    assert data == [ [ 1, 1 ], [ 2, 1 ], [ 3, 1 ] ]

def test_each_2() -> None:
    class A:
        def __init__( self, x: int ) -> None:
            self.x = x
        def add( self, val: int ) -> None:
            self.x += val

    data = [ A( 4 ), A( 2 ), A( 3 ) ]
    each( lambda x: x.add( 4 ), data )
    assert [ a.x for a in data ] == [ 8, 6, 7 ]

T = TypeVar( 'T' )

def test_each_each() -> None:

    class Node:
        def __init__( self, val: int ) -> None:
            self.val  = val
            self.next : Optional[ Node ] = None

    class LinkedList:

        def __init__( self, node: Node ) -> None:
            self.head = node

        def each( self, f: Callable[ [ Node ], T ] ) -> None:
            node : Optional[ Node ] = self.head
            while node is not None:
                f( node )
                node = node.next

    def foo( node: Node ) -> None:
        node.val = 0

    lst = LinkedList( Node( 6 ) )
    n3 = Node( 3 )
    n_2 = Node( -2 )
    n4 = Node( 4 )
    n_1 = Node( -1 )
    n11 = Node( 11 )
    n18 = Node( 18 )

    lst.head.next = n18
    n18.next = n_1
    n_1.next = n4
    n4.next = n3
    n3.next = n_2
    n_2.next = n11

    each( foo, lst )

    node : Optional[ Node ] = lst.head
    count = 0
    while node is not None:
        assert node.val == 0
        node = node.next
        count += 1
    assert count == 7

def test_len() -> None:
    assert each_len( [ 3, 2, 3 ] ) == 3
    assert each_len( [] ) == 0
    assert each_len( [ "a", "abc", None, -2 ] )  == 4

def test_sum() -> None:
    from math import isclose
    assert each_sum( [ 2, 2, 0, -1, -5 ] ) == -2
    # assert isclose( each_sum( [ 3.9, 0.4, -2.1, -5 ] ), -2.8 )
    assert each_sum( [] ) == 0

def test_avg() -> None:
    from math import isclose
    assert isclose( each_avg( [ 1, 2, 3 ] ), 2 )
    # assert isclose( each_avg( [ 2.4, 5.7, 3.8, -9 ] ), 0.725 )

def test_median() -> None:
    assert each_median( [] ) == None
    assert each_median( [ 7, 6, -2, 0, 1 ] ) == 1
    assert each_median( [ 9, 9, 1, 2, 6, 9, -4, -12, 3, 4 ] ) == 3

if __name__ == "__main__":
    test_each_1()
    test_each_2()
    test_each_each()
    test_len()
    test_sum()
    test_avg()
    test_median()
