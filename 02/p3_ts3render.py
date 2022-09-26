from __future__ import annotations
from p2_ts3norm import *

# At this point, we have a structure made of ‹dict›, ‹list›,
# ‹Template›, ‹Document› and ‹int› instances. The lists and maps can
# be arbitrarily nested. Within templates, the substitutions give
# dot-separated paths into this tree-like structure. If the
# top-level object is a map, the first component of a path is a
# string which matches a key of that map. The first component is
# then chopped off, the value corresponding to the matched key is
# picked as a new root and the process is repeated recursively. If
# the current root is a list and the path component is a number, the
# number is used as an index into the list.
#
# If a ‹dict› meets a number in the path (we will only deal with
# string keys), or a ‹list› meets a string, treat this as a
# precondition violation – fail an ‹assert› – and let someone else
# deal with the problem later.
#
# At this point, we prefer to avoid the complexity of rendering all
# the various data types. Assume that the tree is only made of
# documents and templates, and that only scalar substitution (using
# ‹${path}›) happens. Bail with an ‹assert› otherwise. We will
# revisit this next week.
#
# The ‹${path}› substitution performs «scalar rendering», while
# ‹#{path}› substitution performs «composite rendering». Scalar
# rendering resolves the path to an object, and depending on its
# type, performs the following:
#
#  • ‹Document› → replace the ‹${…}› with the text of the document;
#    the pasted text is excluded from further processing,
#  • ‹Template› → the ‹${…}› is replaced with the text of the
#    template; occurrences of ‹${…}› and ‹#{…}› within the pasted text
#    are further processed.
#
# The top-level entity passed to ‹ts3_render› must always be a
# ‹dict›. The starting template is expected to be in the key
# ‹$template› of that ‹dict›. Remember that ‹##{…}›, ‹$${…}› and so
# on must be unescaped but not substituted.
#
# If you encounter nested templates while parsing the path, e.g.
# ‹${abc${d}}›, give up (again via a failed assertion); however, see
# also exercise ‹r3›.
import re


def returnOutputDoc(tree: OutputDoc) -> str:
    if isinstance(tree, list) or \
       isinstance(tree, dict) or \
       isinstance(tree, int):
        return ''
    return tree.text


def replace_dot(matches: list[str], tree: OutputDoc) -> str:
    if not matches:
        return returnOutputDoc(tree)
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
    if text.find('#{') != -1:
        raise AssertionError
    if re.search(r'(\${[a-zA-Z0-9.]*[${]+[a-zA-Z0-9.]*})', text):
        raise AssertionError
    matches = re.search(r'(\${[a-zA-Z0-9.]+})', text)
    if matches is None:
        return text
    for match in matches.groups():
        if match.find('.') != -1:
            dot = match.split('.')
            dot[0] = dot[0][2:]
            dot[-1] = dot[-1][:-1]
            change = replace_dot(dot, tree)
        else:
            try:
                test = match[2:-1]
                if isinstance(tree, Template) or isinstance(tree, Document) or isinstance(tree, list) or isinstance(tree, int):
                    return ""
                pos = tree[test]
                if isinstance(pos, Template) or isinstance(pos, Document):
                    change = pos.text
                else:
                    raise AssertionError
            except KeyError:
                return text
        text = text.replace(match, change)
        return replace(text, tree)
    return text


def ts3_render(tree: OutputDoc) -> str:
    if not isinstance(tree, dict):
        return ''
    text = replace(tree['$template'].text, tree)
    text = text.replace('$${', '${')
    return text


def test_scalar_individual() -> None:

    template = Template("Here is input: ${input}")

    t: OutputDoc
    t = {'$template': template, 'input': Document("blahblah")}
    assert ts3_render(t) == "Here is input: blahblah"

    t = {'$template': template, 'input': Document("blah ${t}")}
    assert ts3_render(t) == "Here is input: blah ${t}"

    t = {'$template': template,
         'input': Document('abc}')}
    assert ts3_render(t) == "Here is input: abc}"

    t = {'$template': template,
         'input': Template("would need ${more.input}"),
         'more': {'input': Document("hello"),
                  'output': Document("bye")}}
    assert ts3_render(t) == "Here is input: would need hello"


def test_template() -> None:

    template = Template("Print ${name.idea} and" +
                        " ${name.group.3.person}..")

    # encountering list in path resolution means an index
    people: OutputDoc = {'person': Document('Bernard')}
    group: OutputDoc = [Document('0'), Document('1'),
                        Document('2'), people]
    t: OutputDoc
    t = {'$template': template,
         'name': {'idea': Document('fireflies'),
                  'group': group}}
    assert ts3_render(t) == "Print fireflies and Bernard.."


def test_escape() -> None:

    template = Template("${header}: show me ${person.name} " +
                        "and ${person.age} of ${person.name} " +
                        "but not $${ppl}")

    t: OutputDoc
    t = {'$template': template,
         'header': Document("automatic"),
         'person': {'name': Document("Villa"),
                    'age': Document('17')}}
    t_orig = t.copy()

    expect = "automatic: show me Villa and 17 of Villa " + \
             "but not ${ppl}"

    assert ts3_render(t) == expect
    assert t == t_orig


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

    # composites
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

    t = {'$template': Template("${ab${t}c}"),
         'ab': Document("wrong"),
         'ab${t}c': Document('still wrong')}
    assert_throws(t)


def assert_throws(t: OutputDoc) -> None:
    try:
        ts3_render(t)
    except AssertionError:
        return

    raise AssertionError("expected a failed assertion")


if __name__ == "__main__":
    test_scalar_individual()
    test_template()
    test_escape()
    test_errors()
