# Implement a linked list with the following operations:
#
#  • ‹append› – add an item at the end
#  • ‹join›   – concatenate 2 lists
#  • ‹shift›  – remove an item from the front and return it
#  • ‹empty›  – is the list empty?
#
# The class should be called ‹Linked› and should have a single type
# parameter (the type of item stored in the list). The ‹join› method
# should re-use nodes of the second list. The second list thus
# becomes empty.

from typing import TypeVar, Generic, List

T = TypeVar('T')

class Linked(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []

    def append(self, item: T) -> None:
        self.items.append(item)

    def join(self, list: "Linked[T]") -> None:
        while not list.empty():
            self.items.append(list.shift())

    def shift(self) -> T:
        return self.items.pop(0)

    def empty(self) -> bool:
        return not self.items


def test_elementary() -> None:
    l : Linked[ int ] = Linked()
    assert l.empty()
    l.append( 7 )
    assert not l.empty()
    assert l.shift() == 7
    assert l.empty()

def test_join() -> None:
    l_1 : Linked[ int ] = Linked()
    l_2 : Linked[ int ] = Linked()

    l_1.append( 7 )
    l_2.append( 3 )
    l_2.append( 7 )
    l_1.join( l_2 )

    assert l_2.empty()
    assert l_1.shift() == 7
    assert l_1.shift() == 3
    assert l_1.shift() == 7
    assert l_1.empty()

def test_str() -> None:
    l : Linked[ str ] = Linked()
    assert l.empty()
    l.append( 'hello' )
    l.append( 'world' )
    assert not l.empty()
    assert l.shift() == 'hello'
    assert l.shift() == 'world'
    assert l.empty()

def test_nested() -> None:
    l : Linked[ Linked[ int ] ] = Linked()

    u : Linked[ int ] = Linked()
    u.append( 3 )
    u.append( 4 )

    l.append( u )
    l.append( u )

    u = Linked()
    u.append( 1 )
    l.append( u )

    v = l.shift()
    assert v.shift() == 3
    w = l.shift()
    assert w.shift() == 4
    assert v.empty()

    v = l.shift()
    assert v.shift() == 1
    assert v.empty()
    assert l.empty()

    l.append( v )
    w = l.shift()
    assert w.empty()
    assert l.empty()


if __name__ == '__main__':
    test_elementary()
    test_join()
    test_str()
    test_nested()
