# pragma mypy relaxed

from typing import Protocol, Any, TypeVar, Generic

T = TypeVar( 'T' )

class Obj( Protocol ):
    def __call__( self, __msg: str, *args: Any ) -> Any: ...

# Build a simple closure-based object system and use it to model a
# pedestrian crossing with a button-operated traffic light. Design
# two objects:
#
#  • ‹traffic_light› – a 2-state light, either ‘red’ or ‘green’,
#    toggled by messages ‹set_red›, ‹set_green› and queried using
#    ‹is_green›; the ‹set_green› method operates immediately
#    (‹is_green› right after ‹set_green› returns ‹True›) but
#    ‹set_red› has a safety timeout: the light turns red, but
#    ‹is_green› will only become ‹False› after 5 seconds to clear
#    the crossing,
#  • ‹button› – takes a reference to two traffic lights; when pushed
#    (message ‹push›), it requests that the first is turned green,
#    then after a timeout (20s), requests it to go back to red; the
#    second light vice-versa; it must ensure that under no
#    circumstances the lights both return ‹is_green› at the same
#    time.
#
# Every second, all objects in the system receive a ‹tick› message
# with no arguments.

def traffic_light(): pass
def button( pedestrian_light, vehicle_light ): pass

def test_basic() -> None:
    p = traffic_light()
    v = traffic_light()
    b = button( p, v )
    b( 'push' )
    tick( 7, p, v, b )
    assert p( 'is_green' )
    tick( 20, p, v, b )
    assert not p( 'is_green' )

def tick( n: int, *args: Obj ) -> None:
    for i in range( n ):
        for o in args:
            o( 'tick' )

if __name__ == '__main__':
    test_basic()
