from typing import Callable, Set

# Add the ‘sweep’ phase to the mark & sweep collector from previous
# exercise. That is, find all objects which are reachable from the
# root set, then ‘free’ all objects which were previously alive but
# are not anymore. Freeing objects is simulated using a callback,
# which is passed to the constructor of ‹Heap›. The callback must be
# passive (unlike the finalizer from ‹p2_final›).
#
# Again, roots are marked using ‹add_root› and references are
# added/removed using ‹add_ref› and ‹del_ref›. You can assume that
# the number of ‹del_ref› calls on given arguments is always at most
# the same as the number of corresponding ‹add_ref› calls.

class Heap:
    def __init__( self, free: Callable[ [ int ], None ] ) -> None:
        self.objects: list[tuple[int, int | None]] = list()
        self.free = free

    def add_root( self, obj: int ) -> None:
        self.objects.append((obj, None))

    def add_ref( self, obj_from: int, obj_to: int ) -> None:
        self.objects.append((obj_from, obj_to))

    def del_ref( self, obj_from: int, obj_to: int ) -> None:
        self.objects.remove((obj_from, obj_to))

    def collect( self ) -> None:
        output: set[int] = set()
        for x, y in self.objects:
            if y is None:
                output.add(x)
            elif x in output:
                output.add(y)
        for x, y in self.objects:
            if y is not None and y not in output:
                self.free(x)

def test_basic() -> None:
    freed : Set[ int ] = set()
    h = Heap( lambda x: freed.add( x ) )
    h.add_root( 1 )
    h.add_ref( 1, 2 )
    h.add_ref( 1, 3 )
    h.add_ref( 2, 3 )
    h.add_ref( 3, 4 )
    h.add_ref( 4, 3 )
    h.collect()
    assert freed == set(), freed
    h.del_ref( 1, 3 )
    h.collect()
    assert freed == set(), freed
    h.del_ref( 1, 2 )
    h.collect()
    assert freed == { 2, 3, 4 }, freed
    h.add_ref( 1, 13 )
    h.add_ref( 13, 9 )
    h.add_ref( 1, 7 )
    h.add_ref( 7, 8 )
    h.add_ref( 8, 1 )
    h.collect()
    assert freed == { 2, 3, 4 }, freed
    h.add_ref( 7, 9 )
    h.add_ref( 9, 8 )
    h.add_ref( 8, 7 )
    h.add_ref( 1, 9 )
    h.collect()
    assert freed == { 2, 3, 4 }, freed
    h.del_ref( 1, 7 )
    h.collect()
    assert freed == { 2, 3, 4 }, freed
    h.del_ref( 1, 9 )
    h.collect()
    assert freed == { 2, 3, 4 }, freed
    h.del_ref( 13, 9 )
    h.collect()
    assert freed == { 2, 3, 4, 7, 8, 9 }, freed

if __name__ == '__main__':
    test_basic()
