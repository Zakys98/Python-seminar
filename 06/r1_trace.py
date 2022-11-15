from typing import Callable

# Write a decorator that prints a message every time a function is
# called or it returns. The output should be indented when calls are
# nested, and should include arguments and the return value.

# Aim for output like this:

#     foo [13]
#       bar [13] -> 20
#       bar [26] -> 33
#     returned 53

class traced:
    def __init__(self) -> None:
        self.indent = 0
        self.counter = 0

    def __call__(self, fun):
        def wrapper(*args, **kwargs):
            now = self.counter
            fun_name = fun.__name
            

        return wrapper

def test_main() -> None:
    @traced
    def bar( x: int ) -> int:
        return x + 7

    @traced
    def foo( x: int ) -> int:
        return bar( x ) + bar( 2 * x )

    output = redirect_out( foo, 13 )

    assert output == " foo [13]\n" \
                     "   bar [13] -> 20\n" \
                     "   bar [26] -> 33\n" \
                     " returned 53\n"

def redirect_out( test: Callable[ ..., object ], *args: object ) -> str:

    import sys
    from io import StringIO

    stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    test( *args )

    sys.stdout = stdout
    return out.getvalue()

if __name__ == "__main__":
    test_main()
