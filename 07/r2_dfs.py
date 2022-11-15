from typing import Dict, List, TypeVar, Set, Iterable

# You are given a semi-coroutine which is supposed to yield nodes of
# a graph in the ‘leftmost’ DFS post-order. That is, it visits the
# successors of a vertex in order, starting from leftmost. The input
# graph is encoded using a dictionary of neighbour lists.

# Make sure it is correct (and if not, fix it).

T = TypeVar( 'T' )

def dfs( graph: Dict[ T, List[ T ] ], initial: T ) \
        -> Iterable[ T ]:
    seen : Set[ T ] = set()
    yield from dfs_rec( graph, initial, seen )

def dfs_rec( graph: Dict[ T, List[ T ] ], initial: T,
             seen: Set[ T ] ) -> Iterable[ T ]:

    seen.add( initial )

    for n in graph[ initial ]:
        yield from dfs_rec( graph, n, seen )

    yield initial
