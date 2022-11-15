from __future__ import annotations
import re
#from p2_ts3norm import *
from typing import Union, Protocol, Type, TYPE_CHECKING

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


class Document:
    def __init__(self, text: str) -> None:
        self.text = text


class Template:
    def __init__(self, text: str) -> None:
        self.text = text


def replace_dot(matches: list[str], tree: OutputDoc) -> str:
    if not matches:
        if isinstance(tree, list):
            return str(len(tree))
        if isinstance(tree, int):
            return str(tree)
        if isinstance(tree, dict):
            return ''
        return tree.text
    try:
        if isinstance(tree, dict):
            tree = tree[matches[0]]
        elif isinstance(tree, list):
            tree = tree[int(matches[0])]
    except TypeError:
        raise AssertionError
    except KeyError:
        raise AssertionError
    except ValueError:
        raise AssertionError
    return replace_dot(matches[1:], tree)


def replace(text: str, tree: OutputDoc) -> str:
    # if text.find('#{') != -1:
    #    raise AssertionError
    if re.search(r'(\${[a-zA-Z0-9.]*[${]+[a-zA-Z0-9.]*})', text):
        raise AssertionError
    keys = re.search(r'(\${[a-zA-Z0-9.]+})|(\#{[a-zA-Z0-9.]+})', text)
    if keys is None:
        return text
    for key in keys.groups():
        if key is None:
            continue
        if key.find('.') != -1:
            dot = key.split('.')
            dot[0] = dot[0][2:]
            dot[-1] = dot[-1][:-1]
            change = replace_dot(dot, tree)
        else:
            try:
                if isinstance(tree, Template) or \
                   isinstance(tree, Document) or \
                   isinstance(tree, list) or \
                   isinstance(tree, int):
                    return ""
                pos = tree[key[2:-1]]
                if isinstance(pos, Template) or \
                   isinstance(pos, Document):
                    change = pos.text
                elif isinstance(pos, list):
                    if isinstance(pos[0], Template) or \
                       isinstance(pos[0], Document):
                            change = ''
                            for item in pos:
                                change += f'{item.text}, '
                            change = change[:-2]
                    else:
                        change = str(len(pos))
                elif isinstance(pos, dict):
                    change = pos['default'].text
                elif isinstance(pos, int):
                    change = str(pos)
                else:
                    raise AssertionError
            except KeyError:
                return text
        text = text.replace(key, change)
        return replace(text, tree)
    return text


def ts3_render(tree: OutputDoc) -> str:
    if not isinstance(tree, dict):
        return ''
    text = replace(tree['$template'].text, tree)
    text = text.replace('$${', '${')
    print(text)
    return text


def test_scalar_individual() -> None:

    template = Template("Here is input: ${input}")

    t: OutputDoc
    t = {'$template': template, 'input': Document("blahblah")}
    assert ts3_render(t) == "Here is input: blahblah"

    t = {'$template': template, 'input': Document("blah ${t}")}
    assert ts3_render(t) == "Here is input: blah ${t}"

    t = {'$template': template, 'input': [1, 2, 3]}
    assert ts3_render(t) == "Here is input: 3"

    t = {'$template': template,
         'input': {'a': 7, 'default': Document("abc}")}}
    assert ts3_render(t) == "Here is input: abc}"

    t = {'$template': template, 'input': -22}
    assert ts3_render(t) == "Here is input: -22"

    t = {'$template': template,
         'input': Template("would need ${more.input}"),
         'more': {'input': Document("hello"),
                  'output': Document("bye")}}
    assert ts3_render(t) == "Here is input: would need hello"


def test_composite_individual() -> None:

    template = Template("List: #{items} and a dog.")
    t: OutputDoc
    t = {'$template': template,
         'items': list(map(Document,
                           ['carrot', 'cat', 'potato']))}
    assert ts3_render(t) == "List: carrot, cat, potato and a dog."

    # dict, sort(!)
    t = {'$template': template,
         'items': {'c': Document('foo'), 'a': 7,
                   'd': Template("${foo}"),
                   't': -1, }, 'foo': [Document('1')]}
    assert ts3_render(t) == "List: 7, foo, 1, -1 and a dog."


