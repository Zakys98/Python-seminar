# pragma mypy relaxed
from typing import TypeVar, Generic, Optional

# The class ‹Tree› represents a binary search tree. Implement
# ‹search› that performs a search for a given key, in logarithmic
# time and constant latency (between two calls to ‹suspend›). In
# each step, pass the value through which the search has passed to
# ‹suspend›, so that the caller can monitor the progress of the
# search.

T = TypeVar( 'T' )

class Tree( Generic[ T ] ):
    def __init__( self, value ) -> None:
        self.left  : Optional[ Tree ] = None
        self.right : Optional[ Tree ] = None
        self.value = value

    async def search( self, key: T, suspend ):
        await suspend(self.value)
        if(key == self.value):
            return self.value

        if key < self.value and self.left is not None:
            return await self.left.search(key, suspend)
        if key > self.value and self.right is not None:
            return await self.right.search(key, suspend)
        return None


def test_basic() -> None:
    t : Tree[ int ] = Tree(  7 )
    t.left          = Tree(  2 )
    t.left.left     = Tree(  1 )
    t.left.right    = Tree(  4 )
    t.right         = Tree( 12 )
    t.right.left    = Tree(  9 )
    t.right.right   = Tree( 17 )

    class suspend:
        def __init__( self, v ): self.v = v
        def __await__( self ): yield self.v

    def search_l( t, v ):
        return list( t.search( v, suspend ).__await__() )

    def search_r( t, v ):
        try:
            coro = t.search( v, suspend ).__await__()
            while True: next( coro )
        except StopIteration as stop:
            found = stop.value
        return found

    assert search_l( t,  9 ) == [ 7, 12, 9 ]
    assert search_l( t, 12 ) == [ 7, 12 ]
    assert search_l( t,  4 ) == [ 7, 2, 4 ]
    assert search_l( t,  7 ) == [ 7 ]
    assert search_l( t,  8 ) == [ 7, 12, 9 ]

    assert     search_r( t, 1 )
    assert     search_r( t, 2 )
    assert not search_r( t, 3 )
    assert     search_r( t, 4 )
    assert not search_r( t, 5 )
    assert not search_r( t, 5 )


if __name__ == '__main__':
    test_basic()
