from typing import Optional
from r2_reach import Heap

# Add the sweep procedure to the ‹Heap› implementation from previous
# exercise.

class GcHeap( Heap ):
    def collect( self ) -> None: pass


def test_basic() -> None:
    h = GcHeap()

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
    assert h.read( a, 0 ) is not None
    h.collect()
    assert h.read( a, 0 ) is None
    assert h.read( b, 0 ) is None


if __name__ == '__main__':
    test_basic()
