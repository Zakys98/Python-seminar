# Implement suffix list and suffix sum as a generator, with an
# arbitrary ‹Sequence› as an input.
#
# Examples:
#
#     suffixes( [ 1, 2 ] )      # [] [ 2 ] [ 1, 2 ]
#     suffix_sum( [ 1, 2, 3 ] ) # [ 3, 5, 6 ]

def suffixes( list_in ):
    pass

def suffix_sum( list_in ):
    pass

def test_main() -> None:

    res = [ [], [ 7 ], [ 8, 7 ], [ 6, 8, 7 ], [ 5, 6, 8, 7 ] ]

    for i in suffixes( [ 5, 6, 8, 7 ] ):
        assert i in res
        res.remove( i )

    assert not res # emptied

    lst = [ 1, 2, 3, 4, 5 ]
    res = [ 5, 9, 12, 14, 15 ]
    dbl = [ 15, 29, 41, 50, 55 ]

    assert list( suffix_sum( lst ) ) == res
    assert list( suffix_sum( suffix_sum( lst ) ) ) == dbl

if __name__ == "__main__":
    test_main()
