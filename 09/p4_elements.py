# In this exercise, we will read in a CSV (comma-separated values)
# file and produce a JSON file. The input is in ‹zz.elements.csv›
# and each row describes a single chemical element. The columns are,
# in order, the atomic number, the symbol (shorthand) and the full
# name of the element. Generate a JSON file which will consist of a
# list of objects, where each object will have attributes ‹atomic
# number›, ‹symbol› and ‹name›. The first of these will be a number
# and the latter two will be strings. The names of the input and
# output files are given to ‹csv_to_json› as strings.

# Note that the first line of the CSV file is a header.

import csv  # we want csv.reader
import json # and json.dumps

def csv_to_json( source: str, target: str ):
    out = []
    with open(source) as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            pass

def test_main() -> None:
    import os

    try:
        os.unlink( 'zt.elements.json' )
    except FileNotFoundError:
        pass

    csv_to_json( "zz.elements.csv", "zt.elements.json" )

    try:
        with open( "zt.elements.json" ) as js:
            data = json.load( js )
    except FileNotFoundError as e:
        assert False, e

    with open( "zx.elements.json" ) as js:
        expect = json.load( js )

    assert data == expect

if __name__ == "__main__":
    test_main()
