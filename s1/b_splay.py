# Implement the «splay tree» data structure (an adaptively
# self-balancing binary search tree). Provide at least the following
# operations:
#
#  • ‹insert›  – add an element to the tree (if not yet present)
#  • ‹find›    – find a previously added element (return a ‹bool›)
#  • ‹erase›   – remove an element
#  • ‹to_list› – return the tree as a sorted list
#  • ‹filter›  – remove all elements failing a given predicate
#  • ‹root›    – obtain a reference to the root node
#
# Nodes should have (at least) attributes ‹left›, ‹right› and
# ‹value›. The class which represents the tree should be called
# ‹SplayTree›.

# You can find the required algorithms online (wikipedia comes to
# mind, but also check out ‹https://is.muni.cz/go/uvcjn9› for some
# intuition how the tree works).

# The main operation is ‘splaying’ the tree, which moves a
# particular node to the root, while rebalancing the tree. How
# balanced the tree actually is depends on the order of splay
# operations. The tree will have an «expected» logarithmic depth
# after a random sequence of lookups (splays). If the sequence is
# not random, the balance may suffer, but the most-frequently looked
# up items will be near the root. In this sense, the tree is
# self-optimizing.

# Note: it's easier to implement ‹erase› using splaying than by using
# the ‘normal’ BST delete operation:
#
#  1. splay the to-be-deleted node to the root, then
#  2. join its two subtrees L and R:
#     ◦ use splay again, this time on the largest item of the
#       left subtree L,
#     ◦ the new root of L clearly can't have a right child,
#     ◦ attach the subtree R in place of the missing child.


class SplayTree:
    def __init__(self) -> None:
        self.rootNode = None

    def insert(self, value):
        if self.rootNode == None:
            self.rootNode = Node(value)
            return
        self.rootNode.insert(value)

    def find(self, value):
        if self.rootNode == None:
            return False
        self.rootNode.find(value)

    def erase(self, value):
        pass

    def to_list(self):
        pass

    def filter(self, predicate):
        pass

    def root(self):
        return self.rootNode


class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    def insert(self, value):
        if (value < self.value):
            if (self.left == None):
                self.left = Node(value)
            else:
                self.left.insert(value)
        else:
            if (self.right == None):
                self.right = Node(value)
            else:
                self.right.insert(value)

def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        print(f' ' * 4 * level + f'-> {node.value}')
        printTree(node.right, level + 1)

splay = SplayTree()
splay.insert(5)
splay.insert(4)
splay.insert(7)
splay.insert(2)
splay.insert(8)
splay.insert(1)
splay.insert(3)
splay.insert(6)
root = splay.root()
root.value = 4
print(root.value)
printTree(splay.root)