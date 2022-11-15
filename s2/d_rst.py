# This task is based on the splay tree from ‹s1/b_splay›. The
# changes are aimed at making the tree useful in low-latency
# applications: all operations become coroutines which must perform
# at most a constant amount of work between yields. This way, if the
# application needs to attend to other tasks while a lengthy splay
# is ongoing, it can simply keep the coroutine suspended. At any
# point of execution, the time until the next suspend is bounded by
# a constant, giving us a worst-case latency guarantee (i.e. the
# data structure is, in principle, suitable for hard-realtime
# systems).
#
# To achieve the required properties, the tree needs to use top-down
# splaying, where the lookup is performed as part of the splay.
# Resources describing the top-down splay operation can be found
# here: ‹https://www.link.cs.cmu.edu/splay/› (including pseudocode¹
# and a C implementation of the operation). Here is my own
# description of the top-down splay operation:
#
#  • set up 2 subtrees, initially both empty, called ‹l› and ‹r›,
#  • there are 3 or 4 helper functions:
#    ◦ ‹link_left›, which takes a subtree and hangs it onto ‹l›
#      using the «rightmost» link (i.e. as the right child of the
#      bottom-right node) – you must maintain a pointer to that
#      bottom-right node, to ensure ‹link_left› runs in O(1),
#    ◦ ‹link_right›, which is the mirror image of ‹link_left›,
#    ◦ the usual ‹rotate› (with two nodes as arguments, or possibly
#      split into ‹rotate_left› and ‹rotate_right›);
#  • repeat until not interrupted:
#    ◦ if the value belongs into the «left-left» subtree of the
#      current root, ‹rotate› the root with its left child (if this
#      child exists) [first step of the zig-zig case],
#    ◦ if the «new root» lacks its «left» child, break the loop,
#    ◦ if the value belongs to the «left» subtree, perform
#      ‹link_right› on the root and shift the root pointer to its
#      «right» child [completes the zig-zig, or performs a
#      simplified zig-zag],
#    ◦ the «right-right» and «right» cases are mirror images of the
#      same.
#  • reassemble the tree:
#    ◦ perform ‹link_left› on the left child of the current root,
#    ◦ ‹link_right› on its right child,
#    ◦ attach ‹l› and ‹r› to the root, ‹l› as the left and ‹r› as
#      the right child (replacing the now invalid links).
#
# Remaining operations (‹find›, ‹insert› and ‹erase›) must perform
# all operations that are not O(1) by splaying the tree (and yield
# to the caller whenever the splay operation yields). The ‘splay
# maximum to the top’ operation (needed for erase) can be
# implemented by repeatedly ‘splaying to the right’ (in the sense of
# ‹splay( root.right.value )›, though of course taking 2 steps at a
# time will leave the tree in a significantly better shape),
#
# The splay itself proceeds in a standard manner, except that after
# each step (zig, zig-zag, or zig-zig as appropriate), it yields the
# key of the new root. If the result of that yield is ‹None› (as
# happens when simply iterating the coroutine), the splay continues
# as usual. If it is anything else (delivered via ‹send›), the tree
# is reassembled into a consistent state (this must still happen in
# constant time!) and the operation is aborted.
#
# The code to perform tree operations looks like this:
#
#     for _ in tree.insert( 7 ): pass
#     for _ in tree.erase( 3 ): pass
#     for _ in tree.filter( pred ): pass
#     for x in tree.find( 5 ):
#         if x == 5:
#             found()
#
# Finally, the ‹to_list› operation is replaced by an iterator. This
# iterator is the only exception to the O(1) latency bound – it
# should not use ‹splay›. Instead, it should implement standard
# in-order traversal of the tree (i.e. yielding the keys stored in
# the tree in sorted order). It must be possible to have multiple
# simultaneously-active iterators over a single tree. All iterators
# however become invalid upon invocation of any of the remaining 4
# operations. (Note: it is possible to implement an O(1)-latency
# iterator with a standard interface, but not one that also iterates
# the tree in sorted order.)

# ¹ Please note that if you use the pseudo-code from the Sleator &
#   Tarjan paper, you need to be careful about parallel assignment –
#   in Python, it does not have the semantics intended by the
#   authors and you will need to write it out in multiple steps.
