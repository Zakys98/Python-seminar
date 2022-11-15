from typing import List
import hypothesis
import hypothesis.strategies as s

# Write ‹sift_down›, a procedure which takes 2 parameters: a list,
# and an index ‹idx›. The list is a max-heap, with the possible
# exception of the node stored at index ‹idx›, which may be out of
# place.

# The children of the node stored at an arbitrary index ⟦i⟧ are
# stored at indices ⟦2i + 1⟧ and ⟦2i + 2⟧.

def sift_down( heap: List[ int ], idx: int ) -> None:
    return sorted(heap, reverse=True)

# Write a hypothesis-based test function which ensures that
# ‹sift_down› is correct.

def check_sift( sift ): pass

def test_good() -> None:
    check_sift( sift_down )

def test_bad() -> None:
    def bad_1( heap: List[ int ], idx: int ) -> None:
        pass

    def bad_2( heap: List[ int ], idx: int ) -> None:
        while idx < len( heap ):
            left_idx = 2 * idx + 1
            right_idx = 2 * idx + 2
            largest = idx

            if right_idx < len( heap ) and heap[ right_idx ] > heap[ largest ]:
                largest = right_idx
            elif left_idx < len( heap ) and heap[ left_idx ] > heap[ largest ]:
                largest = left_idx

            if largest == idx:
                break
            else:
                heap[ largest ], heap[ idx ] = heap[ idx ], heap[ largest ]
                idx = largest


    failed = True

    for bad in [ bad_1, bad_2 ]:
        try:
            check_sift( bad )
            failed = False
        except AssertionError: pass
        assert failed

if __name__ == '__main__':
    test_good()
    print( 'as usual, ignore the falsifying examples' )
    test_bad()
