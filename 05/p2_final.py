from typing import List

# Same as previous exercise, but with the additional requirement
# that whenever an object becomes garbage (unreachable), a finalizer
# is immediately called on it. The finalizer may perform arbitrary
# heap manipulation (as long as it is otherwise legal; in
# particular, it may ‘re-animate’ the object it is finalizing, by
# storing a reference to this object). A finalizer must not be
# called on an object if a reference exists to this object (even if
# that reference is from another dead object).


class Heap:
    def __init__(self) -> None:
        self.objects: list[tuple[int, int | None]] = list()
        self.finalizer = None

    def add_root(self, obj):
        self.objects.append((obj, None))

    def add_ref(self, obj_from, obj_to):
        self.objects.append((obj_from, obj_to))

    def del_ref(self, obj_from, obj_to):
        help: set[tuple[int, int]] = set(self.objects)
        self.objects.remove((obj_from, obj_to))
        output: set[int] = set()
        for x, y in self.objects:
            if y is None:
                output.add(x)
            elif x in output:
                output.add(y)
        help -= set(self.objects)
        for x, y in self.objects:
            if y is not None and y not in output:
                #self.objects.remove((x, y))
                self.finalizer(x)
                self.finalizer(y)
                output.add(x)
                output.add(y)

    def set_finalizer(self, callback):
        self.finalizer = callback


def test_basic() -> None:
    h = Heap()
    h.add_root(1)
    fin: List[int] = []
    h.set_finalizer(lambda x: fin.append(x))

    h.add_ref(1, 2)
    h.add_ref(1, 3)
    h.add_ref(2, 3)
    h.add_ref(3, 4)
    h.add_ref(4, 5)
    h.del_ref(3, 4)
    assert fin == [4, 5]
    h.add_ref(3, 4)
    h.add_ref(4, 5)

    h.set_finalizer(lambda x: h.add_ref(1, x))
    h.del_ref(3, 4)
    h.set_finalizer(lambda x: fin.append(x))
    h.del_ref(1, 4)
    assert fin == [4, 5, 4, 5]
    h.del_ref(1, 3)
    assert fin == [4, 5, 4, 5]
    h.del_ref(1, 2)
    assert fin == [4, 5, 4, 5, 2, 3]


if __name__ == '__main__':
    test_basic()
