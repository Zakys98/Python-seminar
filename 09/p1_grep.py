# The goal of this exercise is to write a simple program that works
# like UNIX ‹grep›.

# Part 1: Write a procedure which takes 2 arguments, a string
# representation of a regex and a filename. It will print the lines
# of the file that match the regular expression (in the same order
# as they appear in the file). Prefix the line with its line number
# like so (hint: check out the ‹enumerate› built-in):

#     43: This line matched a regex,

# Part 2: Change the code in the ‹if __name__ …› block below to only
# run ‹test_main› if an argument ‹--test› is given. Otherwise,
# expect 2 command-line arguments: a regular expression and a file
# name, and pass those to the ‹grep› procedure.

def grep(regex, filename):
    pass


def test_basic() -> None:
    from typing import Callable

    def redirect_out(test: Callable[[], None]) -> str:
        import sys
        from io import StringIO

        stdout = sys.stdout
        out = StringIO()
        sys.stdout = out

        test()

        sys.stdout = stdout
        return out.getvalue()

    def t1() -> None:
        grep("empty", "zz.grep.txt")

    def t2() -> None:
        grep("p[p|t]", "zz.grep.txt")

    output = redirect_out(t1)
    assert output == "4: be nonempty.\n" \
                     "6: Has some empty lines, too.\n"

    output = redirect_out(t2)
    assert output == "3: is not very long and appears to\n" \
                     "4: be nonempty.\n" \
                     "6: Has some empty lines, too.\n"


if __name__ == "__main__":
    test_basic()
