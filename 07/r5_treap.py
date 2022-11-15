from typing import Generic, TypeVar, Tuple, Optional, Protocol, Any

class SupportsLessThan( Protocol ):
    def __lt__( self, other: Any ) -> bool: ...
    def __le__( self, other: Any ) -> bool: ...

T = TypeVar( 'T', bound = SupportsLessThan )

# Remember treaps from week 2? A treap is a combination of a binary
# search tree and a binary heap: each node has a «key» (these form a
# search tree) and a randomized «priority» (these form a heap).
#
# The role of the heap part of the structure is to keep the tree
# approximately balanced. Your task is to decide whether the below
# treap implementation works correctly. Keep in mind that treaps
# are only «approximately» balanced: your tests need to take this
# into account.

class Treap( Generic[ T ] ):
    def __init__( self, key: T, priority: int ):
        self.left  : Optional[ Treap[ T ] ] = None
        self.right : Optional[ Treap[ T ] ] = None
        self.key = key
        self.priority = priority

    def rotate_left( self: Treap[ T ] ) -> Treap[ T ]:
        assert self.left is not None
        r = self.left
        detach = r.right
        r.right = self
        self.left = detach
        return r

    def rotate_right( self: Treap[ T ] ) -> Treap[ T ]:
        assert self.right is not None
        r = self.right
        detach = r.left
        r.left = self
        self.right = detach
        return r

    def _insert( node: Optional[ Treap[ T ] ], key: T, prio: int ) -> Treap[ T ]:
        if node is None:
            return Treap( key, prio )
        else:
            return node.insert( key, prio )

    def _fix_right( self ) -> Treap[ T ]:
        assert self.right is not None

        if self.priority > self.right.priority:
            return self
        else:
            return self.rotate_right()

    def _fix_left( self ) -> Treap[ T ]:
        assert self.left is not None

        if self.priority > self.left.priority:
            return self
        else:
            return self.rotate_left()

    def insert( self, key: T, prio: int ) -> Treap[ T ]:
        if key > self.key:
            self.right = Treap._insert( self.right, key, prio )
            return self._fix_right()
        else:
            self.left = Treap._insert( self.left, key, prio )
            return self._fix_left()
