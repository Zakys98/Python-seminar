from __future__ import annotations
from typing import Union, Protocol, Type, TYPE_CHECKING

# (continued from ‹01/p3_ts3esc›) Eventually, we will want to
# replicate the actual substitution into the templates. This will be
# done by the ‹ts3_render› function (next exercise). However,
# somewhat surprisingly, that function will only take one argument,
# which is the structured document to be converted into a string.
# Recall that the template system is recursive: before ‹ts3_render›,
# another function, ‹ts3_combine› combines the document and the
# templates into a single tree-like structure. One of your less
# fortunate colleagues is doing that one.

# This structure has 5 types of nodes: lists, maps, templates
# (strings), documents (also strings) and integers. In the original
# system there are more types (like decimal numbers, booleans and so
# on) but it has been decided to add those later.  Many documents
# only make use of the above 5.

# A somewhat unfortunate quirk of the system is that there are
# multiple types of nodes represented using strings. The way the
# original system dealt with this is by prefixing each string by its
# type; ‹$document$ › (with a trailing space!) and ‹$template$ ›.
# Those prefixes are stored in the database. To make matters worse,
# there are strings with no prefix: earlier versions looked for ‹${›
# and ‹#{› sequences in the string, and if it found some, treated
# the string as a template, and as a document otherwise.

# The team has rightly decided that this is stupid. You drew the
# short straw and now you are responsible for function
# ‹ts3_normalize›, which takes the above slightly baroque structure
# and sorts the strings into two distinct types, which are
# represented using Python classes. Someone else will deal with
# converting the database ‘later’.


class Document:
    def __init__(self, text: str) -> None:
        self.text = text


class Template:
    def __init__(self, text: str) -> None:
        self.text = text

# Each of the above classes keeps the actual text in a string
# attribute called ‹text›, without the funny prefixes. The lists,
# maps and integers fortunately arrive as Python ‹list›, ‹dict› and
# ‹int› into this function. Return the altered tree (without
# disturbing the original), the strings substituted for their
# respective types.

# The mypy type for the function is simple on the surface, but the
# machinery that makes it type is «ugly». On the logic that it is
# prepared for you, this exercise still requires passing strict
# mypy, because given ‹InputDoc› and ‹OutputDoc›, the function types
# are straightforward. You can use either ‹isinstance› or ‹type› and
# equality to guard code that uses specific union members – either
# is understood by ‹mypy›.


def removeTemplate(text: str) -> str:
    if text.find('$template$') != 0:
        return text
    return text.replace('$template$ ', '')


def removeDocument(text: str) -> str:
    if text.find('$document$') != 0:
        return text
    return text.replace('$document$ ', '')


def ts3_normalize(tree: InputDoc) -> OutputDoc:
    if isinstance(tree, dict):
        out = {}
        for key in tree:
            out[key] = ts3_normalize(tree[key])
    elif isinstance(tree, list):
        lal = list()
        for item in tree:
            lal.append(ts3_normalize(item))
        return lal
    elif isinstance(tree, str):
        if tree.find('$${') == -1 and tree.find('${') != -1 or tree.find('#{') != -1 and tree.find('##{') == -1:
            return Template(removeTemplate(tree))
        return Document(removeDocument(tree))
    elif isinstance(tree, int):
        return tree
    return out


def test_map() -> None:
    from copy import deepcopy

    tree: InputDoc
    tree = {'templ': "$template$ …${product}…: #{product.names}"}
    tree_orig = deepcopy(tree)
    norm = ts3_normalize(tree)

    assert tree == tree_orig  # do not modify the tree in place
    assert get_len(norm) == 1
    assert get_type(norm, 'templ') == Template
    assert get_text(norm, 'templ') == "…${product}…: #{product.names}"


def test_list_1() -> None:
    from copy import deepcopy

    tree: InputDoc
    tree = {'templs': ["${product}", "#{products}",
                       "$template$ main: ${product}, other: ${products}"]}
    tree_orig = deepcopy(tree)
    norm = ts3_normalize(tree)

    assert tree == tree_orig
    assert get_len(norm) == 1
    assert get_len(norm, 'templs') == 3

    for i in range(3):
        assert get_type(norm, 'templs', i) == Template

    assert get_text(norm, 'templs', 0) == "${product}"
    assert get_text(norm, 'templs', 1) == "#{products}"
    assert get_text(
        norm, 'templs', 2) == "main: ${product}, other: ${products}"


