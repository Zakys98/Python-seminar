from typing import Set

# Implement the ‘mark’ phase of a mark & sweep collector. That is,
# find all objects which are reachable from the root set.
#
# Like before, roots are marked using ‹add_root› and references are
# added/removed using ‹add_ref› and ‹del_ref›. You can assume that
# the number of ‹del_ref› calls on given arguments is always at most
# the same as the number of corresponding ‹add_ref› calls.


class Heap:

    def __init__(self) -> None:
        self.objects: list[tuple[int, int | None]] = []

    def add_root(self, obj: int) -> None:
        self.objects.append((obj, None))

    def add_ref(self, obj_from: int, obj_to: int) -> None:
        self.objects.append((obj_from, obj_to))

    def del_ref(self, obj_from: int, obj_to: int) -> None:
        self.objects.remove((obj_from, obj_to))

    def reachable(self) -> Set[int]:
        output: set[int] = set()
        for x, y in self.objects:
            if y is None:
                output.add(x)
            elif x in output:
                output.add(y)
        return output


def test_basic() -> None:
    h = Heap()
    assert h.reachable() == set()
    h.add_root(1)
    assert h.reachable() == {1}
    h.add_ref(1, 2)
    assert h.reachable() == {1, 2}
    h.add_ref(1, 3)
    assert h.reachable() == {1, 2, 3}
    h.add_ref(2, 3)
    assert h.reachable() == {1, 2, 3}
    h.add_ref(3, 4)
    h.add_ref(4, 3)
    assert h.reachable() == {1, 2, 3, 4}
    h.del_ref(1, 3)
    assert h.reachable() == {1, 2, 3, 4}
    h.del_ref(1, 2)
    assert h.reachable() == {1}


if __name__ == '__main__':
    test_basic()
