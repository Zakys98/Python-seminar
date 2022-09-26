# While not normally thought of as a data type, «functions» are an
# important category of entities that appear in programs. As will
# eventually become apparent, in Python, we would be justify to also
# call them «objects» (in other languages with first-class objects,
# this could be a bit confusing).
#
# Functions are defined using the ‹def› keyword, or using the
# ‹lambda› keyword. The main difference is that the former is a
# «statement» while the latter is an «expression» (the other
# difference is that the former has a name, unlike the latter). The
# main thing that you can do with functions (other than defining
# them) is «calling» them. The mechanics of this are essentially the
# same in Python as in any other programming language that you may
# know.  Frames (invocation records) are kept on a «call stack»,
# calling a function creates a new such record and returning from a
# function destroys its frame¹ and continues executing the caller
# where it left off.
#
# As the existence of ‹lambda› foreshadows, we will be able to
# create functions within other functions and get «closures». That
# will be our main topic the week after the next. For now, we will
# limit ourselves to «toplevel» functions (we will see «methods»
# next week).
#
# The one possible remaining question is, what about arguments and
# return values? Let's define a function and see how that goes:

def foo( x ):
    x[ 0 ] = 1
    return x[ 1 ]

# One conspicuous aspect of that definition is the absence of «type
# annotations». We will address that next week – for now, we will
# treat Python like the dynamic language it is. Anything goes, as
# far as it works out at runtime. So how can we call ‹foo›? It
# clearly expects a list (or rather something that we can index, but
# a list will do) with at least 2 items in it.

a_list = [ 3, 2, 1 ]
two = foo( a_list )

# Now depending on the argument passing mechanism, we can either
# expect ‹a_list› to remain unchanged (with items 3, 2, 1) or to be
# changed by the function to ‹[ 1, 2, 1 ]›. You are probably aware
# that in Python it is the second case. In fact, argument passing
# is the same as «binding»: the «cells» (objects) of the «actual
# arguments» are bound to the «names» of the «formal arguments».²
# That's all there is to it.

assert a_list == [ 1, 2, 1 ]

# However, you might be wondering about the following:

def bar( x ):
    x = 1

a_int = 3
bar( a_int )

# If you think in terms of «bindings», this should be no surprise.
# If you instead think in terms of ‘pass by reference’, you might
# have expected to find that ‹a_int› is ‹1› after the call. This is
# a mistake: if ‹3› was passed ‘by reference’ into ‹bar›, the ‹=›
# operator behaves unexpectedly. Again, if you remember that ‹=› is
# «binding» (as long as left-hand side is a name, anyway), it is
# clear that within ‹bar›, the name ‹x› was simply bound to a new
# value. To wit:

assert a_int == 3

# To drive the point home, let's try the same thing with a list:

def baz( x ):
    x[ 0 ] = 2
    x = [ 3, 2, 1 ]
    x[ 0 ] = 1

b_list = [ 3, 3, 3 ]
baz( b_list )

# Now we have 3 possible outcomes to consider:
#  • ‹[ 3, 3, 3 ]› – we can immediately rule this out based on the
#    above,
#  • ‹[ 2, 3, 3 ]› – this would be consistent with all of the above,
#  • ‹[ 1, 2, 1 ]› – if ‹int› was actually handled differently from
#    lists (spoiler: it isn't).³

assert b_list == [ 2, 3, 3 ]

# We can demonstrate that all types of objects are treated the same
# quite easily using ‹id›, which returns the address of an object,
# and an ‹int› object:

x = 2 ** 100
y = 2 ** 101

assert id( x ) == id( x )
assert id( x ) != id( y )

z = x
assert id( z ) == id( x )
z = y
assert id( z ) == id( y )

# So how do we check what is passed to a function? If the object is
# the same on the inside and the outside, ‹id› will return the same
# value n both cases. Observe:

def check_id( x, id_x ):
    assert id( x ) == id_x

check_id( x, id( x ) )

# ¹ This is a simplification, as we will see two weeks from now.
#   Like many dynamic languages, Python allocates frames in the
#   garbage-collected ‘heap’ and they are reclaimed by the collector
#   (which would normally mean by reference count – so after all,
#   they usually do get destroyed immediately… we will talk about
#   this too, eventually).

# ² You will probably encounter this being labelled as ‘call by
#   reference’. This is not a great name for what is happening, but
#   it's less bad than some of the other common misconceptions about
#   function calls in Python. If you want to think of argument
#   passing as being ‘by reference’, try to remember that
#   «everything» is passed ‘by reference’ in this sense (mutable and
#   immutable values alike).

# ³ You might have read on the internet, or heard, that Python passes
#   ‘immutable values by value and mutable by reference’. This is
#   «not the case» (in fact, it could reasonably be called
#   nonsense).
