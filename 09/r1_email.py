# In this exercise, we will parse a format that is based on RFC 822
# headers, though our implementation will only handle the simplest
# cases. The format looks like this:

#     From: Petr Ročkai <xrockai@fi.muni.cz>
#     To: Random X. Student <xstudent@fi.muni.cz>
#     Subject: PV248

# and so on and so forth. In real e-mail (and in HTTP), each header
# entry may span multiple lines, but we will not deal with that.

# Our goal is to create a ‹dict› where the keys are the individual
# header fields and the corresponding values are the strings coming
# after the colon. In this iteration, assume that each header is
# unique.

def parse_rfc822( filename: str ) -> dict[str, str]:
    res = {}
    with open(filename) as file:
        for line in file:
            sliced = line.split(':')
            res[sliced[0]] = sliced[1].strip()
    return res

def test_main() -> None:
    res = parse_rfc822( "zz.email.txt" )
    assert len( res ) == 3
    for k in [ "From", "To", "Subject" ]:
        assert k in res

    assert res[ "From" ] == "Petr Ročkai <xrockai@fi.muni.cz>"
    assert res[ "To" ] == "Random X. Student <xstudent@fi.muni.cz>"
    assert res[ "Subject" ] == "PV248"

if __name__ == "__main__":
    test_main()
