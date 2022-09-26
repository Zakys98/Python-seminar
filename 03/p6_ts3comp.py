from __future__ import annotations
from p2_ts3norm import *

# This is the final part of the ‘template system 3’ series of
# exercises (previously: ‹01/p3_ts3esc›, ‹02/p2_ts3norm›,
# ‹02/p3_ts3render› and ‹02/r3_ts3bugs›).
#
# Our starting point this time is ‹02/p3_ts3render› – we will add
# support for missing data types and for rendering of composite data.
#
# For scalar substitution (using ‹${…}›), add the following data
# types (on top of existing ‹Document› and ‹Template›):
#
#  • ‹int› → it is formatted as a decimal number and the resulting
#    string replaces the ‹${…}›,
#  • ‹list› → the length of the list is formatted as if it was an
#    ‹int›, and finally,
#  • ‹dict› → ‹.default› is appended to the path and the
#    substitution is retried.
#
# Composite rendering using ‹#{…}› is similar, but:
#
#  • a ‹dict› is rendered as a comma-separated (with a space) list
#    of its values, after the keys are sorted alphabetically, where
#    each value is rendered «as a scalar»,
#  • a ‹list› is likewise rendered as a comma-separated list of its
#    values as scalars,
#  • everything else is an error: like before, treat this as a failed
#    precondition, fail an ‹assert›, and leave it to someone else
#    (or future you) to fix later.
#
# Everything else about ‹ts3_render› is unchanged from the last time.

def ts3_render( tree: OutputDoc ) -> str:
    pass


def test_scalar_individual() -> None:

    template = Template( "Here is input: ${input}" )

    t : OutputDoc
    t = { '$template': template, 'input': Document( "blahblah" ) }
    assert ts3_render( t ) == "Here is input: blahblah"

    t = { '$template': template, 'input': Document( "blah ${t}" ) }
    assert ts3_render( t ) == "Here is input: blah ${t}"

    t = { '$template': template, 'input': [ 1, 2, 3 ] }
    assert ts3_render( t ) == "Here is input: 3"

    t = { '$template': template,
          'input': { 'a': 7, 'default': Document( "abc}" ) } }
    assert ts3_render( t ) == "Here is input: abc}"

    t = { '$template': template, 'input': -22 }
    assert ts3_render( t ) == "Here is input: -22"

    t = { '$template': template,
          'input': Template( "would need ${more.input}" ),
          'more': { 'input': Document( "hello" ),
                    'output': Document( "bye" ) } }
    assert ts3_render( t ) == "Here is input: would need hello"


def test_composite_individual() -> None:

    template = Template( "List: #{items} and a dog." )
    t : OutputDoc
    t = { '$template': template,
          'items': list( map( Document,
                              [ 'carrot', 'cat', 'potato' ] ) ) }
    assert ts3_render( t ) == "List: carrot, cat, potato and a dog."

    # dict, sort(!)
    t = { '$template': template,
          'items': { 'c': Document( 'foo' ), 'a': 7,
                     'd': Template( "${foo}" ),
          't': -1, }, 'foo': [ Document( '1' ) ] }
    assert ts3_render( t ) == "List: 7, foo, 1, -1 and a dog."


def test_template() -> None:

    template = Template( "Print ${name.idea} and" +
                         " ${name.group.3.people}.." )

    # encountering list in path resolution means an index
    people : OutputDoc = { 'people': [ Document( 'Bernard' ),
                                       Document( 'Ann' ) ] }
    group : OutputDoc = [ 0, 1, 2, people ]
    t : OutputDoc
    t = { '$template': template,
          'name': { 'idea': Document( 'fireflies' ),
                    'group': group } }
    assert ts3_render( t ) == "Print fireflies and 2.."


def test_escape() -> None:

    template = Template( "${header}: show me ${person.name} " +
                         "and ${person.age} of #{persons} " +
                         "but not $${ppl}" )

    t : OutputDoc
    t = { '$template': template,
          'header': Document( "automatic" ),
          'person': { 'name': Document( "Villa" ), 'age': 17 },
          'persons': [ Document( 'Villa' ), Document( 'Serrat' ) ] }
    t_orig = t.copy()

    expect = "automatic: show me Villa and 17 of Villa, " + \
             "Serrat but not ${ppl}"

    assert ts3_render( t ) == expect
    assert t == t_orig


def test_composite() -> None:

    # composite within composite
    template = Template( "Fields: #{fields}!#}" )
    t : OutputDoc
    t = { '$template': template,
          'fields': [ Document( 'CS' ), Document( 'Law' ),
                      Template( 'Others: #{others}' ) ],
          'others': { 'field2': Document( 'Art' ),
                      'field3': Document( 'Archery' ),
                      'field1': Document( 'Plants' ) } }

    assert ts3_render( t ) == "Fields: CS, Law, Others: Plants, Art, Archery!#}"

def test_errors() -> None:
    t : OutputDoc

    # dict meets a number in the path
    t = { '$template': Template( "${path.0}" ),
          'path': { 'foo': 2 } }
    assert_throws( t )

    # list meets a string in the path
    t = { '$template': Template( "${path.a}" ),
          'path': [ Document( 'a' ) ] }
    assert_throws( t )

    # dict end of scalar, no 'default' key
    t = { '$template': Template( "a ${path}" ),
          'path': { 'not-default': 1 } }
    assert_throws( t )

    # composite meets int/Template/Document
    t = { '$template': Template( "#{comp}" ), 'comp': 7 }
    assert_throws( t )

    t = { '$template': Template( "#{comp}" ),
          'comp': Document( "$doc" ) }
    assert_throws( t )

    t = { '$template': Template( "#{comp}" ),
          'comp': Template( "foo" ) }
    assert_throws( t )

    # nested templates
    t = { '$template': Template( "#{ab${t}c}" ),
          'ab': Document( "wrong" ) }
    assert_throws( t )

def assert_throws( t: OutputDoc ) -> None:
    try:
        ts3_render( t )
    except AssertionError:
        return

    raise AssertionError( "expected a failed assertion" )

if __name__ == "__main__":
    test_scalar_individual()
    test_composite_individual()
    test_template()
    test_escape()
    test_composite()
    test_errors()
