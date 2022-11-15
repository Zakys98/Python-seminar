# Write two generators, one which simply yields numbers 1-5 and
# another which implements a counter (which also starts at 1):
# sending a number to the generator will adjust its value by the
# amount sent. Then write a driver loop that sends the output of
# ‹numbers()› into ‹counter()›. Try adding print statements to both
# to make it clear in which order the code executes.

def numbers():
    yield from range(1, 6)

def counter():
    value = 1
    while True:
        number = yield value
        if number is None:
            return
        value += number

def driver():
    numb = numbers()
    count = counter()
    yield next(count)
    for number in numb:
        yield count.send(number)


# After you are done with the above, implement the same thing with
# plain objects: ‹Numbers› with a ‹get()› method and ‹Counter› with
# a ‹get()› and with a ‹put( n )› method.

class Numbers:    pass
class Counter:    pass
def driver_obj(): pass # a driver loop again, now with objects

def test_main() -> None:

    for dr in [ driver ]:
        nums = iter( [ 1, 2, 4, 7, 11, 16 ] )
        d = dr()
        for n in d:
            num = next( nums )
            assert n == num, "{} != {} in {}".format( n, num, dr.__name__ )
        try: # check that we exhausted nums
            lol = next( nums )
            assert False
        except StopIteration:
            pass

if __name__ == "__main__":
    test_main()
