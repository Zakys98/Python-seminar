from typing import Optional

# Implement a simple reference-counting garbage collector. The
# interface is described in the class ‹Heap› below. Objects are
# represented using lists of integers, and the heap as a whole is a
# list of such objects. Negative numbers are data, non-negative
# numbers are references (indices into the main list of objects).
# The root object (with index 0) is immortal.

# The interface:
#
#  • the ‹count› method returns the number of live objects,
#  • the ‹write› method returns ‹True› iff the write was successful
#    (the object was alive and the index was within its bounds)
#  • likewise, the ‹read› method returns ‹None› if the object is
#    dead or invalid or the index is out of bounds.
#  • the ‹make› method returns an unused object identifier (and
#    grows the heap as required).
#
# The first call to ‹make› creates the root object. A freshly-made
# objects starts out with «zero» references. A reference to this
# object «must» be written somewhere into the heap.

class Heap:
    def __init__( self ):
        self.data : List[ List[ int ] ] = []
        pass # …

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
    assert h.count() == 3
    h.write( 0, 1, -7 )
    assert h.count() == 3
    h.write( 0, 0, -3 )
    assert h.count() == 1
    assert h.read( a, 0 ) is None
    assert h.read( b, 0 ) is None


if __name__ == '__main__':
    test_basic()
