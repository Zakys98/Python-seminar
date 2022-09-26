# pragma mypy relaxed

from __future__ import annotations
from typing import TypeVar, Generic, Any

# You might be familiar with the «zipper» data structure, which is
# essentially a ‘linked list with a finger’. Let us consider
# traversal of binary trees instead of lists. Implement two methods,
# ‹rotate_left› and ‹rotate_right›, on a binary tree object.

# These methods shuffle the tree so that the left/right child of the
# current root becomes the new root. If rotating right, the old root
# becomes the left child of the new root, and the previous left
# child of the new root is attached as the right child of the old
# root. If rotating left, the opposite. Notably, these
# rearrangements preserve the in-order of the tree.

# Question: can we reach all nodes using just these two rotations?
# Can you think of an operation that, combined with the two
# rotations, would make the entire tree reachable? Can you think of
# a set of operations that make the entire tree reachable «and»
# preserve in-order? Learn more in S.1.

class Tree:
    def __init__( self, value ) -> None:
        self.left  : Optional[ Tree ] = None
        self.right : Optional[ Tree ] = None
        self.value = value

    def rotate_left( self ): pass
    def rotate_right( self ): pass


def test_basic() -> None:
    r = Tree( 7 )
    r.left  = Tree( 1 )
    r.right = Tree( 2 )

    r = r.rotate_left()
    assert r.left        is     None
    assert r.right       is not None
    assert r.right.right is not None

    assert r.right.value       == 7
    assert r.right.right.value == 2

    r = r.rotate_right()
    assert r.left  is not None
    assert r.right is not None
    assert r.value       == 7
    assert r.left.value  == 1
    assert r.right.value == 2

    r.right.left  = Tree( 5 )
    r.right.right = Tree( 6 )

    r = r.rotate_right()

    assert r.left       is not None
    assert r.right      is not None
    assert r.left.left  is not None
    assert r.left.right is not None

    assert r.value             == 2
    assert r.left.value        == 7
    assert r.right.value       == 6
    assert r.left.left.value   == 1
    assert r.left.right.value  == 5

    r = r.rotate_left()

    assert r.left        is not None
    assert r.right       is not None
    assert r.right.left  is not None
    assert r.right.right is not None

    assert r.value             == 7
    assert r.left.value        == 1
    assert r.right.value       == 2
    assert r.right.left.value  == 5
    assert r.right.right.value == 6


if __name__ == '__main__':
    test_basic()
