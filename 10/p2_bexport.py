from collections import defaultdict
from p1_bimport import import_books

# In the second exercise, we will take the database created in the
# previous exercise (‹books.dat›) and generate the original JSON.
# You may want to use a join or two.

# First write a function which will produce a ‹list› of ‹dict›'s
# that represent the books, starting from an open ‹sqlite›
# connection.

import sqlite3
import json


def read_books(conn: sqlite3.Connection) -> list[dict[str, str]]:
    cursor = conn.cursor()
    cursor.execute('select * from book order by id')
    books = cursor.fetchall()
    cursor.execute('select * from author order by id')
    authors = cursor.fetchall()
    cursor.execute('select * from book_author_list order by book_id')
    book_author_ids = cursor.fetchall()
    book_author_ids_merged: dict[int, set[int]] = defaultdict(set)
    for book_id, author_id in book_author_ids:
        book_author_ids_merged[book_id].add(author_id)
    output = []
    for book_id, book_name in books:
        book = {}
        book['name'] = book_name
        for id, author_ids in book_author_ids_merged.items():
            if book_id == id:
                book['authors'] = [author_name for author_id, author_name in authors if author_id in author_ids]
                break
        output.append(book)
    return output

# Now write a driver that takes two filenames. It should open the
# database (do you need the foreign keys pragma this time? why yes
# or why not? what are the cons of leaving it out?), read the books,
# convert the list to JSON and store it in the output file.


def export_books(file_in: str, file_out: str) -> None:
    conn = sqlite3.connect(file_in)
    books = read_books(conn)
    json_object = json.dumps(books, indent=2)
    with open(file_out, 'w') as file:
        file.write(json_object)


def test_main() -> None:
    import os
    try:
        os.unlink('zt.books.json')
    except FileNotFoundError:
        pass

    conn = sqlite3.connect('zt.books.dat')
    import_books('zz.books.json', 'zt.books.dat')
    export_books('zt.books.dat', 'zt.books.json')

    with open('zz.books.json', 'r') as f1:
        js1 = json.load(f1)
    with open('zt.books.json', 'r') as f2:
        js2 = json.load(f2)
    assert js1 == js2


if __name__ == "__main__":
    test_main()
