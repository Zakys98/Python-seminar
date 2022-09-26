from typing import TypeVar, Dict, Callable

K = TypeVar( 'K' )
V = TypeVar( 'V' )
R = TypeVar( 'R' )

# The ‹make_counter› function should return a pair consisting of a
# function ‹fun› and a dictionary ‹ctr›, where ‹fun› accepts a
# single parameter of type ‹K›, which is also the key type of ‹ctr›.
# Calling ‹fun› on a value ‹key› then increments the corresponding
# counter in ‹ctr›. Don't forget the type annotations.

def make_counter(): pass


def test_counter() -> None:
    ctr_1 : Dict[ str, int ]
    ctr_2 : Dict[ int, int ]
    fun_1 : Callable[ [ str ], None ]
    fun_2 : Callable[ [ int ], None ]

    fun_1, ctr_1 = make_counter()
    fun_2, ctr_2 = make_counter()

    each_key( { 'foo': 1, 'bar': 2, 'baz': 1 }, fun_1 )

    assert ctr_1[ 'foo' ] == 1
    assert ctr_1[ 'bar' ] == 1
    assert ctr_1[ 'baz' ] == 1

    each_value( { 'foo': 1, 'bar': 2, 'baz': 1 }, fun_2 )

    assert ctr_2[ 1 ] == 2
    assert ctr_2[ 2 ] == 1

    assert len( ctr_1 ) == 3
    assert len( ctr_2 ) == 2

    ctr_1.clear()
    each_value( { 'x': 'foo', 'y': 'bar', 'z': 'foo' }, fun_1 )

    assert len( ctr_1 ) == 2
    assert ctr_1[ 'foo' ] == 2, ctr_1
    assert ctr_1[ 'bar' ] == 1, ctr_1


def each_key( data: Dict[ K, V ], fun: Callable[ [ K ], R ] ) -> None:
    for k in data.keys():
        fun( k )

def each_value( data: Dict[ K, V ], fun: Callable[ [ V ], R ] ) -> None:
    for v in data.values():
        fun( v )


if __name__ == '__main__':
    test_counter()
