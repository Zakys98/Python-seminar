from typing import Coroutine, TypeVar, Generator

# In this demonstration, we will leave out requests (except a very
# simple one, that will allow us to actually switch fibres) and
# focus on fibre switching. For this purpose, our scheduler will
# take two coroutines at the start and switch between them whenever
# one of them yields¹ the CPU. First the trivial request:

class sched_yield:
    def __await__( self ) -> Generator[ None, None, None ]:
        yield None

# A couple of type aliases for later convenience.

T = TypeVar( 'T' )
Coro = Coroutine[ None, None, T ]

# That done, we can focus on the scheduler. As mentioned, we will
# pass two coroutines (each of them becoming a ‘main’ function of a
# single fibre) to the scheduler. We will collect their results and
# return them as a 2-tuple. For simplicity, we require both
# coroutines to have the same return type.

def run_scheduler( coro_a: Coro[ T ],
                   coro_b: Coro[ T ] ) -> tuple[ T, T ]:

    result: dict[ Coro[ T ], T ] = {}

    # Since we have exactly two fibres, we can simply bind them to a
    # pair of variables to indicate their status. The ‹active› fibre
    # will be the one to execute in the next ‘timeslot’.

    active:  None | Coro[ T ] = coro_a
    waiting: None | Coro[ T ] = coro_b

    # And the main loop: while we have a fibre to run, run it. If it
    # yields (using ‹sched_yield›), swap it with the waiting fibre
    # (if we have one, i.e. it did not terminate yet). If a fibre
    # terminates, stash its result in a dictionary.

    while active:
        try:
            active.send( None )
        except StopIteration as e:
            result[ active ] = e.value
            active = None

        if waiting:
            active, waiting = waiting, active

    # Both fibres have terminated, give back their results to the
    # caller.

    return result[ coro_a ], result[ coro_b ]


# That's all there is for the scheduler. We can now write a simple
# (async) function which will serve as the main function of both our
# test fibres. It will simply print some progress messages and yield
# the processor in between. What message order do we expect?

async def fibre( n: int ) -> int:
    print( f'fibre {n} runs' )
    await sched_yield()

    for i in range( 2 * n ):
        print( f'fibre {n} continues' )
        await sched_yield()

    print( f'fibre {n} done' )
    return n

def test_scheduler():
    assert run_scheduler( fibre( 1 ), fibre( 2 ) ) == ( 1, 2 )

# ¹ The confusion of terminology here is unfortunate, but «yield» is
#   a standard term here. We will call the request ‹sched_yield›
#   (after the POSIX function), since ‹yield› would conflict with a
#   keyword anyway. The more or less ‘standard’ way to do the
#   equivalent of this with ‹asyncio› is ‹sleep( 0 )›.

if __name__ == '__main__':
    test_scheduler()