def test_template() -> None:

    template = Template("Print ${name.idea} and" +
                        " ${name.group.3.people}..")

    # encountering list in path resolution means an index
    people: OutputDoc = {'people': [Document('Bernard'),
                                    Document('Ann')]}
    group: OutputDoc = [0, 1, 2, people]
    t: OutputDoc
    t = {'$template': template,
         'name': {'idea': Document('fireflies'),
                  'group': group}}
    assert ts3_render(t) == "Print fireflies and 2.."


def test_escape() -> None:

    template = Template("${header}: show me ${person.name} " +
                        "and ${person.age} of #{persons} " +
                        "but not $${ppl}")

    t: OutputDoc
    t = {'$template': template,
         'header': Document("automatic"),
         'person': {'name': Document("Villa"), 'age': 17},
         'persons': [Document('Villa'), Document('Serrat')]}
    t_orig = t.copy()

    expect = "automatic: show me Villa and 17 of Villa, " + \
             "Serrat but not ${ppl}"
    print(expect)
    assert ts3_render(t) == expect
    assert t == t_orig


def test_composite() -> None:

    # composite within composite
    template = Template("Fields: #{fields}!#}")
    t: OutputDoc
    t = {'$template': template,
         'fields': [Document('CS'), Document('Law'),
                    Template('Others: #{others}')],
         'others': {'field2': Document('Art'),
                    'field3': Document('Archery'),
                    'field1': Document('Plants')}}

    assert ts3_render(t) == "Fields: CS, Law, Others: Plants, Art, Archery!#}"


def test_errors() -> None:
    t: OutputDoc

    # dict meets a number in the path
    t = {'$template': Template("${path.0}"),
         'path': {'foo': 2}}
    assert_throws(t)

    # list meets a string in the path
    t = {'$template': Template("${path.a}"),
         'path': [Document('a')]}
    assert_throws(t)

    # dict end of scalar, no 'default' key
    t = {'$template': Template("a ${path}"),
         'path': {'not-default': 1}}
    assert_throws(t)

    # composite meets int/Template/Document
    t = {'$template': Template("#{comp}"), 'comp': 7}
    assert_throws(t)

    t = {'$template': Template("#{comp}"),
         'comp': Document("$doc")}
    assert_throws(t)

    t = {'$template': Template("#{comp}"),
         'comp': Template("foo")}
    assert_throws(t)

    # nested templates
    t = {'$template': Template("#{ab${t}c}"),
         'ab': Document("wrong")}
    assert_throws(t)


def assert_throws(t: OutputDoc) -> None:
    try:
        ts3_render(t)
    except AssertionError:
        return

    raise AssertionError("expected a failed assertion")


if TYPE_CHECKING:  # make mypy go brrr
    class InList(list[InputDoc], Protocol):   # type: ignore
        __class__: Type[list[InputDoc]]       # type: ignore

    class OutList(list[OutputDoc], Protocol):  # type: ignore
        __class__: Type[list[OutputDoc]]      # type: ignore

    class InDict(dict[str, InputDoc], Protocol):   # type: ignore
        __class__: Type[dict[str, InputDoc]]       # type: ignore

    class OutDict(dict[str, OutputDoc], Protocol):  # type: ignore
        __class__: Type[dict[str, OutputDoc]]      # type: ignore

    InputDoc = Union[int, str, InList, InDict]
    OutputDoc = Union[int, Document, Template, OutList, OutDict]
else:
    InputDoc = dict  # see override at the end of the file
    OutputDoc = dict  # same

if __name__ == "__main__":
    test_composite_individual()
    test_template()
    test_scalar_individual()

    test_escape()
    test_composite()
    test_errors()
