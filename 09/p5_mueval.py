# Write an evaluator for a very small lisp-like language. Let there
# only be compound expressions (delimited by parentheses) which
# always have an integer arithmetic operator in the first position
# (‹+›, ‹-›, ‹*›, ‹/›) and the remainder of the compound are either
# non-negative integer constants or other compounds. Assume the
# input is well-formed.

def mueval( expr: str ) -> int:
    pass

def test_main() -> None:
    assert mueval( "4" ) == 4
    assert mueval( "(+ 4 4)" ) == 8
    assert mueval( "(* 2 2)" ) == 4
    assert mueval( "(+ (* 2 2) 4)" ) == 8
    assert mueval( "(/ (* 2 2) 2)" ) == 2
    assert mueval( "(/ (+ 2 2) (* 2 2))" ) == 1
    assert mueval( "(- (+ 2 (- 2 1)) (* 2 2))" ) == -1
    assert mueval( "(+ 1 2 3)" ) == 6
    assert mueval( "(+ 10 5)" ) == 15

if __name__ == "__main__":
    test_main()
