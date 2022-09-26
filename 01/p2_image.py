# You are given a function ‹f› which takes a single integer
# argument, and a list of closed intervals ‹domain›. For instance:
#
#     f = lambda x: x // 2                          # python
#     domain = [ ( 1, 7 ), ( 3, 12 ), ( -2, 0 ) ]
#
# Find the «image» of the set represented by ‹domain› under ‹f›, as
# a list of disjoint, closed intervals, sorted in ascending order.
# Produce the shortest list possible.
#
# Values which are not in the image must not appear in the result.
# For instance, if the image is ⟦{1, 2, 4}⟧, the intervals would be
# ⟦(1, 2), (4, 4)⟧ – not ⟦(1, 4)⟧ nor ⟦(1, 1), (2, 2), (4, 4)⟧.

def image( f, domain ):
    pass

def test_main():
    f = lambda x: x
    g = lambda x: x // 2
    assert image( f, {} ) == []
    assert image( f, [ ( 1, 1 ) ] ) == [ ( 1, 1 ) ]
    assert image( g, [ ( 1, 3 ) ] ) == [ ( 0, 1 ) ]
    assert image( g, [ ( 1, 4 ) ] ) == [ ( 0, 2 ) ]
    assert image( g, [ ( 1, 1 ), ( 7, 8 ) ] ) \
            == [ ( 0, 0 ), ( 3, 4 ) ]
    assert image( g, [ ( 1, 7 ), ( -1, 1 ) ] ) == [ ( -1, 3 ) ]
    assert image( g, [ ( 1, 1 ), ( 3, 4 ) ] ) == [ ( 0, 2 ) ]
    assert image( g, [ ( 7, 7 ), ( 3, 4 ), ( 5, 5 ) ] ) == \
            [ ( 1, 3 ) ]
    assert image( g, [ ( 1, 10 ), ( 100, 200 ), ( 50, 80 ) ] ) == \
            [ ( 0, 5 ), ( 25, 40 ), ( 50, 100 ) ]

if __name__ == "__main__":
    test_main()
