# Assume a non-empty tree with nodes labelled by unique integers:
#
#             ┌───┐
#             │ 1 │
#             └───┘
#          ╭───╯ ╰─────╮
#          ▼           ▼
#        ┌───┐       ┌───┐
#        │ 2 │       │ 3 │
#        └───┘       └───┘
#    ╭────╯│╰────╮     │
#    │     │     │     │
#    ▼     ▼     ▼     ▼
#  ┌───┐ ┌───┐ ┌───┐ ┌───┐
#  │ 4 │ │ 5 │ │ 6 │ │ 7 │
#  └───┘ └───┘ └───┘ └───┘
#
# We can store such a tree in a dictionary like this:


def example_tree():
    return {1: [2, 3],
            2: [4, 5, 6],
            3: [7],
            4: [], 5: [], 6: [], 7: []}


# Keys are node numbers while the values are lists of their (direct)
# descendants. Write a function which computes a few simple
# statistics about the widths of individual levels of the tree (a
# level is the set of nodes with the same distance from the root;
# its width is the number of nodes in it). Return a tuple of
# average, median and maximum level width.

def breadth(tree):
    pass


def test_main():
    from math import isclose

    avg, med, maxi = breadth( example_tree() )
    assert isclose( avg, 7/3 )
    assert med == 2
    assert maxi == 4

    avg, med, maxi = breadth( { 1:[] } )
    assert avg == 1
    assert med == 1
    assert maxi == 1

    tree = {1: [2],
            2: [3,4],
            3: [],
            4: [5,6],
            5: [7],
            6: [8],
            7: [9,10],
            8: [11],
            9: [],
            10: [12],
            11: [],
            12: []}
    avg, med, maxi = breadth( tree )
    assert isclose( avg, 12/7 )
    assert med == 2
    assert maxi == 3

if __name__ == "__main__":
    test_main()
