from typing import Generator

# Normally, generators are used in for loops. However, when you
# simply call a generator, the result is an object of type
# ‹generator›, which represents the suspended computation. (For
# future reference, native coroutines declared with ‹async def›
# behave the same way, just the object type is different.)

# Let's define a generator:

def gen1() -> Generator[ int, None, None ]:
    print( "before yield 1" )
    yield 1
    print( "before yield 2" )
    yield 2

# To actually run the computation, you can call ‹__next__()› on the
# ‹generator› object. Alternatively, you can call ‹next› with
# generator object as the argument. Once you do that, the execution
# of the body of ‹gen1› starts, and continues until it hits a yield.
# At that point, the yielded value becomes the return value of
# ‹__next__()›, like this:

def test_gen1() -> None: # demo
    x = gen1()
    print( "constructed gen1" )
    assert x.__next__() == 1
    print( "no longer interested in gen1...\n" )

# Since ‹x› is just a normal object, we can abandon it at any time.
# Nothing forces us to keep calling ‹__next__()› on it. Let's look
# at ‹send()› now.

def gen2() -> Generator[ int, int, None ]:
    v = yield 1
    print( "received", v )
    yield 2
    print( "returning from gen2()" )
    pass # StopIteration is automatically raised here

def test_gen2() -> None: # demo
    y = gen2()
    assert y.__next__() == 1
    assert y.send( 24 ) == 2 # resumes execution of ‹y›
    print( "sent 24, got 2 back" )
    try: y.__next__() # generators do not return
    except StopIteration: print( "generator done" )

if __name__ == '__main__':
    test_gen1()
    test_gen2()
