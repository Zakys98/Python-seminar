from typing import TypeVar, List, Callable, Tuple

T = TypeVar( 'T' )

# Write a function, ‹partition›, which takes a predicate and a list
# and returns a pair of lists: one with items that pass the
# predicate (like filter) and the other with items which don't.

def partition( predicate, items ): pass

# Then write tests using ‹hypothesis› that show a given
# implementation of ‹partition› works as expected.

def check_partition( part ): pass

def test_self() -> None:
    check_partition( partition )

def test_bad() -> None:
    def bad_1( predicate: Callable[ [ T ], bool ],
               items: List[ T ] ) -> Tuple[ List[ T ], List[ T ] ]:
        return ( items, [] )

    def bad_2( predicate: Callable[ [ T ], bool ],
               items: List[ T ] ) -> Tuple[ List[ T ], List[ T ] ]:
        return ( [], items )

    def bad_3( predicate: Callable[ [ T ], bool ],
               items: List[ T ] ) -> Tuple[ List[ T ], List[ T ] ]:
        return ( list( filter( predicate, items ) ),
                 list( filter( predicate, items ) ) )

    def bad_4( predicate: Callable[ [ T ], bool ],
               items: List[ T ] ) -> Tuple[ List[ T ], List[ T ] ]:
        return ( [], [] )

    def bad_5( predicate: Callable[ [ T ], bool ],
               lst: List[ T ] ) -> Tuple[ List[ T ], List[ T ] ]:
        return ( [ x for i, x in enumerate( lst ) if i % 2 == 1 ],
                 [ x for i, x in enumerate( lst ) if i % 2 == 0 ] )

    failed = True

    for bad in [ bad_1, bad_2, bad_3, bad_4, bad_5 ]:
        try:
            check_partition( bad )
            failed = False
        except AssertionError: pass
        assert failed


if __name__ == '__main__':
    test_self()
    print( 'as usual, ignore the falsifying examples' )
    test_bad()
