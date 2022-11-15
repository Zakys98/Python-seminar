from typing import Tuple, Callable
import hypothesis
import hypothesis.strategies as s

# Implement the cross product and check the following properties:
#
#  • anti-commutativity
#  • distributivity over addition
#  • compatibility with scalar multiplication:
#    ra × b = a × rb = r(a × b)
#  • Jacobi identity: a × (b × c) + b × (c × a) + c × (a × b) = 0

# Check all of them on integer inputs.

Vector = Tuple[ int, int, int ]
BinOp  = Callable[ [ Vector, Vector ], Vector ]

def add( a: Vector, b: Vector ) -> Vector:
    ax, ay, az = a
    bx, by, bz = b
    return ( ax + bx, ay + by, az + bz )

def mul( r: int, a: Vector ) -> Vector:
    ax, ay, az = a
    return ( r * ax, r * ay, r * az )

def cross( a, b ): pass

def check_anticommutativity( cross: BinOp ) -> None: pass
def check_distributivity( cross: BinOp ) -> None: pass
def check_jacobi( cross: BinOp ) -> None: pass
def check_compatibility( cross: BinOp ) -> None: pass

def test_self() -> None:
    check_anticommutativity( cross )
    check_distributivity( cross )
    check_jacobi( cross )
    check_compatibility( cross )

def test_cross() -> None:
    assert cross( ( 1, 0, 0 ), ( 0, 1, 0 ) ) == ( 0, 0,  1 )
    assert cross( ( 0, 1, 0 ), ( 1, 0, 0 ) ) == ( 0, 0, -1 )

def test_bad() -> None:
    def bad_cross( a: Vector, b: Vector ) -> Vector:
        ax, ay, az = a
        bx, by, bz = b
        return ( ax * bx, ay * by, az * bz )

    failed = True

    try:
        check_anticommutativity( bad_cross )
        failed = False
    except AssertionError: pass
    assert failed

    check_distributivity( bad_cross )

    try:
        check_jacobi( bad_cross )
        failed = False
    except AssertionError: pass
    assert failed

    check_compatibility( bad_cross )

def test_alsobad() -> None:
    def bad_cross( a: Vector, b: Vector ) -> Vector:
        return add( a, mul( -1, b ) )

    failed = True

    # it is anti-commutative all right
    check_anticommutativity( bad_cross )

    # but everything else fails
    try:
        check_distributivity( bad_cross )
        failed = False
    except AssertionError: pass
    assert failed

    try:
        check_jacobi( bad_cross )
        failed = False
    except AssertionError: pass
    assert failed

    try:
        check_compatibility( bad_cross )
        failed = False
    except AssertionError: pass
    assert failed

if __name__ == '__main__':
    test_self()
    test_cross()
    print( "note: ignore the 'falsifying examples' below" )
    test_bad()
    test_alsobad()
