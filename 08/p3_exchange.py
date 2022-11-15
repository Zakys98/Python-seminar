from typing import Generic, TypeVar, Generator, Optional, List, \
                   Coroutine, cast

# Implement a class which coordinates a multi-producer,
# multi-consumer system built out of ‹async› coroutines. Each
# coroutine can either produce items (by calling ‹put›) or consume
# them (by calling ‹get›). Constraints:
#
#  • a given coroutine cannot call both ‹put› and ‹get›,
#  • a producer is blocked until the item can be consumed,
#  • a consumer is blocked until an item is produced.
#
# These constraints mean that there can be at most one unconsumed
# item per producer in the system. If multiple producers have a
# value ready, the system picks up the one that has been waiting the
# longest. If multiple consumers are waiting for an item, again, the
# longest-waiting one is given the next item.
#
# When ‹run› is called, all coroutines are started up, until each
# blocks on either ‹put› or ‹get›. The system terminates when no
# further items can be produced (there are no producers left).

T = TypeVar( 'T' )

class Exchange( Generic[ T ] ): pass

def test_basic() -> None:
    got = 0

    async def make( xchg: Exchange[ int ] ) -> None:
        await xchg.put( 1 )
        await xchg.put( 2 )

    async def take( xchg: Exchange[ int ] ) -> None:
        nonlocal got
        while True:
            x : int = await xchg.get()
            got += 1
            assert x == got

    xchg : Exchange[ int ] = Exchange()
    xchg.add( make( xchg ) )
    xchg.add( take( xchg ) )
    xchg.run()
    assert got == 2, got


def test_multi() -> None:
    counters = [ 0 for _ in range( 5 ) ]
    consumed = set()
    produced = set()

    async def make( xchg: Exchange[ int ], start: int, end: int ) -> None:
        for i in range( start, end ):
            produced.add( i )
            await xchg.put( i )

    async def take( xchg: Exchange[ int ], idx: int ) -> None:
        while True:
            x : int = await xchg.get()
            counters[ idx ] += 1
            consumed.add( x )
            assert idx == x // 7 or idx + 5 == x // 7, ( idx, x )
            if x % 7 != 6:
                assert x + 1 not in produced

    xchg : Exchange[ int ] = Exchange()
    for i in range( 10 ):
        xchg.add( make( xchg, 7 * i, 7 * ( i + 1 ) ) )
    for i in range( 5 ):
        xchg.add( take( xchg, i ) )
    xchg.run()

    assert sum( counters ) == 70
    assert produced == consumed
    for c in counters:
        assert c == 14


if __name__ == '__main__':
    test_basic()
    test_multi()
