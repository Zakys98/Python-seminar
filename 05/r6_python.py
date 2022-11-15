from typing import Optional, Set

# Implement the ‘Python’ collector: reference counting, with mark &
# sweep to deal with cycles. Objects that are not on loops, or
# reachable from loops, are destroyed immediately when last
# reference to them is lost. Unreachable loops are destroyed on
# ‹collect›.

class Heap:
    def __init__( self ):
        self.data : List[ List[ int ] ] = []

    def read( self, obj_id: int, index: int ) -> Optional[int]: pass
    def write( self, obj_id: int, index: int,
               value: int ) -> bool: pass
    def make( self, size: int ) -> int: pass
    def collect( self ) -> int: pass


def test_basic() -> None:
    h = Heap()

    def read( obj_id: int, idx: int ) -> int:
        r = h.read( obj_id, idx )
        assert r is not None
        return r

    h.make( 6 ) # create the root
    h.write( 0, 1, a := h.make( 3 ) )
    h.write( 0, 2, b := h.make( 3 ) )
    h.write( 0, 3, c := h.make( 3 ) )
    h.write( 0, 4, d := h.make( 3 ) )
    h.write( 0, 5, e := h.make( 2 ) )

    for i in range( 1, 6 ):
        h.write( read( 0, i ), 0, -i )

    h.write( read( 0, 1 ), 1, read( 0, 2 ) )
    h.write( read( 0, 1 ), 2, read( 0, 3 ) )
    h.write( read( 0, 3 ), 1, read( 0, 4 ) )
    h.write( read( 0, 4 ), 1, read( 0, 3 ) )
    h.write( read( 0, 4 ), 2, read( 0, 2 ) )
    h.write( read( 0, 5 ), 1, read( 0, 1 ) )

    def check( yes: Set[ int ], no: Set[ int ] ) -> None:
        print( h.data )
        for i in yes:
            assert h.read( i, 0 ) is not None
        for i in no:
            assert h.read( i, 0 ) is None

    check( { a, b, c, d, e }, set() )
    h.write( 0, 2, 0 )
    check( { a, b, c, d, e }, set() )
    h.write( 0, 3, 0 )
    check( { a, b, c, d, e }, set() )
    h.write( 0, 5, 0 )
    check( { a, b, c, d }, { e } )

    h.write( 0, 4, 0 )
    check( { a, b, c, d }, { e } )

    h.write( 0, 1, 0 )
    check( { b, c, d }, { a, e } )
    h.collect()
    check( set(), { a, b, c, d, e } )

if __name__ == '__main__':
    test_basic()
