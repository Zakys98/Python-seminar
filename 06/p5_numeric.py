# Implement a meta-class ‹Numeric› such that numbers (floats,
# integers, …) may appear to be instances of ‹Numeric›-based classes
# (the normal, non-meta class itself should be able to decide which,
# if any; you may find a class attribute useful here).

# Don't forget to derive your custom metaclass from the builtin
# (default) metaclass, ‹type›. When dealing with ‹mypy›, you can get
# away with annotating the type of the (non-meta!) class attribute
# you want to use in the ‹isinstance› override directly in the
# «metaclass».

class Numeric: pass

# Now implement classes ‹Complex› which represents standard complex
# numbers (based on ‹float›) and ‹Gaussian›, which represents Gaussian
# integers (complex numbers with integer real and imaginary part).
# The following should hold:
#
#  • integer values (including literals) are instances of ‹Gaussian›,
#  • float values are «not» instances of ‹Gaussian›,
#  • both integer and float values (including literals) are
#    instances of ‹Complex›.
#
# Other than that, implement addition and equality so that all
# reasonable combinations of parameters work (integers can be added
# to Gaussian integers and all of floats, normal integers and
# Gaussian integers can be added to Complex numbers).

class Gaussian: pass
class Complex: pass


def test_gaussian() -> None:
    assert     isinstance( 3, Gaussian )
    assert not isinstance( 3.1, Gaussian )
    x = 7
    assert     isinstance( x, Gaussian )
    y = Gaussian( x, 1 )
    assert     isinstance( y, Gaussian )
    z = Gaussian( x )
    assert     isinstance( z, Gaussian )

def test_complex() -> None:
    assert isinstance( 3, Complex )
    assert isinstance( 3.1, Complex )
    x = 7
    assert isinstance( x, Complex )
    y = Complex( x, 1.3 )
    assert isinstance( y, Complex )
    z = Complex( x )
    assert isinstance( z, Complex )

def test_addition() -> None:
    assert 3 == Gaussian( 3 )
    assert 3 != Gaussian( 3, 1 )
    assert Gaussian( 3 ) + 1 == 4
    assert Gaussian( 3, 1 ) + 1 == Gaussian( 4, 1 )
    assert Gaussian( 3, 1 ) + Gaussian( 4, 1 ) == Gaussian( 7, 2 )
    assert 7.3 != Gaussian( 7 )

    assert 3 == Complex( 3 )
    assert 3 != Complex( 3, 1 )
    assert Complex( 3 ) + 1 == 4
    assert Complex( 3, 1 ) + 1 == Complex( 4, 1 )
    assert Complex( 3, 1 ) + Gaussian( 1, 1 ) == Complex( 4, 2 )
    assert Complex( 3, 1 ) + Complex( 4, 1 ) == Complex( 7, 2 )
    assert 7.3 != Complex( 7 )
    assert 7.3 == Complex( 7.3 )
    assert 7.3 != Complex( 7.3, 1 )
    assert Complex( 0, 1.1 ) + 1.1 == Complex( 1.1, 1.1 )


if __name__ == '__main__':
    test_gaussian()
    test_complex()
    test_addition()
