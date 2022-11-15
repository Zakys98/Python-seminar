# You are given a database which stores information about packages,
# with the following tables:
#
#     package: id (primary key), name (string)
#     version: id (primary key), package_id (foreign key),
#              number (string)
#     depends: version_id (foreign key), depends_on (foreign key)
#
# Where ‹depends_on› also refers to ‹version.id›. Write the
# following functions.

from sqlite3 import Connection, connect
from typing import List, Tuple

# Return a list of packages, along with the number of distinct
# versions of each package.

def list_packages( db: Connection ) -> List[ Tuple[ str, int ] ]:
    pass

# Return the package versions (as a tuple of the package name and
# version ‘number’) that are not required by any other package (i.e.
# they form leaf nodes in the dependency tree).

def list_leaves( db: Connection ) -> List[ Tuple[ str, str ] ]:
    pass

# For each package version, give the number of packages (package
# versions) which directly depend on it.

def sum_depends( db: Connection ) -> List[ Tuple[ str, str, int ] ]:
    pass

# ----- >% ----- >% -----

def mkdb() -> Connection:
    conn = connect( ':memory:' )
    c = conn.cursor()
    c.execute( 'create table package ( id integer primary key, ' + \
               'name varchar )' )
    c.execute( 'create table version ( id integer primary key, ' + \
               'package_id integer, number varchar )' )
    c.execute( 'create table depends ( version_id integer,' + \
               'depends_on integer )' )

    def add_pkg( name: str, *vers: str ) -> None:
        c.execute( 'insert into package ( name ) values ( ? )',
                   ( name, ) )
        pid = c.lastrowid
        for v in vers:
            c.execute( 'insert into version ( package_id, ' + \
                       'number ) values ( ?, ? )', ( pid, v ) )

    def add_dep( p1: str, v1: str, p2: str, v2: str ) -> None:
        get = '( select version.id from version join ' + \
              'package on package.id = package_id ' + \
              'where name = ? and number = ? )'

        c.execute( 'insert into depends ( version_id, depends_on ) ' + \
                   f'values ( {get}, {get} )', ( p1, v1, p2, v2 ) )

    add_pkg( 'libc', '2.0', '2.1', '2.2' )
    add_pkg( 'ksh', '1.0', '1.1' )
    add_pkg( 'dummy' )

    add_dep( 'ksh', '1.0', 'libc', '2.0' )
    add_dep( 'ksh', '1.1', 'libc', '2.1' )

    return conn

def test_list() -> None:
    c = mkdb()
    pkgs = set( list_packages( c ) )
    assert pkgs == { ( 'libc', 3 ), ( 'ksh', 2 ),
                     ( 'dummy', 0 ) }, pkgs

def test_leaves() -> None:
    c = mkdb()
    pkgs = set( list_leaves( c ) )
    assert pkgs == { ( 'libc', '2.2' ), ( 'ksh', '1.0' ),
                     ( 'ksh', '1.1' ) }, pkgs

def test_depends() -> None:
    c = mkdb()
    pkgs = set( sum_depends( c ) )
    assert pkgs == { ( 'libc', '2.2', 0 ),
                     ( 'libc', '2.1', 1 ),
                     ( 'libc', '2.0', 1 ),
                     ( 'ksh', '1.0', 0 ),
                     ( 'ksh', '1.1', 0 ) }, pkgs


if __name__ == '__main__':
    test_list()
    test_leaves()
    test_depends()
