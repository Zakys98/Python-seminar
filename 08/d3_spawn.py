from __future__ import annotations
from collections import deque
from typing import Coroutine, TypeVar, Generator

# The final piece of using ‹async› coroutines to implement fibres is
# creation of fibres on demand. In some sense, this is just a
# straightforward extension of the previous example: we simply need
# to realize that coroutine objects (and thus fibres) can be created
# by existing fibres and that they can be passed to the scheduler
# using the same request mechanism we have been using earlier (but
# with a new twist, combining the special function and the ‘request’
# into a single entity – notice the ‹yield self›):

class async_spawn:
    def __init__( self, coro: Coro ):
        self.coro = coro
    def __await__( self ) -> AGen:
        yield self

Coro = Coroutine[ async_spawn, None, None ]
AGen = Generator[ async_spawn, None, None ]


# We also need to extend the scheduler from the previous example to
# support an arbitrary number of fibres (instead of just two). We
# will put them on a queue (implemented using a ‹deque›), running a
# fibre until we can, then popping it off when it returns.

def run_scheduler( main: Coro ) -> None:

    queue  : deque[ Coro ] = deque()
    active : None | Coro   = main
    reqs   = 0

    # Request processing: there is only one type of request, so this
    # is really simple. When spawning a new fibre is requested, put
    # the ‘main’ of that fibre at the end of the queue. Eventually,
    # it will get to run as fibres that spawned earlier terminate.

    def process( req ):
        if isinstance( req, async_spawn ):
            queue.append( req.coro )
        else:
            assert False # no other type of request exists

    # And the main loop: while we have a fibre to run, run it. If it
    # terminates, pull out the next one from the queue. If the queue
    # is empty, we are done. We also keep and return the count of
    # requests that we served, as a simple sanity check.

    while active:
        try:
            process( active.send( None ) )
            reqs += 1
        except StopIteration as e:
            active = queue.popleft() if queue else None

    return reqs


# That's our last demo scheduler. You can make a guess how the
# execution goes (i.e. what fibres will run and in what order).

async def fibre( n: int ) -> int:
    for i in range( n % 10 ):
        print( f'fibre {n} spawns {10 * n + i}' )
        await async_spawn( fibre( 10 * n + i ) )

    print( f'fibre {n} done' )
    return n

def test_scheduler():
    assert run_scheduler( fibre( 5 ) ) == 31

if __name__ == '__main__':
    test_scheduler()
