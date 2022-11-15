from __future__ import annotations
from typing import TypeVar, Generic, Optional, List, Generator, Callable
from r3_itree import T, Tree

# Write recursive generators which walk a binary tree in
# pre-/in-/post-order.


def preorder(tree):
    yield tree.value
    if tree.left is not None:
        yield from preorder(tree.left)
    if tree.right is not None:
        yield from preorder(tree.right)

def inorder(tree):
    if tree.left is not None:
        yield from inorder(tree.left)
    yield tree.value
    if tree.right is not None:
        yield from inorder(tree.right)

def postorder(tree):
    if tree.left is not None:
        yield from postorder(tree.left)
    if tree.right is not None:
        yield from postorder(tree.right)
    yield tree.value


def test_int1_gen() -> None:
    t_1 = Tree(7, Tree(2), Tree(3, Tree(4), Tree(5)))

    assert copy_gen(t_1, preorder) == [7, 2, 3, 4, 5]
    assert copy_gen(t_1, inorder) == [2, 7, 4, 3, 5]
    assert copy_gen(t_1, postorder) == [2, 4, 5, 3, 7]


def test_int2_gen() -> None:
    t_2 = Tree(6, Tree(4, Tree(2, Tree(1), Tree(3)),
                       Tree(5)),
               Tree(10, Tree(8, Tree(7), Tree(9)),
                    Tree(11)))

    assert copy_gen(t_2, preorder) == [6, 4, 2, 1, 3, 5, 10, 8, 7, 9, 11]
    assert copy_gen(t_2, inorder) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    assert copy_gen(t_2, postorder) == [1, 3, 2, 5, 4, 7, 9, 8, 11, 10, 6]


def test_int3_gen() -> None:
    t_3 = Tree(6, Tree(4, Tree(2, Tree(1), Tree(3)),
                       Tree(5)),
               Tree(8, Tree(7),
                    Tree(10, Tree(9), Tree(11))))

    assert copy_gen(t_3, preorder) == [6, 4, 2, 1, 3, 5, 8, 7, 10, 9, 11]
    assert copy_gen(t_3, inorder) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    assert copy_gen(t_3, postorder) == [1, 3, 2, 5, 4, 7, 9, 11, 10, 8, 6]


def test_str_gen() -> None:
    t = Tree('x', Tree('y'),
             Tree('u', Tree('v'), Tree('w')))

    assert copy_gen(t, preorder) == ['x', 'y', 'u', 'v', 'w']
    assert copy_gen(t, inorder) == ['y', 'x', 'v', 'u', 'w']
    assert copy_gen(t, postorder) == ['y', 'v', 'w', 'u', 'x']


def copy_gen(tree: Tree[T],
             f: Callable[[Tree[T]],
                         Generator[T, None, None]]) -> List[T]:
    out: List[T] = []
    for i in f(tree):
        out.append(i)
    return out


if __name__ == "__main__":
    test_int1_gen()
    test_int2_gen()
    test_int3_gen()
    test_str_gen()
