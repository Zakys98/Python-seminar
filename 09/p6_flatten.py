# pragma mypy relaxed
import json
from typing import Dict, Union

# In this exercise, your task is to write a function that flattens
# JSON data to a form suitable for storing as TOML.
#
# The result is a single-level (flat) dictionary, where the keys
# represent the previous structure of the data.  We will use the
# period ‹.› for subobjects and ‹#› for subarrays. To make
# unambiguous un-flattening possible, if you encounter ‹.› or ‹#› in
# the original data, prefix it with a dollar sign, ‹$› (i.e. write
# out ‹$.› or ‹$#›), if you encounter ‹$.› or ‹$#›, escape it with
# another dollar sign, to ‹$$.› or ‹$$#›, etc.
#
# Example:
#     { 'student': { 'Joe': { 'full name': 'Joe Peppy',
#                             'address': 'Clinical Street 7',
#                             'aliases': ['Joey', 'MataMata'] } } }
#
# Flattened:
#     { 'student.Joe.full name': 'Joe Peppy',
#       'student.Joe.address': 'Clinical Street 7',
#       'student.Joe.aliases#0': 'Joey',
#       'student.Joe.aliases#1': 'MataMata' }

def flatten( data: str ) -> str:
    pass

def test_main() -> None:
    js =  '''{ "student":
               { "Joe":
                 { "full name": "Joe Peppy",
                   "address": "Clinical Street 7",
                   "aliases": [ "Joey", "MataMata" ]
                 }
               }
             }'''

    flat : Dict[ str, Union[ str, int ] ]
    flat = { 'student.Joe.full name': 'Joe Peppy',
             'student.Joe.address': 'Clinical Street 7',
             'student.Joe.aliases#0': 'Joey',
             'student.Joe.aliases#1': 'MataMata' }

    assert json.loads( flatten( js ) ) == flat

    js = '''{ "product": [ { "id": [ 2327, 7824 ],
                             "info": { "description": "lcd monitor",
                                       "price in $": 22 } },
                           { "id": [ 33 ],
                             "info": { "description": "mouse",
                                       "price in $": 4 } } ] }'''

    flat = { 'product#1.info.description': 'mouse',
             'product#0.info.price in $': 22,
             'product#0.id#1': 7824,
             'product#0.info.description': 'lcd monitor',
             'product#0.id#0': 2327,
             'product#1.info.price in $': 4,
             'product#1.id#0': 33 }

    assert json.loads( flatten( js ) ) == flat

    js = '''{ "evil.genius": "no",
              "evil$.genius": "yes",
              "evil#genius": "maybe",
              "evil$#genius": "certainly not",
              "evil": { "genius": "srsly" } }'''

    flat = { 'evil$.genius': 'no',
             'evil$$.genius': 'yes',
             'evil$#genius': 'maybe',
             'evil$$#genius': 'certainly not',
             'evil.genius': 'srsly' }

    assert json.loads( flatten( js ) ) == flat

if __name__ == "__main__":
    test_main()
