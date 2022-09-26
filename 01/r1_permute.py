# Given a number ‹n› and a base ‹b›, find all numbers whose digits
# (in base ‹b›) are a permutation of the digits of ‹n›.
#
# Examples:
#
#     (125)₁₀ → { 125, 152, 215, 251, 512, 521 }
#     (1f1)₁₆ → { (1f1)₁₆, (f11)₁₆, (11f)₁₆ }
#     (20)₁₀  → { 20, 2 }

def permute_digits( n, b ):
    pass

def test_main():
    check( 1234, 10, [ 4321, 4312, 4231, 4213, 4132, 4123,
                       3421, 3412, 3241, 3214, 3142, 3124,
                       2431, 2413, 2341, 2314, 2143, 2134,
                       1432, 1423, 1342, 1324, 1243, 1234 ] )
    check( 903, 10, [ 309, 390, 39, 93, 930, 903 ] )
    check( 0b1010, 2, [ 0b1010, 0b1001, 0b1100,
                        0b11, 0b110, 0b101 ] )
    check( 0x1f1, 16, [ 0x11f, 0xf11, 0x1f1 ] )

def check( number, base, expected ):
    result = list( permute_digits( number, base ) )
    fmt = ( hex if base == 16 else
            bin if base == 2  else
            oct if base == 8  else str )
    err  = '[' + fmt( number ) + '] '
    rstr = ', '.join( map( fmt, sorted( result ) ) )

    assert len( result ) == len( expected ), err + rstr

    for i in expected:
        assert i in result, err + fmt( i ) + ' missing'

if __name__ == "__main__":
    test_main()
