from typing import Dict

# Your task is to write a function which takes:
#
#  • a list of input files,
#  • a function ‹get_name› which maps input filenames to output
#    filenames.
#  • a pure function ‹fun› which maps strings to strings,
#
# For each input file ‹file›, read the content, apply ‹fun› to that
# content and write the result to ‹get_name( file )›. Make sure
# things work if ‹get_name› is an identity function. Process the
# files left to right. Later files may be overwritten due to
# processing of earlier files.

def with_files( files, get_name, fun ): pass


def test_ident() -> None:
    ident = lambda x: x
    was   = lambda x: x.replace( 'is', 'was' )

    files = prepare()
    check_files( files )
    with_files( list( files.keys() ), ident, was )
    check_files( { k: v.replace( 'is', 'was' )
                   for k, v in files.items() } )

def test_copy() -> None:
    mktmp = lambda x: x + '.tmp'
    ident = lambda x: x

    files = prepare()
    check_files( files )
    with_files( list( files.keys() ), mktmp, ident )
    check_files( files )
    check_files( { k + '.tmp': v for k, v in files.items() } )

def test_change() -> None:
    mktmp = lambda x: x + '.tmp'
    pile  = lambda x: x.replace( 'file', 'pile' )
    ident = lambda x: x

    files = prepare()
    check_files( files )
    with_files( list( files.keys() ), mktmp, pile )
    check_files( files )
    check_files( { k + '.tmp': v.replace( 'file', 'pile' )
                   for k, v in files.items() } )

def prepare() -> Dict[ str, str ]:
    data = { 'zt.x': 'this is file zt.x',
             'zt.y': 'this file is zt.y',
             'zt.z': 'this is zt.z\n' }

    for fn, content in data.items():
        with open( fn, 'w' ) as f:
            f.write( content )

    return data

def check_files( fs: Dict[ str, str ] ) -> None:
    for name, content in fs.items():
        assert open( name, 'r' ).read() == content


if __name__ == '__main__':
    test_ident()
    test_copy()
    test_change()
