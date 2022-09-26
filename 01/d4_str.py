# The last data type we will look at for now is ‹str›, which
# represents Unicode strings. Unlike lists and dictionaries, but
# quite like integers, strings in Python are «immutable». You can
# construct new strings from old strings, but once a string exists,
# it cannot be updated.

# There are many kinds of string literals in Python, some of them
# quite complicated. The basic variation consists single or double
# quotes (and there is no difference between them, though some
# programmers give them different semantics) enclosing a sequence
# of letters:

a_str = 'some string'

# To access a single character in string, you can index it, like you
# would a list:

b_str = a_str[ 1 ]

# Rather confusingly, the result of indexing a ‹str› is another
# ‹str›, with just one character (code point) in it. In this sense,
# indexing strings behaves more like slicing than real indexing.
# There is no data type to represent a single character (other than
# ‹int›, of course).

# Since strings are immutable, you cannot update them in place; the
# following will not work:

#     a_str[ 1 ] = 'x'

# Also somewhat confusingly, you can use ‹+=› to seemingly mutate a
# string:

a_str += ' duh'

# What happened? Well, ‹+=› can do two different things, depending
# on its left-hand side. If the LHS is a mutable type, it will
# internally call a method on the value to update it. If this is not
# possible, it is treated as the equivalent of:

c_str = 'string'
c_str = c_str + ' …and another'

# which of course builds a new string (using ‹+›, which concatenates
# two strings to make a new one) and then «binds» that new string to
# the name ‹c_str›. We will deal with this in more detail in the
# lecture.

# Important corollaries: strings, being immutable, can be used as
# dictionary keys. Building long strings with ‹+=› is pretty
# inefficient.¹ In essence, even though you can subscript them,
# strings behave more like integers than like lists. Try to keep
# this in mind.

# As with previous two data types, we will encounter quite a few
# methods and functions which work with strings in the course. Also,
# the reference documentation is pretty okay. Use it. The most basic
# way to get to it is using the ‹help› function of the interpreter:
#
#     >>> help('')
#     >>> help({})
#     >>> help([])
#
# Of course, you can also break out the web browser and point it to
# ‹https://docs.python.org/3› (unfortunately, ‹help› and the online
# docs don't always match, and the online docs are often more
# comprehensive; ‹help› is good for a quick overview, but if you
# don't see what you are looking for, refer to the web before
# despairing).

# ¹ CPython being what it is, of course there is a special case in
#   the interpreter for ‹+=› on strings, when the reference count on
#   the left-hand side is 1 (or rather 2, for complicated technical
#   reasons). This even holds for ‹+› «if» it appears in a statement
#   that looks like ‹foo = foo + bar›. Of course, relying on this
#   optimisation is brittle, because you might have an unintended
#   reference to the original, or you may introduce one long after
#   you wrote the code with ‹+=›.

def test_values():
    assert a_str == 'some string duh'
    assert b_str == 'o'
    assert c_str == 'string …and another'