def test_list_2() -> None:
    from copy import deepcopy

    tree: InputDoc
    tree = ["instructions of use: please do not use", 7,
            "instructions: ${instructions}", "documentation ##{}"]
    tree_orig = deepcopy(tree)
    norm = ts3_normalize(tree)

    assert tree == tree_orig
    assert get_len(norm) == 4
    assert get_type(norm, 0) == Document
    assert get_type(norm, 1) == int
    assert get_type(norm, 2) == Template
    assert get_type(norm, 3) == Document


def test_complex() -> None:
    from copy import deepcopy

    tree: InputDoc = {'names': ["Name1", "Name: ${name}",
                                "Names: #{names}", "Name ###{$}", 1,
                                "Oscar"],
                      'tpls': {'tpl1': 0, 'tpl2': " $document$ abc",
                               'tpl3': "ab${t}",
                               'tpl4':
                               ['a', "$$doc", "$document$ ",
                                {'root': "$document@ no? #{${e}}",
                                 'foo': 78,
                                 'foo2': "$document$ $template$?"}]},
                      'not-tpls': 9}

    tree_orig = deepcopy(tree)
    norm = ts3_normalize(tree)
    assert tree == tree_orig

    assert get_len(norm) == 3
    assert get_type(norm, 'not-tpls') == int

    names = get_item(norm, 'names')

    assert get_len(names) == 6
    assert get_type(names, 0) == Document
    assert get_type(names, 1) == Template
    assert get_type(names, 2) == Template
    assert get_type(names, 3) == Document
    assert get_type(names, 4) == int
    assert get_type(names, 5) == Document

    assert get_text(names, 0) == "Name1"
    assert get_text(names, 1) == "Name: ${name}"
    assert get_text(names, 2) == "Names: #{names}"
    assert get_text(names, 3) == "Name ###{$}"
    assert get_item(names, 4) == 1
    assert get_text(names, 5) == "Oscar"

    tpls = get_item(norm, 'tpls')

    assert get_len(tpls) == 4
    assert get_type(tpls, 'tpl1') == int
    assert get_type(tpls, 'tpl2') == Document
    assert get_type(tpls, 'tpl3') == Template
    assert get_type(tpls, 'tpl4') == list

    assert get_item(tpls, 'tpl1') == 0
    assert get_text(tpls, 'tpl2') == " $document$ abc"
    assert get_text(tpls, 'tpl3') == "ab${t}"

    assert get_len(tpls, 'tpl4') == 4
    assert get_type(tpls, 'tpl4', 0) == Document
    assert get_type(tpls, 'tpl4', 1) == Document
    assert get_type(tpls, 'tpl4', 2) == Document
    assert get_type(tpls, 'tpl4', 3) == dict

    assert get_text(tpls, 'tpl4', 0) == "a"
    assert get_text(tpls, 'tpl4', 1) == "$$doc"
    assert get_text(tpls, 'tpl4', 2) == ""

    assert get_len(tpls, 'tpl4', 3) == 3
    assert get_type(tpls, 'tpl4', 3, 'root') == Template
    assert get_type(tpls, 'tpl4', 3, 'foo') == int
    assert get_type(tpls, 'tpl4', 3, 'foo2') == Document

    tpl4 = get_item(norm, 'tpls', 'tpl4')
    assert get_text(tpl4, 3, 'root') == "$document@ no? #{${e}}"
    assert get_text(tpl4, 3, 'foo2') == "$template$?"


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


def get_item(doc: OutputDoc, *args: Union[str, int]) -> OutputDoc:
    if not args:
        return doc

    if isinstance(doc, dict) and isinstance(args[0], str):
        return get_item(doc[args[0]], *args[1:])
    elif isinstance(doc, list) and isinstance(args[0], int):
        return get_item(doc[args[0]], *args[1:])
    else:
        assert False


def get_len(doc: OutputDoc, *args: Union[str, int]) -> int:
    item = get_item(doc, *args)
    assert isinstance(item, list) or isinstance(item, dict)
    return len(item)


def get_type(doc: OutputDoc, *args: Union[str, int]) -> type:
    item = get_item(doc, *args)
    return type(item)


def get_text(doc: OutputDoc, *args: Union[str, int]) -> str:
    item = get_item(doc, *args)
    assert isinstance(item, Document) or \
        isinstance(item, Template)
    return item.text


if __name__ == "__main__":
    test_map()
    test_list_1()
    test_list_2()
    test_complex()
