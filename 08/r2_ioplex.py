from typing import Coroutine, Generator, Iterator, List, Any
from time import sleep

# Write an IO multiplexer for ‹async› coroutines. The constructor is
# given a ‘coroutine function’ (i.e. an ‹async def›, that is a
# function which returns a coroutine object) which serves as a
# factory. There are 3 methods:
#
#  • ‹connect›, which creates a new connection (i.e. it spawns a new
#    server coroutine to handle requests) and returns a connection
#    identifier,
#  • ‹close› which, given a valid identifier, terminates the
#    corresponding connection,
#  • ‹send› which, given a connection identifier and a piece of
#    data, sends the latter on to the corresponding server coroutine
#    and returns the reply of that coroutine.
#
# When creating server coroutines, the multiplexer passes ‹read› and
# ‹write› as arguments to the factory, where ‹read› is an ‹async›
# function (i.e. its result is ‹await›-ed) and returns the data that
# was passed to ‹send›; ‹write›, on the other hand, is a regular
# function and is called when the server coroutine wants to send
# data to the client. In other words, reading may block, but not
# writing.

class IOPlex: pass


def test_basic() -> None:
    who = [ 'dana', 'charlie', 'bob', 'alice' ]

    async def serve( read: Any, write: Any ) -> Any:
        me = who.pop()
        while True:
            what = await read()
            write( me + ': ' + what )

    io = IOPlex( serve )
    a = io.connect()
    b = io.connect()

    assert io.send( b, 'foo' ) == 'bob: foo'
    assert io.send( a, 'bar' ) == 'alice: bar'

    io.close( a )

    assert io.send( a, 'baz' ) is None
    assert io.send( b, 'boo' ) == 'bob: boo'

    c = io.connect()
    d = io.connect()

    assert io.send( a, 'baz' ) is None
    assert io.send( c, 'baz' ) == 'charlie: baz'
    assert io.send( d, 'baz' ) == 'dana: baz'

    assert io.send( c, 'oh' ) == 'charlie: oh'
    assert io.send( d, 'scully, no' ) == 'dana: scully, no'

if __name__ == '__main__':
    test_basic()
