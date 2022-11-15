# You are given a JSON file which describes a (very rudimentary)
# database schema. The top-level value is an object (dictionary)
# with table names as keys and objects which describe the columns
# as values.
#
# The keys in the table description are column names and values
# (strings) are SQL types of those columns. Given a database
# connection and a path to the JSON file, create the tables. If one
# of them already exists, raise an error.

from sqlite3 import Connection, OperationalError, connect

def create_tables( schema: str, db: Connection ):
    pass


def test_schema1() -> None:
    conn = connect( ":memory:" )
    create_tables( 'zz.schema1.json', conn )
    conn.execute( "insert into package values ( 7, 'foo' )" )
    x, = conn.execute( 'select * from package' );
    assert x == ( 7, 'foo' )
    
    try:
        create_tables( 'zz.schema1.json', conn )
        assert False
    except OperationalError:
        pass

    try:
        create_tables( 'zz.schema2.json', conn )
        assert False
    except OperationalError:
        pass

def test_schema2() -> None:
    conn = connect( ":memory:" )
    create_tables( 'zz.schema2.json', conn )
    conn.execute( "insert into version values ( 7, 'foo' )" )

if __name__ == '__main__':
    test_schema1()
    test_schema2()
