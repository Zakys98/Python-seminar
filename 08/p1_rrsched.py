from collections import deque
from typing import Coroutine, Deque, Generator, Iterator, List, Optional

# Write an ‹async› (coroutine) scheduler which executes a given list
# of coroutines (the ‹async def› type) in a round-robin fashion.
# That is:
#
#  • provide ‹suspend›, an ‹async› method, which, when awaited,
#    suspends the currently executing coroutine and allows the
#    others to be scheduled (that is, given ‹sched›, a reference to
#    the scheduler, a coroutine should be able to perform ‹await
#    sched.suspend()›),
#  • tasks are added using ‹add›, which takes an unstarted (never
#    awaited) coroutine as an argument and appends it to the end of
#    the round-robin execution order (i.e. the coroutine that is
#    added first is executed first, until it suspends, then the
#    second executes until it suspends, and so on; when the last
#    coroutine on the list suspends, wake up the first to continue,
#    until it suspends, wake up the second, …),
#  • after at least one coroutine is added, calling ‹run› on the
#    scheduler will start executing the tasks; ‹run› returns
#    normally after all the tasks finish (note, however, that some
#    tasks may terminate earlier than others).
#
# See ‹test_basic› for a simple usage example. A few hints follow
# (you can skip them if you know what you are doing):
#
#  1. To implement ‹suspend›, you will want to create a low-level
#     awaitable object (i.e. one which is not the result of ‹async
#     def›). This is done by providing a special method ‹__await__›,
#     which is a «generator» (i.e. it uses ‹yield›).
#  2. This ‹yield› suspends the entire stack of awaitables (most of
#     which will be typically ‹async› coroutines), returning control
#     to whoever called ‹next› on the iterator (the result of
#     calling ‹__await__› on the top-level awaitable).
#  3. Regarding ‹mypy›:
#     ◦ the ‹task› passed to ‹add› should be a ‹Coroutine› (since
#       the scheduler won't touch any of its outputs, these can be
#       all set to ‹object›, instead of the much more problematic
#       ‹Any›),
#     ◦ the ‹Awaitable› protocol needs ‹__await__› to be a
#       ‹Generator› (you will need this for implementing ‹suspend›),
#     ◦ when you call ‹__await__()› on an awaitable, the result is,
#       among others, an ‹Iterator›.


class async_spawn:
    def __init__(self, coro: 'Coro') -> None:
        self.coro = coro

    def __await__(self) -> 'Agen':
        yield self

Coro = Coroutine[async_spawn, None, None]
Agen = Generator[async_spawn, None, None]

class RoundRobin:
    def __init__(self) -> None:
        self.waiting: Deque[Coro] = deque()
        self.active: Optional[Coro] = None

    def add(self, task: Coro) -> None:
        self.waiting.append(task)

    async def suspend(self) -> None:
        assert self.active is not None
        await async_spawn(self.active)

    def run(self) -> None:
        if not self.waiting:
            return

        self.active = self.waiting.popleft()
        while self.active:
            try:
                self.active.send(None)
                self.add(self.active)
            except StopIteration:
                return

        self.active = None
        if self.waiting:
            self.active = self.waiting.popleft()


def test_basic() -> None:
    ticks = []

    async def coro( sched: RoundRobin, start: int ) -> None:
        ticks.append( start + 1 )
        await sched.suspend()
        ticks.append( start + 2 )
        await sched.suspend()
        ticks.append( start + 3 )

    async def short( sched: RoundRobin ) -> None:
        ticks.append( 7 )
        await sched.suspend()
        ticks.append( 8 )

    s = RoundRobin()
    s.add( coro( s, 10 ) )
    s.add( coro( s, 20 ) )
    s.add( short( s ) )
    s.add( coro( s, 30 ) )
    s.run()
    assert ticks == [ 11, 21, 7, 31, 12, 22, 8, 32,
                      13, 23, 33 ], ticks

if __name__ == '__main__':
    test_basic()
