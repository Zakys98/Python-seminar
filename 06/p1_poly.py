from __future__ import annotations

# Implement polynomials which can be added and printed. Do not print
# terms with coefficient 0, unless it is in place of ones and the
# only term. For example:
#
#     x = Poly( 2, 7, 0, 5 )                        # python
#     y = Poly( 2, 4 )
#
#     print( x )     # prints 2x³ + 7x² + 5
#     print( y )     # prints 2x + 4
#     print( x + y ) # prints 2x³ + 7x² + 2x + 9
#
# The implementation goes here:

class Poly:
    def __init__(self, *args) -> None:
        self.list: list[int] = list(args)

    def __add__(self, o: Poly) -> Poly:
        pass

    def __str__(self) -> str:
        pass

# We will do one more exercise with operators, ‹mod.py›, before
# moving on to exceptions.

def test_main() -> None:

    x = Poly( 2, 7, 3, 5 )
    y = Poly( 2, 4 )
    z = Poly( 0, 4, 1, -3, 0 )
    a = Poly( 0 )
    b = Poly( -1, 1, 1, 1, 1, 1 )
    c = Poly( 17, 0, 0, 0, 0, -1, 1, 1, 1, 1, 1 )

    assert str( x ) == "2x³ + 7x² + 3x + 5", str( x )
    assert str( y ) == "2x + 4", str( y )
    assert str( z ) == "4x³ + x² - 3x", str( z )
    assert str( a ) == "0", str( a )
    assert str( b ) == "-x⁵ + x⁴ + x³ + x² + x + 1", str( b )
    assert str( c ) == "17x¹⁰ - x⁵ + x⁴ + x³ + x² + x + 1", str( c )

    assert str( x + a ) == "2x³ + 7x² + 3x + 5"
    assert str( a + a ) == "0"

    assert str( x + y ) == "2x³ + 7x² + 5x + 9"
    assert str( y + x ) == str( x + y )

    assert str( x + z ) == "6x³ + 8x² + 5"
    assert str( z + x ) == str( x + z )

    assert str( y + z ) == "4x³ + x² - x + 4"
    assert str( z + y ) == str( y + z )

    z_neg = Poly( 0, -4, -1, 3, 0 )
    assert str( z_neg + z ) == "0"

if __name__ == "__main__":
    test_main()
