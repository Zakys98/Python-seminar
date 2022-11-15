from typing import List
import hypothesis
import hypothesis.strategies as s

# Write a function, ‹search›, which takes an item and a «sorted»
# list of integers and returns a ‹bool› indicating whether the item
# was present in the list. Implement it using binary search.

def search( needle, haystack ): pass

# As before, make sure the ‹search› predicate is correct. Write some
# tests by hand and then write a hypothesis check. Which do you
# reckon is easier and which harder?

def check_search_manual( part ): pass
def check_search_auto( part ): pass

def test_self() -> None:
    check_search_manual( search )
    check_search_auto( search )

def test_bad() -> None:
    def bad_1( item: int, items: List[ int ] ) -> bool:
        return True

    def bad_2( item: int, items: List[ int ] ) -> bool:
        return False

    def bad_3( item: int, items: List[ int ] ) -> bool:
        return item not in items

    def bad_4( item: int, items: List[ int ] ) -> bool:
        low, high = 0, len( items ) - 1
        mid = 0

        print( 'bad_4', item, items )
        while low <= mid <= high:
            mid = ( low + high ) // 2
            if mid == high:
                break
            if items[ mid ] < item:
                low = mid + 1
            if items[ mid ] > item:
                high = mid
            if items[ mid ] == item:
                return True

        return items[ mid ] == item if 0 <= mid < len( items ) else False

    def bad_5( item: int, items: List[ int ] ) -> bool:
        low, high = 0, len( items )
        mid = 0

        print( 'bad_5', item, items )
        while low <= mid <= high:
            mid = ( low + high ) // 2
            if mid == low:
                break
            if items[ mid ] < item:
                low = mid
            if items[ mid ] > item:
                high = mid - 1
            if items[ mid ] == item:
                return True

        return items[ mid ] == item

    failed = True

    for bad in [ bad_1, bad_2, bad_3, bad_4, bad_5 ]:
        try:
            check_search_auto( bad )
            failed = False
        except AssertionError: pass
        assert failed

        try:
            check_search_manual( bad )
            failed = False
        except AssertionError: pass
        assert failed


if __name__ == '__main__':
    test_self()
    print( 'as usual, ignore the falsifying examples' )
    test_bad()
