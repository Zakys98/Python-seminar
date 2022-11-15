from typing import Optional

# Implement the mark part of a mark & sweep collector. The interface
# of ‹Heap› stays the same as it was in ‹r1›.

class Heap:
    def __init__( self ):
        self.data : List[ List[ int ] ] = []

    def read( self, obj_id: int, index: int ) -> Optional[int]: pass
    def write( self, obj_id: int, index: int,
               value: int ) -> bool: pass
    def make( self, size: int ) -> int: pass
    def count( self ) -> int: pass


def test_basic() -> None:
    h = Heap()

    def read( obj_id: int, idx: int ) -> int:
        r = h.read( obj_id, idx )
        assert r is not None
        return r

    h.make( 5 ) # create the root
    h.write( 0, 0, a := h.make( 2 ) )
    assert h.count() == 2
    h.write( 0, 1, b := h.make( 3 ) )
    h.write( read( 0, 0 ), 0, read( 0, 1 ) )
    h.write( read( 0, 1 ), 0, read( 0, 0 ) )
    assert h.count() == 3
    h.write( 0, 1, -7 )
    assert h.count() == 3
    h.write( 0, 0, -3 )
    assert h.count() == 1


if __name__ == '__main__':
    test_basic()
