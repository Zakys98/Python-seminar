from typing import List
import hypothesis
import hypothesis.strategies as s

# Write a procedure which sorts the input list and removes any
# duplicated entries (in place).

def sort_uniq( items ): pass

# Write a hypothesis-based test function which ensures a given
# sort-uniq procedure is correct.

def check_sort( sort ): pass

def test_good() -> None:
    check_sort( sort_uniq )

def test_bad() -> None:
    def bad_1( items: List[ int ] ) -> None:
        pass

    def bad_2( items: List[ int ] ) -> None:
        import random
        random.shuffle( items )

    def bad_3( items: List[ int ] ) -> None:

        if len( items ) > 5: # not worth checking for short lists
            is_sorted = True

            for i in range( len( items ) - 1 ):
                if items[ i ] <= items[ i + 1 ]:
                    is_sorted = False

            if is_sorted:
                return

        result: List[ int ] = []

        for i in range( len( items ) ): # select sort
            min_idx = i
            for j in range(i + 1, len( items ) ):
                if items[min_idx] > items[j]:
                    min_idx = j
            items[ i ], items[ min_idx ] \
                = items[ min_idx ], items[ i ]
            if not result or items[ i ] != result[ -1 ]:
                result.append( items[ i ] )

        items.clear()
        items.extend( result )

    def bad_4( items: List[ int ] ) -> None:
        result: List[int] = []

        for i in range( len( items ) ): # select sort
            min_idx = 0

            for idx, item in enumerate( items ):
                if result and item <= result[ -1 ]:
                    continue
                if items[ min_idx ] > items[ idx ]:
                    min_idx = idx

            if not result or items[ min_idx ] != result[ -1 ]:
                result.append( items[ min_idx ] )

        items.clear()
        items.extend( result )

    def bad_5( items: List[ int ] ) -> None:
        items.sort()

    failed = True

    for bad in [ bad_1, bad_2, bad_3, bad_4, bad_5 ]:
        try:
            check_sort( bad )
            failed = False
        except AssertionError: pass
        assert failed

if __name__ == '__main__':
    test_good()
    print( 'as usual, ignore the falsifying examples' )
    test_bad()
