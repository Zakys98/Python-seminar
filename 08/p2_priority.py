from __future__ import annotations
from typing import Coroutine, Generator, Iterator, List, Set

# Write an ‹async› scheduler which executes a given list of
# coroutines in a priority-driven fashion. The ‹add› method takes,
# in addition to the coroutine itself, a «static priority». Higher
# priorities get executed more often. Here is how it works:
#
#  1. In addition to the «static» priority (a fixed number), each
#     task is assigned a «dynamic» priority. The dynamic priority
#     starts out equal to the static one, but is decremented each
#     time a coroutine is awakened.
#  2. The next coroutine to be awakened is always the one with the
#     highest dynamic priority.
#  3. Whenever the highest dynamic priority in the system drops to
#     zero, all tasks get their dynamic priority reset to their
#     static priority.
#
# Except as noted above, the interface and semantics of the
# scheduler carry over from ‹p1›.

class PrioritySched: pass

def test_basic() -> None:
    stop = False
    checked = 0
    ticks : Set[ int ] = set()

    async def low( sched: PrioritySched ) -> None:
        nonlocal checked
        i = 0
        while True:
            await sched.suspend()
            if stop: break
            assert i in ticks, ( i, ticks )
            i += 1
            assert i in ticks, ( i, ticks )
            i += 1
            checked += 2

    async def high( sched: PrioritySched ) -> None:
        i = 0
        while not stop:
            ticks.add( i )
            i += 1
            await sched.suspend()

    async def tick( sched: PrioritySched ) -> None:
        nonlocal stop
        for i in range( 50 ):
            await sched.suspend()
            assert 2 * i <= checked <= 2 * ( i + 1 )
        stop = True

    s = PrioritySched()
    s.add( high( s ), 2 )
    s.add( low( s ), 1 )
    s.add( tick( s ), 1 )
    s.run()
    assert stop
    assert 98 <= checked <= 102
    assert set( range( 98 ) ) <= ticks

if __name__ == '__main__':
    test_basic()
