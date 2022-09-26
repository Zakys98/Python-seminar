# In this unit (and most future units), we will add static type
# annotations to our programs, to be checked by ‹mypy›. Annotations
# can be attached to variables, function arguments and return types.
# In ‹--strict› mode (which we will be using), ‹mypy› requires that
# each function header (arguments and return type) is annotated.
# e.g. the function ‹divisor_count› takes a single ‹int› parameter
# and returns another ‹int›:

def divisor_count( n: int ) -> int:
    count = 0
    for i in range( 1, n + 1 ):
        if n % i == 0:
            count += 1
    return count

def test_divcount() -> None:
    assert divisor_count( 5 )  == 2 # 1 and 5
    assert divisor_count( 6 )  == 4 # 1, 2, 3 and 6
    assert divisor_count( 12 ) == 6 # 1, 2, 3, 4, 6 and 12

# For more complex types, we need to import some helper classes from
# module ‹typing› (those will be mentioned when they are required;
# probably the most common is ‹Optional›, with ‹Union› a far
# second). For most built-in types, we will use the actual builtins
# for annotations (this works from Python 3.9 onwards).

# Many of these types are «generic», i.e. they have one or more
# «type parameters». You know these from Haskell (they are
# everywhere) or perhaps C++/Java/C# (templates and generics,
# respectively). Like in Haskell but unlike in C++, generic types
# have no effect on the code itself – they are just annotations.
# Type parameters are given in square brackets after the generic
# type.

def divisors( n: int ) -> list[ int ]:

    # For local variables, ‹mypy› can usually deduce types
    # automatically, even when they are of a generic type. However,
    # sometimes this fails, a prominent example being the empty list
    # – it's impossible to find the type parameter, since there are
    # no values to look at. Annotations of local variables can be
    # combined with initialization.

    res: list[ int ] = []

    for i in range( 1, n + 1 ):
        if n % i == 0:
            res.append( i )

    return res

def test_divisors() -> None:
    assert divisors( 5 )  == [ 1, 5 ]
    assert divisors( 6 )  == [ 1, 2, 3, 6 ]
    assert divisors( 12 ) == [ 1, 2, 3, 4, 6, 12 ]


# TBD: Examples for ‹Optional› and ‹Union›.
