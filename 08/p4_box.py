from typing import Generic, TypeVar, Generator, Coroutine, Callable

# Implement a class which coordinates a single producer and a single
# consumer (the producer puts the value in the ‘box’, where the
# consumer fetches it). The roles (producer vs consumer) are known
# upfront. The coroutines are passed to the constructor unevaluated
# (i.e. not as coroutine objects, but as functions which take the
# box as a parameter and return coroutine objects; see also below).

T = TypeVar( 'T' )
class Box( Generic[ T ] ): pass

def test_basic() -> None:
    got = 0

    async def make( box: Box[ int ] ) -> None:
        await box.put( 1 )
        assert got == 1, got
        await box.put( 2 )

    async def take( box: Box[ int ] ) -> None:
        nonlocal got
        while True:
            x : int = await box.get()
            got += 1
            assert x == got, ( x, got )

    Box( make, take ).run()
    assert got == 2, got


if __name__ == '__main__':
    test_basic()
