from typing import Optional, Set

# Write a semi-space collector, using the same interface as before.
# The requirement is that after a collection, the objects all occupy
# contiguous indices. For simplicity, we index the semispaces
# independently, so the objects always start from 0. Make sure that
# the root always retains index 0.

class Heap:
    def __init__( self ):
        self.data : List[ List[ int ] ] = []

    def read( self, obj_id: int, index: int ) -> Optional[int]: pass
    def write( self, obj_id: int, index: int,
               value: int ) -> bool: pass
    def make( self, size: int ) -> int: pass
    def count( self ) -> int: pass
    def collect( self ) -> None: pass


def test_basic() -> None:
    h = Heap()

    def read( obj_id: int, idx: int ) -> int:
        r = h.read( obj_id, idx )
        assert r is not None
        return r

    def check( expect: Set[ int ] ) -> None:
        found = set()

        for i in range( 1, len( expect ) + 1 ):
            x = h.read( i, 0 ) 
            assert x is not None, i
            found.add( -x )

        for i in range( len( expect ) + 1, 5 ):
            assert h.read( i, 0 ) is None, i

        assert found == expect, ( found, expect )

        for i in expect:
            x = h.read( 0, i )
            assert x is not None
            if x != 0:
                assert h.read( x, 0 ) == -i

    h.make( 5 ) # create the root
    h.write( 0, 1, a := h.make( 2 ) )
    h.write( read( 0, 1 ), 0, -1 )
    h.write( 0, 2, h.make( 2 ) )
    h.write( read( 0, 2 ), 0, -2 )
    h.write( 0, 3, h.make( 2 ) )
    h.write( read( 0, 3 ), 0, -3 )
    h.write( 0, 4, b := h.make( 3 ) )
    h.write( read( 0, 4 ), 0, -4 )

    check( { 1, 2, 3, 4 } )
    h.collect()
    check( { 1, 2, 3, 4 } )

    h.write( read( 0, 1 ), 1, read( 0, 4 ) )
    h.write( read( 0, 4 ), 1, read( 0, 1 ) )

    check( { 1, 2, 3, 4 } )
    h.collect()
    check( { 1, 2, 3, 4 } )

    h.write( 0, 2, 0 )
    h.write( 0, 3, 0 )
    h.collect()
    check( { 1, 4 } )

    h.write( 0, 1, 0 )
    h.collect()
    check( { 1, 4 } )
    h.write( 0, 4, 0 )
    h.collect()
    check( set() )


if __name__ == '__main__':
    test_basic()
