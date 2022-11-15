# In this task, you will extend ‹s1/a_while› with pointers and
# garbage collection. The syntax is unchanged, except for addition
# of 3 new operations:
#
#  • ‹addr_ = set addr val› takes the value from variable ‹val› and
#    stores it at the address ‹addr›; the result is ‹addr› shifted
#    one cell to the right,
#  • ‹val = get addr off› loads the value from address ‹addr + off›
#    and stores it in ‹val›,
#  • ‹addr = alloc count init› allocates a new object with ‹count›
#    cells; all the cells are set to the value of variable ‹init›.
#
# The memory available to the program is a fixed-size array of cells
# (its size is given to the interpreter at the start). It is an
# error if the program attempts to allocate more memory than it has
# available.
#
# However, if the total size of reachable objects never exceeds that
# of the fixed-size memory, the program «must not» die with an
# out-of-memory error. A reachable object is one that the program
# can, at least in principle, read using a ‹get› operation (‘in
# principle’ means, in this case, that the program might need to
# execute an arbitrary sequence of operations to read the memory –
# even if the sequence doesn't actually appear in the program).
#
# Addresses are treated as a distinct data type from numbers:
#
#  • the first argument of ‹get› and ‹set› must be a number,
#  • new addresses are created by ‹alloc›,
#  • adding a number and an address results in an address iff the
#    result is within the bounds of the same object as the original
#    address (same limitation applies to the result of ‹set›),
#  • an address may be stored in memory using ‹set›, and will still
#    be an address if it is later retrieved by ‹get›,
#  • the numeric values of addresses are unspecified, except that:
#    ◦ addresses of different objects always compare unequal,
#    ◦ addresses within the same object compare reasonably (higher
#      offsets are greater),
#    ◦ addresses always evaluate as ‹true› in ‹while› or ‹if›, or when
#      used as an operand in a logical operator,
#  • the result of any other operation is a number (if any addresses
#    appear as operands, the result will depend on their unspecified
#    numeric values).
#
# New semantic errors (compared to ‹s1/a_while›) – these are all
# reported at «runtime» i.e. when the offending operation executes:
#
#  • passing a number (i.e. not an address) as a first argument of
#    ‹get› or ‹set›, or an address as the first argument to ‹alloc›
#    or as a second argument to ‹get›,
#  • adding the address and the offset passed to ‹get› is out of
#    bounds of the object into which the address originally pointed,
#  • memory allocation which would exceed the permitted memory size.
#
# The error reporting mechanism is otherwise unchanged. An example
# program:
#
#     one = 1
#     two = 2
#     off = 2
#     x = alloc off two
#     while off
#      off = sub off one
#      y = get x off
#      z = add z y
#
# The interpreter shall be available via ‹do_ptr› with the program
# and the memory size in cells as arguments, and a dictionary of
# variables as the result.
