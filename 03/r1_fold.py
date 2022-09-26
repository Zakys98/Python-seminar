# pragma mypy relaxed

# Implement ‹foldr›, a function which takes a binary callback ‹f›, a
# list ‹l› and an initial value ‹i›. Use the function ‹f› to reduce
# the list to a single value, from right to left. (Note: this is
# similar, but not the same as ‹functools.reduce›, due to different
# bracketing).

def foldr( f, l, i ): pass

# Now use ‹foldr› to implement the following functions:
#
#  • ‹fold_len› – get the length of a list,
#  • ‹fold_pairs› – create a ‘cons list’ made of pairs, such that
#    ‹[1, 2, 3]› becomes ‹(1, (2, (3, ())))›,
#  • ‹fold_rev› – reverse the input list.
#
# You will probably need ‹Any› to type ‹fold_pairs› (there might be
# ways around it, but they are going to be ugly).

def fold_len( l ): pass
def fold_pairs( l ): pass
def fold_rev( l ): pass


def test_foldr() -> None:
    from math import isclose

    plus = lambda x, y: x + y
    minus = lambda x, y: x - y
    divide = lambda x, y: x / y

    assert foldr( plus, [], -2 ) == -2
    assert foldr( plus, [ 7, 3, 9, -1 ], 2 ) == 20
    assert foldr( minus, [ 7, 3, 9, -1 ], 2 ) == 16
    assert foldr( plus, "aeiou", "y" ) == "aeiouy"
    assert isclose( foldr( divide, [ 9, 12, 6, 6, 8 ], 2 ), 3.0 )

def test_len() -> None:
    assert fold_len( [ 1, 2, 3 ] ) == 3
    assert fold_len( [] ) == 0
    assert fold_len( [ "ar", "er", "ir", "or" ] ) == 4

def test_pairs() -> None:
    assert fold_pairs( [ 1, 2, 3 ] ) == (1, (2, (3, () )))
    assert fold_pairs( [] ) == ()
    assert fold_pairs( [ (1,2), (3,4) ] ) \
                   == ((1,2),((3,4),()))

def test_rev() -> None:
    assert fold_rev( [] ) == []
    assert fold_rev( [ 1, 2, 3 ] ) == [ 3, 2, 1 ]
    assert fold_rev( [ "ar", "er", "ir", "or" ] ) \
                  == [ "or", "ir", "er", "ar" ]

if __name__ == "__main__":
    test_foldr()
    test_len()
    test_pairs()
    test_rev()
