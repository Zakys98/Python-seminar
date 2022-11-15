# Implement a simple reference-counting garbage collector. The
# interface is described in the class ‹Heap› below. The root objects
# are immortal (those are established by ‹add_root›). The ‹count›
# method returns the number of reachable live objects. The ‹alive›
# method checks whether a given object is alive. All objects start
# out dead.
#
# References are added/removed using ‹add_ref› and ‹del_ref›. You
# can assume that the number of ‹del_ref› calls on given arguments
# is always at most the same as the number of corresponding
# ‹add_ref› calls. Assume that no reference cycles are created. You
# need to keep track of the references yourself.

class Heap:

    def __init__(self) -> None:
        self.list: list[tuple[int, int | None]] = []

    def add_root(self, obj: int) -> None:
        self.list.append((obj, None))

    def add_ref(self, obj_from: int, obj_to: int) -> None:
        helper = {obj_from: False, obj_to: False}
        for x, y in self.list:
            if y == obj_to:
                helper[obj_to] = True
            if y == obj_from:
                helper[obj_from] = True
        if helper[obj_from] and helper[obj_to]:
            return
        self.list.append((obj_from, obj_to))

    def del_ref(self, obj_from: int, obj_to: int) -> None:
        for x, y in self.list:
            if obj_to == y:
                self.list.remove((x, y))

    def count(self) -> int:
        return len(self.list)

    def alive(self, obj: int) -> bool:
        for x, y in self.list:
            if x == obj or y == obj:
                return True
        return False


def test_basic() -> None:
    h = Heap()
    assert h.count() == 0
    h.add_root(1)
    assert h.count() == 1
    assert h.alive(1)
    assert not h.alive(2)

    h.add_ref(1, 2)
    assert h.count() == 2
    assert h.alive(1)
    assert h.alive(2)

    h.add_ref(1, 3)
    assert h.count() == 3
    assert h.alive(1)
    assert h.alive(2)
    assert h.alive(3)

    h.add_ref(2, 3)
    assert h.count() == 3
    assert h.alive(1)
    assert h.alive(2)
    assert h.alive(3)

    h.del_ref(1, 2)
    assert h.count() == 2
    assert h.alive(1)
    assert not h.alive(2)
    assert h.alive(3)

    h.del_ref(1, 3)
    assert h.count() == 1
    assert h.alive(1)
    assert not h.alive(2)
    assert not h.alive(3)


if __name__ == '__main__':
    test_basic()
