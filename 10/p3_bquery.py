from p1_bimport import import_books
import sqlite3

# In the final exercise of this set, you will write a few functions
# which search the book data. Like you did for export, get a cursor
# from the connection and use ‹execute› and ‹fetchone› or ‹fetchall›
# to process the results. Use SQL to limit the result set.

# Fetching everything (‹select * from table› without a ‹where›
# clause) and processing the data using Python constructs is «bad»
# and will make your program «unusable» for realistic data sets.

# The first function will fetch all books by a given author. Use the
# ‹like› operator to allow «substring matches» on the name. E.g.
# calling ‹books_by_author( conn, "Brontë" )› should return books
# authored by any of the Brontë sisters.


def books_by_author(conn: sqlite3.Connection, name: str) -> list[str]:
    cursor = conn.cursor()
    cursor.execute(
        'SELECT id, name FROM author WHERE name LIKE ?', [f'%{name}%'])
    authors = cursor.fetchall()
    output = list()
    for author_id, _ in authors:
        cursor.execute(
            'select * from book_author_list WHERE author_id=? order by book_id', [author_id])
        book_ids = set(cursor.fetchall())
        for book_id, _ in book_ids:
            cursor.execute('select name from book WHERE id=?', [book_id])
            book = cursor.fetchone()
            output.append(book[0])
    return output


# The second will fetch the «set» of people (i.e. each person
# appears at most once) who authored a book with a name that
# contains a given string. For instance, ‹authors_by_book( conn,
# "Bell" )› should return the 3 Brontë sisters and Ernest Hemingway.
# Try to avoid fetching the same person multiple times (i.e. use SQL
# to get a set, instead of a list).


def authors_by_book(conn: sqlite3.Connection, name: str) -> list[str]:
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM book WHERE name LIKE ?', [f'%{name}%'])
    books = cursor.fetchall()
    output = list()
    for book_id, _ in books:
        cursor.execute(
            'select * from book_author_list WHERE book_id=? order by book_id', [book_id])
        authors_ids = set(cursor.fetchall())
        for _, author_id in authors_ids:
            cursor.execute('select name from author WHERE id=?', [author_id])
            author = cursor.fetchone()
            output.append(author[0])
    return output

# Another function will return names of books which have at least
# ‹count› authors. For instance, there are 3 books in the data set
# with 2 or more authors.


def books_by_author_count(conn: sqlite3.Connection, count: int) -> list[str]:
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM(SELECT book.id as num FROM book_author_list, book WHERE book.id = book_id GROUP BY book.id HAVING COUNT(author_id) >= ?), book WHERE num = id', [count])
    book_author_ids = cursor.fetchall()
    return [book_name[0] for book_name in book_author_ids]

# Finally, write a function which returns the average author count
# for a book. The function should return a single ‹float›, and
# ideally it would not fetch anything from the database other than
# the result: try to do the computation only using SQL.


def average_author_count(conn: sqlite3.Connection) -> float:
    cursor = conn.cursor()
    cursor.execute('SELECT AVG(num) FROM(SELECT COUNT(author_id) as num FROM book_author_list, book WHERE book.id = book_id GROUP BY book.id)')
    avg = cursor.fetchone()
    return float(avg[0])


def test_main() -> None:
    from math import isclose

    import_books('zz.books.json', 'zt.books.dat')
    conn = sqlite3.connect('zt.books.dat')

    res = books_by_author(conn, 'Brontë')
    assert set(res) == {'Poems by Currer, Ellis and Acton Bell',
                        'Jane Eyre',
                        'The Professor',
                        'Wuthering Heights'}
    res = books_by_author(conn, 'son')
    assert res == ['The Rise and Fall of D.O.D.O.']

    res = authors_by_book(conn, 'Bell')
    assert set(res) == {'Charlotte Brontë',
                        'Emily Brontë',
                        'Anne Brontë',
                        'Ernest Hemingway'}

    res = authors_by_book(conn, 'н')
    assert set(res) == {'Аркадий Стругацкий',
                        'Борис Стругацкий'}

    res = books_by_author_count(conn, 2)
    assert set(res) == {'Poems by Currer, Ellis and Acton Bell',
                        'Улитка на склоне',
                        'The Rise and Fall of D.O.D.O.'}

    res = books_by_author_count(conn, 3)
    assert res == ['Poems by Currer, Ellis and Acton Bell']

    res = books_by_author_count(conn, 4)
    assert not res

    avg = average_author_count(conn)
    assert isclose(avg, 1.4444444444444444)


if __name__ == "__main__":
    test_main()
