from __future__ import annotations

# In this exercise, you will implement the ring ⟦ℤ/nℤ⟧ of integers
# modulo ⟦n⟧. Welcome to abstract algebra: a ring is a set with two
# operations defined on it: addition and multiplication. The
# operations must have some nice properties. Specifically, the set
# we consider in this exercise is the set of all possible remainders
# in the division by ⟦n⟧; you can read up on the necessary axioms on
# e.g. Wikipedia (under `Ring (mathematics)`).

# Interaction of elements in different modulo classes results in a
# ‹TypeError›. When printing, use the notation ⟦[x]ₙ⟧, such as
# ⟦[5]₇⟧ to represent all integers with remainder 5. Implement
# equality, comparison, printing, and the respective addition and
# multiplication (all should also work with plain integer operands
# on either side).

# An instance of ‹Mod› represents a congruence class ⟦x⟧ modulo ⟦n⟧.

class Mod:
    def __init__( self, x: int, n: int ) -> None:
        pass


def test_main() -> None:

    x = Mod( 3, 7 )
    y = Mod( 4, 7 )
    z = Mod( 1, 2 )

    assert str( x )     == "[3]₇", str( x )
    assert str( x + y ) == "[0]₇", str( x + y )
    assert str( 1 + y ) == "[5]₇"
    assert str( 1 * y ) == "[4]₇"
    assert str( y * 1 ) == "[4]₇"
    assert str( x * y ) == "[5]₇"

    try:
        print( x + z ) # TypeError
        assert False
    except TypeError:
        pass

    assert str( x + 1 ) == "[4]₇"
    assert str( y - x ) == "[1]₇"

    assert x == 3
    assert x == x

    try:
        x == z
        assert False
    except TypeError:
        pass

    assert not x == y
    assert not x > y 
    assert x < y

    assert Mod( 1, 7 ) == Mod( 8, 7 )
    assert 1 == Mod( 1, 7 )
    assert 2 != Mod( 1, 7 )

    assert str( Mod( 2, 6 ) - 5 ) == "[3]₆"
    assert str( 5 - Mod( 2, 6 ) ) == "[3]₆"


if __name__ == '__main__':
    test_main()
