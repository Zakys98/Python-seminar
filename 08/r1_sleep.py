from typing import Coroutine, Generator, Iterator, List
from time import time, sleep
from queue import PriorityQueue

# Write an ‹async› (coroutine) scheduler which executes a given list
# of coroutines (the ‹async def› type). When a coroutine suspends
# (using ‹sched.suspend›) it specifies how long it wants to sleep,
# in milliseconds. The scheduler wakes up a particular coroutine
# when its sleep timer expires (it should try to do it exactly on
# time, but sometimes this will be impossible because another
# coroutine blocks for too long).
#
# Like before, implement ‹add› to attach coroutines to the scheduler
# and ‹run› to start executing them. The latter returns when no
# coroutines remain.


def time_millis() -> int:
    return round(time() * 1000)


Coro = Coroutine[None, int, None]


class CoroBox:
    def __init__(self, time: int, coro: Coro) -> None:
        self.time = time
        self.coro: Coro = coro
    def __lt__(self, other):
        return self.time < other.time
    def __eq__(self, other):
        return self.time == other.time

class Sched:
    def __init__(self) -> None:
        self.threads: PriorityQueue[CoroBox] = PriorityQueue()

    def add(self, coro: Coro):
        self.threads.put(CoroBox(0, coro))

    def suspend(self, delay: int):
        class rr_awaitable(self):
            def __await__(self):
                yield delay
        return rr_awaitable()

    def run(self) -> None:
        while not self.threads.empty():
            box = self.threads.get()
            if box.time > time_millis():
                self.threads.put(box)
                sleep(1/1000)
                continue
            try:
                next_delay = box.coro.send(None)
                self.threads.put(CoroBox(time_millis() + next_delay, box.coro))
            except StopIteration:
                pass


def test_basic() -> None:
    from time import time
    ticks = []
    start = time()

    async def coro(sched: Sched, ident: int, delay: int) -> None:
        for i in range(5):
            await sched.suspend(delay)
            passed = time() - start
            ticks.append((ident, int(1000 * passed)))
            print(ticks[-1])

    s = Sched()
    s.add(coro(s, 1, 210))
    s.add(coro(s, 2, 390))
    s.add(coro(s, 3, 90))
    s.run()

    expect = [(3,   90), (3,  180), (1,  210),
              (3,  270), (3,  360), (2,  390),
              (1,  420), (3,  450), (1,  630),
              (2,  780), (1,  840), (1, 1050),
              (2, 1170), (2, 1560), (2, 1950)]

    drift = 15
    for (ex_i, ex_t), (act_i, act_t) in zip(expect, ticks):
        assert ex_i == act_i, (ex_i, act_i)
        assert act_t - ex_t <= drift, (ex_t, act_t)
        drift += 7


if __name__ == '__main__':
    test_basic()
