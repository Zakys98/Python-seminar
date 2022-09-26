# Internally, tuples are immutable lists. The main difference in the
# implementation is that being immutable, tuples have a fixed number
# of elements. However, there are important «use case» differences:
# lists are «usually» homogeneous, with an arbitrary (unknown ahead
# of time) number of elements. Even when heterogeneous, they usually
# hold related types. Syntactically, tuples are written into
# parentheses and separated by commas. In many cases, the
# parentheses are optional, though. A one-tuple is denoted by a
# trailing comma,¹ while an empty tuple is denoted by empty
# parentheses (in this case, they cannot be omitted).

a_tuple = ( 1, 2, 3 )
b_tuple = 1, 2, 3 # same thing
c_tuple = ()      # empty tuple / zero-tuple
d_tuple = ( 1, )  # one-tuple
e_tuple = 1,      # also one-tuple

# Tuples are «usually» the exact opposite of lists: fixed number of
# elements, but each element of possibly different type. This is
# reflected by the way they are constructed, but even more so in the
# way the are «used». Lists are indexed and iterated (using ‹for›
# loops), or possibly filtered and mapped when writing
# functional-style code.
#
# Tuples are rarely iterated and even though they are sometimes
# indexed, it's a «very bad practice» and should be avoided
# (especially when indexing by constants). Instead, tuples should
# be «destructured» using tuple binding:

a_int, b_int, c_int = a_tuple

# As you might expect, ‹a_int›, ‹b_int› and ‹c_int› are newly bound
# variables with values ‹1›, ‹2› and ‹3›.
#
# ¹ This is a bit of a nuisance, actually, since leaving an
#   accidental trailing comma on a line will quietly wrap the value
#   in a one-tuple.
