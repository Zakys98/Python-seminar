# Load the file ‹zz.books.json› and store the data in a database
# with 3 tables: ‹author›, ‹book› and ‹book_author_list›. Each
# author is uniquely identified by their name (which is a
# substantial simplification, but let's roll with it). The complete
# schema is defined in ‹zz.books.sql› and you can create an empty
# database with the correct data definitions by running the
# following command:

#     $ sqlite3 books.dat < zz.books.sql

import sqlite3
import json

# NB. You want to execute ‹pragma foreign_keys = on› before
# inserting anything into sqlite. Otherwise, your foreign key
# constraints are just documentation and are not actually enforced.
# Let's write an ‹opendb› function which takes a filename and
# returns an open connection. Execute the above-mentioned ‹pragma›
# before returning.


def opendb(filename: str) -> sqlite3.Connection:
    return sqlite3.connect(filename)

# Of course, you can also create the schema using Python after
# opening an empty database. See ‹executescript›. Define a function
# ‹initdb› which takes an open ‹sqlite3› connection, and creates the
# tables described in ‹sql_file› (in our case ‹zz.books.sql›). You
# can (and perhaps should) open and read the file and feed it into
# sqlite using ‹executescript›.


def initdb(conn: sqlite3.Connection, sql_file: str) -> None:
    with open(sql_file, 'r') as file:
        lines = file.read()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.executescript(lines)

# Now for the business logic. Write a function ‹store_book› which
# takes a ‹dict› that describes a single book (using the schema used
# by ‹books.json›) and stores it in an open database. Use the
# ‹execute› method of the connection. Make use of query parameters,
# like this (‹cur› is a «cursor», i.e. what you get by calling
# ‹conn.cursor()›):
#
#     cur.execute( "insert into ... values ( ? )", ( name, ) )
#
# The second argument is a tuple (one-tuples are written using a
# trailing comma). To fetch results of a query, use ‹cur.fetchone()›
# or ‹cur.fetchall()›. The result is a tuple (even if you only
# selected a single column). Or rather, it is a sufficiently
# tuple-like object (quacks like a tuple and all that).


def store_book(conn: sqlite3.Connection, book: dict[str, str]) -> None:
    book_name = book['name']
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM book WHERE name=?', [book_name])
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO book(name) values(?)', [book_name])
    for author in book['authors']:
        cursor.execute('SELECT id FROM author WHERE name=?', [author])
        result = cursor.fetchone()
        if not result:
            cursor.execute('INSERT INTO author(name) values(?)', [author])
        cursor.execute('SELECT id FROM book WHERE name=?', [book_name])
        book_id = cursor.fetchone()
        cursor.execute('SELECT id FROM author WHERE name=?', [author])
        author_id = cursor.fetchone()
        cursor.execute('SELECT * FROM book_author_list WHERE book_id=? AND author_id=?', [book_id[0], author_id[0]])
        result = cursor.fetchone()
        if not result:
            cursor.execute('INSERT INTO book_author_list(book_id, author_id) values(?, ?)', [book_id[0], author_id[0]])


# With the core logic done, we need a procedure which will set up
# the database, parse the input JSON and iterate over individual
# books, storing each:


def import_books(file_in: str, file_out: str) -> None:
    conn = opendb(file_out)
    initdb(conn, 'zz.books.sql')
    with open(file_in, 'r') as file:
        for book in json.load(file):
            store_book(conn, book)
    conn.commit()
    conn.close()


def test_main() -> None:
    import os
    try:
        os.unlink('zt.books.dat')
    except FileNotFoundError:
        pass

    conn = sqlite3.connect('zt.books.dat')
    import_books('zz.books.json', 'zt.books.dat')
    cur = conn.cursor()

    books_authors_ref = {}
    for item in json.load(open('zz.books.json')):
        books_authors_ref[item['name']] = item['authors']

    cur.execute('select * from book order by id')
    books = cur.fetchall()
    book_names = set([name for id, name in books])
    assert book_names == books_authors_ref.keys()

    cur.execute('select * from author order by id')
    authors = cur.fetchall()
    author_names = set([name for id, name in authors])
    all_authors = set(sum(books_authors_ref.values(), []))
    assert author_names == all_authors

    cur.execute('select * from book_author_list order by book_id')
    book_author = cur.fetchall()
    assert len(book_author) == sum([len(l)
                                    for l in books_authors_ref.values()])
    for b_id, a_id in book_author:
        _, b_name = books[b_id - 1]
        _, a_name = authors[a_id - 1]
        assert a_name in books_authors_ref[b_name]

    conn.close()


if __name__ == "__main__":
    test_main()
