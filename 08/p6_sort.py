from __future__ import annotations
from typing import Sized, Callable, Awaitable, TypeVar, Iterable, \
                   List, Protocol, Generator, Tuple, Sequence

# You are given ‹sched_yield›, an awaitable that allows the
# scheduler to switch to a different coroutine, if needed. Given
# that, write a ‘low-latency’ sort function – one that does only
# O(1) work between two consecutive calls to ‹sched_yield›.
# Requirements:
#
#  • the sort should be in-place,
#  • the total runtime should be O(n⋅logn),
#  • use ‹data.compare( a, b )› to compare items:
#    ◦ ‹-1› means ‹data[ a ] < data[ b ]›,
#    ◦ ‹0› means ‹data[ a ] == data[ b ]›
#    ◦ finally ‹1› means ‹data[ a ] > data[ b ]›,
#  • use ‹data.swap( a, b )› to swap values with indices ‹a›, ‹b›,
#  • ‹len( data )› gives you the number of items.

class Array( Sized ):
    def compare( self, a: int, b: int ) -> int: ...
    def swap( self, a: int, b: int ) -> None: ...

async def sort( data: Array, suspend: Suspend ) -> None: pass

def check_run( data: Sequence[ int ] ) -> List[ int ]:
    counter = 0
    work_done = []

    def tick() -> None:
        nonlocal counter
        counter += 1
    def lap() -> None:
        nonlocal counter
        work_done.append( counter )
        counter = 0

    class array( Array ):
        def __init__( self, data: List[ T ] ) -> None:
            self.__data = data
        def compare( self, idx_a: int, idx_b: int ) -> int:
            tick()
            a = self.__data[ idx_a ]
            b = self.__data[ idx_b ]
            return 0 if a == b else 1 if a > b else -1
        def swap( self, idx_a: int, idx_b: int ) -> None:
            tick()
            val_a = self.__data[ idx_a ]
            val_b = self.__data[ idx_b ]
            self.__data[ idx_b ] = val_a
            self.__data[ idx_a ] = val_b
        def __len__( self ) -> int:
            return len( self.__data )

    Pause = Generator[ Tuple[ () ], None, None ]

    class pause( Awaitable[ None ] ):
        def __await__( self ) -> Pause: yield ()

    to_sort = array( list( data ) )
    the_sort = sort( to_sort, pause ).__await__()

    try:
        while True:
            assert next( the_sort ) == ()
            lap()
    except StopIteration:
        lap()

    for i in range( len( data ) - 1 ):
        assert to_sort.compare( i, i + 1 ) <= 0

    return work_done

def test_order() -> None:
    check_run( [ 3, 1, 2 ] )
    check_run( [ 1, 2, 3 ] )
    check_run( [ 1, 2, 3, 4 ] )
    check_run( [ 3, 4, 1, 2 ] )

def test_latency() -> None:
    def do_test( data: Sequence[ int ] ) -> None:
        work = check_run( data )
        for ops in work:
            assert ops <= 16, work

    from random import shuffle
    do_test( [ 1, 2, 3 ] )
    do_test( range( 1024 ) )
    do_test( range( 2047, -1, -1 ) )
    data = list( range( 0, 32768, 7 ) )
    for i in range( 5 ):
        shuffle( data )
        do_test( data )

def test_complexity() -> None:
    from random import shuffle

    def do_test( data: List[ int ] ) -> float:
        return sum( check_run( data ) ) / len( data )

    data = list( range( 8 ) )
    trials = []

    for i in range( 12 ):
        count = len( data )
        new = range( count // 2, 3 * count // 2 )
        data.extend( new )
        shuffle( data )
        trials.append( do_test( data ) )

    bound = 2 * ( trials[ 1 ] - trials[ 0 ] )

    for i in range( len( trials ) - 1 ):
        assert trials[ i + 1 ] - trials[ i ] < bound

if __name__ == '__main__':
    test_order()
    test_latency()
    test_complexity()

T = TypeVar( 'T', bound = 'SupportsLessThan' )

class SupportsLessThan( Protocol ):
    def __lt__( self: T, other: T ) -> bool: ...
    def __le__( self: T, other: T ) -> bool: ...

Suspend = Callable[ [], Awaitable[ None ] ]
