# Implement the following functions:
#
# • ‹sort_by› (with an order relation)
# • ‹group_by› (with an equivalence relation)
# • ‹nub_by› (likewise)
#
# The order/equivalence relation are callbacks that take two
# elements and return a boolean. The order is given as
# less-or-equal: ‹order( x, y )› means ‹x <= y›.

# The ‹sort_by› function should return a new list, sorted according
# to the order The sort must be stable (i.e. retain the relative
# order of items which compare equal).

# The ‹group_by› function should return a list of lists, where each
# sub-list contains equivalent items. Joining all the sub-lists
# together must yield the original list (i.e. the order of input
# elements is retained). The sub-lists must be as long as possible.

# Finally ‹nub_by› should output a list where each equivalence class
# has at most one representative – the first one that appears in the
# input list. The relative order of items must remain unperturbed.
# In other words, if an item is equivalent (according to the
# provided equivalence relation) to an earlier item, do not include
# the new item in the output.


def sort_by(data, order):
    output = data[:]
    for i, item in enumerate(output):
        for j, change in enumerate(output):
            if order(item, change):
                #print(item)
                ##print(change)
                #if isinstance(item, tuple):
                #    if
                output[i], output[j] = output[j], output[i]
    return output

def group_by(data, eq_rel): pass
def nub_by(data, eq_rel): pass


def test_sort_1() -> None:

    data = [4, 5, 8, 1, 0, 0, 2]
    res = sort_by(data, lambda x, y: y <= x)
    assert res == [8, 5, 4, 2, 1, 0, 0]


def test_sort_2() -> None:
    data = [{'a': 7, 'b': 3, 'c': 10},
            {'a': 17, 'd': 0, 'c': 9},
            {'a': 5, 'e': 0, 'c': -2}]
    res = sort_by(data, lambda x, y: (x['a'] + x['c']) <= (y['a'] + y['c']))
    assert len(res) == 3
    assert all(list(map(lambda x: type(x) == dict, res)))

    assert 'e' in res[0]
    assert 'b' in res[1]
    assert 'd' in res[2]
    assert list(map(lambda x: x['a'] + x['c'], res)) == [3, 17, 26]


def test_stable() -> None:
    data = [(1, 'f'), (2, 'b'), (3, 'c'), (2, 'd'), (1, 'e')]
    res = sort_by(data, lambda x, y: x[0] <= y[0])
    print(res)
    assert res == [(1, 'f'), (1, 'e'), (2, 'b'), (2, 'd'), (3, 'c')]


def test_group_1() -> None:
    data = [1, 5, 9, 10, 2, 4, 2, 2, 5, 7, 3, 2]
    res = group_by(data, lambda x, y: x % 2 == y % 2)
    assert res == [[1, 5, 9], [10, 2, 4, 2, 2],
                   [5, 7, 3], [2]], res


def test_group_2() -> None:
    data = ["abc", "banana", "random", "abduct", "conduct",
            "moon", "sane", "ablaze", "start"]
    res = group_by(data, lambda x, y: x[1] == y[1])
    assert res == [["abc"], ["banana", "random"],
                   ["abduct"], ["conduct", "moon"],
                   ["sane"], ["ablaze"], ["start"]], res


def test_nub_1() -> None:
    data = [1, 5, 2, 0, 9, 10, 2, 4, 3]
    res = nub_by(data, lambda x, y: x % 3 == y % 3)
    assert res == [1, 5, 0]


def test_nub_2() -> None:
    data = ["abc", "banana", "abduct", "random", "conduct",
            "moon", "sane", "ablaze", "start"]
    res = nub_by(data, lambda x, y: x[1] == y[1])
    assert res == ["abc", "banana", "conduct", "start"]


if __name__ == "__main__":
    test_sort_1()
    test_sort_2()
    test_stable()
    test_group_1()
    test_group_2()
    test_nub_1()
    test_nub_2()
