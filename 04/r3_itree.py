from __future__ import annotations
from typing import TypeVar, Generic, Optional, List

T = TypeVar( 'T' )

class Tree( Generic[ T ] ):
    def __init__( self, value: T,
                  left:  Optional[ Tree[ T ] ] = None,
                  right: Optional[ Tree[ T ] ] = None ) -> None:
        self.left  = left
        self.right = right
        self.value = value
        self.parent : Optional[ Tree[ T ] ] = None

        if left is not None:
            left.parent = self
        if right is not None:
            right.parent = self

# Write an in-order iterator for binary trees. Write it as a class
# with a ‹__next__› method.

class TreeIter: pass

def test_int_iter() -> None:
    t_1 = Tree( 7, Tree( 2 ), Tree( 3, Tree( 4 ), Tree( 5 ) ) )

    t_2 = Tree( 6, Tree(  4, Tree( 2, Tree( 1 ), Tree( 3 ) ),
                             Tree( 5 ) ),
                   Tree( 10, Tree( 8, Tree( 7 ), Tree( 9 ) ),
                              Tree( 11 ) ) )

    t_3 = Tree( 6, Tree( 4, Tree( 2, Tree( 1 ), Tree( 3 ) ),
                            Tree( 5 ) ),
                   Tree( 8, Tree( 7 ),
                             Tree( 10, Tree( 9 ), Tree( 11 ) ) ) )

    assert copy_iter( t_1 ) == [ 2, 7, 4, 3, 5 ]
    assert copy_iter( t_2 ) == [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ]
    assert copy_iter( t_3 ) == [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ]

def test_str_iter() -> None:
    t = Tree( 'x', Tree( 'y' ),
                   Tree( 'u', Tree( 'v' ), Tree( 'w' ) ) )

    assert copy_iter( t ) == [ 'y', 'x', 'v', 'u', 'w' ]


def copy_iter( tree: Tree[ T ] ) -> List[ T ]:
    out : List[ T ] = []
    for i in TreeIter( tree ):
        out.append( i )
    return out


if __name__ == '__main__':
    test_int_iter()
    test_str_iter()
