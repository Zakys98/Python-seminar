from typing import Generator, TypeVar, Coroutine, cast

# In this demo, we will look at first part of the scheduler's job:
# handling requests from ‘special’ functions. First, however, let's
# define a helper class to represent the requests that we are going
# to pass from the ‹async› functions to the scheduler. To make
# things simpler, the scheduler will pass back the result by
# updating the request (in particular its ‹result› attribute, which
# we set up in ‹__init__›).

class Request:
    pass

class ReadRequest( Request ):
    def __init__( self, file: str ):
        self.file = file
        self.result : str

class WriteRequest( Request ):
    def __init__( self, file: str, data: str ):
        self.file = file
        self.data = data
        self.result = None

# To simplify working with type annotations, we will define a pair
# of generic aliases. The first, ‹AwaitGen› is going to be the type
# of ‹__await__› methods that cooperate with our scheduler (and
# hence they yield instances of ‹Request›). The latter, ‹Coro›, is
# the type of coroutines that we want to use. Somewhat
# unfortunately, ‹mypy› does not actually care about the yield (or
# send) type of the ‹async def› – we are sufficiently deep into
# plumbing that we are simply expected to get this right without
# static types.

ResultT  = TypeVar( 'ResultT' )
AwaitGen = Generator[ Request, None, ResultT ]
Coro     = Coroutine[ Request, None, ResultT ]

# With that out of the way, we can define some ‘special’ functions
# that can be awaited, but are not defined using ‹async def›, which
# means that they will be able to yield into the scheduler. Recall
# that ‹await› expects an awaitable object and calls ‹__await__› on
# it. The result of ‹__await__› should be an iterator.

# Of course, we can simply provide ‹__await__› as a method, and to
# make things particularly easy, we can make it a «generator». That
# way, calling ‹__await__› automatically gets us a generator object,
# which happens to also be an iterator. We have already prepared a
# type alias for this occasion above: ‹AwaitGen›.

# As always, calling ‹async_read( 'foo' )› will use ‹__init__› to
# initialize the object, at which point we create the request so
# that ‹__await__› can forward it into the scheduler using ‹yield›.
# When control returns to ‹__await__›, we extract the ‹result› and
# pass it onto our caller.

class async_read:
    def __init__( self, file: str ):
        self.req = ReadRequest( file )
    def __await__( self ) -> AwaitGen[ str ]:
        yield self.req
        return self.req.result

# Basically the same as above. Notice the different annotation on
# ‹__await__›, and how that matches the type of ‹self.result› in the
# above request types.

class async_write:
    def __init__( self, file: str, data: str ):
        self.req = WriteRequest( file, data )
    def __await__( self ) -> AwaitGen[ None ]:
        yield self.req
        return self.req.result

# A helper function to actually process requests in the scheduler.
# We fake everything, for the sake of a demonstration.

def process( request: Request ) -> None:
    if isinstance( request, ReadRequest ):
        request.result = f'content of {request.file}'
    if isinstance( request, WriteRequest ):
        print( 'async_run: writing',
                request.data, 'into', request.file )

# Finally the scheduler itself (not the most accurate name in this
# case, since it ‘schedules’ a single coroutine). We will look at
# the other aspect (actually scheduling green threads) in the next
# demo. Notice that we always send ‹None› as the response – we could
# actually send a response, but that would make the types uglier,
# and updating the request is also quite reasonable.

def async_run( coro: Coro[ ResultT ] ) -> ResultT:
    while True:
        try:
            request = coro.send( None )
            process( request )
        except StopIteration as e:
            return cast( ResultT, e.value )


# Finally, we write a couple of ‘user’ functions using ‹async def›.
# To call into other ‹async› coroutines, We use the standard ‹await›
# construct now (we are no longer doing plumbing).

async def read_foo() -> str:
    foo = await async_read( 'foo' )
    return f'read_foo: {foo}'

async def main() -> int:
    x = await read_foo()
    print( f'main: result of read_foo was "{x}"' )
    await async_write( 'bar', 'stuff' )
    return 13

def test_run():
    assert async_run( main() ) == 13

if __name__ == '__main__':
    test_run()
