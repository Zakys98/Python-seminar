# Implement a decorator which will keep track of how many times
# which function was called. The decorator should be available as
# ‹@profile› and calling ‹profile.get()› should return a dictionary
# with function names as keys and call counts as values.

from collections import defaultdict
from typing import Callable, Any


class profile:
    calls: dict[str, int] = defaultdict(int)

    def __init__(self, f: Callable) -> None:
        self.f = f

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        profile.calls[self.f.__name__] += 1
        return self.f(*args, **kwargs)

    @classmethod
    def get(self):
        return profile.calls

def test_basic() -> None:
    @profile
    def bar( i: int ) -> None:
        if i == 0:
            foo( 1 )

    @profile
    def foo( start: int ) -> None:
        for i in range( start, 10 ):
            bar( i )

    assert profile.get() == {}, profile.get()
    bar( 7 )
    assert profile.get() == { 'bar': 1 }, profile.get()
    foo( 9 )
    assert profile.get() == { 'bar': 2, 'foo': 1 }, profile.get()
    foo( 0 )
    assert profile.get() == { 'bar': 21, 'foo': 3 }, profile.get()


if __name__ == '__main__':
    test_basic()
