from typing import Generator, Optional, Tuple

# In the second exercise in the stream series, we will define a
# simple stream-based lexer. That is, we will take, as an input, a
# stream of text chunks and on the output produce a stream of
# lexemes (tokens). The lexemes will be tuples, where the first item
# is the classification (a keyword, an identifier or a number) and
# the second item is the string which holds the token itself.

# Let the keywords be ‹set›, ‹add› and ‹mul›. Identifiers start with
# an alphabetic letter and continue with letters and digits. Numbers
# are made of digits. You can use ‹StrStream› below as a template
# for writing the type of a ‘lexeme stream’.

StrStream = Generator[ Optional[ str ], None, None ]

IDENT = 1
KW = 2
NUM = 3

def stream_lexer( text_stream ):
    pass


def test_main() -> None:
    stream, counter = make_test_source()
    assert counter.value == 0
    tokens = stream_lexer( stream )
    assert counter.value == 0
    assert next( tokens ) == ( IDENT, "identifier" )
    assert counter.value == 1
    assert next( tokens ) == ( KW, "mul" )
    assert counter.value == 2
    assert next( tokens ) == ( NUM, "321" )
    assert counter.value == 3
    assert next( tokens ) == ( IDENT, "multiply" )
    assert counter.value == 4
    assert next( tokens ) == ( IDENT, "add32" )
    assert counter.value == 5
    assert next( tokens ) == ( NUM, "1" )
    assert counter.value == 6
    assert next( tokens ) is None
    assert counter.value == 6

    tokens = stream_lexer( bad_stream() )
    try:
        next( tokens )
        assert False
    except RuntimeError:
        pass

class Box:
    def __init__( self, v: int ) -> None:
        self.value = v

def make_test_source() -> Tuple[ StrStream, Box ]:
    counter = Box( 0 )
    def test_source() -> StrStream:
        yield "ident"
        counter.value += 1
        yield "ifier\nm"
        counter.value += 1
        yield "ul 32"
        counter.value += 1
        yield "1 mul"
        counter.value += 1
        yield "tiply add"
        counter.value += 1
        yield "32 1"
        counter.value += 1
        while True:
            yield None
    return ( test_source(), counter )

def bad_stream() -> StrStream:
    yield "12"
    yield "x"


if __name__ == '__main__':
    test_main()
