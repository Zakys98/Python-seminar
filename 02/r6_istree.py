from __future__ import annotations

# We define a standard binary tree:

class Tree:
    def __init__( self ) -> None:
        self.left  : Optional[ Tree ] = None
        self.right : Optional[ Tree ] = None

# However, not all structures built from the above data type are
# necessarily trees, since it's possible to create cycles. Write a
# predicate, ‹is_tree›, which decides if a given instance is
# actually a tree (i.e. it does not contain an «undirected» cycle).

def is_tree( tree ):
    pass

def test_basic() -> None:
    r = Tree()
    r.left = Tree()
    r.right = Tree()

    assert is_tree( r )

    r.left.left = Tree()
    r.right.left = Tree()

    assert is_tree( r )

    r.right.right = Tree()
    r.right.left = Tree()

    assert is_tree( r )

    r.left.left.left = r.right

    assert not is_tree( r )

    r.left.left.left = r.left.left

    assert not is_tree( r )


if __name__ == '__main__':
    test_basic()
