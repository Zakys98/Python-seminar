# Dictionaries (associative arrays) are another basic (and very
# useful) data structure. Literals are written using curly braces,
# with colons separating keys from values and commas separating
# multiple key-value pairs from each other:

a_dict = { 1: 1, 2: 7, 3: 1 }

# In Python, dictionaries are implemented as hash tables. This gives
# constant expected complexity for most single-item operations
# (insertion, lookup, erase, etc.). One would expect that this also
# means that dictionaries are unordered, but this is not quite so
# (details some other day, though).

# Like lists, dictionaries are «mutable»: you can add or remove
# items, or, if the values stored in the dictionary are themselves
# mutable, update those. However, «keys» cannot be changed, since
# this would break the internal representation. Hence, only
# «immutable» values can be used as keys (or, to be more precise,
# only «hashable» values – another thing to deal with later).

# Most operations on items in the dictionary are written using
# subscripts, like with lists. Unlike lists, the keys don't need to
# be integers, and if they are integers, they don't need to be
# contiguous. To update a value associated with a key, use the
# assignment syntax:

a_dict[ 1 ] = 2
a_dict[ 337 ] = 1

# To iterate over key-value pairs, use the ‹items()› method:

a_list = []

for key, value in a_dict.items():
    a_list.append( key )

# You can ask (efficiently) whether a key is present in a dictionary
# using the ‹in› operator:

assert 2 in a_dict
assert 4 not in a_dict

# Side note: ‹assert› does what you would expect it to do; just make
# sure you do «not» write it like a function call, with parentheses
# – that will give you unexpected results if combined with a comma.

# Again, like with lists, we will encounter dictionaries pretty
# often, so you will get acquainted with their methods soon enough.

def test_values():
    assert a_dict == { 1: 2, 2: 7, 3: 1, 337: 1 }
