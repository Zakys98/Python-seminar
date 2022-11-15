# pragma mypy relaxed

# Write a decorator ‹@noexcept()›, which turns a function which
# might throw an exception into one that will instead return ‹None›.
# If used with arguments, those arguments indicate which exception
# types should be suppressed.

# Note: typing this correctly with mypy is probably impossible. You
# can try using ‹Callable[ ..., Any ]› and/or ‹Any› if you want to
# add annotations.

def noexcept( *ignore ):
    def decorate( f ):
        return f
    return decorate


def test_main() -> None:

    @noexcept( TypeError, AssertionError )
    def foo() -> None:
        assert int( 1 ) == 2

    @noexcept()
    def bar() -> None:
        assert int( 2 ) == 3

    assert foo() == None
    assert bar() == None

    @noexcept( TypeError )
    def baz() -> None:
        raise AssertionError

    try:
        baz()
        assert False
    except AssertionError:
        pass

    @noexcept( TypeError, AssertionError, RuntimeError )
    def bazz( a1: int, a2: int, a3: int ) -> int:
        assert a1 == 3
        return a1 + a2 + 7 + a3

    assert bazz( 3, -4, a3 = -1 ) == 5
    assert bazz( 4, -4, a3 = -1 ) is None

if __name__ == "__main__":
    test_main()

