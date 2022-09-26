# Implement the radix sort algorithm for strings. Use a dictionary
# to keep the buckets, since the ‘radix’ (the number of all possible
# ‘digits’) is huge for Unicode. To iterate the dictionary in the
# correct order, you can use:
#
#     sorted( d.items(), key = lambda x: x[ 0 ] )
#
# NB. Make sure that you don't accidentally sort the whole sequence
# using the built-in sort in your implementation.

def radix_sort( strings ):
    pass

def test_main():
    for i in range( 50 ):
        check_random( i )

def check_random( size ):
    from random import randint, choices
    letters = "abcdefgháčžŕřx1"

    strings = []
    for i in range( 50 ):
        wlen = randint( 1, size + 1 )
        word = ''.join( choices( letters, k = wlen ) )
        strings.append( word )

    result = radix_sort( strings )
    expect = sorted( strings )
    assert result == expect, (result, expect)

if __name__ == "__main__":
    test_main()
