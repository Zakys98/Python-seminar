# This exercise is the same as the previous one, with one important
# difference: if some of the tables already exist, this is not an
# error. However, the columns of the existing table and those
# specified by the schema might be different. In this case, «create»
# any missing columns, but do not touch columns that already exist.
#
# Optional extension: print names of any extra columns, as a warning
# to the user that they no longer appear in the current schema and
# should be removed.
#
# Note: the ‹alter table› command in ‹sqlite› is very limited. In a
# ‘real’ database, it is possible to alter column types, add and
# remove constraints and so on, all transactionally protected.

from sqlite3 import Connection, OperationalError, connect

def upgrade_tables( schema: str, db: Connection ) -> None:
    pass


def test_basic() -> None:
    conn = connect( ":memory:" )
    upgrade_tables( 'zz.schema1.json', conn )
    conn.execute( "insert into package values ( 7, 'foo' )" )
    x, = conn.execute( 'select * from package' );
    assert x == ( 7, 'foo' )
    upgrade_tables( 'zz.schema2.json', conn )
    conn.execute( "insert into version values ( 3, 'bar' )" )
    x, = conn.execute( 'select * from package' );
    assert x == ( 7, 'foo' )
    x, = conn.execute( 'select * from version' );
    assert x == ( 3, 'bar' )


if __name__ == '__main__':
    test_basic()
