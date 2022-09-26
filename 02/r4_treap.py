from __future__ import annotations
from typing import Generic, TypeVar, Tuple, Optional, Protocol, Any

class SupportsLessThan( Protocol ):
    def __lt__( self: T, other: T ) -> bool: ...
    def __le__( self: T, other: T ) -> bool: ...

T = TypeVar( 'T', bound = SupportsLessThan )

# A treap is a combination of a binary search tree and a binary
# heap. Of course, a single structure cannot be a heap and a search
# tree on the same value:
#
#  • a search tree demands the value in the right child to be
#    greater than the value in the root,
#  • a max heap demands that the value in both children be smaller
#    than the root (and hence specifically in the right child).
#
# Treap has therefore a «pair» of values in each node: a «key» and a
# «priority». The tree is arranged so that it is a binary search
# tree with respect to keys, and a binary heap with respect to
# priorities.
#
# The role of the heap part of the structure is to keep the tree
# approximately balanced. Your task is to implement the insertion
# algorithm which works as follows:
#
#  1. insert a new node into the tree, based on the key alone, as
#     with a standard binary search tree,
#  2. if this violates the heap property, rotate the newly inserted
#     node toward the root, until the heap property is restored.
#
# The deeper the node is inserted, the more likely it is to violate
# the heap property and the more likely it is to bubble up, causing
# the affected portion of the tree to be rebalanced by the
# rotations. Remember that rotations do not change the in-order of
# the tree and hence cannot disturb the search tree property.

class Treap( Generic[ T ] ):
    def __init__( self, key: T, priority: int ):
        self.left  : Optional[ Node ] = None
        self.right : Optional[ Node ] = None
        self.priority = priority
        self.key = key

    def insert( self, val, prio ): pass


def test_random() -> None:
    for i in range( 1, 50, 5 ):
        check_sized( i )


def check_heap( t: Treap[ T ] ) -> None:
    if t.left is not None:
        assert t.left.priority <= t.priority
        check_heap( t.left )

    if t.right is not None:
        assert t.right.priority <= t.priority
        check_heap( t.right )

def check_search( t: Optional[ Treap[ T ] ], bound: T ) \
        -> Tuple[ T, T ]:

    if t is None:
        return ( bound, bound )

    l_min, l_max = check_search( t.left, t.key )
    r_min, r_max = check_search( t.right, t.key )

    assert l_max <= t.key <= r_min, ( l_max, t.key, r_min )
    return ( l_min, r_max )

def make_treap( count: int ) -> Treap[ int ]:
    from random import randint

    items = [ ( randint( -1000, 1000 ),
                randint( -1000, 1000 ) ) for i in range( count ) ]

    t : Treap[ int ] = Treap( 0, 0 )
    for v, p in items:
        t = t.insert( v, p )
        check_search( t, 0 )
        check_heap( t )

    return t

def get_depth( t: Treap[ int ] ) -> int:
    d = 1

    if t.left is not None:
        d = max( d, get_depth( t.left ) + 1 )
    if t.right is not None:
        d = max( d, get_depth( t.right ) + 1 )

    return d

def check_sized( count: int ) -> None:
    from statistics import mean
    from math import log2

    depths : list[ int ] = []

    for i in range( 100 ):
        t = make_treap( count )
        depths.append( get_depth( t ) )

    assert mean( depths ) <= 2 * ( log2( count ) + 1 ), mean( depths )


if __name__ == '__main__':
    test_random()
