# In this exercise, you will implement the Rail Fence cipher
# algorithm, also called the Zig-Zag cipher.
#
# The way this cipher works is as follows: there is a given number
# of rows (‘rails’). You write your message on those rails, starting
# in the top-left corner and moving in a zig-zag pattern: ↘ ↗ ↘ ↗ ↘
# ↗ from top to bottom rail and back to top rail, until the text
# message is exhausted.
#
# Example: ‹HELLO_WORLD› with 3 rails
#
#   ┌─────────────────┐
#   │ ‹ H...O...R.. › │
#   │ ‹ .E.L._.O.L. › │
#   │ ‹ ..L...W...D › │
#   └─────────────────┘
#
# The encrypted message is read off row by row: ‹HOREL_OLLWD›.
#
# Your task is to write a function which, given the plain text and
# the number of rails/rows, returns the encrypted text:

def encrypt(text, rails):
    pass

# And another, which deciphers the text back to the plain text:

def decrypt(text, rails):
    pass


def test_main():
    msg = "HELLO WORLD"
    cipher = "HOREL OLLWD"
    assert encrypt( msg, 3 ) == cipher
    assert decrypt( cipher, 3 ) == msg

    msg = "HELLOWORLD"
    cipher = "HOEWRLOLLD"
    assert encrypt( msg, 4 ) == cipher
    assert decrypt( cipher, 4 ) == msg

    msg = "HELP WE'RE SINKING"
    cipher = "HL ER IKNEPW'ESNIG"
    assert encrypt( msg , 2 ) == cipher
    assert decrypt( cipher, 2 ) == msg

    cipher = "HRNE'EIGLE KPWSN I"
    assert encrypt( msg, 5 ) == cipher
    assert decrypt( cipher, 5 ) == msg

if __name__ == "__main__":
    test_main()
