from __future__ import annotations

# Write a coroutine-based parser for mbox files. It should yield
# elements of the message as soon as it has enough bytes. The input
# will be an iterable, but not indexable, sequence of characters.
#
# In an mbox file, each message starts with a line like this:
#
#     From someone@example.com Wed May  1 06:30:00 MDT 2019
#
# You do not need to look at the structure of this line, look for
# the string ‹From › (with a trailing space) at the start of a line,
# and gobble it up to the nearest newline.
#
# After the separator line, an rfc-822 e-mail follows, with any
# lines that start with ‹From › changed to ‹>From › (do not forget
# to un-escape those). The headers are separated from the rest of
# the body by a single blank line. You can also assume that each
# header takes exactly one line.

# The reported elements are always pairs of strings, with the
# following content:
#
#  • message start: the string 'message' followed by the content of
#    the separator line with the ‹From › removed,
#  • header: yield the name of the field and the content; yield as
#    soon as you read the first character of the next header field, or
#    the body separator,
#  • body: yield a single string with the entire body in it, as soon
#    as you encounter the end of the file

def parse_mbox( chars ):
    pass


def test_main() -> None:
    f = FileIter( "zz.mbox.txt" )
    g = parse_mbox( f )

    item = next( g )
    assert item == ( 'message', 'MAILER-DAEMON Thu Feb 21 11:35:54 2013' )
    assert f.chars_given == 44, f.chars_given

    item = next( g )
    assert item == ( 'From', 'Author <author@example.com>' )
    assert f.chars_given == 78, f.chars_given # 44 + 34 ( line1 + line2 )

    item = next( g )
    assert item == ( 'To', 'Recipient <recipient@example.com>' )
    assert f.chars_given == 116, f.chars_given # 78 + 38

    item = next( g )
    assert item == ( 'Subject', 'Sample message 1' )
    assert f.chars_given == 142, f.chars_given

    item = next( g )
    assert item == ( 'body', 'This is the body.\n' \
                   'From (should be escaped).\n' \
                   'Fromage?\n' \
                   'There are 4 lines.\n' \
                   '\n' ), item
    assert f.chars_given == 222, f.chars_given

    item = next( g )
    assert item == ( 'message',
                     'MAILER-DAEMON Thu Feb 21 12:35:54 2013' )
    assert f.chars_given == 261, f.chars_given # 222 + 38

    item = next( g )
    assert item == ( 'From', 'Author <author2@example.com>' )
    assert f.chars_given == 296, f.chars_given

    item = next( g )
    assert item == ( 'To', 'Rec <rec@example.com>, Rec 2 <rec2.2@example.com>' )
    assert f.chars_given == 350, f.chars_given

    item = next( g )
    assert item == ( 'Subject', 'Sample message 2' )
    assert f.chars_given == 376, f.chars_given

    item = next( g )
    assert item == ( 'body', "This is the second body.\n" ), item
    assert f.chars_given == 407, f.chars_given

    item = next( g )
    assert item == ( 'message', 'MAILER-DAEMON Thu Feb 21 11:35:54 2014' )
    assert f.chars_given == 446, f.chars_given

    item = next( g )
    assert item == ( 'From', 'Author <author3@example.com>' )
    assert f.chars_given == 481, f.chars_given

    item = next( g )
    assert item == ( 'To', 'Recipient <recipient36@example.com>' )
    assert f.chars_given == 521, f.chars_given

    item = next( g )
    assert item == ( 'Subject', 'Msg 3' )
    assert f.chars_given == 536, f.chars_given

    item = next( g )
    assert item == ( 'body', "Msg body 3.\n" )
    assert f.chars_given == 549, f.chars_given

    try:
        next( g )
        assert False
    except StopIteration:
        pass


class FileIter:

    def __init__( self, filename: str ) -> None:
        self.file = open( filename, "r" )
        self.chars_given = 0

    def __iter__( self ) -> FileIter:
        return self

    def __next__( self ) -> str:
        c = self.file.read( 1 )
        if not c:
            self.file.close()
            raise StopIteration
        self.chars_given += 1
        return c


if __name__ == "__main__":
    test_main()
