# Implement a prefix sum and a prefix list on arbitrary ‹Iterable›
# instances, using the iterator approach (class with an ‹__iter__›
# method).
#
# Examples:
#
#     dump( prefixes( [ 1, 2, 3 ] ) )   # [] [1] [1, 2] [1, 2, 3]
#     dump( prefix_sum( [ 1, 2, 3 ] ) ) # [ 1, 3, 6 ]
from typing import Generic, Iterable, TypeVar, Iterator

T = TypeVar("T")

class PrefixIterator(Generic[T]):
        def __init__(self, iterable: Iterable[T]) -> None:
            super().__init__()
            self.iterable = iterable

        def __next__(self) -> T:
            pass

class PrefixIterable(Generic[T]):

    def __init__(self, iterable) -> None:
        self.iterable = iterable
        self.running = iter(iterable)
        self.list = []
        self.first = True

    def __iter__(self) -> Iterator[list[T]]:
        return PrefixIterator(self.iterable)

    def __next__(self) -> list[T]:
        if self.first:
            self.first = False
            return []
        result = self.list.copy()
        item = next(self.running)
        self.list.append(item)
        return result

def prefixes( list_in: Iterable[T] ) -> Iterable[list[T]]:
    return PrefixIterable(list_in)

def prefix_sum( list_in ):
    pass


def test_main() -> None:
    import types

    pref = [ [], [ 1 ], [ 1, 2 ], [ 1, 2, 3 ], [ 1, 2, 3, 4 ] ]
    assert not isinstance( prefixes( [] ), types.GeneratorType )

    for i in prefixes( [ 1, 2, 3, 4 ] ):
        assert i in pref
        pref.remove( i )

    assert not pref

    lst = [ 1, 2, 3, 4, 5 ]
    out = [ 1, 3, 6, 10, 15 ]

    count = 0
    for item in prefix_sum( lst ):
        count += 1 # is iterable
    assert count == 5

    assert list( prefix_sum( lst ) ) == out


if __name__ == "__main__":
    test_main()

