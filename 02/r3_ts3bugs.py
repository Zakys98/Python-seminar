# Let's pick up where ‹p3_ts3render› left off. It turns out that the
# original system had a bug, where a template could look like this:
# ‹${foo.bar}.baz}› – if ‹${foo.bar}› referenced a template and
# «that» template ended with ‹${quux› (notice all the oddly
# unbalanced brackets!), the system would then paste the strings to
# get ‹${quux.baz}› and proceed to perform that substitution.
#
# The real clincher is that template authors started to use this as
# a feature, and now we are stuck with it. Replicate this
# functionality. However, make sure that this does «not» happen when
# the «first» part of the pasted substitution comes from a document!
#
# The original bug would still do the substitution if the second
# part was a document and not a template. Feel free to replicate
# that part of the bug too.  As far as anyone knows, the variant
# with template + document is not abused in the wild, so it is also
# okay to fix it.

# Now the other part. If you encounter nested templates while
# parsing the path, first process the innermost substitutions,
# resolve the inside path and append the path to the outer one, then
# continue resolving the outer path.
#
# Example: ‹${path${inner.tpl}}›, first resolve ‹inner.tpl›, append
# the result after ‹path›, then continue parsing. If the ‹inner.tpl›
# path leads to a document with text ‹.outside.2›, the outer path is
# ‹path.outside.2›.


