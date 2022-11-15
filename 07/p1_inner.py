from typing import Tuple, Callable
import hypothesis
import hypothesis.strategies as s

# 1. Implement the standard dot product on 3D «integer» vectors.
# 2. Use hypothesis to check its properties:
#    ◦ commutativity
#    ◦ distributivity over addition a⋅(b + c) = a⋅b + a⋅c
#    ◦ bilinearity a⋅(rb + c) = r(a⋅b) + (a⋅c)
#    ◦ compatibility with scalar multiplication: (r₁a)⋅(r₂b) = r₁r₂(a⋅b)
#
# Bonus: Try the same with floats. Cry quietly. Disallow ‹inf›. And
# ‹nan›. Then cry some more.

Vector = Tuple[int, int, int]
Inner = Callable[[Vector, Vector], int]


def add(a: Vector, b: Vector) -> Vector:
    ax, ay, az = a
    bx, by, bz = b
    return (ax + bx, ay + by, az + bz)


def mul(r: int, a: Vector) -> Vector:
    ax, ay, az = a
    return (r * ax, r * ay, r * az)


def dot(a, b):
    list = [x * y for x, y in zip(a, b)]
    output = 0
    for x in list:
        output += x
    return output

vector = s.tuples(s.integers(), s.integers(), s.integers())

def check_commutativity(dot: Inner) -> None:
    @hypothesis.given(vector, vector)
    def inner(vec1: Vector, vec2: Vector) -> None:
        assert dot(vec1, vec2) == dot(vec2, vec1)
    inner()


def check_distributivity(dot: Inner) -> None: pass
def check_bilinearity(dot: Inner) -> None: pass
def check_compatibility(dot: Inner) -> None: pass


def test_self() -> None:
    check_commutativity(dot)
    check_distributivity(dot)
    check_bilinearity(dot)
    check_compatibility(dot)


def test_bad() -> None:
    def bad_dot(a: Vector, b: Vector) -> int:
        ax, ay, az = a
        bx, by, bz = b
        return ax * bx + ay * bz

    failed = True

    try:
        check_commutativity(bad_dot)
        failed = False
    except AssertionError:
        pass
    assert failed

    # everything else should work okay
    check_distributivity(bad_dot)
    check_bilinearity(bad_dot)
    check_compatibility(bad_dot)


def test_verybad() -> None:
    def badder_dot(a: Vector, b: Vector) -> int:
        ax, ay, az = a
        bx, by, bz = b
        return ax - bx

    failed = True

    try:
        check_commutativity(badder_dot)
        failed = False
    except AssertionError:
        pass
    assert failed

    try:
        check_distributivity(badder_dot)
        failed = False
    except AssertionError:
        pass
    assert failed

    try:
        check_bilinearity(badder_dot)
        failed = False
    except AssertionError:
        pass
    assert failed

    try:
        check_compatibility(badder_dot)
        failed = False
    except AssertionError:
        pass
    assert failed


if __name__ == '__main__':
    test_self()
    print("note: ignore the 'falsifying examples' below")
    test_bad()
    test_verybad()
