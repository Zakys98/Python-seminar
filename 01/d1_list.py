# In Python, list literals are written in square brackets, with
# items separated by commas, like this:

a_list = [ 1, 2, 3 ]

# Lists are «mutable»: the value of a list may change, without the
# list itself changing identity. Methods like ‹append› and operators
# like ‹+=› update the list in place.

# Lists are internally implemented as arrays. Appending elements is
# cheap, and so is indexing. Adding and removing items at the front
# is expensive. Lists are indexed using (again) square brackets and
# indices start from zero:

one = a_list[ 0 ]

# Lists can be «sliced»: if you put 2 indices in the indexing
# brackets, separated by a colon, the result is a list with the
# range of elements on those indices (the element on the first index
# is included, but the one on the second index is not). The slice is
# «copied» (this can become expensive).

b_list = a_list[ 1 : 3 ]

# You can put pretty much anything in a list, including another
# list:

c_list = [ a_list, [ 3, 2, 1 ] ]

# You can also construct lists using comprehensions, which are
# written like ‹for› loops:

d_list = [ x * 2 for x in a_list if x % 2 == 1 ]

# There are many useful methods and functions which work with lists.
# We will discover some of them as we go along. To see the values of
# the variables above, you can do:
#
#     python -i d1_list.py
#     >>> d_list
#     [2, 6]

def test_values():
    assert a_list == [ 1, 2, 3 ]
    assert one == 1
    assert b_list == [ 2, 3 ]
    assert c_list == [ [ 1, 2, 3 ], [ 3, 2, 1 ] ]
    assert d_list == [ 2, 6 ]
