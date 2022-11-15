# Write a parser (of any kind) that validates a ‹resolv.conf› file
# (which contains DNS configuration). The simplified grammar is as
# follows:
#
#     top     := { stmt | comment } ;
#     stmt    := server, ( comment | [ spaces ], '\n' ) ;
#     server  := 'nameserver', spaces, addr ;
#     addr    := num, '.', num, '.', num, '.', num ;
#     num     := '0' | nonzero, { digit } ;
#     nonzero := '1' | '2' | … | '9' ;
#     digit   := '0' | nonzero ;
#     spaces  := ws_char, { ws_char } ;
#     ws_char := ? isspace() is True, except newline ? ;
#     comment := [ ws ], '#', { nonnl }, '\n' ;
#     nonnl   := ? any char except '\n' ? ;

def resolv_valid( rc: str ) -> bool: pass

def test_errors() -> None:
    assert not resolv_valid( '# foo' )
    assert not resolv_valid( 'nameserver foo\n' )
    assert not resolv_valid( 'nameserver 1.2.3\n' )
    assert not resolv_valid( 'nameserver\n1.2.3.4\n' )
    assert not resolv_valid( 'nameserver 1.2.3.4 5.6.7.8\n' )
    assert not resolv_valid( 'nameserver 1.2.3.4' )
    assert not resolv_valid( 'nameserver 1.00.3.4\n' )
    assert not resolv_valid( 'nameserver 1.01.3.4\n' )
    assert not resolv_valid( '#\n ' )
    assert not resolv_valid( ' ' )
    assert not resolv_valid( ' \n' )

def test_valid() -> None:
    assert resolv_valid( '# foo\n' )
    assert resolv_valid( ' # foo\n' )
    assert resolv_valid( 'nameserver 1.2.3.4\n' )
    assert resolv_valid( 'nameserver 1.2.3.4\nnameserver 4.5.0.1\n' )
    assert resolv_valid( 'nameserver 1.2.3.4 \n' )
    assert resolv_valid( 'nameserver  1.2.3.4 \n' )
    assert resolv_valid( 'nameserver  1.2.3.4# comment\n' )
    assert resolv_valid( 'nameserver  1.2.3.4 # comment\n' )
    assert resolv_valid( 'nameserver 1.2.3.4 # comment\n' )
    assert resolv_valid( 'nameserver 1.2.3.4#\nnameserver 4.5.0.1\n' )
    assert resolv_valid( 'nameserver 1.2.3.4\n#nameserver 4.5.0.1\n' )

if __name__ == '__main__':
    test_errors()
    test_valid()
