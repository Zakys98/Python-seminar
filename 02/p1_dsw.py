from __future__ import annotations
from typing import Optional, Protocol, Any, TypeVar, Set
import math

# Since a search tree must be ordered, we need to be able to compare
# (order) the values stored in the tree. For that, we need a type
# variable that is constrained to support order comparison
# operators:


class SupportsLessThan(Protocol):
    def __lt__(self: T, other: T) -> bool: ...


T = TypeVar('T', bound=SupportsLessThan)

# Now that ‹T› is defined, you can use it to type your code below;
# values of ‹T› can be compared using ‹<› and equality (but not
# other operators, since we did not explicitly mention them above).

# The actual task: implement the DSW (Day, Stout and Warren)
# algorithm for rebalancing binary search trees. The algorithm is
# ‘in place’ – implement it as a procedure that modifies the input
# tree. You will find suitable pseudocode on Wikipedia, for
# instance.
#
# The constructor of ‹Node› should accept a single parameter (the
# value). Do not forget to type the classes.


class Node:  # add ‹left›, ‹right› and ‹value› attributes
    def __init__(self, value) -> None:
        self.left : Optional[Node] = None
        self.right : Optional[Node] = None
        self.value = value


class Tree:  # add a ‹root› attribute
    def __init__(self, root: Node) -> None:
        self.root = root

def tree_to_vine(root: Node) -> None:
    count = 0
    tmp = root.right
    while tmp is not None:
        if tmp.left is None:
            count += 1
            root = tmp
            tmp = tmp.right
        else:
            old = tmp
            tmp = tmp.left
            old.left = tmp.right
            tmp.right = old
            root.right = tmp
    return count

"""
routine tree-to-vine(root)
// Convert tree to a "vine", i.e., a sorted linked list,
// using the right pointers to point to the next node in the list
tail ← root
rest ← tail.right
while rest ≠ nil
    if rest.left = nil
        tail ← rest
        rest ← rest.right
    else
        temp ← rest.left
        rest.left ← temp.right
        temp.right ← rest
        rest ← temp
        tail.right ← temp
"""

def vine_to_tree(root: Node, number: int) -> None:
    pass

def compress(node: Node, number: int):
    tmp = node.right
    for i in range(0, number):
        old = tmp
        tmp = tmp.right
        node.right = tmp
        old.right = tmp.left
        tmp.left = old
        node = tmp
        tmp = tmp.right

def dsw(tree: Tree) -> T:  # add a type signature here
    pseudo = Node(0)
    pseudo.right = tree.root
    count = tree_to_vine(pseudo)
    h = int(math.log2(count + 1))
    m = int(pow(2, h) - 1)
    compress(pseudo, count - m)
    for i in range(m // 2, m > 0, m // 2):
        compress(pseudo, m)

    return pseudo.right;

"""
routine vine-to-tree(root, size)
    leaves ← size + 1 − 2⌊log2(size + 1))⌋
    compress(root, leaves)
    size ← size − leaves
    while size > 1
        compress(root, ⌊size / 2⌋)
        size ← ⌊size / 2⌋

routine compress(root, count)
    scanner ← root
    for i ← 1 to count
        child ← scanner.right
        scanner.right ← child.right
        scanner ← scanner.right
        child.right ← scanner.left
        scanner.left ← child

"""


def test_random() -> None:
    for i in range(200):
        t, vals = random_tree(12, -1000, 1000)
        dsw(t)
        ok, _, _ = check_ordering(t.root, 0)
        lb, ub = check_balance(t.root, 0)
        vals = check_values(t.root, vals)
        assert not vals, vals
        assert ok
        assert ub - lb <= 1


def check_values(node: Optional[Node[int]],
                 vals: Set[int]) -> Set[int]:
    if node is not None:
        assert node.value in vals
        vals = check_values(node.left,  vals - {node.value})
        return check_values(node.right, vals)
    else:
        return vals


def check_ordering(node: Optional[Node[T]], bound: T) \
        -> tuple[bool, T, T]:

    if node is None:
        return (True, bound, bound)

    l_ok, l_min, l_max = check_ordering(node.left,  node.value)
    r_ok, r_min, r_max = check_ordering(node.right, node.value)

    this_ok = l_ok and r_ok and \
        (node.value == l_max or node.value > l_max) and \
        (node.value == r_max or node.value < r_max)

    return (this_ok, l_min, r_max)


def check_balance(node: Optional[Node[T]], depth: int) \
        -> tuple[int, int]:

    if node is None:
        return (depth, depth)

    lb_l, ub_l = check_balance(node.left,  depth + 1)
    lb_r, ub_r = check_balance(node.right, depth + 1)

    return (min(lb_l, lb_r), max(ub_l, ub_r))


def random_subtree(depth: int, lb: int, ub: int) \
        -> tuple[Optional[Node[int]], Set[int]]:

    if not depth or lb >= ub:
        return None, set()

    from random import randint
    val = randint(lb, ub)
    node: Node[int] = Node(val)

    skip_l = randint(1, max(1, depth // 2))
    skip_r = randint(1, max(1, depth // 2))

    node.left,  l_vals = random_subtree(depth - skip_l, lb, val - 1)
    node.right, r_vals = random_subtree(depth - skip_r, val + 1, ub)
    return node, l_vals | r_vals | {val}


def random_tree(depth: int, lb: int, ub: int) \
        -> tuple[Tree[int], Set[int]]:
    root, vals = random_subtree(depth, lb, ub)
    return Tree(root), vals


if __name__ == '__main__':
    test_random()
