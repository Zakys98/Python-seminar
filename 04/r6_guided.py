from __future__ import annotations
from typing import TypeVar, Generic, Generator, Optional, Callable
from queue import PriorityQueue, Queue

# Write an A* ‘guided search’ that finds a shortest path in a graph,
# implemented using coroutines. The search coroutine should yield
# the nodes of the graph as they are explored. In response to each
# yield, the driver (semantically also a coroutine, though not
# necessarily a coroutine or a generator in the Python sense) will
# send the corresponding priority which should be assigned to
# exploring the successors of the given node.

T = TypeVar( 'T' )
S = TypeVar( 'S' )

class cor_iter( Generic[ T, S ] ): pass

# Note: A* is essentially just BFS with a priority queue instead of
# a regular queue. To simplify matters, here is an implementation of
# standard BFS.

Graph = dict[ T, set[ T ] ]
Gen2 = Generator[ T, S, None ]

def bfs( graph: Graph[ T ], start : T ) -> Gen2[ T, int ]:

    q : Queue[ T ] = Queue()
    q.put( start )
    seen : set[ T ] = set()
    while not q.empty():
        item = q.get()
        for succ in graph[ item ]:
            yield succ
            if succ not in seen:
                q.put( succ )
            seen.add( succ )

def a_star( graph, start ): pass


def test_routing() -> None:
    for f, lst in ROUTES.items(): # sanity check
        for t in lst:
            assert f in ROUTES[ t ], ( f, t )

    avoid = { 'opava', 'ostrava', 'olomouc', 'frýdek' }
    n_astar = run( a_star, avoid )
    n_bfs = run( bfs, set() )
    assert n_astar < n_bfs, ( n_astar, n_bfs )

CITIES = { 'brno':      ( 49.1951, 16.6068 ),
           'svitavy':   ( 49.7556, 16.4694 ),
           'olomouc':   ( 49.5938, 17.2509 ),
           'opava':     ( 49.9407, 17.8948 ),
           'ostrava':   ( 49.8209, 18.2625 ),
           'zlín':      ( 49.2248, 17.6728 ),
           'frýdek':    ( 49.6819, 18.3673 ),
           'prostějov': ( 49.4727, 17.1068 ),
           'jihlava':   ( 49.3684, 15.5870 ),
           'pardubice': ( 50.0343, 15.7812 ),
           'hradec':    ( 50.2104, 15.8252 ),
           'liberec':   ( 50.7663, 15.0543 ),
           'ústí':      ( 50.6611, 14.0531 ),
           'praha':     ( 50.0755, 14.4378 ),
           'děčín':     ( 50.7726, 14.2128 ),
           'kladno':    ( 50.1417, 14.1067 ) }

ROUTES = { 'brno':      { 'olomouc', 'opava', 'pardubice', 'zlín' },
           'praha':     { 'pardubice', 'kladno', 'liberec' },
           'liberec':   { 'praha', 'hradec' },
           'hradec':    { 'liberec', 'pardubice', 'opava' },
           'opava':     { 'ostrava', 'olomouc', 'hradec' },
           'ostrava':   { 'opava', 'frýdek' },
           'olomouc':   { 'prostějov', 'zlín', 'opava' },
           'prostějov': { 'olomouc', 'brno' },
           'zlín':      { 'brno', 'olomouc', 'frýdek' },
           'brno':      { 'prostějov', 'svitavy', 'zlín' },
           'frýdek':    { 'ostrava', 'zlín' },
           'svitavy':   { 'brno', 'pardubice' },
           'pardubice': { 'svitavy', 'hradec', 'praha' },
           'kladno':    { 'praha' } }

def run( what: Callable[ [ Graph[ str ], str ], Gen2[ str, int ] ],
         avoid: set[ str ] ) -> int:
    found = False
    count = 0

    for city in ( it := cor_iter( what( ROUTES, 'praha' ) ) ):
        from math import sqrt
        x_1, y_1 = CITIES[ 'zlín' ]
        x_2, y_2 = CITIES[ city ]
        assert city not in avoid
        dist = sqrt( ( x_1 - x_2 ) ** 2 + ( y_1 - y_2 ) ** 2 )
        if abs( dist ) < 1e-10:
            found = True
            break
        else:
            count += 1
            it.reply( int( 10000 * dist ) )

    assert found
    return count

if __name__ == '__main__':
    test_routing()
