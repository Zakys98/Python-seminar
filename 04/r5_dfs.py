# Write a semi-coroutine which yields nodes of a graph in the
# ‘leftmost’ DFS post-order. That is, visit the successors of a
# vertex in order, starting from leftmost (different exploration
# order will result in different post-orders). The graph is encoded
# using neighbour lists.

def dfs( graph, initial ):
    pass

def test_int() -> None:
    g : Dict[ int, List[ int ] ]
    g = { 1: [ 2, 3, 4 ],
          2: [ 1, 2 ],
          3: [ 3, 4 ],
          4: [],
          5: [ 3 ] }

    for i in dfs( g, 4 ):
        assert i == 4

    assert list( dfs( g, 5 ) ) == [ 4, 3, 5 ]
    assert list( dfs( g, 2 ) ) == [ 4, 3, 1, 2 ]
    assert list( dfs( g, 1 ) ) == [ 2, 4, 3, 1 ]

def test_str() -> None:
    g : Dict[ str, List[ str ] ]
    g = { 'red':    [ 'blue', 'green', 'yellow' ],
          'blue':   [ 'red', 'blue' ],
          'green':  [ 'green', 'yellow' ],
          'yellow': [],
          'purple': [ 'green' ] }

    ygp  = [ 'yellow', 'green', 'purple' ]
    ygrb = [ 'yellow', 'green', 'red', 'blue' ]
    bygr = [ 'blue', 'yellow', 'green', 'red' ]

    assert list( dfs( g, 'purple' ) ) == ygp
    assert list( dfs( g, 'blue' ) ) == ygrb
    assert list( dfs( g, 'red' ) ) == bygr


if __name__ == '__main__':
    test_int()
    test_str()
