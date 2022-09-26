# pragma mypy relaxed

from __future__ import annotations
from typing import TypeVar, Generic, Optional, Callable, Any

T = TypeVar( 'T' )
S = TypeVar( 'S' )

# Given the following representation of trees:

class Node( Generic[ T ] ):
    def __init__( self, val: T ) -> None:
        self.left  : Optional[ Node[ T ] ] = None
        self.right : Optional[ Node[ T ] ] = None
        self.val   : T = val

class Tree( Generic[ T ] ):
    def __init__( self ) -> None:
        self.root : Optional[ Node[ T ] ] = None

# Implement a bottom-up fold on binary trees, with the following
# arguments:
#
#  • a ternary callback ‹f›: the first argument will be the value of
#    the current node and the other two the folded values of the left
#    and right child, respectively,
#  • the binary tree ‹tree›,
#  • an ‘initial’ value which is used whenever a child is missing
#    (leaf nodes are folded using ‹f( leaf_val, initial, initial)›).

def fold( f, tree, initial ): pass

def test_sum() -> None:
    tree = ex_tree()
    assert fold( lambda x, a, b: x + a + b, tree, 0 ) == 23

def test_list() -> None:
    tree = ex_tree()
    init   : Any = []
    expect : Any = [ 5, [ 2, [ 9, [], [] ], [] ],
                        [ -4, [], [ 1, [ 7, [], [] ], [ 3, [], [] ] ] ] ]
    assert fold( lambda x, a, b: [ x, a, b ], tree, init ) == expect

def ex_tree() -> Tree[ int ]:
    tree : Tree[ int ] = Tree()
    n5 = Node(5)
    n2 = Node(2)
    n_4 = Node(-4)
    n1 = Node(1)
    n9 = Node(9)
    n7 = Node(7)
    n3 = Node(3)

    tree.root = n5
    n5.left = n2
    n5.right = n_4
    n2.left = n9
    n_4.right = n1
    n1.left = n7
    n1.right = n3
    return tree

if __name__ == "__main__":
    test_sum()
    test_list()
