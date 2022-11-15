from typing import Optional, Dict

# In this exercise, we will move one level down and one step closer
# to reality. Your task is to implement simplified versions of the
# ‹malloc› and ‹free› functions, in a fixed-size memory represented
# as a Python ‹list› of integers.

# For simplicity, the memory will be ‘word-addressed’, that is, we
# will not deal with individual bytes – instead, each addressable
# memory cell will be an ‹int›. To further simplify matters, ‹free›
# will get the size of the object as a second parameter (you can
# assume that this is correct).

# Use a first-fit strategy: allocate objects at the start of the
# first free chunk of memory. It is okay to scan for free memory in
# linear time.  The ‹malloc› method should return ‹None› if there
# isn't enough (continuous) memory left.

class Heap:
    def __init__( self, size: int ) -> None:
        self.memory: list[int | None] = [None] * size
        self.size = size

    def read( self, addr: int ) -> Optional[int]:
        return self.memory[addr]

    def write( self, addr: int, value: int ) -> None:
        self.memory[addr] = value

    def malloc( self, size: int ) -> Optional[ int ]:
        counter = 0
        start = 0
        for i, item in enumerate(self.memory):
            if item is None:
                counter += 1
            else:
                counter = 0
                start = i + 1
            if counter == size:
                break
        if start == self.size:
            return None
        for i in range(start, start + size):
            self.memory[i] = -1
        return start


    def free( self, addr: int, size: int ) -> None:
        for i in range(addr, addr + size):
            self.memory[i] = None


def test_basic() -> None:
    amap : Dict[ Optional[ int ], int ] = {}
    h = Heap( 20 )

    def check_amap() -> None:
        for a_addr, a_size in amap.items():
            assert a_addr is not None
            for b_addr, b_size in amap.items():
                assert b_addr is not None
                a_bad = a_addr < b_addr < a_addr + a_size
                b_bad = b_addr < a_addr < b_addr + b_size
                assert not a_bad and not b_bad

    def check_write() -> None:
        from random import shuffle
        objs = list( amap.items() )
        shuffle( objs )
        i = 0
        for start, size in objs:
            assert start is not None
            for addr in range( start, start + size ):
                h.write( addr, i )
                i += addr

        i = 0
        for start, size in objs:
            assert start is not None
            for addr in range( start, start + size ):
                assert h.read( addr ) == i
                i += addr

    amap[ ( a := h.malloc( 4 ) ) ] = 4
    amap[ ( b := h.malloc( 6 ) ) ] = 6
    check_amap() ; check_write()
    amap[ ( c := h.malloc( 5 ) ) ] = 5
    check_amap() ; check_write()
    assert a is not None
    h.free( a, 4 ) ; del amap[ a ]

    amap[ ( a := h.malloc( 5 ) ) ] = 5
    check_amap() ; check_write()
    assert h.malloc( 7 ) is None
    amap[ ( d := h.malloc( 4 ) ) ] = 4
    check_amap() ; check_write()
    assert c is not None
    h.free( c, 5 ) ; del amap[ c ]

    amap[ h.malloc( 1 ) ] = 1
    amap[ h.malloc( 1 ) ] = 1
    check_amap() ; check_write()
    amap[ ( x := h.malloc( 1 ) ) ] = 1
    amap[ ( y := h.malloc( 1 ) ) ] = 1
    amap[ h.malloc( 1 ) ] = 1
    check_amap() ; check_write()
    assert h.malloc( 1 ) is None
    assert x is not None
    assert y is not None
    h.free( x, 1 ) ; del amap[ x ]
    h.free( y, 1 ) ; del amap[ y ]
    amap[ h.malloc( 2 ) ] = 2
    check_amap() ; check_write()


if __name__ == '__main__':
    test_basic()
