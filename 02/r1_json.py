from __future__ import annotations
from typing import Any, Union

# As you might have noticed in prep exercises 2 and 3, the support
# for recursive data types in ‹mypy› is somewhat spotty. When
# designing new types, though, there is a compromise that types okay
# in ‹mypy› – at the price of creating a monomorphic wrapper for
# every recursive type in evidence. In other words, you can pick any
# two of [ recursive types, generic types, sanity ]. The ‹JSON› type
# will look as follows:

JSON = Union['JsonArray', 'JsonObject', 'JsonInt', 'JsonStr']
JsonKey = Union[str, int]  # for ‹get› and ‹set›

# Now implement the classes ‹JsonArray› and ‹JsonObject›, with ‹get›
# and ‹set› methods (which take a key/index) and in the case of
# ‹JsonArray›, an ‹append› and a ‹pop› method. The ‹set› methods
# should also accept ‘raw’ ‹str› and ‹int› objects.


class JsonArray:
    def __init__(self) -> None:
        self.arr: list[Any] = list()

    def get(self, index: int) -> Any:
        if index > len(self.arr) - 1:
            raise IndexError
        return self.arr[index]

    def append(self, obj: Any) -> None:
        self.arr.append(obj)

    def pop(self) -> Any:
        return self.arr.pop()


class JsonObject:
    def __init__(self) -> None:
        self.obj: dict[Any, Any] = {}

    def set(self, key: Any, obj: Any) -> None:
        self.obj[key] = obj

    def get(self, key: Any) -> Any:
        return self.obj[key]

# The classes ‹JsonStr› and ‹JsonInt› are going to be a little
# special, since they should behave like ‹str› and ‹int›, but also
# provide ‹get›/‹set› (which fail with an assertion) to make life
# easier for the user.


class JsonInt:
    pass


class JsonStr:
    pass


def test_basic() -> None:
    x = JsonObject()
    x.set('foo', 7)
    y = JsonArray()
    y.append(x)
    assert x.get('foo') == 7
    assert y.get(0).get('foo') == 7


if __name__ == '__main__':
    test_basic()
