from __future__ import annotations
from typing import TypeVar, Callable, Union, Protocol, Any


class SupportsLessThan(Protocol):
    def __lt__(self: K, other: K) -> bool: ...


K = TypeVar('K', bound=SupportsLessThan)
V = TypeVar('V')
W = TypeVar('W')

# Write a function ‹merge_dict› which takes these 3 arguments:
#
#  • a ‹dict› instance, in which some keys are deemed equivalent:
#    the goal of ‹merge_dict› is to create a new dictionary, where
#    all equivalent keys have been merged; keys which are not
#    equivalent to anything else are left alone (though the single
#    value is still passed through ‹combine›),
#  • a ‹list› of ‹set› instances, where each ‹set› describes one set
#    of equivalent keys (the sets are pairwise disjoint), and
#    finally,
#  • a function ‹combine› which takes a ‹list› of values (not a set,
#    because we may care about duplicates): ‹merge_dict› will pass,
#    for each set of equivalent keys, all the values corresponding to
#    those keys into ‹combine›.
#
# In the output dictionary, create a single key for each equivalent
# set:
#
#  • the key is the «smallest» of the keys from the set which were
#    actually present in the input ‹dict›,
#  • the value is the result of calling ‹combine› on the list of
#    values associated with all the equivalent keys in the input
#    ‹dict›.
#
# Do not modify the input dictionary.


def merge_dict(dict_in: dict[K, V],
               equiv: list[set[K]],
               combine: Callable[[list[V]], W]) \
        -> dict[K, W]:
    output: dict[K, W] = dict()
    used = []
    for set in equiv:
        use = []
        for key in dict_in:
            if key in set:
                used.append(key)
                use.append(key)
        value = combine([dict_in[key] for key in dict_in if key in set])
        if len(use) == 0:
            continue
        output[min(use)] = value
    for key in dict_in:
        if key not in used:
            output[key] = combine([dict_in[key]])
    return output


def test_a() -> None:
    def combine(x): return sum(x)
    dict_in = {1: 1, 2: 2, 3: 3, 4: 4, 5: 1, 6: 2, 7: 3}
    eq = [set([1, 3, 5, 7]), set([2, 4, 6])]

    dict_orig = dict_in.copy()
    merged = merge_dict(dict_in, eq, combine)
    assert merged == {1: 8, 2: 8}, merged
    assert dict_in == dict_orig
    merged = merge_dict({0: 0, -1: 0}, [{0, -1}], combine)


def test_b() -> None:
    def combine(x: list[str]) -> int:
        return sum([len(s) for s in x])

    dict_in = {2: 'two', 3: 'three', 6: 'two', 1: 'one', 9: 'woo'}
    eq = [set([2]), set([3, 6, 1])]

    dict_orig = dict_in.copy()
    assert merge_dict(dict_in, eq, combine) == {2: 3, 1: 11, 9: 3}
    assert dict_in == dict_orig


def test_c() -> None:
    def combine(x): return "".join([str(y) for y in x])
    dict_in: dict[Union[int, str], Union[int, str]]
    dict_in = {1: 9, 8: "eek", "ef": 22}
    eq: list[set[Union[str, int]]] = []

    dict_orig = dict_in.copy()
    expect = {1: "9", 8: "eek", "ef": "22"}
    assert merge_dict(dict_in, eq, combine) == expect
    assert dict_in == dict_orig


def test_d() -> None:
    from copy import deepcopy

    dict_in = {"ab": {7: 33, 9: 1, 13: 45}, "abcde": {3: 9, 0: 5, -1: 4},
               "foo": {1: 3, 91: 3, 4: 3, 5: -1, 8: 4}, "val": {6: 7}}
    eq_out = [set(["ab", "abcde", "val"])]
    eq_in = [set([1, 91, 8, 6]), set([3, 7, 9, -1]), set([0])]

    dict_orig = deepcopy(dict_in)

    # list of dictionaries into one dictionary
    def flatten(x: list[dict[K, V]]) -> dict[K, V]:
        d = {}
        for dic in x:
            d.update(dic)
        return d

    def combine(x): return merge_dict(flatten(x), eq_in, lambda y: sum(y))

    expect = {"ab": {13: 45, -1: 47, 0: 5, 6: 7},
              "foo": {1: 10, 4: 3, 5: -1}}
    res = merge_dict(dict_in, eq_out, combine)
    assert res == expect, res
    assert dict_in == dict_orig


if __name__ == "__main__":
    test_a()
    test_b()
    test_c()
    test_d()
