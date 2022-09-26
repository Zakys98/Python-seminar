from doctest import FAIL_FAST
from turtle import right
from typing import Optional, Union, List

# In this exercise, we will evaluate boolean trees, where operators
# are represented as internal nodes of the tree. All of the Node
# types should have an ‹evaluate› method.  Implement the following
# Node types (logical operators): ‹and›, ‹or›, ‹implication›,
# ‹equality›, ‹nand›. The operators should short-circuit (skip
# evaluating the right subtree) where applicable. Leaves of the tree
# contain boolean constants.

# Example of a boolean tree:
#
#             ┌───┐
#         ┌───│⟦∧⟧│───┐
#         ▼   └───┘   ▼
#       ┌───┐       ┌───┐
#      ┌│⟦∨⟧│┐     ┌│⟦⇒⟧│┐
#      ▼└───┘▼     ▼└───┘▼
#    ┌───┐ ┌───┐ ┌───┐ ┌───┐
#    │ 1 │ │ 0 │ │ 1 │ │ 1 │
#    └───┘ └───┘ └───┘ └───┘
#
# In this case the ‹or› (∨) node evaluates to ‹True›, the
# implication (⇒) evaluates to ‹True› as well, and hence the whole
# tree (‹and›, ∧) also evaluates to ‹True›.

# Add methods and attributes to ‹Node› and ‹Leaf› as/if needed.


class Node:
    def __init__(self) -> None:
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None

    def evaluate(self) -> bool:
        pass


class Leaf(Node):
    def __init__(self, value: bool) -> None:
        self.truth_value = value

    def evaluate(self) -> bool:
        return self.truth_value

# Complete the following classes as appropriate.


class AndNode(Node):
    def evaluate(self) -> bool:
        if self.left is None or self.right is None:
            return False
        l = self.left.evaluate()
        if not l:
            return False
        r = self.right.evaluate()
        if not r:
            return False
        return True


class OrNode(Node):
    def evaluate(self) -> bool:
        if self.left is None or self.right is None:
            return False
        l = self.left.evaluate()
        if l:
            return True
        r = self.right.evaluate()
        if r:
            return True
        return True if r == True or l == True else False


class ImplicationNode(Node):
    def evaluate(self) -> bool:
        if self.left is None or self.right is None:
            return False
        l = self.left.evaluate()
        if not l:
            return True
        r = self.right.evaluate()
        return True if l == r else False


class EqualityNode(Node):
    def evaluate(self) -> bool:
        if self.left is None or self.right is None:
            return False
        l = self.left.evaluate()
        r = self.right.evaluate()
        return True if r == l else False



class NandNode(Node):
    def evaluate(self) -> bool:
        if self.left is None or self.right is None:
            return False
        l = self.left.evaluate()
        if not l:
            return True
        r = self.right.evaluate()
        return True if l != r else False


def test_basic() -> None:

    tree: Node = Leaf(True)
    assert tree.evaluate()

    tree = Leaf(False)
    assert not tree.evaluate()

    truth_table = [(True,  True),
                   (True,  False),
                   (False, True),
                   (False, False)]

    operators_table = [
        (AndNode,         (True,  False, False, False)),
        (OrNode,          (True,  True,  True,  False)),
        (ImplicationNode, (True,  False, True,  True)),
        (EqualityNode,    (True,  False, False, True)),
        (NandNode,        (False, True,  True,  True))]

    for op, results in operators_table:
        for i in range(len(truth_table)):
            tree = op()
            left, right = truth_table[i]
            tree.left, tree.right = Leaf(left), Leaf(right)
            assert tree.evaluate() == results[i]


def test_short_circuit() -> None:

    def check(node_type: type, left: bool, result: bool) -> None:
        tree: Node = node_type()
        tree.left = Leaf(left)
        tree.right = tree
        assert tree.evaluate() == result

    check(AndNode, False, False)
    check(OrNode, True, True)
    check(ImplicationNode, False, True)
    check(NandNode, False, True)


def test_complex() -> None:
    from queue import Queue

    tree_list: List[Union[type, bool]]
    tree_list = [ImplicationNode, NandNode, OrNode, EqualityNode,
                 OrNode, ImplicationNode, AndNode, True, False,
                 True, True, False, NandNode, False, AndNode,
                 OrNode, True, OrNode, EqualityNode, True, False,
                 False, True, True, True]

    lst = iter(tree_list)
    it = next(lst)

    assert type(it) == type
    tree = it()
    nodes: Queue[Node] = Queue()
    nodes.put(tree)

    while not nodes.empty():
        node = nodes.get()

        left = next(lst)
        if type(left) == bool:
            node.left = Leaf(left)
        else:
            node.left = left()
            assert node.left is not None
            nodes.put(node.left)

        right = next(lst)
        if type(right) == bool:
            node.right = Leaf(right)
        else:
            node.right = right()
            assert node.right is not None
            nodes.put(node.right)

    assert tree.evaluate() == True


if __name__ == "__main__":
    test_basic()
    test_short_circuit()
    test_complex()
