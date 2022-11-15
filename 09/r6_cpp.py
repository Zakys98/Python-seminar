# Implement a C preprocessor which supports ‹#include "foo"›
# (without a search path, working directory only), ‹#define› without
# a value, ‹#undef›, ‹#ifdef› and ‹#endif›. The input is provided in
# a file, but the output should be returned as a string. Do not
# include line and filename information that ‹cpp› normally adds to
# files.

def cpp( filename: str ) -> str:
    pass

def test_1() -> None:
    actual = cpp( 'zz.preproc_1.txt' )
    expect = '\n'.join( [ 'included foo',
                          'included bar',
                          'xoo',
                          'foo', '' ] )
    assert actual == expect, actual

def test_2() -> None:
    actual = cpp( 'zz.preproc_2.txt' )
    expect = '\n'.join( [ 'included bar',
                          'included baz',
                          'included bar', '' ] )
    assert actual == expect, actual

if __name__ == '__main__':
    import sys
    if len( sys.argv ) >= 2:
        print( end = cpp( sys.argv[ 1 ] ) )
    else:
        test_1()
        test_2()
