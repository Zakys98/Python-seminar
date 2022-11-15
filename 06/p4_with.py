# pragma mypy relaxed
from typing import Callable, List
import contextlib
import sys

# Write a simple context manager to be used in a ‹with› block. The
# goal is to enrich stack traces with additional context, like this:

@contextlib.contextmanager
def context( *args ):
    try:
        yield
    except Exception as ex:
        print(*args, file=sys.stderr)
        raise ex


# For example:

def foo( x: int, y: int ) -> None:
    with context( "asserting equality", x, '=', y ):
        assert x == y

# Calling ‹foo( 1, 1 )› should print nothing (the assertion does not
# fail and no exceptions are thrown). On the other hand,
# ‹foo( 7, 8 )› should print something like this:

#     asserting equality 7 = 8
#     Traceback (most recent call last):
#       File "with.py", line 20, in <module>
#         foo( 7, 8 )
#       File "with.py", line 17, in foo
#         assert x == y
#     AssertionError

def test_main() -> None:

    def foo( x: int, y: int ) -> None:
        with context( "asserting equality", x, '=', y ):
            assert x == y

    def test() -> None:
        foo( 1, 1 )
        foo( 7, 8 )

    caught = False

    try:
        output: List[str] = []
        redirect_err( test, output )
    except AssertionError as e:
        caught = True

    assert caught
    assert output[0] == "asserting equality 7 = 8"

def redirect_err( f: Callable[ [], None ],
                  lines: List[ str ] ) -> None:

    import sys
    import traceback
    from io import StringIO

    stderr = sys.stderr
    out = StringIO()
    sys.stderr = out

    try:
        f()
    finally:
        sys.stderr = stderr
        lines.extend( out.getvalue().split( '\n' ) )

if __name__ == "__main__":
    test_main()
