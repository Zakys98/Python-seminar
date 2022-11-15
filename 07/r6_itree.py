from __future__ import annotations
from typing import TypeVar, Generic, Optional, List

# Below, you will find an implementation of an in-order iterator for
# binary trees. Make sure it is correct and fix it if it isn't.

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

class TreeIter( Generic[ T ] ):

    def __init__( self, tree: Tree[ T ] ) -> None:
        self.n : Optional[ Tree[ T ] ] = tree

    def descend( self ) -> None:
        assert self.n is not None

        while self.n.left is not None:
            self.n = self.n.left

    def ascend( self ) -> None:
        assert self.n is not None

        while ( self.n.parent is not None and
                self.n == self.n.parent.right ):
            self.n = self.n.parent

        self.n = self.n.parent # coming from left

    def __iter__( self ) -> TreeIter[ T ]:
        assert self.n is not None
        i = TreeIter( self.n )
        i.descend()
        return i

    def __next__( self ) -> T:
        v = self.n.value

        if self.n.right is not None:
            self.n = self.n.right
            self.descend()
        else:
            self.ascend()

        return v
