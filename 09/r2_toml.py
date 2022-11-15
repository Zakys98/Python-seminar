from typing import Dict, Optional

# Write a recursive descent parser for simplified TOML (essentially
# an old-style INI file with restricted right-hand sides), with the
# following grammar:
#
#     top    = { line } ;
#     line   = ( header | kvpair ), '\n' ;
#     header = '[' word ']' ;
#     kvpair = word, '=', word ;
#     word   = alpha, { alnum } ;
#     alpha  = ? any letter on which isalpha() is true ? ;
#     alnum  = ? any letter on which isalnum() is true ? ;
#
# If the input does not conform to the grammar exactly, reject it
# and return ‹None›. Otherwise return a dictionary of sections (see
# the type below). If the initial section does not have a header, it
# is stored under ‹''› (empty string) in the section dictionary.

Section = Dict[ str, str ]
TOML = Dict[ str, Section ]

def parse_toml( toml: str ) -> Optional[ TOML ]:
    pass


def test_errors() -> None:
    assert parse_toml( 'foo\n' ) is None
    assert parse_toml( 'foo=x' ) is None
    assert parse_toml( 'foo=x\nbar=y' ) is None
    assert parse_toml( 'foo=1\n' ) is None
    assert parse_toml( '[]\n' ) is None
    assert parse_toml( '[x\n]\n' ) is None
    assert parse_toml( 'foo = a\n' ) is None
    assert parse_toml( 'foo = a\n' ) is None
    assert parse_toml( '[x]foo=a\n' ) is None
    assert parse_toml( '[x]foo=\na' ) is None

def test_good() -> None:

    def dfl( **kwargs: str ) -> TOML:
        return { '': { **kwargs } }

    def eq( toml: str, **kwargs: str ) -> None:
        x = parse_toml( toml )
        assert x == dfl( **kwargs ), x

    def fq( toml: str, dfl: Section, **kwargs: Section ) -> bool:
        return parse_toml( toml ) == { '': dfl, **kwargs }

    eq( 'foo=a\n', foo = 'a' )
    eq( 'foo=a\nbar=a\n', foo = 'a', bar = 'a' )
    assert fq( 'x=a\ny=a\n[s]\nx=z\n',
               { 'x': 'a', 'y': 'a' }, s = { 'x': 'z' } )
    assert fq( '[k]\nx=a\ny=a\n[s]\nx=z\n',
               {}, k = { 'x': 'a', 'y': 'a' }, s = { 'x': 'z' } )


if __name__ == '__main__':
    test_errors()
    test_good()
