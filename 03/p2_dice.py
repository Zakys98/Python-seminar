# pragma mypy relaxed

# Typing note: If you decide to use type annotations, be aware that
# they are quite heavy. What's worse, ‹zip_n_with› and ‹chunk_with›
# cannot be typed using ‹Callable› without resorting to ‹Callable[
# ..., X ]› which is just a masked way to use ‹Any›. You have been
# warned (but it's still an interesting exercise to make it type,
# with this limitation in mind).

# The ‹zip_with› function takes 2 lists and a callback and
# constructs a new list from results of applying the callback to
# pairs of items from the input lists (each item from one of the
# lists). Stop when the shorter list runs out.

def zip_with( func, list_1, list_2 ): pass

# The ‹pair_with› function is similar, but only has a single input
# list and applies the callback to consecutive non-overlapping pairs
# of items in this list. Any unpaired items at the end of the list
# are thrown away.

def pair_with( func, items ): pass

# The following two functions are like the above, but work with more
# than 2 items at a time. The lists in the ‹zip› case must be all of
# the same type (to make things typecheck).

def zip_n_with( func, *args ): pass
def chunk_with( func, chunk_size, items ): pass


def test_zip() -> None:
    assert zip_with( lambda x, y: x + y,
                     [ 1, 2, 3 ], [ 3, 2 ] ) == [ 4, 4 ]
    assert zip_with( lambda x, y: x + y,
                     [ 'x' ], [ 'foo', 'bar' ] ) == [ 'xfoo' ]
    assert zip_with( lambda x, y: { x: y },
                     [ 'foo', 'bar' ], [ 1, 2 ] ) == \
        [ { 'foo': 1 }, { 'bar': 2 } ]


def test_pair() -> None:
    assert pair_with( lambda x, y: { x: y }, [ 1, 2, 2, 1 ] ) == \
            [ { 1: 2 }, { 2: 1 } ]
    assert pair_with( lambda x, y: x + y,
                      [ 1, 2, 3, 4, 5 ] ) == [ 3, 7 ]

def test_n_zip() -> None:
    assert zip_n_with( lambda x, y, z: int( x + y + z ),
                       [ 1, 2, 3 ], [ 3, 2 ], [ 1 ] ) == [ 5 ]
    assert zip_n_with( lambda x, y, z: str( x + y + z ),
                       [ 'zz', 'z' ], [ 'x' ],
                       [ 'foo', 'bar' ] ) == [ 'zzxfoo' ]
    assert zip_n_with( lambda x, y, z, u: str( x + y + z ),
                       [ 'zz', 'z' ], [ 'x' ],
                       [ 'foo', 'bar' ], [ '0' ] ) == [ 'zzxfoo' ]

def test_chunk() -> None:
    assert chunk_with( lambda x, y: { x: y }, 2,
                       [ 1, 2, 2, 1 ] ) == [ { 1: 2 }, { 2: 1 } ]
    assert chunk_with( lambda x, y, z: int( x + y + z ), 3,
                      [ 1, 2, 3, 4, 5, 6 ] ) == [ 6, 15 ]


if __name__ == '__main__':
    test_zip()
    test_pair()
    test_n_zip()
    test_chunk()
